# AI Mastery Track

From-scratch AI, end to end: backprop → tokenizer → transformer → pretrain → align → serve → ship → research. 30 weeks. Weekend-heavy.

Runs alongside the [LLD track](../LLD/README.md) and the [DSA track](../DSA/README.md). Those two stay at ~1 hr/day each on weekdays; this one takes the weekend.

**The endpoint:** you can re-derive any component of a modern LLM from first principles, train one, make it fast, ship a feature on it, and read a paper the week it drops and say whether the result is real.

## Budget

| When | Time | What |
|---|---|---|
| Mon–Fri | 30 min | One **rep** — a derivation, a paper section, a prediction. Small and concrete. |
| Saturday | 3–4 hrs | **Build.** Cold prediction → notes → write the artifact from scratch. |
| Sunday | 2–3 hrs | **Break it.** Ablations, measurement, the failure exercise, review. |

~9 hrs/week × 30 weeks ≈ 270 hours. That is what "everything" actually costs. Nothing here is padding; if a week gets skipped it slides, it does not get dropped.

## How this works

The loop mirrors DSA — **predict cold, then get taught** — because the skill being trained is derivation, not recall.

1. Sunday night I write `week-NN/BRIEF.md`: the week's question, the artifact due, the paper, and the five weekday reps.
2. **Mon–Fri**, one rep/day. You paste the answer, I mark it. Reps are graded but not scored — they're the trail of where your understanding actually is.
3. **Saturday, prediction phase — 15 minutes, timed, cold.** Before any notes, you write four things:
   1. **What is this component actually solving?** The failure it exists to fix.
   2. **Predict the shapes.** Every tensor in the forward pass, by hand.
   3. **Predict the failure mode.** If this were implemented naively, what breaks first — and does it break loudly or silently?
   4. **Predict the numbers.** Starting loss, where loss plateaus, param count, memory. Say it before you have the code.
4. You paste those four. I mark **HIT / PARTIAL / MISS** on each with **no teaching yet**, and log it verbatim. Item 4 is the one that matters: a starting cross-entropy loss of `ln(vocab_size)` is derivable, and if you can't predict it you can't tell a broken training run from a slow one.
5. **Then** `week-NN/NOTES.md` — derived from a worked example with real traces, aimed at whatever your prediction got wrong. Never asserted.
6. You build `week-NN/build.py` **from scratch**, not from the lecture's code. Reference implementations stay closed until you've run yours.
7. **Sunday: you break it.** Every week has an ablation set — remove the residual connection and show the gradient dying, drop the LR schedule and show the loss curve, quantize and measure the quality loss. The claim is never accepted without the number.
8. You say **`done`** → I run your code, write `week-NN/REVIEW.md`, update the tables.

### The standing rule: measure, don't assert

Every claim in this track needs a number behind it. "Attention is O(n²)" is not knowledge; a plot of latency vs. context length on your own M2 is. "LayerNorm helps training" is not knowledge; two loss curves are. If a week ends with a belief you can't point at a measurement for, that belief is on the list for next week.

## Scoring

Each week scored 0–5 on five axes:

| Axis | What it measures |
|---|---|
| **Correctness** | Gradcheck passes, loss hits the target, shapes right, reproduces the reference number |
| **Derivation** | Got there from first principles vs. recalled the lecture |
| **Diagnostics** | Can read a broken training run — histogram, loss curve, grad norm — and name the cause |
| **Engineering** | Reproducible, seeded, measured, committed; not a notebook that only ran once |
| **Communication** | States shapes, bounds and tradeoffs unprompted; can defend the design |

Below 3 becomes a **standing weakness** in PROGRESS.md and gets a targeted rep 3–5 weeks later. Clears after two consecutive clean weeks.

## Rules

- **Don't open the reference implementation first.** Karpathy's code, the paper's repo, anything. I can tell, and grading a transcription teaches nothing.
- **Write the shapes as comments before the loop.** Most transformer bugs are shape bugs wearing a costume.
- **Gradcheck everything you differentiate by hand.** Numeric vs. analytic, `max |Δ| < 1e-5`. Non-negotiable through Phase 0–1.
- **Seed everything and log the seed.** A result you can't rerun is not a result.
- **Paste the version that ran, not the tidied one.**
- **Hard stop at the weekend budget.** Stuck on Saturday → paste what you have and say `stuck`. A reviewed failure beats a 9-hour grind.

## Progress

Full verbatim log — prediction reads, run output, defects, standing weaknesses — lives in **[PROGRESS.md](PROGRESS.md)**.

