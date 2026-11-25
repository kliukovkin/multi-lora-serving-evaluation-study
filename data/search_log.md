# Search log and IN/OUT decisions (generated 2026-11-23)

Rule used everywhere: IN if the item addresses a systems problem of executing, placing, loading, caching or managing MANY variants (adapters/deltas) of a shared base model at inference time AND reports a systems metric (latency/throughput/memory); OUT otherwise.

## Method notes and deviations

- WebFetch refused export.arxiv.org (robots_disallowed) and rate-limited arxiv.org. The Part 2 queries were therefore run with curl against https://export.arxiv.org/api/query (User-Agent research-script/1.0, 4 s between calls, max_results=100, sortBy=submittedDate). Several arXiv html pages were also read with curl for the same reason.
- Every query was ANDed with submittedDate:[202201010000 TO 202612312359]. Query text used field prefixes, e.g. all:"multi-LoRA" AND (all:serving OR all:inference).
- The API returned fewer than 100 hits for every query (max 30), so no truncation occurred. Result sets contain many off-topic items (the API ranks loosely on tokens).
- Recall check: the 9 queries together return 37 of the 64 coded records (58%). 22 coded records with an arXiv id are not returned by any query (e.g. FlexLLM, Chameleon, Symbiosis, AdaFuse, Scute, MARLaaS, PRIMAL, MinT, FLoRA, LoRA-Switch, aLoRA), so this protocol alone misses many known systems; treat the log as a supplement to citation chasing, not a census. (Five more coded records have no arXiv id.)
- Decisions for hits are from title+abstract, plus full text where I opened it (marked in out5.jsonl evidence).

## Part 2: per-query hit counts

| # | query | API totalResults | returned | already in all.json | not in corpus |
|---|---|---|---|---|---|
| 1 | `all:"multi-LoRA" AND (all:serving OR all:inference)` | 28 | 28 | 14 | 14 |
| 2 | `all:"LoRA adapters" AND all:serving AND (all:latency OR all:throughput)` | 19 | 19 | 14 | 5 |
| 3 | `all:"multi-tenant" AND all:LoRA AND all:serving` | 6 | 6 | 6 | 0 |
| 4 | `all:"adapter serving"` | 30 | 30 | 6 | 24 |
| 5 | `all:"LoRA serving"` | 18 | 18 | 15 | 3 |
| 6 | `all:"LoRA" AND all:"cold start"` | 23 | 23 | 3 | 20 |
| 7 | `all:"delta" AND all:"fine-tuned" AND all:serving AND all:compression` | 6 | 6 | 1 | 5 |
| 8 | `all:"KV cache" AND all:LoRA AND (all:agents OR all:sharing)` | 20 | 20 | 7 | 13 |
| 9 | `all:"co-serving" AND all:"fine-tuning" AND all:inference` | 3 | 3 | 3 | 0 |

Sum of per-query hits: 153. Unique hits: 120. Already in corpus (all.json): 37. Not in corpus: 83, of which newly IN: 7, OUT: 76.

Newly IN (arXiv id, title, one-line reason):

- 2402.10193 | BitDelta: Your Fine-Tune May Only Be Worth One Bit | 1-bit full-model deltas; multi-tenant memory and per-user decoding latency (>10x vs naive at B>=16)
- 2512.19720 | Per-Axis Weight Deltas for Frequent Model Updates | compressed deltas for serving many variants; cold-start load time 0.80 s vs 2.08 s
- 2406.08903 | Delta-CoMe: Training-Free Delta-Compression with Mixed-Precision for Large Language Models | mixed-precision deltas for multi-model serving; 50 models on one GPU, Triton kernel 3x
- 2406.09041 | ME-Switch: A Memory-Efficient Expert Switching Framework for Large Language Models | delta compression + routing for serving many experts; 16 models on one A100, latency vs naive
- 2405.00732 | LoRA Land: 310 Fine-tuned LLMs that Rival GPT-4, A Technical Report | benchmarks LoRAX with 25 adapters (TTFT, throughput); borderline: evaluation of an existing server
- 2603.15965 | MoLoRA: Composable Specialization via Per-Token Adapter Routing | per-token routing across adapters, hot-set memory, kernel speedups vs S-LoRA-style serving
- 2609.23321 | Co-occurrence Patterns of LoRA Adapters in Production Diffusion Model Inference Services | production adapter popularity and latency characterization plus preloading; borderline: characterization

## Part 2: every hit, by query

### Query 1: `all:"multi-LoRA" AND (all:serving OR all:inference)` (28 hits)

