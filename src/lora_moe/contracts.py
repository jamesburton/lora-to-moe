"""Strict, dependency-free validation for portable expert graph manifests."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ValidationError(ValueError):
    """A manifest violates an interoperability or safety invariant."""


def _required(data: dict[str, Any], key: str, expected: type) -> Any:
    value = data.get(key)
    if not isinstance(value, expected) or (expected is str and not value.strip()):
        raise ValidationError(f"{key!r} must be a non-empty {expected.__name__}")
    return value


def _sha256(value: str, field: str) -> str:
    if not value.startswith("sha256:") or len(value) != 71:
        raise ValidationError(f"{field!r} must be sha256:<64 lowercase hex characters>")
    digest = value.removeprefix("sha256:")
    if any(character not in "0123456789abcdef" for character in digest):
        raise ValidationError(f"{field!r} contains invalid SHA-256 characters")
    return value


@dataclass(frozen=True)
class ExpertManifest:
    schema_version: str
    expert_id: str
    revision: str
    base_model: str
    base_model_digest: str
    adapter_uri: str
    adapter_digest: str
    architecture: str
    target_modules: tuple[str, ...]
    rank: int
    alpha: float
    dtype: str
    tokenizer_digest: str
    licence: str
    data_card_uri: str
    capabilities: tuple[str, ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ExpertManifest:
        adapter = _required(data, "adapter", dict)
        provenance = _required(data, "provenance", dict)
        compatibility = _required(data, "compatibility", dict)
        targets = _required(adapter, "target_modules", list)
        capabilities = _required(data, "capabilities", list)
        rank = adapter.get("rank")
        alpha = adapter.get("alpha")
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
            raise ValidationError("'adapter.rank' must be a positive integer")
        if not isinstance(alpha, (int, float)) or isinstance(alpha, bool) or alpha <= 0:
            raise ValidationError("'adapter.alpha' must be positive")
        if not targets or not all(isinstance(item, str) and item for item in targets):
            raise ValidationError("'adapter.target_modules' must contain strings")
        if not capabilities or not all(
            isinstance(item, str) and item for item in capabilities
        ):
            raise ValidationError("'capabilities' must contain strings")
        return cls(
            schema_version=_required(data, "schema_version", str),
            expert_id=_required(data, "expert_id", str),
            revision=_required(data, "revision", str),
            base_model=_required(compatibility, "base_model", str),
            base_model_digest=_sha256(
                _required(compatibility, "base_model_digest", str),
                "compatibility.base_model_digest",
            ),
            adapter_uri=_required(adapter, "uri", str),
            adapter_digest=_sha256(
                _required(adapter, "digest", str), "adapter.digest"
            ),
            architecture=_required(adapter, "architecture", str),
            target_modules=tuple(targets),
            rank=rank,
            alpha=float(alpha),
            dtype=_required(adapter, "dtype", str),
            tokenizer_digest=_sha256(
                _required(compatibility, "tokenizer_digest", str),
                "compatibility.tokenizer_digest",
            ),
            licence=_required(provenance, "licence", str),
            data_card_uri=_required(provenance, "data_card_uri", str),
            capabilities=tuple(capabilities),
        )

    @classmethod
    def load(cls, path: str | Path) -> ExpertManifest:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))

    def compatibility_key(self) -> tuple[str, str, str, tuple[str, ...]]:
        return (
            self.base_model_digest,
            self.tokenizer_digest,
            self.architecture,
            self.target_modules,
        )


@dataclass(frozen=True)
class GraphManifest:
    schema_version: str
    graph_id: str
    entry_node: str
    nodes: tuple[dict[str, Any], ...]
    edges: tuple[dict[str, Any], ...]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> GraphManifest:
        nodes = _required(data, "nodes", list)
        edges = _required(data, "edges", list)
        entry_node = _required(data, "entry_node", str)
        node_ids = {
            _required(node, "id", str)
            for node in nodes
            if isinstance(node, dict)
        }
        if len(node_ids) != len(nodes):
            raise ValidationError("all nodes must be objects with unique ids")
        if entry_node not in node_ids:
            raise ValidationError("'entry_node' must reference a node")
        node_types = {
            node["id"]: _required(node, "type", str)
            for node in nodes
        }
        allowed = {"router", "expert", "base", "head", "bounded_loop"}
        unknown = set(node_types.values()) - allowed
        if unknown:
            raise ValidationError(f"unknown node type(s): {sorted(unknown)}")
        adjacency = {node_id: [] for node_id in node_ids}
        for edge in edges:
            if not isinstance(edge, dict):
                raise ValidationError("all edges must be objects")
            source = _required(edge, "from", str)
            target = _required(edge, "to", str)
            if source not in node_ids or target not in node_ids:
                raise ValidationError("edge endpoints must reference nodes")
            adjacency[source].append(target)

        # Ordinary graph edges must be acyclic. Recurrence is represented inside a
        # bounded_loop node so a static validator can prove a finite outer graph.
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise ValidationError(
                    "unbounded cycle detected; use a bounded_loop node"
                )
            if node_id in visited:
                return
            visiting.add(node_id)
            for target in adjacency[node_id]:
                visit(target)
            visiting.remove(node_id)
            visited.add(node_id)

        visit(entry_node)
        reachable = visited
        if reachable != node_ids:
            raise ValidationError(f"unreachable node(s): {sorted(node_ids - reachable)}")
        if not any(node_types[node_id] == "head" for node_id in reachable):
            raise ValidationError("graph must have a reachable head")
        if not any(node_types[node_id] == "base" for node_id in reachable):
            raise ValidationError("graph must expose a base/null path")
        for node in nodes:
            if node["type"] == "bounded_loop":
                maximum = node.get("max_iterations")
                if not isinstance(maximum, int) or maximum < 1:
                    raise ValidationError("bounded loops require max_iterations >= 1")
                if not isinstance(node.get("exit_policy"), str):
                    raise ValidationError("bounded loops require an exit_policy")
                if not isinstance(node.get("fallback"), str):
                    raise ValidationError("bounded loops require a fallback")
        return cls(
            schema_version=_required(data, "schema_version", str),
            graph_id=_required(data, "graph_id", str),
            entry_node=entry_node,
            nodes=tuple(nodes),
            edges=tuple(edges),
        )

    @classmethod
    def load(cls, path: str | Path) -> GraphManifest:
        return cls.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def canonical_digest(data: dict[str, Any]) -> str:
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")).encode()
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"
