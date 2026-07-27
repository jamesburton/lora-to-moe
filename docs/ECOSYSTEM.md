# Shared expert ecosystem

## Artifact model

Use Hugging Face or another object store for large immutable safetensors and
GitHub for human-reviewed manifests, graphs, code, data cards, and evaluation
reports. The protocol must not require either provider: URIs and digests are
portable, and a future registry indexes rather than owns every artifact.

An expert release contains:

- LoRA safetensors only, never pickle;
- PEFT-compatible adapter configuration;
- `expert-manifest.json` validated by `schemas/expert-manifest.schema.json`;
- model and data cards with intended use and limitations;
- evaluation JSON and per-slice summary;
- licence expression and compatibility analysis;
- dataset lineage/digests without redistributing restricted data;
- security scan, optional signature/attestation, and SBOM;
- a reproducible training recipe or a documented reason it cannot be shared.

## Compatibility

Hard requirements for direct composition:

- exact base checkpoint and tokenizer digests;
- architecture and target module names/shapes;
- adapter method and runtime operator support;
- embedding/vocabulary compatibility;
- position-encoding and chat-template assumptions;
- quantisation/compute dtype combination validated by the runtime;
- licences mutually compatible with the proposed distribution and use.

Rank and alpha may differ if the backend supports heterogeneous factorisations.
Otherwise the registry can publish rank-bucketed or converted variants, never
silently pad or truncate without a new digest and evaluation.

## Catalog and discovery

Search fields include base, capability taxonomy, language, domain, task,
benchmark evidence, licence, safety, rank, targets, size, latency, hardware,
publisher trust, update time, and compatible graph primitives.

Discovery produces candidates, not admission. A local policy evaluates:

1. digest and signature;
2. schema and base compatibility;
3. licence/data policy;
4. malware/unsafe-format scan;
5. minimum evidence;
6. local canary evaluation;
7. tenant-specific approval.

## Router lifecycle

Router manifests pin the ordered expert set and digests. Adding, upgrading, or
revoking an expert creates a new router release. Warm-start is allowed, but old
domain regression and calibration are mandatory. A missing or rejected expert
must route to an explicit fallback rather than shift array indices.

To keep retraining cheap, maintain:

- a public routing dataset of observable prompts and expected capability tags;
- private tenant routing examples stored separately;
- distilled expert competence embeddings/scorecards;
- hard mixed-domain and negative/base cases;
- replay samples for every accepted expert;
- canary and rollback router revisions.

## Contribution path

1. Publish an expert artifact and draft manifest.
2. Automated compatibility/security checks.
3. Isolated quality and regression evaluation.
4. Human review of provenance, licence, and intended use.
5. Sandbox admission to an experimental catalog.
6. Router integration benchmark against catalog baselines.
7. Signed stable release, or documented rejection/reopen condition.

Useful but incompatible experts may trigger a separate base-model catalog rather
than unsafe conversion.

## Trust and incentives

Track evidence, not popularity alone. Publisher reputation can prioritise review
but cannot override digest, licence, or quality policy. Reports should credit
expert/data/evaluation contributors and make hardware cost transparent.

Potential collaboration surfaces:

- CLI: validate, benchmark, publish, compose, reproduce.
- Python SDK: training, runtime, metrics, registry client.
- Web portal: discovery, graph builder, evidence comparison, reviews.
- API/MCP: policy-controlled catalog and experiment operations.
- .NET SDK: manifests, serving orchestration, enterprise integration.

Do not build the full portal before the manifest and Phase A workflow survive
real independent submissions.