- 2611.10049 (2026-11-05) LoRazor: Trimming Adapter Execution for Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as LoRazor
- 2611.01256 (2026-10-31) LoRAForge: Co-Designing Post-Hoc Compression and Execution for Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as LoRAForge
- 2610.27444 (2026-10-20) LoRASpace: A Pool-Wide Shared Substrate for Static and Dynamic Multi-LoRA Composition -> OUT: OUT (borderline): multi-LoRA composition (N>=2 active LoRAs per generation, diffusion and FLAN-T5 pools) judged on quality; speedup only versus composite; not many-tenant serving
- 2609.34054 (2026-09-28) PReCache: Efficient KV Cache Sharing for Multi-LoRA Agents via Low-Rank Precomputation and Neutral Reconstruction -> IN-CORPUS: already coded as PReCache
- 2609.25884 (2026-09-22) LoRango: It Takes Two LoRAs to Unlock Hidden Behaviors in Diffusion Models -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2608.11752 (2026-08-12) UniSwap: Streaming Audio-Visual Identity Swapping for Talking Videos -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2608.05483 (2026-08-06) PLoRA: An NDP-Enhanced Pooled-Memory System for Cost-Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as PLoRA (NDP pooled memory)
- 2607.28848 (2026-07-30) DeltaServe: Host-Agnostic Co-Serving of Inference and Fine-Tuning for LLMs -> IN-CORPUS: already coded as DeltaServe
- 2606.03792 (2026-06-02) Training-Free Multi-Concept LoRA Composition with Prompt-Aware Weighting -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2604.18655 (2026-04-20) Unlocking the Edge deployment and ondevice acceleration of multi-LoRA enabled one-for-all foundational LLM -> IN-CORPUS: already coded as Multi-LoRA one-for-all on-device LLM (Samsung)
- 2604.07173 (2026-04-08) InfiniLoRA: Disaggregated Multi-LoRA Serving for Large Language Models -> IN-CORPUS: already coded as InfiniLoRA
- 2604.06370 (2026-04-07) ForkKV: Scaling Multi-LoRA Agent Serving via Copy-on-Write Disaggregated KV Cache -> IN-CORPUS: already coded as ForkKV
- 2603.29535 (2026-03-31) Quantization with Unified Adaptive Distillation to enable multi-LoRA based one-for-all Generative Vision Models on edge -> IN-CORPUS: already coded as QUAD
- 2602.07263 (2026-02-06) tLoRA: Efficient Multi-LoRA Training with Elastic Shared Super-Models -> IN-CORPUS: already coded as tLoRA
- 2601.09527 (2026-01-14) Private LLM Inference on Consumer Blackwell GPUs: A Practical Guide for Cost-Effective Local Deployment in SMEs -> OUT: OUT: consumer-GPU benchmarking study; multi-LoRA is one workload with 3 adapters on stock vLLM
- 2601.07376 (2026-01-12) OpenTinker: Separating Concerns in Agentic Reinforcement Learning -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2511.00101 (2025-10-30) Loquetier: A Virtualized Multi-LoRA Framework for Unified LLM Fine-tuning and Serving -> IN-CORPUS: already coded as Loquetier
- 2510.00206 (2025-09-30) LoRAFusion: Efficient LoRA Fine-Tuning for LLMs -> IN-CORPUS: already coded as LoRAFusion
- 2509.24229 (2025-09-29) Model Fusion with Multi-LoRA Inference for Tool-Enhanced Game Dialogue Agents -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2508.13037 (2025-08-18) Can Large Models Teach Student Models to Solve Mathematical Problems Like Human Beings? A Reasoning Distillation Method via Multi-LoRA Interaction -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2508.11624 (2025-08-15) LoRAtorio: An intrinsic approach to LoRA Skill Composition -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2505.14468 (2025-05-20) ServerlessLoRA: Enabling Low-Latency Serverless Multi-LoRA Serving -> IN-CORPUS: already coded as ServerlessLoRA
- 2505.03756 (2025-04-19) Improving the Serving Performance of Multi-LoRA Large Language Models via Efficient LoRA and KV Cache Management -> IN-CORPUS: already coded as ELORA (preprint FastLibra)
- 2502.04923 (2025-02-07) Cached Multi-Lora Composition for Multi-Concept Image Generation -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2411.14064 (2024-11-21) Multi LoRA Meets Vision: Merging multiple adapters to create a multi task model -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2405.00557 (2024-05-01) Mixture of insighTful Experts (MoTE): The Synergy of Thought Chains and Expert Mixtures in Self-Alignment -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2405.00732 (2024-04-29) LoRA Land: 310 Fine-tuned LLMs that Rival GPT-4, A Technical Report -> NEW-IN: benchmarks LoRAX with 25 adapters (TTFT, throughput); borderline: evaluation of an existing server
- 2402.00913 (2024-02-01) Institutional Platform for Secure Self-Service Large Language Model Exploration -> OUT: OUT: institutional platform description built on multi-LoRA inference; no systems metric

