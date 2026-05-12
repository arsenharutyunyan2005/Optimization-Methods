import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

# ── Transition matrix (rows = from, cols = to) ─────────────────────────────
P = np.array([
    [0.54, 0.19, 0.10, 0.08, 0.03, 0.06],  # Idle
    [0.14, 0.52, 0.18, 0.09, 0.05, 0.02],  # Light
    [0.07, 0.22, 0.39, 0.21, 0.06, 0.05],  # Normal
    [0.06, 0.04, 0.08, 0.62, 0.11, 0.09],  # Busy
    [0.03, 0.03, 0.10, 0.15, 0.54, 0.15],  # Heavy
    [0.05, 0.02, 0.08, 0.10, 0.20, 0.55],  # Congested
])

states = ['Idle', 'Light', 'Normal', 'Busy', 'Heavy', 'Congested']
n = len(states)

colors = {
    'Idle':      '#A8D8EA',
    'Light':     '#7EC8A4',
    'Normal':    '#F7DC6F',
    'Busy':      '#F0A500',
    'Heavy':     '#E07B54',
    'Congested': '#C0392B',
}
state_colors = [colors[s] for s in states]

np.random.seed(42)

# ── Task 1: 350-step path starting from Normal (index 2) ──────────────────
def simulate(n_steps, start=2):
    path = [start]
    for _ in range(n_steps - 1):
        path.append(np.random.choice(n, p=P[path[-1]]))
    return path

path = simulate(350, start=2)

# ── Task 2: 1800 simulations, each 350 steps, starting from Normal ─────────
all_steps = []
for _ in range(1800):
    all_steps.extend(simulate(350, start=2))

empirical = np.array([all_steps.count(i) / len(all_steps) for i in range(n)])

# ── Stationary distribution: solve πP = π, sum(π) = 1 ────────────────────
A = (P.T - np.eye(n))
A = np.vstack([A, np.ones(n)])
b = np.zeros(n + 1); b[-1] = 1.0
pi, *_ = np.linalg.lstsq(A, b, rcond=None)

# ── Plot ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 11))
fig.patch.set_facecolor('#F8F9FA')
gs = GridSpec(2, 2, figure=fig, hspace=0.48, wspace=0.35)

# 1. Runway state sequence strip
ax1 = fig.add_subplot(gs[0, :])
for i, s in enumerate(path):
    ax1.bar(i, 1, color=state_colors[s], width=1.0, linewidth=0)
ax1.set_xlim(0, 350)
ax1.set_ylim(0, 1)
ax1.set_xlabel('Step', fontsize=11)
ax1.set_title('Task 1 — 350-Step Runway State Sequence (starting: Normal)', fontsize=13, fontweight='bold')
ax1.set_yticks([])
patches = [mpatches.Patch(color=colors[s], label=s) for s in states]
ax1.legend(handles=patches, loc='upper right', framealpha=0.9, ncol=3, fontsize=9)

# 2. Empirical fractions bar chart
ax2 = fig.add_subplot(gs[1, 0])
x = np.arange(n)
bars = ax2.bar(x, empirical, color=state_colors, edgecolor='white', linewidth=1.5, width=0.6)
for bar, val in zip(bars, empirical):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.004, f'{val:.4f}',
             ha='center', va='bottom', fontsize=9, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(states, fontsize=9, rotation=20, ha='right')
ax2.set_ylabel('Fraction', fontsize=11)
ax2.set_ylim(0, max(empirical) * 1.22)
ax2.set_title('Task 2 — Empirical Fractions\n(1800 × 350-step simulations, start: Normal)', fontsize=11, fontweight='bold')
ax2.set_facecolor('#FAFAFA')
ax2.grid(axis='y', alpha=0.4)

# 3. Stationary vs empirical comparison
ax3 = fig.add_subplot(gs[1, 1])
w = 0.35
darker = ['#6BAED6','#41AB5D','#FEC44F','#FE9929','#D94801','#67000D']
b1 = ax3.bar(x - w/2, pi,       width=w, color=darker,
             label='Stationary π', edgecolor='white')
b2 = ax3.bar(x + w/2, empirical, width=w, color=state_colors,
             label='Empirical', edgecolor='white', alpha=0.85)
for bar, val in zip(list(b1) + list(b2), list(pi) + list(empirical)):
    ax3.text(bar.get_x() + bar.get_width()/2, val + 0.003, f'{val:.4f}',
             ha='center', va='bottom', fontsize=7.5)
ax3.set_xticks(x)
ax3.set_xticklabels(states, fontsize=9, rotation=20, ha='right')
ax3.set_ylabel('Fraction', fontsize=11)
ax3.set_ylim(0, max(max(pi), max(empirical)) * 1.28)
ax3.set_title('Stationary π  vs  Empirical\n(πP = π)', fontsize=11, fontweight='bold')
ax3.legend(fontsize=9)
ax3.set_facecolor('#FAFAFA')
ax3.grid(axis='y', alpha=0.4)

plt.suptitle('Markov Chain — Airport Runway Traffic Model', fontsize=15, fontweight='bold', y=1.01)
plt.savefig('airport_markov.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.show()

print("Stationary distribution π:")
for s, v in zip(states, pi):
    print(f"  {s:>10}: {v:.6f}")
print("\nEmpirical fractions (1800 sims × 350 steps):")
for s, v in zip(states, empirical):
    print(f"  {s:>10}: {v:.6f}")