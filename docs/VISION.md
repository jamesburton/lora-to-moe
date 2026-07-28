# Vision and hypotheses

## Product thesis

Today, adapting one base model to many domains usually means training one
multi-task adapter, switching whole adapters per request, statically merging
adapters, or serving multiple models. LoRA → MoE proposes a fifth option:
begin with a smaller, less capable dense model; train broad expert LoRAs and a
root router; then grow only the knowledge paths that need more capacity by
training another residual LoRA over the frozen selected stack.

The long-term unit of collaboration is not a monolithic checkpoint. It is a
signed expert artifact plus evidence, provenance, compatibility metadata, and a
graph describing how experts, routers, base paths, heads, exits, and bounded
loops compose.

## Falsifiable hypotheses

| ID | Hypothesis | Cheapest useful falsification |
|---|---|---|
| H1 | Independent LoRAs retain ≥95% of their isolated specialist gain after frozen composition. | Four disjoint synthetic/real tasks on a ≤1.5B base. |
| H2 | A learned router beats retrieval and static merging at matched active parameters without >1 point general regression. | Phase A on three seeds. |
| H3 | A path can grow from X to X+1 matched expert-capacity units and outperform equal-budget widening, continued training, and a flat sibling. | Add one residual child to the best broad expert, then repeat once. |
| H4 | A base/null route reduces negative transfer and unnecessary compute. | Remove it and compare calibration, general quality, and activation. |
| H5 | Bounded latent loops provide a quality/compute Pareto improvement over fixed depth or extra output tokens. | One loop location, 0–3 iterations, forced-depth and post-hoc exit baselines. |
| H6 | Generated LoRA deltas cut time-to-expert materially while retaining ≥90% of a trained expert’s gain. | Hypernetwork before diffusion; held-out tasks and ranks. |
| H7 | A portable manifest/graph is sufficient to reproduce routing semantics across CUDA and portable inference backends. | Golden routing traces on two backends. |

## What may be unique

Mixtures of LoRA experts, hierarchical adapter routing, adapter retrieval, and
generated LoRA weights all have prior art. The defensible research contribution
is the combined systems hypothesis:

- experts trained independently by different parties;
- a compatibility-checked, content-addressed registry and declarative graph;
- routers retrained cheaply when catalog membership changes;
- broad expert → specialist residual-stack growth driven by measured residual
  error, with calibrated stop/head routes at every boundary;
- content-addressed ancestry so independently shared children reproduce the
  exact frozen expert stack they were trained upon;
- explicit base/head/exit choices;
- bounded latent recursion as a later graph primitive;
- generated expert candidates subjected to the same evidence and governance;
- matched-cost evaluation and portable execution on consumer hardware.

Claims must remain scoped to what experiments actually show. “Novel” means a
literature search did not find the same combination, not proof of patentability
or absence of unpublished work.

## Non-goals until earned

- Training a foundation model from scratch.
- Unbounded recurrent graphs.
- Assuming more experts, deeper paths, or larger ranks are inherently better.
- Calling rank equal to hidden width “matched expert size”; matching applies to a
  declared whole-adapter capacity unit and must survive equal-budget controls.
- Treating Vulkan as the initial training API. It is primarily an inference and
  portability target; CUDA, XPU, and ROCm are separate training backends.
- Hosting arbitrary pickle files or executable expert install hooks.
- Enterprise control-plane work before Phase A has a positive signal.
