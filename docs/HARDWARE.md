# Hardware and backend plan

## RTX 3060 12 GB reference

Reserve approximately 0.8 GiB for allocator variance, kernels, and evaluation.
The configuration caps measured peak usage at 11.2 GiB.

### Progressive ladder

| Stage | Model | Purpose | Expected method |
|---|---:|---|---|
| CI | synthetic / 135M | contracts and semantic smoke | CPU or CUDA |
| Fail-fast | 0.5–1.5B | rank/router screens | BF16/FP16 LoRA |
| Primary | 2–4B | decision-grade Phase A | NF4 QLoRA |
| Confirmation | ~7B | scale transfer only | NF4, batch 1, checkpointing |

Do not assume a model fits from weight size alone. Record CUDA context,
quantisation metadata, activations, gradients, optimiser state, router/expert
residency, fragmentation, and evaluation generation cache.

### Default tactics

- NF4 frozen base with double quantisation where supported.
- BF16 compute if the exact GPU/runtime path is stable; otherwise FP16.
- Router logits/loss in FP32.
- Batch 1, gradient accumulation, gradient checkpointing, length bucketing.
- Paged 8-bit optimiser for trainable adapters.
- Train experts one at a time; keep inactive experts on CPU/disk.
- During router training, measure all-resident against cache/streaming designs.
- Disable long generation during training evaluation; run it as a separate job.

The 7B profile is not the default: several active high-rank adapters, long
contexts, or top-2 routing may exceed 12 GB even with a 4-bit base.

## Vulkan portability lane

Vulkan is primarily an inference target. The first goal is semantic and quality
parity on quantised base + selected adapter, then routing overhead:

1. Export or convert base and adapters to a runtime-supported representation.
2. Validate one adapter against CUDA golden logits/tokens within declared
   quantisation tolerance.
3. Validate top-1 adapter selection at sequence boundaries.
4. Measure adapter switching and cache residency.
5. Add top-2 only when the runtime can combine deltas without material CPU
   fallback or recompilation.
6. Run identical traces on Meteor Lake and Strix Halo.

Per-token dynamic routing may be impractical in generic Vulkan runtimes until
fused kernels exist. Sequence routing/hotswap is the viable first target.

## Meteor Lake

Test three distinct paths rather than labelling all of them “Vulkan”:

- Vulkan runtime for portable quantised inference.
- PyTorch XPU/Intel GPU stack for native operator coverage.
- CPU/NPU path only where the chosen runtime supports the graph.

Record shared-memory reservation, driver, oneAPI/Level Zero versions, power
mode, thermals, precision, and unsupported/fallback operators. Integrated GPU
bandwidth and memory contention may dominate nominal compute.

## Strix Halo

Test:

- ROCm/PyTorch on a supported Linux or WSL combination for training/native
  inference;
- Vulkan runtime for portable inference;
- unified-memory allocation and bandwidth sensitivity.

ROCm support changes quickly and is specific to SKU, OS, kernel, driver, and
runtime versions. Pin and publish the entire environment. Do not infer support
for “Strix Halo” generally from one working SKU.

## Cross-backend acceptance

- Same manifest and graph accepted.
- Router top-k choices match on golden inputs unless declared tolerance applies.
- Greedy output matches for unquantised comparable paths; quantised paths report
  logit error and task-score tolerance.
- No silent CPU fallback.
- Peak memory, power mode, TTFT, token latency, throughput, load time, and
  adapter switch time reported.
- Backend limitations recorded as capability metadata, not hidden branches.
