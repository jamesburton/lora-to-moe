# Agent operating contract

## Mission

Build the smallest reproducible system that can disprove or advance the
LoRA-to-MoE hypothesis. Optimise for information gained per unit of time,
compute, money, and human attention. Preserve the option to revisit a rejected
idea when new evidence changes its expected value.

## Work loop

1. **Orient.** Read `README.md`, `docs/HANDOFF.md`, relevant decisions, and the
   files you will change. Confirm the current branch and dirty state.
2. **Research.** State the question, hypotheses, adjacent work, novelty boundary,
   assumptions, and cheapest discriminating experiment. Prefer primary sources.
3. **Plan.** Define inputs, baselines, controlled variables, metrics, budget,
   success/stop thresholds, artifacts, and rollback before implementation.
4. **Refine.** Challenge leakage, unfair baselines, hidden compute, licence
   incompatibility, routing collapse, and conclusions unsupported by sample size.
5. **Implement.** Make the smallest vertical slice. Agents may divide independent
   work, but one owner must integrate contracts and resolve disagreements.
6. **Verify.** Run unit, integration, deterministic smoke, benchmark, and
   hardware checks appropriate to the change. Record commands and results.
7. **Score.** Update the experiment ledger using quality, uniqueness, expected
   impact, confidence, compute, engineering cost, and operational risk.
8. **Decide.** Continue, revise, pause, or reject. Human review is mandatory for
   rejection of a high-uniqueness path or any irreversible compatibility choice.
9. **Loop.** If evidence exposes a missing hypothesis or invalid plan, return to
   research or planning instead of forcing implementation onward.
10. **Handoff and sync.** Update `docs/HANDOFF.md` in the same change. Commit
    coherent, tested increments regularly.

## Experiment definition of done

An experiment is not complete until it has:

- an immutable configuration and environment fingerprint;
- fixed train/validation/test splits with contamination notes;
- dense-base, single-LoRA, dense multi-task LoRA, static merge, retrieval-router,
  learned-router, and oracle-router baselines where applicable;
- at least three seeds for decision-grade claims, with uncertainty reported;
- quality, forgetting, routing, utilisation, latency, throughput, peak VRAM,
  active/trainable/stored parameters, energy estimate, and failure cases;
- artifacts and provenance sufficient to reproduce the run;
- a decision against a threshold declared before viewing the result.

Toy runs may use one seed but must be labelled `smoke`, never `evidence`.

## Architecture invariants

- The base model is content-addressed and immutable during router-only training.
- Root experts are independently loadable artifacts with explicit base-model,
  architecture, target-module, rank, dtype, tokenizer, licence, data-provenance,
  evaluation, and safety compatibility.
- A residual child pins its ordered ancestor adapter digests. It is loadable as
  an artifact but executable only over that exact frozen path; never silently
  attach it to the dense base or another parent.
- Router inputs and routing granularity are declared. Hidden oracle labels are
  forbidden outside the oracle baseline.
- Every graph has a base/null path and an output path.
- Every expert boundary exposes `answer`, `extend`, and `branch` semantics.
  Evaluate the decision class separately from the selected destination, even if
  an implementation fuses both into one router head.
- Cycles are rejected unless represented as bounded loop nodes with maximum
  iterations, compute budget, exit policy, and fallback.
- Expert weights remain frozen during the primary router comparison. During
  X→X+1 growth, freeze the base, all ancestors, and existing routers; train only
  the new residual and then its boundary router. Joint tuning is a separate
  ablation because it changes the question.
- Training and inference backends must implement the same observable routing
  semantics or declare the deviation.

## Decision ledger

Record important choices in `docs/DECISIONS.md` with:

- status: proposed, accepted, trial, deferred, rejected, or superseded;
- date, owner, context, alternatives, evidence, decision, and consequences;
- the measurable condition that would reopen a deferred or rejected choice;
- human-review state, especially for rejection.

Do not delete rejected ideas. Do not turn weak or missing evidence into a
confident negative conclusion.

## Collaboration and review

- Give parallel agents non-overlapping outputs and explicit acceptance tests.
- Require each result to include assumptions, sources, files changed, checks,
  uncertainties, and recommended next step.
- Integrators validate results rather than trusting summaries.
- Prefer small commits that leave the repository runnable.
- Do not publish secrets, private `.docs/` content, model weights, raw licensed
  datasets, or personally identifying evaluation data.

## Code and data quality

- Python 3.11+, typed public APIs, deterministic seeds, concise modules.
- Use `ruff`, unit tests, JSON Schema, and dependency-free contract tests in CI.
- Optional heavyweight dependencies belong in extras.
- Configurations contain no secrets or machine-specific absolute paths.
- Dataset transforms are versioned; raw data is referenced by URI and digest.
- Benchmark outputs use machine-readable JSON plus a concise Markdown summary.

## Required handoff update

Every meaningful change updates `docs/HANDOFF.md` with:

- completed work and commit/run identifiers;
- exact validation commands and outcomes;
- evidence learned versus assumptions still open;
- blockers, risks, and failed attempts;
- the top three next actions in priority order;
- whether a human decision is required.
