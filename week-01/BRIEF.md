# Week 1 — Derivatives from code

**The week's question:** *What is a derivative, operationally, and why is backpropagation nothing more than the chain rule with the intermediate results kept around?*

**Artifact due Sunday:** `week-01/build.py` — a scalar autograd engine written from scratch, gradcheck'd against numeric differentiation, training a tiny MLP to convergence.

**Paper:** none. Paper cadence starts week 4. Phase 0 is hands only.

**Calendar note:** you're starting on a Wednesday, so reps 1–3 run Wed/Thu/Fri and reps 4–5 become the Saturday warm-up (10 min each). Reps 4 and 5 are deliberately the two bugs your engine will hit — doing them cold, before the build, is the point.

---

## The one thing to hold onto this week

You already know `d/dx (x²) = 2x`. That is not what's being trained here. What's being trained is the operational reading:

> **The derivative is: if I nudge this input by a tiny amount, how much does the output move, and in what direction?**

Every gradient in every neural network you will ever train is that sentence, applied to a number you can't see directly, computed by chaining together nudges you can. Nothing in the next 29 weeks is deeper than this. If week 1 lands properly, week 6 (hand-deriving the backward pass of an entire MLP) is tedious rather than mysterious.

---

## Weekday reps

30 minutes each, hard stop. Paste your answer, I mark it. Reps aren't scored — they're the trail of where your understanding actually is, so **write what you actually think, not what you think is expected.** A wrong answer you reasoned to is worth more to me than a right one you looked up; I aim the Saturday notes at your misses, so a copied answer aims them at the wrong place.

Show your arithmetic. "I got 8" tells me nothing; "I got 8 because (f(2.001) - f(2))/0.001 = 8.003, and the extra 0.003 is the h I didn't take to zero" tells me everything.

### Rep 1 (Wed) — the number under the definition

```
f(x) = 3x² - 4x + 5
```

1. Compute `f'(2)` analytically, by hand.
2. Now compute it numerically — `(f(2+h) - f(2)) / h` — for **h = 1e-1, 1e-3, 1e-6, 1e-10, 1e-15.** Write a 5-line script, print all five, paste the actual output.
3. **The question:** the numbers get closer to the true answer, and then they get worse. Report the exact h where it turns around, and explain *both* directions — why is large h wrong, and why is tiny h wrong? They are wrong for completely different reasons.
4. One sentence: given (3), why do real autograd engines compute derivatives symbolically at each operation rather than numerically?

### Rep 2 (Thu) — more than one input

```
f(a, b, c) = a*b + c        at a = 2.0, b = -3.0, c = 10.0
```

1. Nudge each input in turn by `h = 1e-5`, holding the other two fixed. Report the three slopes as actual printed output.
2. For each of the three, state the *rule* you just measured, in words — not the number. e.g. for `c`: "adding a constant means a nudge to c moves the output by exactly the same amount, so the slope is 1."
3. **The question:** you should find `df/da = -3.0` and `df/db = 2.0`. Both times, the answer is *the other operand*. Why? Explain it from the definition of multiplication, not from the power rule.
4. Predict, without computing: for `f = a*b*c`, what is `df/da`?

### Rep 3 (Fri) — the chain rule is the whole algorithm

```
e = a * b
d = e + c
L = d * f          at a=2.0, b=-3.0, c=10.0, f=-2.0
```

1. Compute `L` forward. Show every intermediate.
2. Compute `dL/dL`, then `dL/dd`, then `dL/de`, then `dL/dc`, then `dL/da`, then `dL/db` — **in that order**, each one written as `(local derivative) × (the derivative already computed for the node above)`. Write the multiplication out; don't skip to the number.
3. Verify all of them numerically. Paste the output.
4. **The question:** you computed them in a specific order and each step reused the step before it. What would it cost you to compute `dL/da` from scratch, without reusing `dL/dd` and `dL/de`? Now imagine the graph has 10,000 nodes. **That reuse is the entire reason backprop exists** — say in one sentence what would be true of training if it didn't.

### Rep 4 (Sat warm-up, 10 min) — order matters

Take the graph from rep 3. Suppose you walk the nodes backward in the order you *created* them rather than in reverse topological order, so you try to compute `dL/de` before you have `dL/dd`.

1. What value does `dL/de` come out as? Work it through — don't just say "wrong".
2. State the precondition in one sentence: before a node's gradient can be computed, what must already be true?
3. You drilled topological sort as DSA day 15. Same algorithm, different dress. Name the graph, the nodes and the edges here — what exactly is being sorted, and which direction do the edges point?