### Query 2: `all:"LoRA adapters" AND all:serving AND (all:latency OR all:throughput)` (19 hits)

- 2611.22296 (2026-11-17) SpecSearch: Towards Hardware-Aware Efficient Speculative Decoding -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2611.10049 (2026-11-05) LoRazor: Trimming Adapter Execution for Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as LoRazor
- 2611.03899 (2026-11-02) EpiLoRA: Fusing Many LoRA Adapters into Low-Precision GEMMs for Serving and RL -> IN-CORPUS: already coded as EpiLoRA
- 2611.01256 (2026-10-31) LoRAForge: Co-Designing Post-Hoc Compression and Execution for Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as LoRAForge
- 2610.04956 (2026-10-04) From Overloaded to Guaranteed: High-Throughput Multi-SLO Enforcement for LoRA-Assisted On-Premise LLM Deployment -> IN-CORPUS: already coded as HALO
- 2609.23321 (2026-09-20) Co-occurrence Patterns of LoRA Adapters in Production Diffusion Model Inference Services -> NEW-IN: production adapter popularity and latency characterization plus preloading; borderline: characterization
- 2608.23807 (2026-08-24) Serving Masked Diffusion LLMs: Characterization and Design Principles from Real Hardware -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2608.03579 (2026-08-04) Pin Once, Swap Light: Subspace-Aligned Centroid-Residual Training for Efficient Ultra-LoRA Serving -> IN-CORPUS: already coded as SALT (Pin Once, Swap Light)
- 2604.16583 (2026-04-17) POLAR: Online Learning for LoRA Adapter Caching and Routing in Edge LLM Serving -> OUT: OUT (borderline): adapter caching and routing for edge serving, but a simulation with regret as the metric; measured GPU paging latencies (291-1263 ms) only calibrate a penalty; no end-to-end latency/throughput/memory metric
- 2604.07173 (2026-04-08) InfiniLoRA: Disaggregated Multi-LoRA Serving for Large Language Models -> IN-CORPUS: already coded as InfiniLoRA
- 2602.07263 (2026-02-06) tLoRA: Efficient Multi-LoRA Training with Elastic Shared Super-Models -> IN-CORPUS: already coded as tLoRA
- 2511.22880 (2025-11-28) Serving Heterogeneous LoRA Adapters in Distributed LLM Inference Systems -> IN-CORPUS: already coded as LoRAServe
- 2510.19670 (2025-10-22) CoSense-LLM: Semantics at the Edge with Cost- and Uncertainty-Aware Cloud-Edge Cooperation -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2508.08343 (2025-08-11) A Data-driven ML Approach for Maximizing Performance in LLM-Adapter Serving -> IN-CORPUS: already coded as Data-driven ML adapter-serving optimizer (Digital Twin)
- 2508.02932 (2025-08-04) PLoRA: Efficient Concurrent LoRA Training for Large Language Models -> IN-CORPUS: already coded as PLoRA (concurrent LoRA training)
- 2411.00915 (2024-11-01) Empower Vision Applications with LoRA LMM -> IN-CORPUS: already coded as VaLoRA
- 2407.00066 (2024-06-17) Compress then Serve: Serving Thousands of LoRA Adapters with Little Overhead -> IN-CORPUS: already coded as Compress then Serve (JD-Full / JD-Diag)
- 2401.11240 (2024-01-20) CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference -> IN-CORPUS: already coded as Toppings (CaraServe)
- 2311.03285 (2023-11-06) S-LoRA: Serving Thousands of Concurrent LoRA Adapters -> IN-CORPUS: already coded as S-LoRA

### Query 3: `all:"multi-tenant" AND all:LoRA AND all:serving` (6 hits)

