# Result-directed roadmap

## Milestone 0 — Reproducible foundation

- [x] Vision, architecture, prior art, gates, and decision process.
- [x] Expert and graph contracts with dependency-free validation.
- [x] Frozen-expert/router semantic smoke proof.
- [x] RTX 3060 and Vulkan/XPU/ROCm lanes.
- [ ] Full environment lock and CUDA probe.
- [ ] Dataset/evaluation fixture and run-record writer.
- [ ] Base-model selection benchmark.

Exit: harness controls pass and one base fits the 12 GB envelope.

## Milestone A — Flat experts

- [ ] Implement PEFT expert training command.
- [ ] Implement adapter export/admission checks.
- [ ] Train four independent experts.
- [ ] Implement retrieval, learned sequence, and token routers.
- [ ] Dense LoRA, merge, retrieval, and oracle baselines.
- [ ] Three-seed matched evaluation and router addition/removal test.
- [ ] CUDA reference runtime and golden traces.

Exit: Gate A in `EXPERIMENT_PLAN.md`, followed by human review.

## Milestone B — Progressive expert stacks

- [ ] Calibrate the whole-adapter expert-capacity unit and equal-budget controls.
- [ ] Select one broad path by stable residual-error clustering.
- [ ] Freeze Sₖ and train one matched child residual for Sₖ₊₁.
- [ ] Compare residual stacking with wider, continued, replacement, and flat
  sibling training.
- [ ] Implement first-class `answer`/`extend`/`branch` routing at every boundary.
- [ ] Calibrate decision-class confidence separately from destination selection.
- [ ] Repeat one growth event to test transfer of the unit and growth rule.
- [ ] Add ancestor-chain digests to manifest validation and runtime admission.
- [ ] Graph planner, marginal-cost estimator, and topology visualisation.
- [ ] First independently contributed root/extension/branch compatibility trial.
- [ ] Measure router-only catalog integration time for fetch, add, revoke, and
  rollback workflows.

Exit: Gate B. If it fails, retain useful flat experts and do not force depth.

## Milestone C — Adaptive computation

- [ ] Compatible intermediate head and calibration.
- [ ] One bounded loop node/runtime.
- [ ] Forced-depth/intermediate supervision.
- [ ] KV/position semantics and hidden-state stability diagnostics.
- [ ] Equal-FLOP and extra-token baselines.

Exit: Gate C plus safety review.

## Milestone D — Generated experts

- [ ] Same-base adapter corpus and canonical latent representation.
- [ ] Retrieval/interpolation/hypernetwork baselines.
- [ ] Diffusion generator only if simpler generators leave a justified gap.
- [ ] Held-out task/base tests, uncertainty, admission and refinement.

Exit: Gate D. Generated artifacts remain candidates, never trusted shortcuts.

## Ecosystem track

- [ ] Manifest 0.2 from real artifacts.
- [ ] CLI catalog, reproduce, benchmark, and publish commands.
- [ ] Provider-neutral index and Hugging Face/GitHub adapters.
- [ ] Signatures, attestations, licence policy, revocation.
- [ ] Web/API/MCP interfaces after two independent publishers succeed.

## Portability track

- [ ] CUDA reference inference.
- [ ] Vulkan sequence-routing prototype.
- [ ] Meteor Lake Vulkan and XPU profiles.
- [ ] Strix Halo Vulkan and ROCm profiles.
- [ ] Golden routing/logit traces and capability negotiation.
- [ ] ONNX Runtime/.NET integration after contracts stabilise.

## Enterprise track

- [ ] Shared lab artifact/job services.
- [ ] Tenant policy and approval workflow.
- [ ] Canary, rollback, audit, SLO dashboards.
- [ ] OpenAI-compatible serving and Microsoft Agent Framework wrapper.
- [ ] Threat model, red team, recovery, compliance evidence.

Enterprise work starts with small design spikes during A/B and scales only after
the core system demonstrates a workload-specific advantage.
