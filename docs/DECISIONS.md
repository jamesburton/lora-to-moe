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

## D-006 — High rank is an experiment, not the default

- Status: accepted
- Date: 2026-07-27
- Context: “LoRA of matching layer size” could mean rank equal to layer width.
- Decision: sweep practical ranks first. Parameter equality for a projection is
  \(d_{in}d_{out}/(d_{in}+d_{out})\); full-width rank can exceed dense parameter
  count. Use effective-rank and gain-per-parameter evidence.
- Reopen: high-rank probe yields a strategically important ≥3-point gain that a
  practical rank cannot match.

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

## Rejection review queue

No high-uniqueness path has been rejected yet. Future rejected entries must name
a human reviewer or remain `deferred`, not `rejected`.