### Rep 5 (Sat warm-up, 10 min) — the bug that will eat your Saturday

```
L = a + a           at a = 3.0
```

1. Predict `dL/da` before computing anything. Write the prediction down first.
2. Compute it numerically. Paste the output.
3. **The question:** a backward pass walks the graph and, at each node, sets that node's gradient from its parent. If the code writes `node.grad = <contribution>` instead of `node.grad += <contribution>`, what value does `a.grad` end up with here, and is it too big, too small, or right by accident?
4. Generalise: describe the shape of graph where `=` and `+=` give the same answer, and the shape where they don't. Which shape is a neural network?

---

## Saturday

**15-minute cold prediction, before any notes.** Week 1's version of the four questions:

1. **What is this component solving?** What does an autograd engine do that writing derivatives by hand doesn't?
2. **Predict the structure.** For the expression in rep 3, how many nodes does the graph have, and what does a single node need to store? List its fields.
3. **Predict the failure mode.** You're going to write this from scratch. Name the first thing that breaks, and say whether it breaks loudly (exception) or silently (a plausible wrong number). Silent ones are the ones that matter.
4. **Predict the numbers.** A tiny MLP — 3 inputs, two hidden layers of 4 `tanh` neurons, 1 output — trained on 4 examples with MSE loss. How many parameters? What is the loss at initialisation, roughly, and why that value? How many steps to get under 0.01?

Paste those four. I mark HIT/PARTIAL/MISS with no teaching, log it verbatim, then write `NOTES.md` aimed at the misses. Then you build.

## The build — `week-01/build.py`

From scratch. **Do not open micrograd, and do not watch the lecture first.** I'll hand you the reference on Sunday after yours has run.

Must have:
- A `Value` class wrapping a scalar: the number, its gradient, its parents, and how it was made.
- Forward ops: `+`, `*`, `tanh`. Add `**`, `exp`, `/`, unary `-` only if you want `tanh` written out the long way.
- `backward()` — reverse topological order, gradient accumulation.
- **A gradcheck function.** Every op, analytic vs numeric, asserting `max|Δ| < 1e-5`. This is the non-negotiable one: an engine that trains without a gradcheck is an engine you're trusting rather than verifying.
- A tiny MLP (3 → 4 → 4 → 1, `tanh`) trained on 4 hand-written examples, MSE loss, plain gradient descent. Assert the final loss is under 0.01.
- Everything under `if __name__ == "__main__":`, seeded, printing output you can actually read.

**Write the shapes—here, the graph structure—as comments before the loop.** And when `backward()` first works, don't move on: print the gradient of one parameter and check it by hand against a numeric nudge. Your standing weakness from LLD day 3 and day 7 is shipping without running; the AI-track version of that is a gradcheck you wrote but never watched fail. Before you trust it, **break something on purpose and confirm the gradcheck catches it.**

## Sunday — break it

Four ablations, each one a number in your `REVIEW.md`, not a sentence:

1. Change `+=` to `=` in the backward pass. Build a graph that reuses a node. Report both gradients and the ratio between them.
2. Replace the topological sort with insertion order. Report the wrong gradient and explain which node got visited too early.
3. Remove the zero-grad step between training iterations. Plot or print the loss for 20 steps. Report what happens and why — the failure here is more interesting than it sounds.
4. Run the gradcheck against every op, print `max|Δ|` for each. Then deliberately break one op's backward (drop a factor, flip a sign) and confirm the gradcheck catches it. Report the value it caught it at.

Then say `done`.

---

## Success criteria

- [ ] `python3 build.py` runs clean, all asserts pass, output readable
- [ ] Gradcheck covers every op and has been *observed failing* on a deliberate break
- [ ] MLP loss under 0.01, from a seeded init, in a stated number of steps
- [ ] All four ablations have numbers attached
- [ ] You can state, without looking: why reverse topological order, why `+=`, and why numeric differentiation is a test rather than a method

## Setup

```bash
python3 -m venv ~/Documents/Backend/AI/.venv
source ~/Documents/Backend/AI/.venv/bin/activate
pip install numpy matplotlib
```

No torch this week — week 1 has no dependencies at all beyond the stdlib. `matplotlib` is only for Sunday's ablation 3 if you'd rather see the curve than read it.
