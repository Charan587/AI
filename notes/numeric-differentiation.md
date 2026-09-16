# Numeric differentiation — why it's a test, not a method

**Week 1, Rep 1.** Probe: [`week-01/probe_h.py`](../week-01/probe_h.py). Every number below came from running code, not from hand arithmetic.

---

## 1. The problem

```
f(x) = 3x² - 4x + 5        find f'(2)
```

By hand: `f'(x) = 6x - 4`, so `f'(2) = 8`. Exact. Certain. Done.

Now pretend you don't know calculus, or — more to the point — pretend `f` is a neural network with 124 million parameters and nobody is differentiating *that* by hand. All you can do is **evaluate** `f`. Feed it a number, get a number back.

Can you find the slope anyway?

Yes: take two points close together and measure the line between them.

```
        f(x + h) - f(x)
f'(x) ≈ ───────────────
               h
```

The whole question of this rep is: **how small should `h` be?**

The obvious answer is "as small as possible — that's what the limit says." The obvious answer is wrong, and the way it's wrong is worth a whole rep.

## 2. Run it and watch

`h` from `1e-1` down to `1e-17`. True answer is `8`:

```
       h                  slope    abs error
   1e+00     11.000000000000000    3.000e+00
   1e-01      8.300000000000001    3.000e-01
   1e-02      8.029999999999760    3.000e-02
   1e-03      8.003000000000426    3.000e-03
   1e-04      8.000300000023941    3.000e-04
   1e-05      8.000030000054892    3.000e-05
   1e-06      8.000003001384925    3.001e-06
   1e-07      8.000000288888032    2.889e-07
   1e-08      7.999999951380232    4.862e-08   <-- best
   1e-09      8.000000661922968    6.619e-07
   1e-10      8.000000661922968    6.619e-07
   1e-11      8.000000661922968    6.619e-07
   1e-12      8.000711204658728    7.112e-04
   1e-13      7.993605777301127    6.394e-03
   1e-14      8.171241461241152    1.712e-01
   1e-15      7.105427357601001    8.946e-01
   1e-16      0.000000000000000    8.000e+00
   1e-17      0.000000000000000    8.000e+00
```

It gets better. Then it gets worse. Then it collapses to zero.

**There are two different errors here, they run in opposite directions, and they are not the same kind of thing.** One is a maths error. One is a hardware error. Separate them and the table stops being mysterious.

---

## 3. Error one — truncation. Wrong question, perfect instrument.

Look at the top of the error column: `3e-1, 3e-2, 3e-3, 3e-4, 3e-5`. The error is exactly `3h`. Every row.

**This has nothing to do with computers.** Do `h = 0.1` on paper:

```
f(2.1) = 3(4.41) - 4(2.1) + 5 = 13.23 - 8.4 + 5 = 9.83
f(2.0) = 3(4)    - 8      + 5 = 9

(9.83 - 9) / 0.1 = 8.3
```

`8.3` is **exactly correct** — for the question *"what is the slope of the straight line from `(2, 9)` to `(2.1, 9.83)`?"* Every digit is right. It just isn't the question you asked. You wanted the slope **at** 2, and between 2 and 2.1 the curve bends upward, so the straight line comes out steeper than the tangent.

Where does the `3h` come from? Taylor:

```
f(x+h) = f(x) + h·f'(x) + (h²/2)·f''(x) + ...

f(x+h) - f(x)               h
───────────── = f'(x)  +   ─── · f''(x) + ...
      h                     2
                           ^^^^^^^^^^^^^ the part you threw away
```

`f''(x) = 6`, so the leftover is `(h/2)·6 = 3h`. That matches the table to three decimal places, which is how you know the derivation is right rather than plausible.

**This error would exist on a machine with infinite precision.** It shrinks as `h` shrinks. So far the obvious instinct holds.

### The physical version

Measuring how steep a hill is where you're standing. You walk 100 metres and measure the height change. Your tape measure is flawless — but you measured the *average* steepness over 100 metres of bending hill, not the steepness under your feet.

---

## 4. Error two — roundoff. Right question, broken instrument.

Now the other end of the table. This one *is* about the hardware.

### The answer is a digit inside the number

Here are the **true** values of `f(2+h)`, computed at 40 digits of precision so nothing is rounded:

```
       h   f(2+h)
   1e-01   9.83
   1e-03   9.008003
   1e-06   9.000008000003
   1e-10   9.00000000080000000003
   1e-15   9.000000000000008000000000000003
   1e-16   9.00000000000000080000000000000003
            ↑
            the 8 marches one place right per decade
```

Not a coincidence. `f(2+h) - f(2) ≈ 8h`, so the difference is `8 × 10⁻ᵉ` — **the 8 lands at decimal place `e`.** Subtracting `f(2)` and dividing by `h` is just a procedure for walking over and reading that digit.

### The machine's window doesn't move

A float64 holds about **16 significant digits**, counting from the leading `9`. That window is fixed. The 8 keeps marching right. Eventually it marches out of the window:

