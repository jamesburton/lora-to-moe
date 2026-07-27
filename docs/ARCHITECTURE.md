# Architecture

## Computation model

For a frozen linear projection \(W \in \mathbb{R}^{d_{out}\times d_{in}}\), LoRA
expert \(e\) contributes:

\[
\Delta W_e x = \frac{\alpha_e}{r_e} B_e A_e x
\]

where \(A_e \in \mathbb{R}^{r_e\times d_{in}}\) and
\(B_e \in \mathbb{R}^{d_{out}\times r_e}\). A router produces sparse weights
\(g_e(h)\), yielding:

\[
y = Wx + \sum_{e \in \operatorname{TopK}(g(h))} g_e(h)\Delta W_e x
\]

The primary Phase A experiment freezes \(W, A_e, B_e\) and trains only \(g\).
Joint expert/router training is an ablation because it no longer tests whether
independently useful experts can be assembled cheaply.

## Rank is a budget, not layer-size mimicry

A dense projection has \(d_{in}d_{out}\) parameters. A rank-\(r\) LoRA has
\(r(d_{in}+d_{out})\). Parameter equality occurs at:

\[
r_{\text{equal}} = \frac{d_{in}d_{out}}{d_{in}+d_{out}}
\]

For a square width \(d\), this is \(d/2\), while rank \(d\) uses twice the dense
projection’s parameters. High rank may still be a useful capacity experiment,
but it forfeits LoRA’s main efficiency property. Rank selection therefore uses:

1. ranks 8, 16, 32, 64, and 128;
2. singular-value/effective-rank analysis of learned deltas;
3. specialist gain per stored and active parameter;
4. widening only while marginal gains clear a preregistered threshold.

Rank need not match across experts if the runtime executes each factorisation
separately. Static batching and some fused kernels may require rank buckets.

## Graph primitives

| Node | Meaning | Required controls |
|---|---|---|
| `router` | Selects children from declared inputs. | granularity, top-k, capacity, calibration |
| `expert` | Applies a compatible parameter delta. | immutable manifest and digest |
| `base` | Applies no adapter delta. | always available as null route |
| `head` | Leaves the expert graph for the model output path. | output contract |
| `bounded_loop` | Repeats a declared latent block. | max iterations, exit, budget, fallback |

The outer graph is a directed acyclic graph. A loop is encapsulated so static
validation can prove a finite maximum cost. A router may select a head directly,
but skipping remaining pretrained layers changes representation semantics and
must use a trained compatible auxiliary head or a supported layer exit—not the
final head attached to an arbitrary hidden state.

## Routing design space

Phase A tests in increasing complexity:

1. Oracle task labels: upper bound only; illegal at deployment.
2. Retrieval/router from prompt embeddings: strong cheap baseline.
3. Sequence-level learned router: one decision per request/segment.
4. Layer-level sequence router: more flexible, more overhead.
5. Token-level top-1 then top-2: highest flexibility and kernel pressure.
6. Dynamic sparsity only if fixed top-k is clearly limiting.

Router inputs may include hidden state summaries, prompt embedding, layer index,
declared tenant policy, and resource budget. They may not use target labels or
future tokens. Router logits stay float32 initially. Measurements include
entropy, calibration, expert confusion, utilisation, dropped tokens, switching
rate, and base-route frequency—not just task loss.

## Hierarchy

Subdivide a broad expert only when its residual errors cluster into stable,
high-volume subdomains and a child can be trained without erasing the parent’s
coverage. Compare:

- flat router over all leaf experts;
- parent router followed by a specialist router;
- retrieved shortlist followed by a learned router;
- shared parent delta plus one child delta;
- child-only delta from the base.

The hierarchy must win on capability per active byte/millisecond, not merely
parameter count. A flat oracle quantifies the hierarchy’s routing tax.

## Execution planes

- **Artifact plane:** safetensors weights, manifests, data cards, evaluations,
  signatures, SBOMs, and content digests.
- **Graph plane:** declarative topology, policies, budgets, compatible versions.
- **Training plane:** independent expert jobs, router jobs, evaluations, lineage.
- **Runtime plane:** base weight residency, adapter cache, fused routing,
  batching, telemetry, fallback.
- **Control plane:** registry, approvals, tenancy, rollout, revocation, audit.

The contracts are backend-neutral. CUDA is the performance reference; golden
traces establish semantic equivalence for XPU, ROCm, Vulkan/llama.cpp-style
inference, ONNX Runtime, and future .NET adapters.
