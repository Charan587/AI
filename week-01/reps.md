# Week 1 — rep log

Verbatim submissions and grades. Reps are marked, not scored.

---

## Rep 1 — Wed 2026-09-16

**Submitted:** handwritten (`WhatsApp Image 2026-09-16 at 20.58.07.jpeg`) + `week-01/main.py`

### His work, verbatim

Paper:
```
f(x) = 3x² - 4x + 5
f'(x) = d/dx (3x² - 4x + 5)
f'(x) = 6x - 4
f'(2) = 6(2) - 4
f'(2) = 12 - 4
f'(2) = 8

3) okay what i think is when h become minimum it where changes observed at an
   error point. Where minimum changes are minimum, so our result are minimum
   are visible.
   when h is large - difference is too much visible so.

4) Symbolically because it doesn't talk about precision & Numerical always
   talk about precision
```

Code (`main.py`, run verbatim):
```
0.1 8.3
0.001 8.003000000000426
1e-06 8.000003001384925
1e-10 8.000000661922968
1e-15 7.105427357601001
```

### Grade

| Item | Mark | Note |
|---|---|---|
| 1. `f'(2)` analytically | **HIT** | Clean, every step shown |
| 2. Five numeric values | **HIT** | Correct script, raw output pasted, no rounding |
| 3. Turnaround h + both directions | **PARTIAL** | Large-h direction right in substance. Small-h direction gestured at ("changes are minimum... not visible") — right neighbourhood, mechanism unnamed. **Turnaround h not reported at all.** |
| 4. Why symbolic | **PARTIAL** | Precision reason correct. Missed the cost reason (one forward pass per parameter), which is the larger of the two |

### Process defect

**No prediction written before running.** The brief asked for it explicitly ("Write your prediction for the five values down first"). This is the first sighting of the carried-in habit from LLD (W10, submits without running / skips the step that would expose the gap). Logged as **A1**.

### Correction issued

`probe_h.py` written — scans all 18 decades, shows the U-curve, the digit loss, and the non-representability of `h`. Key findings handed over:
- Truncation error is exactly `3h` (= (h/2)·f''), confirmed against the scan
- True turnaround is **h = 1e-8**, error 4.86e-8 ≈ `sqrt(eps)`. His five sample points bracketed it without landing on it (best of his five was 1e-10)
- h = 1e-9, 1e-10, 1e-11 give a **bit-identical slope** — because `(x+h)-x` carries the same relative error 8.27e-8 at all three, which equals the slope's relative error exactly