| Week | Topic | Artifact | Cor | Der | Dia | Eng | Com | Total |
|------|-------|----------|-----|-----|-----|-----|-----|-------|
| 01 | *not started* | | | | | | | |

---

# Curriculum — 30 weeks

## Phase 0 — Math repair, in code (weeks 1–3)

Rusty math, rebuilt by writing the thing rather than reading about it. No abstract linear algebra course; every concept arrives attached to a line of code that needs it.

| Week | Topic | Weekend artifact |
|---|---|---|
| 1 | **Derivatives from code.** Numeric gradient → chain rule → the computation graph. Why backprop is just the chain rule with memoization. | `micrograd.py` — scalar autograd from scratch, gradcheck'd, trains a tiny MLP |
| 2 | **Linear algebra as the matmul.** Broadcasting rules, matrix calculus, backprop through matmul derived (`dA = dC @ B.T` — derived, not memorized), Jacobians and why we never build one | tensor autograd — upgrade micrograd to ndarrays, same gradcheck |
| 3 | **Probability & information.** MLE ⇒ cross-entropy (derived), entropy, KL, perplexity, sampling: temperature/top-k/top-p and what each does to the distribution | bigram char model + full sampler, loss = `ln(V)` verified at init |

## Phase 1 — Build a language model from scratch (weeks 4–9)

| Week | Topic | Weekend artifact |
|---|---|---|
| 4 | **Embeddings and the MLP LM.** One-hot → lookup table, the bottleneck, context windows, train/dev/test discipline, overfitting a single batch as the first debugging move | MLP character LM (Bengio 2003), beats the bigram |
| 5 | **The diagnostics week.** Init scaling, why `tanh` saturates, dead neurons, Kaiming, BatchNorm derived from the failure it fixes, reading activation/gradient histograms | the same MLP, instrumented — five plots that each catch a different bug |
| 6 | **Backprop ninja.** Hand-derive and hand-code the backward pass of the entire MLP — cross-entropy, batchnorm, matmul, tanh, embedding — no autograd | manual backward, gradcheck exact against torch |
| 7 | **Attention, derived.** Running average → weighted average → learned weights → QKV. Why `/√d_k`. Causal masking. Multi-head, and what "head" actually buys | single-head then multi-head attention from scratch |
| 8 | **The transformer block.** Residuals (shown killing the gradient when removed), LayerNorm, position encodings, the FFN's 4× expansion, weight tying | nanoGPT-equivalent, written by you, trained locally |
| 9 | **Tokenization.** BPE from scratch. Why tokenizers cause the weird bugs — arithmetic, non-English, trailing whitespace, SolidGoldMagikarp | `bpe.py` + retrain week 8's GPT on your own tokenizer, compare |

## Phase 2 — Make it real (weeks 10–15)

First Lambda GPU spend lands here. Est. ~$30 across the track at ~$0.75/hr; each GPU week is scoped to a few hours.

| Week | Topic | Weekend artifact |
|---|---|---|
| 10 | **Optimization.** SGD → momentum → RMSProp → Adam → AdamW, each derived from the failure of the previous. LR schedules, warmup, grad clipping, mixed precision | optimizer comparison on a fixed model, five loss curves, one conclusion |
| 11 | **Training engineering + scaling laws.** Data pipeline, checkpointing, FLOPs counting, MFU, Chinchilla. **GPU week** | train a real ~100M model on Lambda; report MFU honestly |
| 12 | **Modern architecture deltas.** RoPE, RMSNorm, SwiGLU, GQA, KV cache — each implemented as a patch on your week-8 model and **measured**, not assumed better | 5 patches, 5 ablations, one table |
| 13 | **Fine-tuning.** SFT, instruction data, catastrophic forgetting, LoRA derived from the rank decomposition up, then compared against `peft`. **GPU week** | LoRA from scratch; fine-tune a real small model |
| 14 | **Alignment.** Reward models, the RLHF pipeline, DPO's loss derived from the PPO objective, why DPO won for practitioners. **GPU week** | DPO from scratch on a preference set |
| 15 | **Consolidation — your own LLM.** tokenizer → pretrain → SFT → DPO → chat, end to end, all your code | a model you can talk to that you built every layer of |

## Phase 3 — Inference and systems (weeks 16–19)

The half of the field that job posts call "AI infra" and most self-taught people skip.