- 2611.03899 (2026-11-02) EpiLoRA: Fusing Many LoRA Adapters into Low-Precision GEMMs for Serving and RL -> IN-CORPUS: already coded as EpiLoRA
- 2608.03579 (2026-08-04) Pin Once, Swap Light: Subspace-Aligned Centroid-Residual Training for Efficient Ultra-LoRA Serving -> IN-CORPUS: already coded as SALT (Pin Once, Swap Light)
- 2604.07173 (2026-04-08) InfiniLoRA: Disaggregated Multi-LoRA Serving for Large Language Models -> IN-CORPUS: already coded as InfiniLoRA
- 2511.22880 (2025-11-28) Serving Heterogeneous LoRA Adapters in Distributed LLM Inference Systems -> IN-CORPUS: already coded as LoRAServe
- 2507.01438 (2025-07-02) EdgeLoRA: An Efficient Multi-Tenant LLM Serving System on Edge Devices -> IN-CORPUS: already coded as EdgeLoRA
- 2310.18547 (2023-10-28) Punica: Multi-Tenant LoRA Serving -> IN-CORPUS: already coded as Punica

### Query 4: `all:"adapter serving"` (30 hits)

- 2611.12304 (2026-11-09) Evolving Infra: Agent-Adaptive LLM Serving at Scale -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2610.34610 (2026-10-25) Do Words Matter? What Text Contributes to Few and Full-Shot Vision-Language Anomaly Detection -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2610.13708 (2026-10-09) Adaptive DHiSparse: Speculative Decoding over a Load-Adaptive KV Hierarchy -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2609.31600 (2026-09-25) New LoRA Skills Should Read but Never Write -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2609.22098 (2026-08-12) TreeSpark: Calibrated, Load-Adaptive Draft Trees for Semi-Autoregressive Speculative Decoding -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2608.09892 (2026-08-10) XPolicyLab: A Unified Standard and Open Ecosystem for Robot Policy Evaluation and Deployment -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2608.09507 (2026-08-10) Learning Preference Adaptation for Large Language Model Personalization via Verbal Reinforcement Learning -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2608.05483 (2026-08-06) PLoRA: An NDP-Enhanced Pooled-Memory System for Cost-Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as PLoRA (NDP pooled memory)
- 2606.21085 (2026-06-19) Sim2O: Efficient Offline-to-Online MARL via Joint Action Composition -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2605.14217 (2026-05-14) PreFT: Prefill-only finetuning for efficient inference -> IN-CORPUS: already coded as PreFT
- 2605.11232 (2026-05-11) Rethinking LLMOps for Fraud and AML: Building a Compliance-Grade LLM Serving Stack -> OUT: OUT (borderline): fraud/AML LLMOps stack; multi-adapter part is a 4-adapter case study on stock vLLM (3.90x over PEFT-style loading), not a multi-adapter serving contribution
- 2604.16117 (2026-04-17) SCRIPT: Implementing an Intelligent Tutoring System for Programming in a German University Context -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2603.15965 (2026-03-16) MoLoRA: Composable Specialization via Per-Token Adapter Routing -> NEW-IN: per-token routing across adapters, hot-set memory, kernel speedups vs S-LoRA-style serving
- 2602.24044 (2026-02-27) Data Driven Optimization of GPU efficiency for Distributed LLM-Adapter Serving -> IN-CORPUS: already coded as Data-driven GPU-efficient LLM-adapter serving (Digital Twin + ML placement)
- 2602.10111 (2026-02-10) Learning Agile Quadrotor Flight in the Real World -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2602.01795 (2026-02-02) RedVisor: Reasoning-Aware Prompt Injection Defense via Zero-Copy KV Cache Reuse -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2509.01760 (2025-09-01) Context dependent adaptation in a neural computation -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2508.17624 (2025-08-25) ExpertWeave: Efficiently Serving Expert-Specialized Fine-Tuned Adapters at Scale -> IN-CORPUS: already coded as ExpertWeave
- 2508.08343 (2025-08-11) A Data-driven ML Approach for Maximizing Performance in LLM-Adapter Serving -> IN-CORPUS: already coded as Data-driven ML adapter-serving optimizer (Digital Twin)
- 2505.14468 (2025-05-20) ServerlessLoRA: Enabling Low-Latency Serverless Multi-LoRA Serving -> IN-CORPUS: already coded as ServerlessLoRA
- 2503.17027 (2025-03-21) RAW-Adapter: Adapting Pre-trained Visual Model to Camera RAW Images and A Benchmark -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2503.11972 (2025-03-15) MoDM: Efficient Serving for Image Generation via Mixture-of-Diffusion Models -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2410.06517 (2024-10-09) Dynamics of Adaptive Continuous Attractor Neural Networks -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2407.14417 (2024-07-19) Mixture of Experts with Mixture of Precisions for Tuning Quality of Service -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2407.14302 (2024-07-19) Dyn-Adapter: Towards Disentangled Representation for Efficient Visual Recognition -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2404.07494 (2024-04-11) Adaptive Fair Representation Learning for Personalized Fairness in Recommendations via Information Alignment -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2309.15785 (2023-09-27) BT-Adapter: Video Conversation is Feasible Without Video Instruction Tuning -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2306.12870 (2023-06-22) HOFA: Twitter Bot Detection with Homophily-Oriented Augmentation and Frequency Adaptive Attention -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2303.00703 (2023-03-01) Nearest Neighbors Meet Deep Neural Networks for Point Cloud Analysis -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2209.13878 (2022-09-28) Near-Optimal Adaptive Policies for Serving Stochastically Departing Customers -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)

