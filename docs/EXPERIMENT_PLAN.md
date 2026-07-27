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

### 0.2 Rank and target-module screen

For one task, sweep rank 8–128 and attention-only versus attention+MLP targets.
Include a high-rank probe calculated from parameter equality, but stop it early
if gain per parameter is dominated. Analyse singular values of the resulting
delta and activation sensitivity per layer.

**Gate 0R:** retain the smallest configuration within 1% absolute of the best
validation score unless a larger rank improves a strategically unique capability
by ≥3%. Record high-rank rejection and reopen condition.

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

## B — Hierarchical specialisation

### B1. Select one parent

Cluster the best broad expert’s held-out failures using representations and
human-readable error taxonomy. Require stable clusters across seeds and enough
volume to justify a child.

### B2. Train children

Compare children trained from:

- base + independent child LoRA;
- frozen parent + child residual LoRA;
- parent checkpoint initialisation then independent fine-tune.

### B3. Compare topology

Flat leaves, parent→children, retrieval→shortlist→router, and shared-parent+
child routes. Measure error propagation: parent miss, child miss, and correct
fallback. Add explicit head and base choices but no loops.

### Gate B → C

Proceed when hierarchy:

- improves the selected hard subdomains ≥3 points over the best flat matched
  baseline;
- retains ≥98% of unaffected-domain performance;
- reduces router search or active adapter cost enough that quality per p95
  millisecond improves ≥10%;
- remains calibrated under mixed and unknown inputs;
- demonstrates an interpretable, repeatable growth rule.

Otherwise retain flat routing and continue ecosystem work without hierarchy.

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
