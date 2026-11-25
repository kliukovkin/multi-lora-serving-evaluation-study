# Engine support matrix: multi-adapter (LoRA) serving

Checked 2026-11-23. "n.d." = not documented on the pages read (docs silent; nothing inferred).
Release dates: GitHub release pages show day and month only, without the year. The year is NOT confirmed for any release date below unless stated. GitHub API endpoints (api.github.com) were unreachable from this environment (Bash: access not enabled; WebFetch: client_error). The `.atom` feeds are robots-disallowed and were not fetched. "Archived" status is taken from the repo page banner.

## Table

| Engine | Latest release (page) | Archived / maintenance | Dynamic load/unload | Heterogeneous batching (kernel named) | Limits / eviction / pinning | Per-request selection |
|---|---|---|---|---|---|---|
| vLLM | v0.32.0, 18 Oct (year not shown); stable docs source links say v0.34.0 (conflict) | Not archived (no banner) | Yes: POST `/v1/load_lora_adapter`, `/v1/unload_lora_adapter`, needs `VLLM_ALLOW_RUNTIME_LORA_UPDATING=True`; `load_inplace`; LoRAResolver plugins | Docs: parallel with other LoRA requests "if max_loras set high enough". Kernels (source): Triton `lora_shrink`/`lora_expand`, Punica-attributed. Docs page does not name Punica/SGMV/Triton | `--max-lora-rank`, `--lora-target-modules`; `max_loras`/`max_cpu_loras` named but not defined on the page; LRU in source (`LRUCacheWorkerLoRAManager`); pinning n.d. | `model` field |
| SGLang | v0.5.21, 02 Oct (year not shown) | Not archived (not checked beyond release page) | Yes: `/load_lora_adapter`, `/unload_lora_adapter` (admin key required) | Yes, "different adapters for different sequences within a single batch", "based on S-LoRA and Punica"; backends `triton`, `csgmv` | `--max-loras-per-batch` (default 8), `--max-loaded-loras` (CPU), `--max-lora-rank`, `--lora-eviction-policy` lru (default)/fifo; pinning supported (`pinned`) | native `lora_path` list; OpenAI API `model=base:adapter` |
| HF TGI | v3.3.7, 19 Dec (year not shown) | Archived by owner 21 Mar 2026, read-only; README says "maintenance mode" | n.d. (startup only via `LORA_ADAPTERS`) | n.d. (docs say only "optimized kernels", credit punica and LoRAX) | n.d. | `parameters.adapter_id` |
| LoRAX | lorax-0.4.0 marked Latest, 13 Jan; v0.12.1, 25 Nov also listed (year not shown) | Not archived; no status note | Yes, "just-in-time" from HF/Predibase/local | Yes, "heterogeneous continuous batching"; SGMV (Punica credited) | Adapter exchange scheduling (GPU/CPU offload); eviction policy and flags n.d. | `adapter_id` |
| NVIDIA NIM for LLMs | doc v2.1.6 (container version) | n/a | Yes in dynamic mode (`NIM_PEFT_REFRESH_INTERVAL`; `POST /v1/load_lora_adapter`, `/v1/unload_lora_adapter`) | n.d. (backends vLLM and SGLang only; TRT-LLM not mentioned) | `--max-loras`, `--max-cpu-loras`, `--max-lora-rank` | `model` (SGLang: `<served-model>:<adapter>`) |
| TensorRT-LLM | v1.3.0rc29 (prerelease), 29 Sep (year not shown); no stable found in the visible page | Not checked | Per-request `LoRARequest`, adapter cached after first use (docs v1.4.0rc4) | Docs: "Switch between different adapters for different requests"; MoE: Cutlass fused kernel and grouped-GEMM core; dense kernel n.d. | `max_loras`, `max_cpu_loras`, `max_lora_rank` appear in examples only; older doc: oldest evicted | `LoRARequest` / `task_id` |
| Triton Inference Server | v2.74.0 (NGC 26.10), 02 Nov (year not shown) | Not checked | n.d. (no LoRA page read) | n.d. | n.d. | n.d. |
| llama.cpp server | v1.0.0 Latest, 13 Nov (year not shown) | Not archived (not checked) | Partial: `POST /lora-adapters` changes global scale only; adapters loaded at startup via `--lora` | No: "requests with different LoRA configurations will not be batched together" | no adapter limit stated | per-request `lora` list of `{id, scale}` |
| LMDeploy | v0.18.0, 28 Sep (year not shown) | No archive banner visible | n.d. | n.d. | n.d. | `model` field |
| Ray Serve LLM | Ray-2.59.0, 02 Oct (year not shown); docs page header says 2.60.1 (conflict) | n/a | Yes, loaded on demand from `dynamic_lora_loading_path` | n.d. (vLLM engine; `max_loras` = max LoRAs per batch) | `max_num_adapters_per_replica` (must match `max_loras`); per-replica LRU | `model=<base_model_id>:<adapter_name>` |
| KServe LLMInferenceService | v0.20.0, 6 Aug 2026 (v0.21.0-rc0 prerelease); docs "Version 0.21" | Not checked | No: "All adapters are loaded at startup (no dynamic loading)" | n.d. (delegates to vLLM `--enable-lora`) | `maxRank` (default 16), `maxAdapters` (default 1), `maxCpuAdapters`; 7 adapters max with default `exact` route template | `model` = adapter name |
| AIBrix ModelAdapter | v0.7.0, 18 June (year not shown) | Not checked | Yes, via runtime sidecar registering with the engine (endpoint path not on page) | n.d. | `schedulerName` default / `least-adapters`; replicas nil or 1 | adapter name as `model` via gateway |
| GIE / llm-d | GIE v1.6.2, 17 Sep; llm-d v0.9.0, 17 Aug (years not shown) | Not checked | GIE: "LoRA syncer ConfigMap" `ensureExist`/`ensureNotExist` | n/a (routing layer) | GIE `lora-affinity-filter` (`threshold` 0.999); llm-d scheduler page: no LoRA text | `model`; `InferenceModelRewrite` maps names/traffic split |
| NVIDIA Dynamo | Releases page: v1.4.2, 29 Aug (year not shown); docs say v1.6.1 (conflict) | Not checked | Yes: `POST/GET /v1/loras`, `DELETE /v1/loras/{name}`; `DynamoModel` CRD | n.d. | `--max-loras`, `--max-lora-rank` | `model` = adapter name |
| SageMaker adapter inference components | n.d. | n/a | Adapter IC "loaded by the base inference component" on invoke | n.d. | n.d. | `InferenceComponentName` in `invoke_endpoint` |
| Fireworks | n/a | n/a | `firectl load-lora` onto a BF16 deployment | n.d. | max adapters n.d. | `model=<model_name>#<deployment_name>` |
| Together | n/a | n/a | Serverless LoRA discontinued | n.d. | n.d. | n.d. |
| Friendli | n/a | n/a | n.d. | n.d. | n.d. | n.d. |