### Query 5: `all:"LoRA serving"` (18 hits)

- 2611.10049 (2026-11-05) LoRazor: Trimming Adapter Execution for Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as LoRazor
- 2611.01256 (2026-10-31) LoRAForge: Co-Designing Post-Hoc Compression and Execution for Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as LoRAForge
- 2608.05483 (2026-08-06) PLoRA: An NDP-Enhanced Pooled-Memory System for Cost-Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as PLoRA (NDP pooled memory)
- 2608.03579 (2026-08-04) Pin Once, Swap Light: Subspace-Aligned Centroid-Residual Training for Efficient Ultra-LoRA Serving -> IN-CORPUS: already coded as SALT (Pin Once, Swap Light)
- 2606.13767 (2026-06-11) Beyond LoRA: Is Sparsity-Induced Adaptation Better? -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2604.07173 (2026-04-08) InfiniLoRA: Disaggregated Multi-LoRA Serving for Large Language Models -> IN-CORPUS: already coded as InfiniLoRA
- 2604.06370 (2026-04-07) ForkKV: Scaling Multi-LoRA Agent Serving via Copy-on-Write Disaggregated KV Cache -> IN-CORPUS: already coded as ForkKV
- 2511.22880 (2025-11-28) Serving Heterogeneous LoRA Adapters in Distributed LLM Inference Systems -> IN-CORPUS: already coded as LoRAServe
- 2510.23346 (2025-10-27) Block-Diagonal LoRA for Eliminating Communication Overhead in Tensor Parallel LoRA Serving -> IN-CORPUS: already coded as BD-LoRA
- 2510.09004 (2025-10-10) Decoupling Safety into Orthogonal Subspace: Cost-Efficient and Performance-Preserving Alignment for Large Language Models -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2508.02932 (2025-08-04) PLoRA: Efficient Concurrent LoRA Training for Large Language Models -> IN-CORPUS: already coded as PLoRA (concurrent LoRA training)
- 2507.07140 (2025-07-09) Exploring Sparse Adapters for Scalable Merging of Parameter Efficient Experts -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2505.14468 (2025-05-20) ServerlessLoRA: Enabling Low-Latency Serverless Multi-LoRA Serving -> IN-CORPUS: already coded as ServerlessLoRA
- 2505.03756 (2025-04-19) Improving the Serving Performance of Multi-LoRA Large Language Models via Efficient LoRA and KV Cache Management -> IN-CORPUS: already coded as ELORA (preprint FastLibra)
- 2407.02031 (2024-07-02) SwiftDiffusion: Efficient Diffusion Model Serving with Add-on Modules -> IN-CORPUS: already coded as SwiftDiffusion
- 2401.11240 (2024-01-20) CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference -> IN-CORPUS: already coded as Toppings (CaraServe)
- 2311.03285 (2023-11-06) S-LoRA: Serving Thousands of Concurrent LoRA Adapters -> IN-CORPUS: already coded as S-LoRA
- 2310.18547 (2023-10-28) Punica: Multi-Tenant LoRA Serving -> IN-CORPUS: already coded as Punica

### Query 6: `all:"LoRA" AND all:"cold start"` (23 hits)

