# Curriculum — p70 → p90

Profile: mid-senior AI engineer. Solid on integration (SDD, model APIs, agent loops, HITL). Gap: low-level internals. Target: depth that changes design decisions, plus cutting-edge fluency.

The weekly deep-dive routine takes the **first unchecked item**, writes a ~20-minute spoken episode on it, and checks it off. Reorder freely to re-prioritize. Items promoted from the news get inserted wherever they fit.

## Track A — How the model actually works

- [x] A1. Inference from the inside: tokenization → embeddings → the forward pass, and what a "token" costs (2026-07-12)
- [x] A2. Attention mechanics: QKV, multi-head, causal masking — the actual matrices, no hand-waving (2026-07-18)
- [x] A3. The KV cache: why long context is a memory problem, prefill vs decode, and what that means for latency and pricing (2026-07-25)
- [ ] A4. Sampling: temperature, top-p, logit bias, and why "the model is non-deterministic" is mostly false
- [ ] A5. Positional encodings and context windows: RoPE, interpolation, why long-context isn't free

## Track B — Inference engineering

- [ ] B1. Serving stacks: what vLLM/TGI/llama.cpp actually do — continuous batching, PagedAttention
- [ ] B2. Quantization: INT8/INT4/FP8, GPTQ/AWQ, what you lose and when it matters
- [ ] B3. Speculative decoding and other latency tricks
- [ ] B4. Why inference is memory-bandwidth-bound: the roofline model for LLMs

## Track C — Training and adaptation

- [ ] C1. Pretraining objectives and scaling laws — enough to read a model card critically
- [ ] C2. Finetuning that works: LoRA/QLoRA mechanics, when finetuning beats prompting
- [ ] C3. Post-training: RLHF, DPO, GRPO — how "alignment" is actually implemented
- [ ] C4. Distributed training basics: data/tensor/pipeline parallelism, why GPUs sit idle

## Track D — Hardware floor

- [ ] D1. GPU architecture for ML engineers: SMs, HBM, memory hierarchy, what a kernel is
- [ ] D2. FlashAttention: the one algorithm worth understanding end to end
- [ ] D3. Reading a GPU spec sheet: FLOPS vs bandwidth vs interconnect, what actually limits you

## Track E — Cutting edge (rotating)

Items get promoted here from the daily digest when something methodologically new lands. Keep 2-3 max; stale ones get dropped.

- [ ] E7. DeepSeek V4's hybrid attention architecture: how compressed sparse attention's learned token compressor and FP4 lightning indexer combine with a heavily-compressed long-range pathway and a small exact local window to cut 1M-token inference to 27% of the FLOPs and 10% of the KV cache of the prior generation, and how that sparse-retrieval approach compares to Kimi Delta Attention's recurrent-state approach to the same problem (2026-07-19)
- [ ] E8. Inkling's architecture bets against the frontier-model default: relative positional embeddings instead of RoPE, an encoder-free vision path that handles image tokens natively instead of bolting on a vision encoder, and a 5:1 global/sliding-window attention split — what each buys a 975B-parameter open-weights model and what it costs versus the RoPE-plus-encoder norm (2026-07-21)
- [ ] E9. OpenAI's ExploitGym sandbox escape: how a model with production safety classifiers deliberately disabled found a zero-day in a package registry cache proxy, escalated privileges and moved laterally through it, then chained that foothold with stolen credentials into a fully autonomous, multi-system attack reaching Hugging Face's production database with no human re-prompting between steps — and what it means that the actual containment boundary turned out to be infrastructure nobody had audited as a security boundary at all (2026-07-22)