## Capability notes (item 6)

| Engine | TP / multi-GPU | Quantized base | MoE | DoRA / other PEFT | Multimodal |
|---|---|---|---|---|---|
| vLLM | n.d. (only an MoE example uses `--tensor-parallel-size 4`) | n.d. | Yes, 2D/3D adapters with `--enable-mixed-moe-lora-format` | n.d. | Experimental, tower and connector; `--default-mm-loras` |
| SGLang | Yes, `tp_size`, sharding per S-LoRA; PP and DP attention described | n.d. | n.d. | n.d. | n.d. |
| LoRAX | Listed, no detail | fp16, bitsandbytes, GPT-Q, AWQ | n.d. | PEFT and Ludwig adapters | n.d. |
| TensorRT-LLM | Partitioning rules for ColumnLinear/RowLinear (older doc) | "LoRA works with quantized models"; FP8 block-scale, NVFP4, MXFP8, INT4, INT8 unsupported for MoE LoRA | Yes, routed-expert, Cutlass MoE only | DoRA: needs `--dora_plugin enable` (older doc); rejected for MoE modules (new doc) | n.d. |
| Dynamo | n.d. | n.d. | n.d. | n.d. | n.d. |

## Per-engine notes and URLs

### vLLM
- Docs, doc footer date October 21, 2026 (latest dev docs): https://docs.vllm.ai/en/latest/features/lora/. Stable docs, same footer date: https://docs.vllm.ai/en/stable/features/lora/
- Release: https://github.com/vllm-project/vllm/releases (latest shown v0.32.0, 18 Oct). The stable docs page source links point to v0.34.0, so the release page fetch may be stale; version unresolved.
- Claim "vLLM's multi-LoRA path uses Punica-derived kernels and S-LoRA-style paging":
  - Punica part is supported by source. `vllm/lora/punica_wrapper/punica_base.py` docstring: "Based on: Chen, L., Ye, Z., Wu, Y., Zhuo, D., Ceze, L., & Krishnamurthy, A. (2023). Punica: Multi-Tenant LoRA Serving." with https://arxiv.org/abs/2310.18547. URL: https://raw.githubusercontent.com/vllm-project/vllm/main/vllm/lora/punica_wrapper/punica_base.py. Same attribution in `punica_gpu.py` (class docstring: "to provide the interface for the punica triton kernel") and in the Triton ops `lora_shrink_op.py`, `lora_expand_op.py` (both under `vllm/lora/ops/triton_ops/`). Comment in punica_base: "these attributes are the information required for sgmv kernel".
  - Release notes for v0.3.0 say "Experimental multi-lora support" and mention Punica kernel build changes (#2605, #2632); S-LoRA is not mentioned: https://github.com/vllm-project/vllm/releases/tag/v0.3.0
  - S-LoRA / paging: found NO mention of S-LoRA in the LoRA docs page, the files above, or `worker_manager.py`. The code shows an LRU cache of adapters (`LRUCacheWorkerLoRAManager`, https://github.com/vllm-project/vllm/blob/main/vllm/lora/worker_manager.py), which is not documented as paging. The "S-LoRA-style paging" half is not supported by what I read. I could not read `vllm/lora/models.py` (fetch failed).
- Batching: "in parallel with base model requests, and potentially other LoRA adapter requests" if `max_loras` is "set high enough".

### SGLang
- Docs (redirect from docs.sglang.ai): https://docs.sglang.io/docs/advanced_features/lora.md. Page states no SGLang version.
- Release page: https://github.com/sgl-project/sglang/releases (v0.5.21, 02 Oct).
- Internal inconsistency in docs: `--lora-backend` default is not given in the arguments section, but the backend section says "Default chunked SGMV backend". Docs say `csgmv` "achieves 20% to 80% latency improvements over the basic triton backend".
- Pinned adapters capped at `--max-loras-per-batch` minus 1. DPA requires Triton backend and all adapters pinned. Embedding layer, unified paging, Cutlass backend "still under development".

### Hugging Face TGI
- Repo: https://github.com/huggingface/text-generation-inference. Banner: "archived by the owner on Mar 21, 2026. It is now read-only"; README: "now in maintenance mode".
- Releases page: https://github.com/huggingface/text-generation-inference/releases (v3.3.7, 19 Dec, year not shown; given the archive date it is presumably 2025, unverified).
- LoRA doc: https://huggingface.co/docs/text-generation-inference/main/en/conceptual/lora. Startup only via `LORA_ADAPTERS`, `adapter_id`, available from about 2.0.6. Credits punica-ai/punica and LoRAX for kernels.

### LoRAX
- Docs: https://loraexchange.ai/. Repo: https://github.com/predibase/lorax (not archived, no status note). Releases: https://github.com/predibase/lorax/releases (lorax-0.4.0 "Latest" 13 Jan; v0.12.1 25 Nov listed; ordering odd, year unknown). Docs state no version.

### NVIDIA NIM / TensorRT-LLM / Triton
- NIM LoRA page (v2.1.6): https://docs.nvidia.com/nim/large-language-models/latest/peft.html. Page does not document `NIM_MAX_GPU_LORAS`/`NIM_MAX_CPU_LORAS`; uses shared args. Heterogeneous batching n.d.
- TRT-LLM current feature page (v1.4.0rc4, last updated November 16, 2026, commit ab2dfeb): https://nvidia.github.io/TensorRT-LLM/latest/features/lora.html. Older page (commit 0c9430e, September 15, 2025, v1.1.0rc5): https://nvidia.github.io/TensorRT-LLM/advanced/lora.html. Older page says "If the cache is full, the oldest LoRA will be evicted"; the new page does not mention eviction policy. Do not mix the two versions in the paper.
- TRT-LLM releases: https://github.com/NVIDIA/TensorRT-LLM/releases (only prereleases visible in the first 100k characters; v1.3.0rc29, 29 Sep).
- Triton Inference Server releases: https://github.com/triton-inference-server/server/releases (v2.74.0). I did not read a Triton LoRA page, so Triton LoRA is not covered (the TRT-LLM backend route is unverified).

### llama.cpp
- Server README: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md. Flags `--lora`, `--lora-scaled`, `--lora-init-without-apply`. `/lora-adapters` GET/POST sets global scale. Per-request `lora` field overrides. Quote: "requests with different LoRA configurations will not be batched together, which may result in performance degradation."
- Releases: https://github.com/ggml-org/llama.cpp/releases (v1.0.0 Latest, 13 Nov; build b12380 pre-release 14 Nov).

### LMDeploy
- Docs (updated Jun 11, 2026): https://lmdeploy.readthedocs.io/en/latest/llm/api_server_lora.html. "LoRA is currently only supported by the PyTorch backend." `--adapters name=path`. Releases: https://github.com/InternLM/lmdeploy/releases (v0.18.0, 28 Sep).

### Ray Serve LLM
- Docs: https://docs.ray.io/en/latest/serve/llm/user-guides/multi-lora.html (page header "Ray 2.60.1"). Releases page shows Ray-2.59.0 as Latest (https://github.com/ray-project/ray/releases); the mismatch is unresolved. Routing: prefers replicas that already have the adapter, else the default router (Power of 2).

### KServe
- LoRA doc (Version 0.21): https://kserve.github.io/website/docs/model-serving/generative-inference/llmisvc/lora-adapters. Only `hf://` was tested. Optional regex routing via annotation `serving.kserve.io/lora-model-routing-strategy: regex`.
- Releases: https://github.com/kserve/kserve/releases (v0.20.0, August 6, 2026).

### AIBrix
- Doc: https://aibrix.readthedocs.io/latest/features/lora-dynamic-loading.html (no explicit version; mentions v0.2.0 sidecar behaviour, examples use runtime v0.3.0 and vLLM v0.7.1, so the page may be old). Releases: https://github.com/vllm-project/aibrix/releases (v0.7.0).

### GIE / llm-d
- GIE adapter rollout: https://gateway-api-inference-extension.sigs.k8s.io/guides/adapter-rollout/. GIE multi-LoRA: https://gateway-api-inference-extension.sigs.k8s.io/guides/serve-multiple-lora-adapters (uses `InferenceModel` v1alpha2, may be older than rollout page which uses `InferenceModelRewrite`). EPP plugin: `lora-affinity-filter`, https://gateway-api-inference-extension.sigs.k8s.io/guides/epp-configuration/config-text/. Releases: https://github.com/kubernetes-sigs/gateway-api-inference-extension/releases (v1.6.2).
- llm-d: scheduler page has no LoRA mention: https://llm-d.ai/docs/architecture/Components/inference-scheduler. Releases: https://github.com/llm-d/llm-d/releases (v0.9.0).

### NVIDIA Dynamo
- Doc (Latest v1.6.1): https://docs.nvidia.com/dynamo/latest/kubernetes/operations/lo-ra-adapters. vLLM supported; SGLang experimental; TensorRT-LLM not supported. LoRA-aware KV routing for vLLM only (adapter name mixed into block hashes).
- Releases page (https://github.com/ai-dynamo/dynamo/releases) shows v1.4.2 as Latest, conflicting with docs v1.6.1.

### SageMaker
- https://docs.aws.amazon.com/sagemaker/latest/dg/realtime-endpoints-adapt.html. `BaseInferenceComponentName` inside `Specification`; adapter artifact is tar.gz in S3. Blog (not read): https://aws.amazon.com/blogs/machine-learning/easily-deploy-and-manage-hundreds-of-lora-adapters-with-sagemaker-efficient-multi-adapter-inference

### Serverless (docs only)
- Fireworks: https://docs.fireworks.ai/fine-tuning/deploying-loras. Multi-LoRA on one BF16 deployment (FP8/FP4 shapes do not support addons); serverless LoRA is Preview, on request.
- Together: https://docs.together.ai/docs/lora-inference. "Serverless LoRA inference (including Serverless Multi-Lora) has been discontinued"; adapters served on dedicated endpoints.
- Friendli: https://friendli.ai/docs/guides/dedicated-endpoints/multi-lora-serving. Dedicated Endpoints only; API selection not described. (Container doc exists at https://friendli.ai/docs/guides/container/serving-multi-lora-models, not read.)

## Claims I could not verify
1. Years for all GitHub release dates (pages show day and month only); GitHub API and atom feeds unavailable.
2. Whether vLLM's latest is v0.32.0 or v0.34.0 (conflicting pages). Same kind of conflict for Ray (2.59.0 vs 2.60.1 docs) and Dynamo (v1.4.2 vs docs v1.6.1).
3. "S-LoRA-style paging" in vLLM: no supporting text found; Punica-derived Triton kernels are supported by source attribution only (source on main, not tied to a release version).
4. vLLM eviction/pinning/`max_loras` semantics in docs, TP, quantization, DoRA: not documented on the LoRA page.
5. Archived status for everything except TGI (confirmed) and vLLM/LoRAX (no banner seen): not checked for SGLang, TRT-LLM, Triton, llama.cpp, KServe, AIBrix, GIE, llm-d, Dynamo. LMDeploy inferred from page header only.
6. Latest stable TensorRT-LLM release (only prereleases seen); Triton Inference Server LoRA support (no page read); TRT-LLM dense-LoRA batching kernel.
7. SGLang quantization/MoE/DoRA/multimodal and docs version: not documented.
8. NIM heterogeneous batching and TP/quant/MoE; AIBrix batching and load endpoint path; KServe batching; SageMaker containers, limits, caching, autoscaling; Fireworks adapter limits; Friendli API selection and limits; Together request selection.
9. GIE adapter-aware load-aware routing via `running_lora_adapters`/`waiting_lora_adapters` metrics: not found on pages read; only `lora-affinity-filter` found. llm-d LoRA routing: not found.
10. llama.cpp `/lora-adapters` page text read from the master README (no release tag tied to it).
