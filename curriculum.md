# Curriculum — p70 → p90

Profile: mid-senior AI engineer. Solid on integration (SDD, model APIs, agent loops, HITL). Gap: low-level internals. Target: depth that changes design decisions, plus cutting-edge fluency.

The weekly deep-dive routine takes the **first unchecked item**, writes a ~20-minute spoken episode on it, and checks it off. Reorder freely to re-prioritize. Items promoted from the news get inserted wherever they fit.

## Track A — How the model actually works

- [x] A1. Inference from the inside: tokenization → embeddings → the forward pass, and what a "token" costs (2026-07-12)
- [ ] A2. Attention mechanics: QKV, multi-head, causal masking — the actual matrices, no hand-waving
- [ ] A3. The KV cache: why long context is a memory problem, prefill vs decode, and what that means for latency and pricing
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

- [ ] E4. One model, three decoding modes: how NVIDIA's Nemotron-Labs-Diffusion lets a single model draft and verify its own tokens via self-speculation, why that sidesteps the draft-target alignment problem ordinary speculative decoding has to manage by hand, and what it costs in throughput versus a dedicated draft model (2026-07-16)
- [ ] E5. Kimi Delta Attention: how Moonshot's linear-attention mechanism extends Gated DeltaNet with finer-grained gating to keep a fixed-size recurrent state instead of a linearly-growing KV cache, why interleaving full attention every fourth layer is enough to preserve long-range recall, and what it costs in exact recall versus standard attention (2026-07-17)
- [ ] E6. SearchOS's externalized agent state: how a frontier task list, evidence graph, coverage map, and failure memory replace an implicit conversation transcript as shared state for a multi-agent search team, why pipeline-parallel scheduling over that state beats running agents in strict sequence, and what it fixes about agents repeating failed searches (2026-07-18)
