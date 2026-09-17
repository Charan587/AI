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

**Durable note:** [`notes/numeric-differentiation.md`](../notes/numeric-differentiation.md)

---

## Rep 2 — Thu 2026-09-17

**Submitted:** handwritten (2 pages) + `week-01/main.py` `day2()`

### His work, verbatim

Paper:
```
Day-2
What should I predict?
f(a,b,c) = a*b + c
a = 2.0, b = -3.0, c = 10.0
f(2.0, -3.0, 10) = 2 x (-3.0) + 10
                 = -6 + 10
f(2.0, -3.0, 10) = 4

1) why 1e-5 and not 1e-15 is we are trying to find a sweet point
   while preserving information and also trying to check the change.

2) I think nudge by a is the closest one.
   Nudge by c is less compared to nudge by b because c is just doing
   addition. no major contribution. like it only helps to offset.

3) It just means that diff of a and diff of b.
   It's because a tiny change in a/b does not affect others in this junction.

4) df/da to f = a*b*c is df/da = b*c. so it just states that any change
   in a will not affect b*c.
```

Code (`day2()`, run verbatim):
```
a nudged by h: 3.9999699999999994
b nudged by h: 4.00002
c nudged by h: 4.00001
```

### Grade

| Item | Mark | Note |
|---|---|---|
| 1. Why `1e-5` not `1e-15` | **HIT** | "sweet point while preserving information" — correct and compact |
| 2. Three slopes + rules in words | **MISS** | Never computed a slope. `slope = f(a+h,b,c)` — the function value, not the difference quotient. Rules not stated; his (2) compares magnitudes of the buggy values |
| 3. Why the other operand | **MISS** | No mechanism offered |
| 4. `f = a*b*c` → `b*c` | **HIT** | Correct |

### Defects

- **W16 (carried from LLD, 3rd sighting)** — variable named `slope` holding a function value. Missing `- f(a,b,c)` and `/ h`. True values: `df/da=-3, df/db=2, df/dc=1`.
- **A1 (2nd consecutive)** — prediction written, but **of the wrong quantity**. He predicted `f = 4`; the rep asked for the three slopes. His buggy output (`3.99997, 4.00002, 4.00001`) then *matched* his prediction and confirmed the bug. Escalating A1: the rule is now **predict the quantity the rep asks you to produce**, not merely "write a prediction".

### Correction issued

- Rectangle/strip derivation of `df/da = b` — "the other operand is the price per unit"
- Algebra showing `h` cancels exactly: `(a+h)b - ab = hb`, no limit taken
- Trace showing the slopes are exact at `h = 1e6`, linked back to rep 1: **truncation error is curvature error**, and `f'' = 0` here
- Box/slab picture for `a*b*c`, explaining his correct Q4