| Week | Topic | Weekend artifact |
|---|---|---|
| 16 | **Inference math.** KV cache memory, arithmetic intensity, memory-bound vs compute-bound, why decode is slow and prefill isn't, batching economics | roofline for your model, predicted then measured on M2 |
| 17 | **Quantization.** int8/int4, symmetric vs asymmetric, outlier channels, GPTQ/AWQ intuition, GGUF | quantize by hand; run a real 7B on the M2 via llama.cpp; quality/latency curve |
| 18 | **Serving.** Paged attention, continuous batching, speculative decoding, vLLM. **GPU week** | benchmark: tokens/sec and $/1M tokens across three configs |
| 19 | **Efficient attention.** Flash attention derived — online softmax, tiling, why it's IO-aware and not FLOP-aware. Sliding window, sparse variants | online-softmax implementation + the memory-traffic argument on paper |

## Phase 4 — Applied LLM engineering (weeks 20–24)

Built against your real repos, not toy data. This is the phase that shows up in your day job.

| Week | Topic | Weekend artifact |
|---|---|---|
| 20 | **Retrieval, from scratch.** Embeddings, cosine vs dot, ANN/HNSW intuition, chunking as the thing that actually decides quality, hybrid search, reranking | RAG over one of the lending repos; a retrieval eval set with real numbers |
| 21 | **Evals — the hard part.** Building a harness, LLM-as-judge and its failure modes, position/verbosity bias, regression suites, significance at n=50 | eval harness + a scored report on week 20's RAG |
| 22 | **Agents.** The loop from scratch, no framework: tool calls, error recovery, termination, context compaction, cost control. Then compare against a framework and justify the choice | an agent that does one real task in your codebase |
| 23 | **Context engineering.** Structured output, constrained decoding, prompt caching, latency/cost budgets, failure taxonomy | a cost/latency/quality frontier for one real feature |
| 24 | **Production AI.** Prompt injection, guardrails, PII, observability, fallback and degradation, incident patterns | ship one AI feature into a real repo, with its eval gate |

## Phase 5 — Research depth (weeks 25–30)

| Week | Topic | Weekend artifact |
|---|---|---|
| 25 | **How to read a paper.** Claim → method → evidence → what they didn't test. Pick one small paper and reproduce its central figure | a reproduction, including where it didn't reproduce |
| 26 | **Interpretability.** Logit lens, activation patching, induction heads, sparse autoencoders | train a small SAE on your week-15 model; find one interpretable feature |
| 27 | **Reasoning and RL.** CoT, test-time compute, verifiers, GRPO/RLVR, reward hacking. **GPU week** | RLVR on a verifiable task; show the reward hack before you fix it |
| 28 | **MoE and long context.** Router, load balancing loss, capacity factor; context extension and the lost-in-the-middle effect | MoE layer from scratch + a needle-in-haystack eval |
| 29 | **Multimodal.** ViT, CLIP's contrastive objective, how a VLM bolts vision onto an LLM | small CLIP trained from scratch |
| 30 | **Capstone.** An original small experiment of your choosing, written up with method, plots, ablations and honest negative results | a short paper you'd be willing to post |

**Paper cadence:** one paper per week from week 4, read across the weekday reps. Foundational first (Attention Is All You Need, GPT-2/3, Chinchilla, LoRA, DPO, FlashAttention, InstructGPT), then current — from week 20 one slot per month is whatever landed on arXiv that month, so the habit of reading live work is built before the track ends.

**Not drilled** (low return for the time): CUDA kernel writing, distributed training beyond DDP concepts, diffusion models, speech, classical ML (SVMs, random forests), AGI/philosophy discourse. One paragraph each in [`notes/not-drilled.md`](notes/not-drilled.md) — know what they are, don't spend a weekend on them.

## Setup

```bash
python3 -m venv ~/Documents/Backend/AI/.venv
source ~/Documents/Backend/AI/.venv/bin/activate
pip install torch numpy matplotlib   # weeks 1-9 need nothing else
```

- **M2 Pro, 16 GB** carries weeks 1–10, 12, 16, 17, 19–26, 28–30. Everything is sized to finish in under 15 min on MPS/CPU.
- **Lambda / cloud GPU** for weeks 11, 13, 14, 15, 18, 27. Rent by the hour, destroy the instance the same day, est. ~$30 total.
- Added later, per week: `transformers` + `datasets` (13), `peft` (13), `trl` (14), `llama.cpp` (17), `vllm` (18), `faiss` (20).
- No notebooks. Plain `.py` files with a `__main__` block, same as your other two tracks — a notebook that ran once isn't a result.