```
        window ends about here ──────────┐
                                         ↓
   1e-06   9.00000800000300138493   8 at place 6    comfortably inside
   1e-10   9.00000000080000006619   8 at place 10   still fine
   1e-15   9.00000000000000710543   8 at place 15   at the edge — and corrupted
   1e-16   9.00000000000000000000   8 at place 16   fell off. gone.
```

Compare the `1e-15` row against its true value. True: `...000008000...`. Stored: `...00710543`. **The 8 isn't there any more.** The machine spent its 16 digits getting `9.00000000000000` right and had to round whatever came next — and the thing it rounded away was the answer.

Then `(9.00000000000000710543 - 9) / 1e-15` reads the corrupted digit and scales it back up: **7.105**.

At `1e-16`, `2.0 + h` rounds straight back to `2.0`, the numerator is a true zero, and the result is `0.0`.

### The important correction

It is tempting — and wrong — to say "subtracting killed the digits."

**The damage happened earlier, when `f(2+h)` was stored.** By the time you subtract, the 8 is already gone. Subtraction destroys nothing; it just strips off the leading `9.00000000000000` that was *hiding* the damage and shows you the junk underneath.

### Shrink the window to see it

Pretend your calculator holds only **4** digits:

```
h = 0.001    true 9.008003   calculator shows 9.008   →  (9.008 - 9)/0.001   = 8   ✓
h = 0.00001  true 9.00008    calculator shows 9.000   →  (9.000 - 9)/0.00001 = 0   ✗
```

Identical disease. Float64 has 16 digits instead of 4, so it survives to `h = 1e-15` instead of `h = 1e-5`.

### The physical version

Same hill. This time you walk 1 millimetre. Now it's the right question — but your tape measure reads to the nearest centimetre, so it says "0".

---

## 5. Putting the two together

```
error(h)  ≈   3h        +        eps·|f(x)| / h
              ↑                   ↑
         truncation            roundoff
      shrinks with h         grows as h shrinks
```

A U-curve. The best `h` is where the two arms cross, which lands near `√eps ≈ 1.5e-8`. The scan's empirical best: **`h = 1e-8`, error `4.9e-8`.**

Five log-spaced sample points (`1e-1, 1e-3, 1e-6, 1e-10, 1e-15`) **straddle that minimum without landing on it** — `1e-6` and `1e-10` sit on opposite arms. Worth remembering on its own: *a handful of log-spaced samples can hide the shape of the thing you're measuring.*

### Curiosity: three identical answers

```
1e-09   8.000000661922968
1e-10   8.000000661922968
1e-11   8.000000661922968
```

Three different `h`, bit-identical results. Cause:

```
h = 1e-10 requested, but (x+h) - x = 1.000000082740371e-10  →  8.27e-8 relative error
```

`1e-10` isn't representable in binary, so the step actually taken isn't the step asked for — and the relative error in `h` happens to be `8.27e-8` at all three magnitudes. The slope's relative error: `6.619e-7 / 8 = 8.27e-8`. **The same number.** You aren't measuring a wrong slope; you're measuring the correct slope of a slightly wrong interval.

---

## 6. So why don't we train networks this way?

Two reasons, and the second is the one that matters.

**Precision.** Everything above. The best you can do is ~7 good digits, and only if you guessed `h` well.

**Cost — the real killer.** `(f(x+h) - f(x))/h` gives the derivative with respect to **one** parameter. One parameter, one full forward pass. GPT-2 small has 124M parameters, so: **124 million forward passes per training step.**

Backprop gets all 124M gradients in **one** backward pass, for roughly the cost of one forward pass.

That is not an optimisation. That is the difference between deep learning existing and not existing.

## 7. What it's actually for

Numeric differentiation survives as a **test**.

On Saturday, `backward()` will produce a gradient. The only way to know it's right is to compute the same gradient the other way — nudge the input, measure — and compare. Which is why the gradcheck threshold is what it is:

```python
assert abs(analytic - numeric) < 1e-5     # not ==, and not 1e-12 either
```

`1e-5` is loose enough that float noise can't fail a correct gradient, tight enough that a real bug can't hide under it. **That number comes from this rep.** It isn't a convention someone handed down; it's the measured precision of the instrument.

---

## 8. Bug list

- Using `==` in a gradcheck. Two correct computations of the same derivative will not produce identical floats, ever.
- A gradcheck tolerance of `1e-12`. Tighter than the instrument can measure — it fails on correct code, you conclude gradchecks are noise, you stop running them.
- A tolerance of `1e-2`. A missing factor of 2 slides straight under it.
- Rounding or `:.2f`-formatting the output while debugging. The failure lives in the digits a format string hides.
- Assuming smaller `h` is always better. It is, right up until it violently isn't.
- Comparing **absolute** difference when gradients are huge or tiny. `1e-5` absolute is meaningless next to a gradient of `1e7`; use relative error there.
- `x**2` vs `x^2` in Python. `^` is bitwise XOR and fails silently on the wrong type.
