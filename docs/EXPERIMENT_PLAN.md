# Experiment plan and gates

## Global protocol

Every decision-grade comparison fixes:

- base checkpoint/tokenizer digest, data splits, tokens seen, optimiser search
  budget, maximum sequence length, decoding, seeds, and evaluation harness;
- stored, trainable, and active parameters separately;
- wall time, accelerator time, peak VRAM, tokens/s, time-to-first-token,
  inter-token latency, batch throughput, and energy estimate;
- general, specialist, mixed-domain, ambiguous, out-of-distribution, and
  adversarial routing sets;
- three seeds with confidence intervals and paired bootstrap tests where useful.

Use a factorial screen at small scale, promote only Pareto candidates, and
confirm once at 2–4B. A 7B run validates scale transfer only after a 4B signal.

## Phase 0 — Instrument and calibrate

### 0.1 Base selection

Run the same small evaluation on 0.5–1.5B candidates, then primary 2–4B
candidates. Score capability headroom, licence, architecture simplicity, PEFT
support, tokenizer, 12 GB feasibility, Vulkan conversion, community adoption,
and measured throughput.

**Gate 0:** choose one base only if it fits the complete primary training
profile below 11.2 GiB and exhibits non-trivial but improvable performance in at
least three target domains. Otherwise shrink sequence length/model or revisit
the hardware plan.

### 0.2 Capacity-unit and target-module calibration

For one task, sweep practical rank and target-module allocations under the
12 GB envelope. Define candidate expert-capacity units by total adapter
parameters across the model, active FLOPs, and latency—not hidden width. Measure
effective rank, activation sensitivity, and marginal validation gain.

Compare at least one two-unit stack against a single wider LoRA with equal stored
parameters and against continued training with equal tokens. This calibrates
whether a repeatable “expert-sized” unit exists before the term is used in
decision claims.

**Gate 0R:** retain the smallest initial unit within 1% absolute of the best
validation score. Retain the X→X+1 formulation only if a second residual unit
adds repeatable capability and is not dominated by the equal-budget wider or
continued-training control. Record the unit definition and reopening condition.

### 0.3 Harness calibration

Verify a memorisation fixture, shuffled-label negative control, deterministic
resume, metric repeatability, routing trace capture, VRAM measurement, and
dataset leakage checks.

**Gate 0H:** no Phase A result is decision-grade until controls behave as
expected and repeated evaluation differs by <0.5 point.

## A — Flat frozen expert composition

### A1. Train independent experts

Choose 3–5 domains with verifiable outcomes and partial overlap: code, maths,
structured extraction/tool calls, general instruction, and optionally one
domain corpus. Use independent jobs and no shared router labels. Save immutable
safetensors, manifests, data cards, isolated benchmarks, and general-regression
scores.

### A2. Establish baselines

1. Frozen base.
2. Each isolated expert.
3. One dense multi-task LoRA at matched total training tokens.
4. One larger multi-task LoRA at matched stored expert parameters.
5. Uniform adapter average and task-vector merge.
6. Retrieval-selected single adapter.
7. Oracle task-label selection.
8. Learned router with base/null path.

### A3. Router matrix

Compare sequence versus token routing, top-1 versus top-2, balance coefficient,
router capacity, prompt embedding versus hidden-state input, and a router-only
attention LoRA if a linear router underfits. Freeze all expert and base weights.

### A4. Addition/removal test

Add a fifth expert, retrain router only, then revoke one expert. Measure training
time, old-domain regressions, routing drift, and whether calibration allows a
safe fallback without full retuning.

### Gate A → B

Proceed when all are true across three seeds:

- routed composition preserves ≥95% of mean isolated specialist gain;
- ≥2 points macro improvement over dense multi-task LoRA, or a statistically
  credible Pareto win at lower active compute;
- ≤1 point regression on general/base capability;
- no dead expert on its intended distribution;
- p95 latency ≤1.25× single-LoRA inference at batch 1;
- router addition/removal is at least 10× cheaper than retraining all experts;
- router beats retrieval on ambiguous/mixed inputs, not just labelled domains.

If quality wins but systems lose, optimise kernels/caching once and repeat. If
the oracle gap is small, better routing is low ROI; if the oracle itself loses,
expert composition or data quality is the problem.

## B — Progressive residual expert stacks

### B1. Select a growth path