- 2611.27148 (2026-11-20) Structure Over Scale: Rethinking Adaptation for Reinforcement Learning with Verifiable Rewards -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2611.11013 (2026-11-07) Slim Foundation Models for Latency-Critical Recommendation Serving -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2609.00590 (2026-09-01) CRAFT: Fine-Tuning Pre-hoc Explainability in AI-native 6G RAN -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2608.05743 (2026-08-06) ConceptADapt: Concept-guided Adaptive Feature Reconstruction with Dynamic Attention for Few-Shot Industrial Anomaly Detection -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2608.12389 (2026-08-01) Learning to Adapt Cross-Domain Preferences via Meta-LoRA for LLM Personalization -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2607.26500 (2026-07-29) Multi-Decoder OneRec: Controllable Generative Retrieval for Multi-Objective Industrial Recommendation -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2607.18302 (2026-07-17) A Better Start for Language Models: Domain-Conditional Position Offsets -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2605.03252 (2026-05-05) Ortho-Hydra: Orthogonalized Experts for DiT LoRA -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2604.17943 (2026-04-20) A Benchmark Construction and Evaluation Framework for Specialist Domains: Case Study on Defense-related Documents -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2603.12811 (2026-03-13) OARS: Process-Aware Online Alignment for Generative Real-World Image Super-Resolution -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2601.10949 (2026-01-16) MMedExpert-R1: Strengthening Multimodal Medical Reasoning via Domain-Specific Adaptation and Clinical Guideline Reinforcement -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2512.20210 (2025-12-23) Predictive-LoRA: A Proactive and Fragmentation-Aware Serverless Inference System for LLMs -> IN-CORPUS: already coded as Predictive-LoRA (P-LoRA)
- 2509.06948 (2025-09-08) Beyond Two-Stage Training: Cooperative SFT and RL for LLM Reasoning -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2507.05733 (2025-07-08) When Transformers Meet Recommenders: Integrating Self-Attentive Sequential Recommendation with Fine-Tuned LLMs -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2507.03018 (2025-07-02) OpenTable-R1: A Reinforcement Learning Augmented Tool Agent for Open-Domain Table Question Answering -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2507.00748 (2025-07-01) Improving the Reasoning of Multi-Image Grounding in MLLMs via Reinforcement Learning -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2506.01910 (2025-06-02) GLoSS: Generative Language Models with Semantic Search for Sequential Recommendation -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2505.14468 (2025-05-20) ServerlessLoRA: Enabling Low-Latency Serverless Multi-LoRA Serving -> IN-CORPUS: already coded as ServerlessLoRA
- 2503.17707 (2025-03-22) PipeBoost: Resilient Pipelined Architecture for Fast Serverless LLM Scaling -> OUT: OUT: serverless whole-model scaling/pipelined loading for generic LLMs; LoRA only motivates shared base; no adapter/delta evaluation in abstract
- 2502.08271 (2025-02-12) RecCocktail: A Generalizable and Efficient Framework for LLM-Based Recommendation -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2409.08543 (2024-09-13) ATFLRec: A Multimodal Recommender System with Audio-Text Fusion and Low-Rank Adaptation via Instruction-Tuned Large Language Model -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2403.06208 (2024-03-10) Personalized LoRA for Human-Centered Text Understanding -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2401.11240 (2024-01-20) CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference -> IN-CORPUS: already coded as Toppings (CaraServe)

### Query 7: `all:"delta" AND all:"fine-tuned" AND all:serving AND all:compression` (6 hits)

- 2512.19720 (2025-12-16) Per-Axis Weight Deltas for Frequent Model Updates -> NEW-IN: compressed deltas for serving many variants; cold-start load time 0.80 s vs 2.08 s
- 2505.11204 (2025-05-16) RanDeS: Randomized Delta Superposition for Multi-Model Compression -> OUT: OUT: adapter/LoRA composition or merging evaluated on quality, no systems metric for serving many variants
- 2406.09041 (2024-06-13) ME-Switch: A Memory-Efficient Expert Switching Framework for Large Language Models -> NEW-IN: delta compression + routing for serving many experts; 16 models on one A100, latency vs naive
- 2406.08903 (2024-06-13) Delta-CoMe: Training-Free Delta-Compression with Mixed-Precision for Large Language Models -> NEW-IN: mixed-precision deltas for multi-model serving; 50 models on one GPU, Triton kernel 3x
- 2402.10193 (2024-02-15) BitDelta: Your Fine-Tune May Only Be Worth One Bit -> NEW-IN: 1-bit full-model deltas; multi-tenant memory and per-user decoding latency (>10x vs naive at B>=16)
- 2312.05215 (2023-12-08) DeltaZip: Efficient Serving of Multiple Full-Model-Tuned LLMs -> IN-CORPUS: already coded as DeltaZip

### Query 8: `all:"KV cache" AND all:LoRA AND (all:agents OR all:sharing)` (20 hits)

