"""Rep 1 probe: where does the forward difference turn around, and why.

Run: python3 probe_h.py
"""

def f(x):
    return 3*x**2 - 4*x + 5

x = 2.0
TRUE = 8.0

print("A. the scan -- error vs h, every decade\n")
print(f"{'h':>8} {'slope':>22} {'abs error':>12}")
best = None
for e in range(0, 18):
    h = 10.0**-e
    slope = (f(x+h) - f(x)) / h
    err = abs(slope - TRUE)
    if best is None or err < best[1]:
        best = (h, err)
    print(f"{h:>8.0e} {slope:>22.15f} {err:>12.3e}")
print(f"\n  best h = {best[0]:.0e}, error {best[1]:.3e}")
print(f"  sqrt(machine epsilon) = {(2.220446049250313e-16)**0.5:.3e}   <- the theoretical optimum\n")

print("B. why tiny h dies -- watch the numerator lose its digits\n")
print(f"{'h':>8} {'f(x+h)':>26} {'f(x+h)-f(x)':>24} {'sig digits left':>16}")
for e in [1, 3, 6, 10, 15, 16]:
    h = 10.0**-e
    num = f(x+h) - f(x)
    # f(x+h) and f(x) each carry ~16 significant digits; the leading digits
    # they share cancel to zero and take their information with them.
    shared = len(str(f(x))) if num == 0 else max(0, 16 - e)
    print(f"{h:>8.0e} {f(x+h):>26.20f} {num:>24.20f} {shared:>16}")

print("\nC. the deeper cause -- x+h is not even the number you asked for\n")
import math
spacing = math.ulp(x)
print(f"  spacing between adjacent float64 near x=2.0 : {spacing:.3e}")
for e in [10, 15, 16]:
    h = 10.0**-e
    actual_h = (x + h) - x           # what the machine actually stepped
    print(f"  h={h:.0e}  requested, but (x+h)-x = {actual_h:.3e}"
          f"   -> off by {abs(actual_h-h)/h*100:6.2f}%")
