# Decision ledger

## D-001 — Research stack first

- Status: accepted
- Date: 2026-07-27
- Decision: Python/PyTorch/Hugging Face is the reference research path. .NET 10,
  TorchSharp, and Microsoft Agent Framework follow through stable contracts.
- Evidence: strongest PEFT/training ecosystem and fastest path to falsification.
- Reopen: TorchSharp reaches required PEFT/quantisation/router coverage or a
  .NET workload demonstrates lower total integration cost.

## D-002 — Hardware ladder

- Status: accepted
- Date: 2026-07-27
- Decision: optimise for RTX 3060 12 GB; test Vulkan inference on Meteor Lake
  and Strix Halo, with XPU/ROCm as distinct native paths.
- Consequence: 2–4B NF4 is primary; 7B is gated confirmation.
- Reopen: measured primary run cannot fit under 11.2 GiB or access to larger
  repeatable hardware changes the ROI.

## D-003 — Publish initial foundation to main

- Status: accepted by repository owner
- Date: 2026-07-27
- Decision: greenfield foundation may publish directly to `main`; later
  substantial work defaults to draft PR review.
- Reopen: first external collaborator or branch protection policy.

## D-004 — Apache-2.0 code and explicit artifact licences

- Status: accepted
- Date: 2026-07-27
- Decision: repository code is Apache-2.0. Each model, adapter, and dataset keeps
  explicit provenance/licence; graph admission evaluates compatibility.
- Reopen: legal review identifies an ecosystem or dependency conflict.

## D-005 — A → B → C → D

- Status: accepted
- Date: 2026-07-27
- Decision: flat frozen experts, hierarchy, bounded adaptive computation, then
  generated deltas. Each transition requires its declared evidence gate.
- Reopen: strong external evidence makes a later phase cheaper to test, but it
  may run only as an isolated spike without bypassing production gates.

## D-006 — Rank-equals-width interpretation

- Status: superseded
- Date: 2026-07-28
- Context: the initial foundation interpreted “LoRA of matching layer size” as a
  possible rank equal to projection width.
- Decision: this was not the intended hypothesis. Preserve high-rank/effective-
  rank analysis only as an equal-budget control.
- Superseded by: D-009.

## D-007 — No raw cycles in expert graphs

- Status: accepted
- Date: 2026-07-27
- Decision: outer graphs are acyclic. Recursion uses a bounded-loop primitive
  with a maximum, exit, budget, and fallback.
- Reopen: never for untrusted/production graphs; research-only runtimes may test
  alternatives inside a hard external watchdog.

## D-008 — Qwen3-4B as initial primary candidate

- Status: trial
- Date: 2026-07-27
- Decision: use Apache-2.0 dense Qwen3-4B as the initial primary candidate, not a
  permanent dependency. Fail-fast and base-selection benchmarks precede spend.
- Reopen: newer candidate wins the declared capability/licence/fit/portability
  scorecard.

## D-009 — Progressive matched expert-capacity units

- Status: accepted clarification from repository owner
- Date: 2026-07-28
- Context: start from a smaller, less capable dense model. A routed knowledge
  path holding X expert-capacity units receives a new residual LoRA only when
  measured residual knowledge justifies growth to X+1.
- Decision: Phase A establishes broad independent roots and routing. Phase B
  freezes the chosen base/ancestor path, trains one matched residual unit,
  exposes stop/head and child routes, and tests repeated growth.
- Meaning of matched: a declared whole-adapter budget across target modules,
  reported by stored/trainable parameters, active FLOPs, latency, and marginal
  capability. It does not prescribe rank equal to hidden width.
- Consequence: children pin their ordered ancestor digests and are not directly
  composable with another path. Flat, wider, continued-training, and replacement
  baselines are mandatory.
- Reopen: revise the unit definition if repeated X→X+1 additions are dominated
  by widening, flat experts, or continued training.

## D-010 — Answer, extend, or branch routing protocol

- Status: accepted clarification from repository owner
- Date: 2026-07-28
- Context: progressive growth needs to distinguish a request that is already
  answerable, one needing more depth on the current knowledge path, and one
  needing a different specialism.
- Decision: every expert boundary exposes three semantic choices: `answer`,
  `extend`, and `branch`. Router evaluation reports decision-class and
  destination errors separately. Experts remain independently trainable and
  shareable; consumers fetch compatible artifacts and retrain or calibrate only
  the router for their catalog, workload, and compute budget.
- Consequence: manifests must distinguish lineage extensions from branches,
  while router releases pin the exact admitted catalog. Fast add/revoke tests
  become a core ecosystem benchmark.
- Reopen: revise the factorisation if a fused flat router is consistently better
  calibrated and cheaper while preserving equivalent observable semantics.

## Rejection review queue

No high-uniqueness path has been rejected yet. Future rejected entries must name
a human reviewer or remain `deferred`, not `rejected`.