- 2610.25456 (2026-10-18) System X: An LLM Decision Model That Replies from Its Own KV Cache -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2609.34054 (2026-09-28) PReCache: Efficient KV Cache Sharing for Multi-LoRA Agents via Low-Rank Precomputation and Neutral Reconstruction -> IN-CORPUS: already coded as PReCache
- 2609.17109 (2026-09-15) Shared-Prefix KV Reuse Across Standard LoRA Adapters: Quality and Serving Tradeoffs -> IN-CORPUS: already coded as Shared-prefix KV reuse across LoRA adapters (RouteKV)
- 2608.11752 (2026-08-12) UniSwap: Streaming Audio-Visual Identity Swapping for Talking Videos -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2608.05483 (2026-08-06) PLoRA: An NDP-Enhanced Pooled-Memory System for Cost-Efficient Multi-LoRA Serving -> IN-CORPUS: already coded as PLoRA (NDP pooled memory)
- 2608.01247 (2026-08-02) RestoreKV: Recovering Full-Cache Behavior Under Aggressive Query-Agnostic KV Cache Eviction -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2607.28069 (2026-07-30) SemPIC: Learning Semantic Position-Independent KV Caches -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2606.20911 (2026-06-18) Latent Personal Memory: Represent personal memory as dynamic soft prompts -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2605.17309 (2026-05-17) StyleText: A Large-Scale Dataset and Benchmark for Stylized Scene Text Inpainting -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2605.13839 (2026-05-13) Good Agentic Friends Do Not Just Give Verbal Advice: They Can Update Your Weights -> OUT: OUT: LoRA used as a fine-tuning/training or application method (accuracy only, no multi-variant serving problem)
- 2604.06370 (2026-04-07) ForkKV: Scaling Multi-LoRA Agent Serving via Copy-on-Write Disaggregated KV Cache -> IN-CORPUS: already coded as ForkKV
- 2603.28554 (2026-03-30) Hydra: Unifying Document Retrieval and Generation in a Single Vision-Language Model -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2603.16867 (2026-03-17) Efficient Reasoning on the Edge -> OUT: OUT: edge reasoning via LoRA adapters; dynamic adapter switching is a small component, no many-variant serving problem or systems metric in abstract
- 2603.13281 (2026-02-27) ICaRus: Identical Cache Reuse for Efficient Multi Model Inference -> IN-CORPUS: already coded as ICaRus
- 2602.01053 (2026-02-01) LRAgent: Efficient KV Cache Sharing for Multi-LoRA LLM Agents -> IN-CORPUS: already coded as LRAgent
- 2508.17624 (2025-08-25) ExpertWeave: Efficiently Serving Expert-Specialized Fine-Tuned Adapters at Scale -> IN-CORPUS: already coded as ExpertWeave
- 2508.05091 (2025-08-07) PoseGen: In-Context LoRA Finetuning for Pose-Controllable Long Human Video Generation -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)
- 2508.00904 (2025-07-29) Forecasting LLM Inference Performance via Hardware-Agnostic Analytical Modeling -> OUT: OUT: serving/KV-cache/speculative-decoding/PD paper without adapters or deltas
- 2507.13575 (2025-07-17) Apple Intelligence Foundation Language Models: Tech Report 2025 -> OUT: OUT: foundation model technical report (adapters on device), not a serving-system study
- 2504.02441 (2025-04-03) Cognitive Memory in Large Language Models -> OUT: OUT: not about LoRA/adapter/delta serving (vision, RL, control, signal or other domain)

### Query 9: `all:"co-serving" AND all:"fine-tuning" AND all:inference` (3 hits)

- 2611.00652 (2026-10-31) Inference First, Training Underneath: Layer-Granular LoRA Co-Serving with LayerLoom -> IN-CORPUS: already coded as LayerLoom
- 2607.28848 (2026-07-30) DeltaServe: Host-Agnostic Co-Serving of Inference and Fine-Tuning for LLMs -> IN-CORPUS: already coded as DeltaServe
- 2511.00101 (2025-10-30) Loquetier: A Virtualized Multi-LoRA Framework for Unified LLM Fine-tuning and Serving -> IN-CORPUS: already coded as Loquetier

## Part 1: IN/OUT decisions for the named candidates

