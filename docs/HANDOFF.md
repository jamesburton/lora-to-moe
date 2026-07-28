# Handoff

Last updated: 2026-07-28

## Current state

The greenfield foundation is published on `main`. The 2026-07-28 architecture
correction now makes progressive matched expert-capacity growth the central
hypothesis: a frozen path Sₖ receives one residual LoRA only when knowledge gaps
justify growth to Sₖ₊₁. “Matched” applies to a declared whole-adapter capacity
unit, not rank equal to hidden width. Every boundary now uses the explicit
`answer`/`extend`/`branch` protocol, and independently published experts are
integrated through cheap router-only retraining or calibration.

Completed:

- research synthesis and explicit novelty boundary;
- corrected README, vision, architecture, experiments, roadmap, benchmarks,
  ecosystem, decisions, and agent invariants for X→X+1 residual growth;
- formalised `answer`/`extend`/`branch` routing and separated decision-class from
  destination-expert evaluation;
- made independent expert publishing plus router-only catalog integration a core
  ecosystem contract and benchmark;
- superseded the incorrect rank-equals-width interpretation in D-006;
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
- progressive residual stacking adds ROI beyond wider, continued-training,
  replacement, and flat-sibling designs;
- one calibrated capacity-unit definition transfers across two growth events;
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
2. Implement one PEFT expert training/export pipeline and reproduce one broad
   root expert across two seeds before expanding to four domains.
3. Add capacity-unit accounting plus a two-step S₀→S₁→S₂ smoke experiment,
   including wider, continued-training, flat-sibling controls, and explicit
   `answer`/`extend`/`branch` routing traces.

## Human review

No decision is currently blocked. Human review is required after Gate A and
before marking any high-uniqueness branch rejected.
