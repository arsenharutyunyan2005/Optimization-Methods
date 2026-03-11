import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
import numpy as np
import math as mt


class Gold:
    @staticmethod
    def new_function(x):
        return float(mt.e**x - 4*x + x**2)

    @staticmethod
    def new_x1(a, b):
        return a + 0.3819 * (b - a)

    @staticmethod
    def new_x2(a, b):
        return a + 0.6180 * (b - a)

    @staticmethod
    def is_done(a, b, eps):
        return abs(b - a) < eps

    @classmethod
    def calc(cls, a, b, eps):
        print("\n\nGolden ratio method:::::::\n")

        hist_x, hist_y, hist_iter = [], [], []
        orig_a, orig_b = a, b

        x1 = cls.new_x1(a, b)
        x2 = cls.new_x2(a, b)
        fx1 = cls.new_function(x1)
        fx2 = cls.new_function(x2)

        i = 0
        while not cls.is_done(a, b, eps):
            print(f"iteration {i}:::")
            print(f"  a  = {a}")
            print(f"  b  = {b}")
            print(f"  x1 = a + 0.3819*(b-a) = {x1:.6f}   →   f(x1) = {fx1:.6f}")
            print(f"  x2 = a + 0.6180*(b-a) = {x2:.6f}   →   f(x2) = {fx2:.6f}")

            hist_x.extend([x1, x2])
            hist_y.extend([fx1, fx2])
            hist_iter.extend([i, i])

            if fx1 > fx2:
                a = x1
                x1, fx1 = x2, fx2
                x2 = cls.new_x2(a, b)
                fx2 = cls.new_function(x2)
                print(f"  f(x1) > f(x2)  →  new a = x1, reuse x2")
            else:
                b = x2
                x2, fx2 = x1, fx1
                x1 = cls.new_x1(a, b)
                fx1 = cls.new_function(x1)
                print(f"  f(x1) ≤ f(x2)  →  new b = x2, reuse x1")

            i += 1
            print()

        x_star = (a + b) / 2
        f_star = cls.new_function(x_star)
        print(f"Converged after {i} iterations")
        print(f"  final a  = {a}")
        print(f"  final b  = {b}")
        print(f"  x*       = (a+b)/2 = {x_star:.6f}")
        print(f"  f(x*)    = {f_star:.6f}")

        cls.plot_results(orig_a, orig_b, hist_x, hist_y, hist_iter,
                         x_star, f_star, a, b, eps, i)

    @classmethod
    def plot_results(cls, orig_a, orig_b, hist_x, hist_y, hist_iter,
                     x_star, f_star, a, b, eps, iterations):

        BG     = "#0c0c10"
        PANEL  = "#11111a"
        GOLD1  = "#c8922a"
        GOLD2  = "#f2c96e"
        ACCENT = "#e8b84b"
        TEXT   = "#ede3cc"
        MUTED  = "#5a5244"

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
            spine.set_edgecolor("#252520")
        ax.grid(True, color="#1c1c18", linewidth=0.7, linestyle="-")
        ax.set_axisbelow(True)

        # ── Gradient curve ───────────────────────────────────────────
        x_smooth = np.linspace(orig_a - 0.5, orig_b + 0.5, 500)
        y_smooth = np.array([cls.new_function(v) for v in x_smooth])

        # Zoom y-axis to the interesting region
        y_lo = y_smooth.min() - 0.3
        y_hi = max(cls.new_function(orig_a), cls.new_function(orig_b)) * 1.15
        ax.set_ylim(y_lo, y_hi)

        pts  = np.array([x_smooth, y_smooth]).T.reshape(-1, 1, 2)
        segs = np.concatenate([pts[:-1], pts[1:]], axis=1)
        cmap_curve = LinearSegmentedColormap.from_list("gc", ["#7a4800", GOLD1, GOLD2])
        lc = LineCollection(segs, cmap=cmap_curve,
                            norm=plt.Normalize(y_smooth.min(), y_smooth.max()),
                            linewidth=2.5, zorder=3)
        lc.set_array(y_smooth[:-1])
        ax.add_collection(lc)

        ax.fill_between(x_smooth, y_smooth, y_lo,
                        alpha=0.06, color=GOLD1, zorder=1)

        # ── Evaluated points (coloured by iteration) ─────────────────
        n = max(hist_iter) + 1 if hist_iter else 1
        cmap_pts = LinearSegmentedColormap.from_list("pts", ["#aa55ff", "#ff55aa", "#ffdd44"])
        sc = ax.scatter(hist_x, hist_y,
                        c=hist_iter, cmap=cmap_pts, vmin=0, vmax=n - 1,
                        s=30, zorder=6, edgecolors="#0c0c10", linewidths=0.5)

        for k, (px, py) in enumerate(zip(hist_x, hist_y)):
            ax.annotate(str(k + 1), (px, py),
                        xytext=(5, 6), textcoords="offset points",
                        fontsize=7, color=MUTED, zorder=7)

        # ── Final interval shading ────────────────────────────────────
        ax.axvspan(a, b, alpha=0.07, color=ACCENT, zorder=2)
        for bound in [a, b]:
            ax.axvline(bound, color=ACCENT, lw=0.8, ls=":", alpha=0.35, zorder=4)

        # ── Optimum line ─────────────────────────────────────────────
        ax.axvline(x_star, color=ACCENT, lw=1.6, ls="--", alpha=0.9, zorder=5,
                   path_effects=[pe.withStroke(linewidth=4, foreground=BG)])

        ax.scatter([x_star], [f_star], marker="o", s=35,
                   color=ACCENT, edgecolors="#fffbe8", linewidths=1.0, zorder=8)

        # Annotation well above the minimum
        ax_yrange = y_hi - y_lo
        ann_y = y_lo + ax_yrange * 0.72
        ann_x = x_star + (orig_b - orig_a) * 0.12
        if ann_x + (orig_b - orig_a) * 0.25 > orig_b + 0.5:
            ann_x = x_star - (orig_b - orig_a) * 0.38

        ax.annotate(
            f"  x*    = {x_star:.4f}\n  f(x*) = {f_star:.4f}",
            xy=(x_star, f_star),
            xytext=(ann_x, ann_y),
            fontsize=8.5, color=TEXT,
            bbox=dict(boxstyle="round,pad=0.5", fc="#15140e",
                      ec=GOLD1, lw=1.0, alpha=0.95),
            arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=1.1,
                            connectionstyle="arc3,rad=0.2"),
            zorder=9,
        )

        # ── Colorbar ──────────────────────────────────────────────────
        cbar = fig.colorbar(sc, ax=ax, pad=0.015, fraction=0.025)
        cbar.set_label("iteration", fontsize=8, color=MUTED)
        cbar.outline.set_edgecolor("#252520")
        cbar.ax.yaxis.set_tick_params(color=MUTED, labelsize=7)
        plt.setp(cbar.ax.yaxis.get_ticklabels(), color=MUTED)

        # ── Title + subtitle ──────────────────────────────────────────
        ax.set_title("GOLDEN RATIO METHOD",
                     fontsize=14, fontweight="bold", color=GOLD2, pad=28,
                     path_effects=[pe.withStroke(linewidth=3, foreground=BG)])
        ax.text(0.5, 1.018,
                f"f(x) = eˣ - 4x + x²   |   ε = {eps}   |   {iterations} iterations",
                transform=ax.transAxes, ha="center", fontsize=8, color=GOLD2)

        ax.set_xlabel("x", fontsize=10, labelpad=6)
        ax.set_ylabel("f(x)", fontsize=10, labelpad=6)
        ax.tick_params(labelsize=8)

        # ── Legend ────────────────────────────────────────────────────
        legend_handles = [
            Line2D([0], [0], color=GOLD1, lw=2.2,
                   label="f(x) = eˣ - 4x + x²"),
            Line2D([0], [0], marker="o", color="none",
                   markerfacecolor="#aa55ff", markeredgecolor="#0c0c10",
                   markersize=7, label="x1, x2  (evaluated points)"),
            Line2D([0], [0], color=ACCENT, lw=1.4, ls="--",
                   label="x*  (approximate minimum)"),
            Line2D([0], [0], marker="o", color="none",
                   markerfacecolor=ACCENT, markeredgecolor="#fffbe8",
                   markersize=7, label=f"f(x*) = {f_star:.4f}"),
        ]
        ax.legend(handles=legend_handles, fontsize=8, loc="upper left",
                  facecolor="#0f0f14", edgecolor="#252520",
                  labelcolor=TEXT, framealpha=0.9)

        # ── φ watermark ───────────────────────────────────────────────
        ax.text(0.965, 0.95, "φ", transform=ax.transAxes,
                fontsize=60, color=GOLD1, alpha=0.055,
                ha="right", va="top", fontweight="bold")

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    a_val = 0.0
    b_val = 2.0
    eps_val = 0.5

    Gold.calc(a_val, b_val, eps_val)