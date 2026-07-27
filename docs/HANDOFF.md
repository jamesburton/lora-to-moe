# Handoff

Last updated: 2026-07-27

## Current state

The greenfield foundation is published on `main` at remote commit
`752d54d36af25f25d19f8c92166d7611a1028538`. It encodes the accepted RTX 3060
12 GB target, Vulkan portability lane, Apache-2.0 code licence, and
A → B → C → D gates.

Completed:

- research synthesis and explicit novelty boundary;
- vision, architecture, experiment protocol, benchmarks, hardware, ecosystem,
  enterprise, roadmap, and reversible decision ledger;
- strict expert and graph manifests plus JSON Schemas;
- graph rejection of unbounded cycles and enforcement of base/head paths;
- dependency-free learned-router reference and frozen-expert semantic demo;
- unit tests, CLI validation, example catalog/graph, 3060 config, and CI.

## Validation

Run from repository root:

```bash
make check
make demo
```

Expected: all unit tests pass, both example manifests validate, and the toy
router clears 0.95 routing accuracy. This is a deterministic smoke test, not
language-model evidence.

## Evidence versus assumptions

Evidence from prior work:

- LoRA expert routing, hierarchy, retrieval, rank-wise routing, frozen reasoning
  expert composition, latent loops, and generated vision LoRAs all have close
  prior art.
- QLoRA makes consumer-GPU testing plausible.
- Portable/native iGPU support is backend- and platform-specific.

Still assumptions requiring local results:

- four useful experts and router training fit the exact 12 GB profile;
- frozen composition beats dense multi-task LoRA at matched cost;
- hierarchy adds ROI beyond a flat/retrieval design;
- dynamic token routing can be served efficiently;
- Vulkan runtimes can implement more than sequence-level adapter selection;
- generated LLM experts generalise beyond their adapter corpus.

## Failed or constrained attempts

- The environment has no `gh` CLI. The connected GitHub app has repository
  administration/push access and will be used for remote publication; plain Git
  is used locally.
- PyTorch is not installed in this execution environment. The foundation and CI
  therefore use dependency-free contract/routing tests. Full CUDA training is
  intentionally the next hardware-backed slice.

## Next three actions

1. Implement environment fingerprinting, run records, CUDA memory probe, and
   base-model selection harness; execute on the RTX 3060.
2. Implement one PEFT expert training/export pipeline and reproduce one expert
   across two seeds before expanding to four domains.
3. Implement dense multi-task, retrieval, oracle, and learned sequence-router
   baselines before token-level routing.

## Human review

No decision is currently blocked. Human review is required after Gate A and
before marking any high-uniqueness branch rejected.
