import sympy as sp
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
import numpy as np
import math as mt


class Options:
    xSymbol = sp.Symbol('x')

    @staticmethod
    def FunctionSymbolic(x):
        return sp.exp(x) - 4*x + x**2

    @staticmethod
    def Function(x):
        return float(mt.e**x - 4*x + x**2)

    @classmethod
    def get_real_root(cls):
        diff = sp.diff(cls.FunctionSymbolic(cls.xSymbol), cls.xSymbol)
        solutions = sp.solve(diff, cls.xSymbol)
        return [x for x in solutions if x.is_real][0]

    @staticmethod
    def CalculateN(first, last, epsilion):
        return int(sp.Rational(last - first, epsilion))

    @classmethod
    def OptionsMethod(cls, first, last, n):
        someXValues = []
        for k in range(0, n + 1):
            tempExpr = first + k * sp.Rational(last - first, n)
            someXValues.append(tempExpr)
        return someXValues

    @classmethod
    def ValueCheck(cls, realroot, xMin, eps):
        diff = abs(realroot - xMin)
        if diff < eps:
            print(f'  x_min is approximate to real root: |{float(realroot):.4f} - {float(xMin):.4f}| = {float(diff):.4f} < {eps}')
        else:
            print(f'  x_min is NOT approximate to real root: |{float(realroot):.4f} - {float(xMin):.4f}| = {float(diff):.4f} >= {eps}')

    @classmethod
    def calc(cls, a, b, eps):
        realRoot = cls.get_real_root()
        n = cls.CalculateN(a, b, eps)

        print("\nOptions method:::\n")
        print(f"  interval  = [{a}, {b}]")
        print(f"  ε         = {eps}")
        print(f"  n         = {n}  (number of segments)")

        someXValues = cls.OptionsMethod(a, b, n)

        print(f"\nDivision points:")
        for k, xi in enumerate(someXValues):
            fxi = cls.Function(float(xi))
            print(f"  x[{k}] = {float(xi):.4f}   →   f(x[{k}]) = {fxi:.6f}")

        functionValues = [cls.Function(float(xi)) for xi in someXValues]
        min_val   = min(functionValues)
        min_index = functionValues.index(min_val)
        xMin      = someXValues[min_index]

        print(f"\n  x_min     = x[{min_index}] = {float(xMin):.4f}   →   f(x_min) = {min_val:.6f}")
        print(f"  real root = {float(realRoot):.6f}")
        cls.ValueCheck(realRoot, xMin, eps)

        realRootX = float(realRoot)
        realRootY = cls.Function(realRootX)
        xMinF     = float(xMin)
        yMinF     = float(min_val)

        cls.plot_results(a, b, eps, n, someXValues, functionValues,
                         xMinF, yMinF, realRootX, realRootY)

        return xMinF

    @classmethod
    def plot_results(cls, a, b, eps, n, someXValues, functionValues,
                     xMinF, yMinF, realRootX, realRootY):

        x_smooth = np.linspace(a - 0.1, b + 0.1, 500)
        f_lamb   = sp.lambdify(cls.xSymbol, cls.FunctionSymbolic(cls.xSymbol), "numpy")
        y_smooth = f_lamb(x_smooth)
        someXFloat          = [float(xi) for xi in someXValues]
        functionValuesFloat = [float(v)  for v  in functionValues]

        BG     = "#f8f9fc"
        PANEL  = "#eef1f7"
        GOLD1  = "#1a3caa"
        GOLD2  = "#2e9de4"
        ACCENT = "#e8420a"
        TEXT   = "#0d1117"
        MUTED  = "#8896aa"

        plt.rcParams.update({
            "font.family":     "monospace",
            "text.color":      TEXT,
            "axes.labelcolor": TEXT,
            "xtick.color":     MUTED,
            "ytick.color":     MUTED,
        })

        fig, ax = plt.subplots(figsize=(11, 6.5), facecolor=BG)
        ax.set_facecolor(PANEL)
        for spine in ax.spines.values():
            spine.set_edgecolor(MUTED)
        ax.grid(True, color=MUTED, linewidth=0.5, linestyle="-", alpha=0.35)
        ax.set_axisbelow(True)

        
        # ── Zoom y-axis ───────────────────────────────────────────────
        y_lo = y_smooth.min() - 0.3
        y_hi = max(cls.Function(a), cls.Function(b)) * 0.55
        ax.set_ylim(y_lo, y_hi)

        # ── Gradient curve ────────────────────────────────────────────
        pts  = np.array([x_smooth, y_smooth]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        cmap_curve = LinearSegmentedColormap.from_list("gc", [GOLD2, GOLD1])
        lc = LineCollection(segs, cmap=cmap_curve,
                            norm=plt.Normalize(y_smooth.min(), y_smooth.max()),
                            linewidth=2.5, zorder=3)
        lc.set_array(y_smooth[:-1])
        ax.add_collection(lc)

        ax.fill_between(x_smooth, y_smooth, y_lo,
                        alpha=0.08, color=GOLD1, zorder=1)

        # ── Division points ───────────────────────────────────────────
        n_pts = len(someXFloat)
        cmap_pts = LinearSegmentedColormap.from_list("pts", ["#90caf9", GOLD1])
        sc = ax.scatter(someXFloat, functionValuesFloat,
                        c=list(range(n_pts)), cmap=cmap_pts, vmin=0, vmax=max(n_pts - 1, 1),
                        s=50, zorder=6, edgecolors=TEXT, linewidths=0.8)

        for k, (px, py) in enumerate(zip(someXFloat, functionValuesFloat)):
            ax.annotate(str(k+1), (px, py),
                        xytext=(5, 6), textcoords="offset points",
                        fontsize=7, color=TEXT, zorder=7)

        # ── x_min point ───────────────────────────────────────────────
        ax.scatter([xMinF], [yMinF], marker="o", s=60, color=ACCENT,
                   edgecolors=TEXT, linewidths=1.0, zorder=8)

        # ── Real root line + marker ───────────────────────────────────
        ax.axvline(realRootX, color=ACCENT, lw=1.6, ls="--", alpha=0.9, zorder=5,
                   path_effects=[pe.withStroke(linewidth=4, foreground=BG)])

        ax.scatter([realRootX], [realRootY], marker="o", s=60,
                   color=ACCENT, edgecolors=TEXT, linewidths=1.0, zorder=9)

        ax_yrange = y_hi - y_lo
        ann_y = y_lo + ax_yrange * 0.72
        ann_x = realRootX + (b - a) * 0.12
        if ann_x + (b - a) * 0.25 > b + 0.3:
            ann_x = realRootX - (b - a) * 0.38

        ax.annotate(
            f"  real root = {realRootX:.4f}\n  f(x)      = {realRootY:.4f}",
            xy=(realRootX, realRootY),
            xytext=(ann_x, ann_y),
            fontsize=8.5, color=TEXT,
            bbox=dict(boxstyle="round,pad=0.5", fc=BG,
                      ec=GOLD1, lw=1.0, alpha=0.95),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1,
                            connectionstyle="arc3,rad=0.2"),
            zorder=10,
        )

        # ── Colorbar ──────────────────────────────────────────────────
        cbar = fig.colorbar(sc, ax=ax, pad=0.015, fraction=0.025)
        cbar.set_label("division point", fontsize=8, color=MUTED)
        cbar.outline.set_edgecolor(MUTED)
        cbar.ax.yaxis.set_tick_params(color=MUTED, labelsize=7)
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTED)

        # ── Title + subtitle ──────────────────────────────────────────
        ax.set_title("OPTIONS METHOD",
                     fontsize=14, fontweight="bold", color=GOLD1, pad=28,
                     path_effects=[pe.withStroke(linewidth=3, foreground=BG)])
        ax.text(0.5, 1.018,
                f"f(x) = eˣ - 4x + x²   |   ε = {eps}   |   n = {n} points",
                transform=ax.transAxes, ha="center", fontsize=8, color=MUTED)

        ax.set_xlabel("x", fontsize=10, labelpad=6)
        ax.set_ylabel("f(x)", fontsize=10, labelpad=6)
        ax.tick_params(labelsize=8)

        # ── Legend ────────────────────────────────────────────────────
        legend_handles = [
            Line2D([0], [0], color=GOLD1, lw=2.2,
                   label="f(x) = eˣ - 4x + x²"),
            Line2D([0], [0], marker="o", color="none",
                   markerfacecolor="#90caf9", markeredgecolor=TEXT,
                   markersize=7, label="division points  (x[k])"),
            Line2D([0], [0], marker="o", color="none",
                   markerfacecolor=ACCENT, markeredgecolor=TEXT,
                   markersize=7, label=f"x_min = {xMinF:.4f}   →   f(x_min) = {yMinF:.4f}"),
            Line2D([0], [0], color=ACCENT, lw=1.4, ls="--",
                   label=f"real root = {realRootX:.4f}"),
            Line2D([0], [0], marker="o", color="none",
                   markerfacecolor=ACCENT, markeredgecolor=TEXT,
                   markersize=7, label=f"f(real root) = {realRootY:.4f}"),
        ]
        ax.legend(handles=legend_handles, fontsize=8, loc="upper left",
                  facecolor=BG, edgecolor=MUTED,
                  labelcolor=TEXT, framealpha=0.95)

        # ── φ watermark ───────────────────────────────────────────────
        ax.text(0.965, 0.95, "φ", transform=ax.transAxes,
                fontsize=60, color=GOLD1, alpha=0.06,
                ha="right", va="top", fontweight="bold")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    Options.calc(0, 2, 0.5)