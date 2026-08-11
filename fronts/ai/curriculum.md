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

- [ ] E11. GPT-5.6 Sol's Ultra Mode: how running several specialized agent nodes in parallel inside one shared context window handles coordination, state-sharing, and result-aggregation that teams currently hand-build across separate subagent calls — the mechanics of shared-context multi-agent orchestration, and why it raises the same containment questions as the OpenAI/Hugging Face sandbox escape (2026-07-28)
- [ ] E12. MCP's 2026-07-28 stateless rewrite: what actually changed when the protocol dropped its stateful initialize/initialized handshake for a plain request-response core, what the new versioned extensions framework (Apps, Tasks) means for tool servers you're building today, and why removing session state is the change that finally lets an MCP server run on serverless or edge infrastructure (2026-07-29)
- [ ] E13. Claude's multi-agent Riemann orchestration pattern: how sixty parallel subagents with cross-validating roles (ideators, contributors, validators, writers) and independent re-derivation as a verification step produced a peer-reviewed mathematical result — the design principles behind assigning explicit roles, using a formal proof as the publication artifact, and building verification oracles that let a multi-agent system self-audit without human review at every step (2026-08-11)