- Cannikin (TPDS 2025): IN. Multi-LoRA SLO-aware scheduling; abstract reports request-rate and burstiness gains (3.6x, 2.8x at >90% SLO attainment). Coded as 1001, abstract only.
- Rock (CLUSTER 2025): IN. Cluster-level orchestration and adapter cache for thousands of LoRA adapters (diffusion); latency, cache-hit metrics. Coded 1002.
- Dynamic Operator Optimization (AAAI 2025): IN. Tunes the SGMV cross-adapter operator; throughput 1.30-1.46x vs Punica. Coded 1003.
- Enhancing LoRA Model Serving Capacity... (IEEE Access 2024): IN (low confidence). Same abstract as the AAAI Dop paper with different authors; full text unreadable; relationship unresolved. Coded 1004.
- LayerLoom (arXiv 2611.00652): IN (as lifecycle_coserving). Co-serves one LoRA fine-tune with inference; SLO attainment and training throughput; same class as FlexLLM (num 75). Already in all.json as a low-confidence stub (num 81); full record 1005 supersedes it. Not multi-adapter.
- AuLoRA (ICCD 2025): IN. Adapter loading/compute orchestration; 3.03x TTFT, 1.27x throughput vs S-LoRA. Coded 1006, abstract only.
- MixLoRA (ICPP 2025): IN. Rank-aware multi-worker multi-LoRA serving; 1.2x throughput. Distinct from arXiv 2404.15159 MixLoRA (fine-tuning MoE). Coded 1007, abstract only.
- CoLoRA (ASP-DAC 2026): IN. Scheduling/eviction/batching for multi-tenant LoRA; throughput, P95 latency. Coded 1008 (slides).
- UniLoRA (ICASSP 2026): IN. Scheduler, predictive caching, LoRA-aware kernels; P99 latency 1.8x. Coded 1009, abstract only. Not the Uni-LoRA parameter-efficiency paper arXiv 2506.00799.
- LoRA-PIM (ISOCC 2025): IN (simulation only). Adapter-switch latency 9.6 ms to 50 us, energy -70%, but only simulated hardware and a 2-page paper. Coded 1010.
- CLIMB (ICML 2026): IN. Admission control around the LoRA residency cliff; VIP TTFT p99 38.7 s to 13.1 s at 10.66 rps. Coded 1011, abstract only.
- DyMerge-LoRA (KDD 2026): IN. Composite-LoRA multi-tenant serving; throughput 1.1-4x, TTFT, memory. Coded 1012, abstract only.
- LoRATEE (ICASSP 2025): IN (conditional). TEE-protected multi-tenant LoRA with adapter prefetching and sharing; abstract gives no numbers, so the metric condition is unverified. Coded 1013.
- FlashServe (Preprints.org 2025): IN. Serverless cold-start plus LoRA multiplexing (128 adapters, swap 2.1 ms); not peer reviewed. Coded 1014.
- PHLoRA (arXiv 2509.10971): OUT. Post-hoc adapter extraction; serving gains estimated from S-LoRA, not measured.
- LoRASpace (arXiv 2610.27444, NeurIPS 2026): OUT (borderline). Composition of several LoRAs per generation judged on quality; speedup only vs composite. Code: https://github.com/Thamirawaran/loraspace.
- Per-Axis Weight Deltas (arXiv 2512.19720): IN. Delta compression with measured load time; no multi-tenant serving run. Coded 1016.
- BitDelta (arXiv 2402.10193): IN. Multi-tenant delta serving with memory and latency measured. Coded 1015.

## Cannikin: does it publish production adapter popularity (Zipf parameter)?

Not verifiable. The only text obtained is the abstract (via OpenAlex): it says the design uses a workload analysis of a real-world trace. IEEE Xplore, computer.org, Semantic Scholar (abstract elided) and Crossref gave no body text; there is no arXiv version; the IEEE staging PDF fetch was denied by the permission classifier and not retried. No Zipf parameter or other adapter-popularity statistic can be quoted, and no secondary source I opened (InfiniLoRA arXiv html, which describes Cannikin only as SLO-aware scheduling plus adapter-aware cache management) reports one. The Crossref reference list includes ShareGPT as a dataset, which suggests public conversation lengths in the evaluation, but that is not evidence about adapter popularity. Do not cite Cannikin for a production Zipf parameter without reading the full paper.

Related production adapter-popularity evidence found while checking (arXiv 2609.23321, Alibaba GenTD26, 874 adapters, 24 days): rank-frequency log-log slope alpha=1.30 (descriptive), pure power-law MLE alpha=1.56 rejected at p=0.003, top 5% of adapters = 53.5% of occurrences, Gini 0.749. Rock (1002) reports about 20% of adapters serving about 80% of requests in its three-month production data, while its introduction says top 5% serve over 60%.
