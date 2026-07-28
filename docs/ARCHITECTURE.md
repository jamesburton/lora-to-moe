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
independently useful experts can be assembled cheaply. Phase B changes the
topology, not this discipline: it trains one new residual adapter while freezing
the base, its ancestor adapters, and the existing routers.

## Progressive expert-capacity growth

Let \(M_0\) be the small dense base and \(\Delta_i\) an expert residual
trained while the preceding path is frozen. A path of depth \(k\) is:

\[
S_k(x) = M_0(x) + \Delta_1(x) + \Delta_2(x) + \cdots + \Delta_k(x)
\]

This is conceptual notation: implementations apply each LoRA delta at its
declared target modules throughout the transformer. It does not imply appending
a transformer layer or merging weights during training.

A router first selects a broad expert. At the next boundary it may:

1. exit through the normal compatible output path;
2. select a child residual and compute \(S_{k+1}\);
3. select another declared branch;
4. later, enter a separately bounded adaptive-computation primitive.

Growth is evidence-triggered. Cluster the residual failures of \(S_k\); add
\(\Delta_{k+1}\) only when a stable, valuable knowledge region cannot be served
efficiently by the current path. Ancestors remain reusable and immutable.

## What “matched expert size” means

Here, \(X\) counts accumulated expert-capacity units. “X→X+1” means adding one
new LoRA unit matched to the project’s declared expert budget across all target
modules. It does **not** mean setting LoRA rank equal to hidden width.

A rank-\(r\) LoRA on one projection has \(r(d_{in}+d_{out})\) parameters, so
rank remains an implementation variable. Each capacity-unit definition records:

- stored and trainable adapter parameters;
- active parameters and FLOPs along the routed path;
- target-module coverage and rank allocation by layer;
- peak VRAM, cache residency, and p95 latency;
- marginal capability gained over \(S_k\).

The initial unit may use a practical rank sweep. The matched-size hypothesis is
then tested with equal-budget alternatives: one additional residual unit, one
wider adapter, a flat sibling, continued training of the current adapter, and a
dense multi-task adapter. “Expert-sized” is earned empirically if repeated units
produce roughly comparable useful capacity; it is not asserted from parameter
count alone.

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

## Progressive hierarchy

Subdivide a broad expert only when its residual errors cluster into stable,
high-volume subdomains. The child is trained over the exact frozen parent path,
so its manifest pins the ordered ancestor digests. A child cannot be attached
directly to the base or a different parent without retraining and evaluation.

Compare:

- flat routing over independently trained leaf experts;
- parent path plus a child residual, \(S_k + \Delta_{k+1}\);
- a single wider LoRA with the same stored/active budget;
- continued tuning or replacement of the parent;
- retrieval shortlist followed by a learned router;
- child-only delta trained directly from the base.

Each boundary exposes a calibrated head/stop route. This makes depth conditional:
easy or already-covered inputs stop at \(S_k\), while only the relevant
knowledge region pays for \(S_{k+1}\). The hierarchy must win on marginal
capability per active byte, FLOP, and millisecond, not merely parameter count. A
flat oracle quantifies the routing tax.

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