For each broad Phase A expert, cluster held-out residual failures using
representations plus a human-readable error taxonomy. Select a parent path only
when clusters are stable across seeds, valuable, and large enough to support an
additional capacity unit. Record the current path as \(S_k\), including its
ordered ancestor digests.

### B2. Train X→X+1 growth

Freeze the base, all ancestors, and existing routers. Train one child residual
\(\Delta_{k+1}\) on the selected residual knowledge so the new path is
\(S_{k+1}=S_k+\Delta_{k+1}\). Match the new adapter to the calibrated
expert-capacity budget across target modules; rank may vary by layer.

Compare against:

1. no growth at \(S_k\);
2. continued parent training for equal tokens;
3. one wider parent LoRA at equal stored parameters;
4. a flat sibling expert trained from the base;
5. parent checkpoint initialisation followed by replacement fine-tuning;
6. a dense multi-task adapter at matched active cost.

### B3. Route and stop

Train a router at the parent boundary with explicit choices to stop/head,
descend to each child, or fall back. Compare flat leaves, progressive
parent→child paths, and retrieval→shortlist→router. Measure ancestor preservation,
parent and child routing errors, path-depth calibration, and shared-prefix cache
reuse.

### B4. Repeatable growth rule

If the first child passes, repeat once on either the same branch or a sibling to
test whether the unit and admission rule transfer. Do not call the mechanism
progressive growth based on a single successful child.

### Gate B → C

Proceed when all are true:

- \(S_{k+1}\) improves its selected hard knowledge region ≥3 points over
  \(S_k\) and beats or Pareto-dominates the equal-budget wider, continued, and
  flat-sibling controls;
- ancestors retain ≥98% of unaffected-domain performance;
- the boundary router sends covered/easy inputs to the earlier exit and remains
  calibrated on mixed and unknown inputs;
- marginal capability per active parameter and p95 millisecond improves ≥10%;
- two growth events demonstrate a repeatable capacity-unit and lineage rule;
- every child is reproducible only from its pinned ancestor chain.

Otherwise keep the useful flat router and any individually useful child
artifact, revise the unit definition, or stop progressive depth without blocking
ecosystem work.

## C — Exit and bounded latent loops

### C1. Early/head exit

Attach and train compatible intermediate readouts; compare fixed layer exits,
confidence thresholding, and router-selected exit. Calibrate on unseen domains.

### C2. One bounded loop

Choose one middle block based on representation similarity and residual error.
Test 0–3 additional applications with positional/KV handling declared. Train
with forced-depth and intermediate supervision so the exit is not the only
source of gradient.

### C3. Baselines

Compare extra output reasoning tokens, fixed extra layers, looped block,
full-model second pass, and equal-FLOP dense computation. Include post-hoc
confidence readout and always-exit/always-loop controls.

### Gate C → D

Proceed when bounded computation produces a statistically credible Pareto
improvement at matched FLOPs, ≤1 point easy-task regression, no divergence or
hidden-state norm drift outside preregistered bounds, and measured latency gains
from exit. Maximum loop count remains enforced regardless of confidence.

## D — Generated expert deltas

### D0. Corpus readiness

Require hundreds to thousands of compatible, quality-filtered adapters trained
from the same base/target schema, with reusable licences and task
demonstrations. Canonicalise scale/sign symmetries before learning weight space.

### D1. Cheapest generators first

1. Retrieve nearest expert and fine-tune.
2. Weighted interpolation/task arithmetic.
3. Hypernetwork predicting low-dimensional coefficients.
4. Hypernetwork predicting LoRA factors.
5. Latent diffusion over canonical adapter representation.

### D2. Held-out tests

Hold out tasks, domains, ranks, publishers, and eventually base models. Compare
zero-step generation and 1/10/100 refinement steps. Train an uncertainty/failure
detector and reject unsafe or off-manifold deltas.

### Gate D

A generator advances only if it retains ≥90% of trained-expert gain, reduces
time-to-qualified-expert ≥10×, stays within general/safety regression limits,
beats retrieve+brief-fine-tune at matched wall time, and generalises to truly
held-out tasks. Generated artifacts never bypass normal admission.

## Stop and reopen rules

Stopping is a successful result when it removes a costly branch. Each rejection
records measured evidence and at least one reopening condition, such as a new
kernel, larger compatible adapter corpus, stronger base, better routing method,
or a user workload whose value changes the cost threshold.
