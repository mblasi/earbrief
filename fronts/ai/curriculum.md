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

- [ ] E17. Ornith-1.5's three-stage self-improvement loop: how jointly optimizing task generation, scaffold construction, and solution rollouts with GRPO — using multiplicative validity/frontier-difficulty/novelty rewards for task generation and separate fidelity/hack-resistance rewards for harness generation — closes the gap between fixed human-curated curricula and a genuinely open-ended training distribution, what the 20%-success-rate frontier-difficulty target does to curriculum difficulty over time, and what the benchmark results (397B matching Opus 4.8 on Terminal Bench 2.1, 35B outperforming 30B dense models) imply about the practical gains achievable from self-generated training distributions in agentic coding (2026-08-19)
- [ ] E18. OpenAI's multistage chain-of-thought monitoring architecture for Astra: how activation classifiers at every sampled token escalate through automated investigator chains to examine tool actions and reasoning sequences, why this requires 20% inference compute overhead, how the 30-minute false-positive SLA shapes organizational response, what this reveals about the practical limits of current alignment techniques when a model crosses the Critical cybersecurity threshold, and what "defense in depth across training" means structurally for how safety infrastructure must scale with capability (2026-08-21)
- [ ] E19. The MCP agent identity and authorization roadmap: how DPoP (RFC 9449) cryptographically binds access tokens to the client's private key to prevent stolen-token replay, how Workload Identity Federation and Enterprise-Managed Authorization replace browser-approval flows with standardized machine identity for agent workloads acting without a present user, what progressive tool discovery means architecturally for model token budgets as catalog size grows, and how the WIMSE and IETF OAuth working groups are shaping the underlying standards that will determine how multi-agent authorization actually works in production infrastructure (2026-08-22)
