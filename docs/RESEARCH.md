# Research synthesis

Research snapshot: 2026-07-27. Prefer primary papers and official project or
vendor documentation. Results below guide experiments; they do not replace
local reproduction.

## Closest prior art

### Mixtures and routing of LoRA experts

- [MoLE](https://arxiv.org/abs/2404.13628) uses hierarchical control and
  flexible branch selection to combine LoRAs, directly establishing that
  routing can outperform arithmetic merging.
- [MixLoRA](https://arxiv.org/abs/2404.15159) inserts routed LoRA experts into
  frozen feed-forward blocks and reports consumer-GPU efficiency. Its stated
  24 GB setting reinforces the need for a more aggressive 12 GB profile here.
- [MoCLE](https://arxiv.org/abs/2312.12379) clusters tasks and mixes
  cluster-conditional LoRA experts with a universal expert, supporting both
  task-aware routing and our base/general path.
- [Retrieval-Augmented Mixture of LoRA Experts](https://arxiv.org/abs/2406.16989)
  frames public adapters as “uploadable ML” and retrieves adapters for a query.
  Retrieval must therefore be a baseline and may become a shortlist stage.
- [SMoRA](https://arxiv.org/abs/2501.15103) shows a useful equivalence between
  multi-LoRA routing and sparsely activating rank components of one LoRA. We
  must compare expert-level against rank-level routing rather than assuming
  expert boundaries are optimal.
- [HoE](https://arxiv.org/abs/2505.20925) and
  [HMoRA](https://openreview.net/forum?id=lTkHiXeuDl) make hierarchical LoRA
  routing an established adjacent design. Our hierarchy claim must focus on
  independently published artifacts, measured graph growth, and portability.
- [LoRA-Mixer](https://arxiv.org/abs/2507.00029) dynamically routes LoRA experts
  in attention projections and highlights cross-architecture linear modules.
- [LD-MoLE](https://arxiv.org/abs/2509.25684) learns dynamic sparsity; this is a
  later comparison if fixed top-k leaves a meaningful quality/compute gap.
- [LoRAuter](https://arxiv.org/abs/2601.21795) routes/composes adapters using
  task representations, strengthening the task-embedding baseline.
- [Hard-Routed Mixtures of Reasoning LoRAs](https://arxiv.org/abs/2606.31413)
  closely matches our two-stage idea: independently trained frozen reasoning
  experts followed by a lightweight router. This sharply narrows any novelty
  claim for Phase A; our value must come from generality, graph hierarchy,
  ecosystem contracts, hardware constraints, and stronger matched baselines.

**Implication:** Phase A is validation and infrastructure, not a claim that
frozen LoRA routing itself is new. The central follow-on question is progressive
residual growth: freeze a routed path Sₖ, train one child LoRA to form Sₖ₊₁, and
let the boundary router stop or descend. This must be distinguished from merely
adding more parallel LoRAs or increasing rank. The null/base route, pinned
ancestor chains, measured growth rule, bounded recursion, and generated-expert
pipeline are the research combination to evaluate.

## Router stability and specialisation

[Switch Transformers](https://arxiv.org/abs/2101.03961) established sparse
top-1 routing and load-balancing concerns.
[ST-MoE](https://arxiv.org/abs/2202.08906) introduced router z-loss for
stability. [Expert Choice](https://arxiv.org/abs/2202.09368) reverses selection
to give experts fixed capacity, but is awkward for causal online decoding.
[Loss-Free Balancing](https://arxiv.org/abs/2408.15664) avoids auxiliary-loss
interference using expert-wise bias.

**Implication:** start with transparent top-1/top-2 plus balance and z-loss
ablations. Measure natural specialisation before forcing uniformity. A perfectly
balanced router is not inherently better; dead experts, overload, and quality
are the actual constraints.

## Hierarchy, exit, and latent recursion

[Mixture-of-Recursions](https://arxiv.org/abs/2507.10524) combines recursive
parameter sharing and adaptive token computation.
[LoopLM](https://arxiv.org/abs/2510.25741) and
[LoopFormer](https://arxiv.org/abs/2602.11451) investigate latent recurrent
depth and early exit. [LoopUS](https://arxiv.org/abs/2605.11011) recasts a
pretrained model into encoder, loop, and decoder with a selective gate and
confidence exit. [MELT](https://arxiv.org/abs/2605.07721) addresses KV memory
growth by updating one entry across loops.
[LoopMoE](https://arxiv.org/abs/2606.04438) explicitly unifies looped
computation with sparse expert routing.

**Implication:** routing back to an earlier arbitrary layer is unlikely to be
stable by configuration alone. Phase C must train a declared loop block,
preserve or explicitly update positional/KV state, supervise intermediate
depths, compare fixed iteration counts, and cap every path. Direct-to-head exits
require compatible intermediate heads and calibration.

## Generated LoRA weights

[DiffLoRA](https://arxiv.org/abs/2408.06740) uses a latent
diffusion-hypernetwork to generate SDXL LoRA weights for identity adaptation.
[HyperDreamBooth](https://arxiv.org/abs/2307.06949) predicts a personalised
delta before lightweight refinement. [SHINE](https://arxiv.org/abs/2602.06358)
explores an in-context hypernetwork that maps demonstrations to adapters.

Evidence is strongest in vision and personalisation; generation of reliable LLM
task adapters remains a higher-risk extrapolation. Diffusion should not be the
first generator baseline: direct hypernetwork regression, retrieval plus
interpolation, and low-dimensional latent prediction are cheaper and easier to
diagnose.

**Implication:** Phase D learns a canonicalised adapter latent space only after
a sizeable, licence-compatible corpus of same-base adapters exists. Evaluate
held-out tasks and base models, distribution shift, interpolation, refinement
steps, failure detection, and whether generation beats simply retrieving and
fine-tuning the nearest expert.

## Adapter interoperability

Hugging Face [PEFT configuration](https://huggingface.co/docs/peft/en/tutorial/peft_model_config)
requires adapter configuration and supports multiple adapters, while
[hotswapping](https://huggingface.co/docs/peft/en/package_reference/hotswap)
replaces LoRA weights in-place to avoid reallocation/recompilation. This is a
useful runtime primitive but does not define a cross-publisher compatibility,
licence, evaluation, graph, or trust contract.

**Implication:** build on PEFT/safetensors rather than replacing them. The
manifest adds immutable base/tokenizer digests, target-module schema,
capabilities, provenance, evaluations, licences, safety status, and graph
budgets. Never load pickle-based community weights in production.

## Hardware and model choice

[QLoRA](https://arxiv.org/abs/2305.14314) and official
[bitsandbytes documentation](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)
support training LoRA through a frozen 4-bit base, making 2–7B experiments
plausible within 12 GB with checkpointing and small micro-batches.
[Qwen3-4B](https://huggingface.co/Qwen/Qwen3-4B) is Apache-2.0, dense, 4B, and
32K-native, making it a practical primary candidate.

PyTorch documents the [`xpu` device](https://docs.pytorch.org/docs/stable/notes/get_start_xpu.html)
for Intel GPU execution. AMD now documents
[Ryzen AI Max / Strix Halo ROCm support](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/compatibility/compatibilityryz/native_linux/native_linux_compatibility.html)
and [WSL support](https://rocm.docs.amd.com/projects/radeon-ryzen/en/latest/docs/install/installryz/wsl/howto_wsl.html),
but support and limitations are version/OS-specific.

**Implication:** CUDA is the initial training reference. XPU and ROCm are native
portability lanes. Vulkan is measured primarily for inference through runtimes
such as llama.cpp/GGUF; it must not be conflated with native PyTorch training.
Backend claims require recorded driver, runtime, OS, precision, power mode, and
model/adapter conversion details.

## Open gaps worth testing

1. Compatibility-safe composition across independently governed publishers.
2. Router retraining cost and regressions as experts are added/removed.
3. Repeatable X→X+1 residual-stack growth based on residual-error clusters,
   tested against equal-budget widening, continued training, and flat siblings.
4. Content-addressed ancestor chains for independently shared child experts.
5. Base/head/child choices inside one constrained graph contract.
6. Portable golden traces for routed adapter semantics.
7. Combining independently trained experts with bounded latent computation.
8. Generated experts that carry uncertainty and pass the same admission gates.
9. Enterprise revocation: removing one compromised expert or ancestor without
   silently leaving dependent descendants active.
