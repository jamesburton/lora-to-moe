# Benchmark and scoring contract

## Scorecard

| Dimension | Primary measures | Why |
|---|---|---|
| Specialist quality | task accuracy/pass@k/F1, isolated-gain retention | Tests whether composition preserves expertise. |
| General quality | perplexity and stable general benchmark suite | Detects negative transfer. |
| Routing | oracle gap, accuracy, regret, calibration error, entropy | Separates expert failure from router failure. |
| Specialisation | confusion matrix, mutual information, per-expert lift | Shows whether experts are meaningfully distinct. |
| Balance | utilisation, dead experts, max/mean load, dropped tokens | Detects collapse and systems hot spots. |
| Robustness | mixed prompts, unknowns, paraphrases, injection, OOD | Tests the base route and router brittleness. |
| Growth | marginal gain from Sₖ→Sₖ₊₁, ancestor retention, stop-depth calibration | Tests whether capacity follows knowledge demand. |
| Efficiency | active/stored/trainable parameters, path depth, FLOPs, VRAM | Prevents misleading “small” claims. |
| Serving | TTFT, inter-token latency, p50/p95, tokens/s, throughput | Captures real runtime cost. |
| Training | GPU-hours, wall time, energy, tokens, failures | Enables ROI and retraining-cost comparison. |
| Governance | licence compatibility, provenance completeness, scans | Determines whether an artifact is deployable. |

## Required evaluation slices

- Each expert’s native domain.
- Every other expert’s domain, to quantify collisions and transfer.
- General/base capability.
- Prompts that genuinely require two experts.
- Ambiguous prompts with no explicit domain words.
- Inputs requiring no expert.
- Distribution shift and adversarial router manipulation.
- Long-context positions and batch mixes.
- Tool/code tasks evaluated by execution in a sandbox, not model grading alone.

Keep a hidden final test set. Router training may use domain labels, but router
evaluation must infer from the same observable inputs available in production.

## Fair comparisons

Report multiple matched views:

1. Same base, training tokens, and data.
2. Same trainable parameter budget.
3. Same total stored adapter parameters.
4. Same active parameters/FLOPs per token.
5. Same p95 latency or energy.
6. Same wall-clock training budget.
7. Same added whole-adapter capacity: residual child versus wider LoRA, continued
   training, replacement, and flat sibling.
8. Same routed path-depth distribution or the latency/energy needed to obtain
   the same quality.

No single view captures all trade-offs. A top-2 system cannot claim efficiency
against top-1 without active-cost and latency measurements.

## Statistical rules

- Smoke: one seed, clearly labelled, no roadmap decision.
- Screen: two seeds and small data; can reject obvious losers but not establish
  a small win.
- Decision: at least three seeds, mean, standard deviation, confidence interval,
  and paired bootstrap where examples align.
- Predeclare the primary metric and threshold.
- Correct or disclose multiple-comparison risk in large sweeps.
- Keep per-example outputs to enable error analysis and future rescoring.

## Run record

Each run writes a JSON record containing:

```json
{
  "run_id": "phase-a/router/2026-07-27T210000Z/seed-17",
  "kind": "decision",
  "git_commit": "<sha>",
  "config_digest": "sha256:<digest>",
  "base_model_digest": "sha256:<digest>",
  "expert_digests": ["sha256:<digest>"],
  "dataset_digests": ["sha256:<digest>"],
  "environment": {
    "os": "<value>",
    "gpu": "<value>",
    "driver": "<value>",
    "backend": "<value>"
  },
  "metrics": {},
  "artifacts": [],
  "decision": "pending"
}
```

## Portfolio priority

Score proposed work 0–5 on expected quality impact, uniqueness, ecosystem value,
confidence, time-to-evidence, compute cost, engineering cost, and operational
risk. Use:

\[
\text{priority} =
\frac{(impact + uniqueness + ecosystem)\times confidence}
{1 + time + compute + engineering + risk}
\]

This orders experiments; it does not automate rejection. High-uniqueness
rejections require human review because estimates are especially uncertain.
