import sys
import os
import math as mt
import sympy as sp

# ── Add subfolders to path ────────────────────────────────────────────
sys.path.append(os.path.join(os.path.dirname(__file__), "Golden Ratio Method"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Options Method"))
sys.path.append(os.path.join(os.path.dirname(__file__), "Section Division Method"))

from golden_ratio_method import Gold
from options_method import Options
from section_division_method import Segment

# ── Shared params ─────────────────────────────────────────────────────
A    = 0.0
B    = 2.0
EPS  = 0.5
BETA = 0.125

# ── True minimum via sympy ────────────────────────────────────────────
xSymbol = sp.Symbol('x')
def FunctionSymbolic(x):
    return sp.exp(x) - 4*x + x**2

diff      = sp.diff(FunctionSymbolic(xSymbol), xSymbol)
solutions = sp.solve(diff, xSymbol)
TRUE_ROOT = float([x for x in solutions if x.is_real][0])
TRUE_FVAL = float(mt.e**TRUE_ROOT - 4*TRUE_ROOT + TRUE_ROOT**2)
f         = lambda x: float(mt.e**x - 4*x + x**2)

print("=" * 60)
print("  TRUE MINIMUM")
print(f"  x*     = {TRUE_ROOT:.6f}")
print(f"  f(x*)  = {TRUE_FVAL:.6f}")
print("=" * 60)
print()

# ── Silent runners (no plot, no print) ───────────────────────────────
def run_gold_silent(a, b, eps):
    x1 = a + 0.3819 * (b - a)
    x2 = a + 0.6180 * (b - a)
    fx1, fx2 = f(x1), f(x2)
    i = 0
    while abs(b - a) >= eps:
        if fx1 > fx2:
            a = x1;  x1, fx1 = x2, fx2
            x2 = a + 0.6180 * (b - a);  fx2 = f(x2)
        else:
            b = x2;  x2, fx2 = x1, fx1
            x1 = a + 0.3819 * (b - a);  fx1 = f(x1)
        i += 1
    return (a + b) / 2, i

def run_segment_silent(a, b, eps, beta):
    i = 0
    while (b - a) >= eps:
        x1 = (a + b) / 2 - beta
        x2 = (a + b) / 2 + beta
        if f(x1) > f(x2):
            a = x1
        else:
            b = x2
        i += 1
    return (a + b) / 2, i

def run_options_silent(a, b, eps):
    n  = int(sp.Rational(b - a, eps))
    xs = [a + k * sp.Rational(b - a, n) for k in range(n + 1)]
    fvals = [f(float(xi)) for xi in xs]
    return float(xs[fvals.index(min(fvals))]), n

# ── Run all three silently ────────────────────────────────────────────
x_gold, i_gold = run_gold_silent(A, B, EPS)
x_seg,  i_seg  = run_segment_silent(A, B, EPS, BETA)
x_opt,  n_opt  = run_options_silent(A, B, EPS)

results = {
    "Golden Ratio":      {"x_star": x_gold, "f_star": f(x_gold), "error": abs(x_gold - TRUE_ROOT), "iters": i_gold},
    "Segmentation":      {"x_star": x_seg,  "f_star": f(x_seg),  "error": abs(x_seg  - TRUE_ROOT), "iters": i_seg},
    "Options Method":    {"x_star": x_opt,  "f_star": f(x_opt),  "error": abs(x_opt  - TRUE_ROOT), "iters": n_opt},
}

# ── Print comparison table ────────────────────────────────────────────
print("=" * 60)
print("  COMPARISON")
print("=" * 60)
print(f"  {'Method':<18} {'x*':>10} {'f(x*)':>10} {'error':>12} {'iters':>7}")
print("  " + "-" * 56)
for name, r in results.items():
    marker = "  ◄ WINNER" if name == min(results, key=lambda k: results[k]["error"]) else ""
    print(f"  {name:<18} {r['x_star']:>10.6f} {r['f_star']:>10.6f} {r['error']:>12.6f} {r['iters']:>7}{marker}")

# ── Find winner ───────────────────────────────────────────────────────
winner_name = min(results, key=lambda k: results[k]["error"])
winner      = results[winner_name]

print()
print("=" * 60)
print(f"  WINNER: {winner_name}")
print(f"  x*     = {winner['x_star']:.6f}")
print(f"  f(x*)  = {winner['f_star']:.6f}")
print(f"  error  = {winner['error']:.6f}  (vs true root {TRUE_ROOT:.6f})")
print("=" * 60)
print()

# ── Run winner with full output + plot ────────────────────────────────
print(f"Running {winner_name} in full...\n")

if winner_name == "Golden Ratio":
    Gold.calc(A, B, EPS)
elif winner_name == "Segmentation":
    Segment.calc(A, B, EPS, BETA)
elif winner_name == "Options Method":
    Options.calc(A, B, EPS)