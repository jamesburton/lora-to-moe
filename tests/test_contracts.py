from __future__ import annotations

import json
import unittest
from pathlib import Path

from lora_moe.contracts import ExpertManifest, GraphManifest, ValidationError


ROOT = Path(__file__).parents[1]


class ExpertManifestTests(unittest.TestCase):
    def test_example_is_valid(self) -> None:
        manifest = ExpertManifest.load(ROOT / "examples/catalog/code-expert.json")
        self.assertEqual("example/code-python", manifest.expert_id)
        self.assertEqual(32, manifest.rank)

    def test_mismatched_digest_is_rejected(self) -> None:
        data = json.loads(
            (ROOT / "examples/catalog/code-expert.json").read_text(encoding="utf-8")
        )
        data["adapter"]["digest"] = "not-a-digest"
        with self.assertRaisesRegex(ValidationError, "adapter.digest"):
            ExpertManifest.from_dict(data)


class GraphManifestTests(unittest.TestCase):
    def test_phase_a_graph_is_valid(self) -> None:
        graph = GraphManifest.load(ROOT / "examples/graphs/phase-a.json")
        self.assertEqual("router", graph.entry_node)

    def test_ordinary_cycle_is_rejected(self) -> None:
        data = json.loads(
            (ROOT / "examples/graphs/phase-a.json").read_text(encoding="utf-8")
        )
        data["edges"].append({"from": "head", "to": "router", "condition": "again"})
        with self.assertRaisesRegex(ValidationError, "unbounded cycle"):
            GraphManifest.from_dict(data)


if __name__ == "__main__":
    unittest.main()
