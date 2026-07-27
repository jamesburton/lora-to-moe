# Enterprise deployment path

## Deployment stages

### 1. Research workstation

Local immutable cache, reproducible configs, single CUDA worker, offline
evaluation, and human-reviewed manifests.

### 2. Shared lab

Object storage, experiment tracker, job queue, GPU scheduling, central catalog,
role-based approvals, artifact retention, and reproducible containers.

### 3. Controlled service

Stateless OpenAI-compatible inference API, adapter cache, router/graph service,
tenant policy, canary rollout, telemetry, fallback, rate/resource budgets, and
signed releases.

### 4. Enterprise platform

Multi-region control plane, SSO/RBAC/ABAC, audit, private registries, customer
keys, residency controls, policy-as-code, supply-chain attestations, disaster
recovery, billing/showback, and formal SLOs.

## Runtime request flow

1. Authenticate tenant and resolve allowed graph revision.
2. Validate prompt/resource/safety policy.
3. Load pinned base/router; resolve admitted expert digests.
4. Route with declared budget and record trace metadata.
5. Apply experts from trusted cache; use base fallback on policy/runtime failure.
6. Generate with bounded compute.
7. Record metrics without raw prompt retention unless explicitly authorised.
8. Return model/router/expert revision identifiers for audit.

## Security

- Safetensors-only production policy and no arbitrary remote code.
- Content-addressed storage, signatures, provenance attestations, SBOMs.
- Sandboxed data preparation and evaluation execution.
- Egress denied by default for training/evaluation jobs.
- Secrets from a managed vault; never configs, manifests, logs, or artifacts.
- Dataset poisoning, backdoor, prompt-routing manipulation, and model-extraction
  tests before admission.
- Per-expert kill switch and cache purge by digest.
- Graph validator enforcing maximum depth, expert count, loop count, tokens,
  latency, and memory.

## Tenancy and governance

Policy can restrict base models, licences, publishers, datasets, regions,
capabilities, safety classifications, and maximum compute. Tenant-specific
experts and examples are invisible to global router training unless explicitly
approved. Aggregate learning needs privacy and contractual review.

Required roles:

- publisher: uploads candidate artifacts;
- evaluator: runs reproducible suites;
- reviewer: approves evidence/licence/provenance;
- operator: promotes/rolls back releases;
- auditor: reads immutable lineage and routing records.

Separate duties for high-risk production releases.

## Observability and SLOs

Metrics:

- per graph/router/expert quality canaries;
- routing entropy, confidence, drift, utilisation, fallback and rejection;
- adapter load/cache hit/switch time;
- TTFT, inter-token latency, throughput, queue, VRAM, OOM/retry;
- per-tenant tokens, active compute, energy estimate, and cost;
- policy denials, signature failures, revoked artifact use attempts.

Trace sampling must avoid secrets and personal data. Use irreversible prompt
features or consented redacted examples where raw text is not required.

Example initial SLOs:

- 99.9% successful requests excluding client/policy errors;
- 100% production artifacts signature- and digest-verified;
- zero execution of revoked experts after propagation window;
- p95 router overhead <5% of end-to-end batch-1 latency;
- fallback succeeds for ≥99.9% of adapter-load failures.

## Release and rollback

Every release pins base, tokenizer, graph, router, experts, runtime, and policy.
Deploy shadow → 1% canary → staged rollout. Automated rollback triggers include
quality-canary regression, router drift, latency/OOM breach, safety signal, or
signature/revocation event. Keep the prior graph warm during rollout.

## .NET integration

After research contracts stabilise:

- generate C# types from JSON Schema;
- expose graph/catalog operations through .NET 10 APIs;
- wrap inference endpoints using Microsoft Agent Framework interfaces;
- add OpenTelemetry and enterprise identity/policy integration;
- use TorchSharp only where its operator/backend coverage matches the reference;
- prefer ONNX Runtime or a native inference service where it is more mature.

Do not fork the Python research truth into a second incompatible format.
