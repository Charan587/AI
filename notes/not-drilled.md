# Not drilled

One paragraph each. Recognise the name, know roughly where it sits, don't spend a weekend on it. Revisit only if a job or a project actually demands it.

- **CUDA kernel writing** — hand-writing GPU kernels in CUDA C or Triton. Real skill, real jobs, but it only pays off after you already know where the bottleneck is, and week 19 (flash attention's IO argument) gives you the reasoning without the syntax. Come back here if you end up on an inference team.
- **Distributed training beyond concepts** — FSDP, tensor/pipeline/sequence parallelism, ZeRO stages. You'll learn what each one shards and why in week 11; actually running a multi-node job needs multi-node hardware and is mostly ops pain, not insight.
- **Diffusion models** — the other half of generative AI (images, video, increasingly audio). Different math: score matching and denoising rather than next-token prediction. Genuinely worth a month someday; it is not on the path to mastering LLMs, which is what this track is.
- **Speech** — Whisper, TTS, streaming ASR. Mostly an application of the same transformer stack to a different input representation. Learn the front end (mel spectrograms) in a day if you ever need it.
- **Classical ML** — SVMs, random forests, gradient boosting, PCA. Still the right tool for tabular problems and still asked in some interviews. Zero of it is load-bearing for LLMs; a weekend with scikit-learn covers it if a job asks.
- **AGI / alignment philosophy discourse** — worth reading for your own views, worth nothing for capability. Not scheduled.
