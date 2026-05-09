import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

P = np.array([
    [0.6, 0.3, 0.1],  
    [0.3, 0.4, 0.3],  
    [0.2, 0.4, 0.4],  
])

states = ['Sunny', 'Cloudy', 'Rainy']
colors = {'Sunny': '#FFD700', 'Cloudy': '#87CEEB', 'Rainy': '#4682B4'}
state_colors = [colors[s] for s in states]

np.random.seed(42)

# ── Task 1: simulate 365-day path ──────────────────────────────────────────
def simulate(n_days, start=0):
    path = [start]
    for _ in range(n_days - 1):
        path.append(np.random.choice(3, p=P[path[-1]]))
    return path

path = simulate(365, start=0)

# ── Task 2: 1000 simulations ───────────────────────────────────────────────
all_days = []
for _ in range(1000):
    all_days.extend(simulate(365, start=0))

empirical = np.array([all_days.count(i) / len(all_days) for i in range(3)])

# ── Stationary distribution: solve πP = π  ↔  π(P-I)=0, sum(π)=1 ──────────
# Build linear system  A^T π = b
A = (P.T - np.eye(3))
A = np.vstack([A, np.ones(3)])
b = np.zeros(4); b[3] = 1.0
pi, *_ = np.linalg.lstsq(A, b, rcond=None)

# ── Plot ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor('#F8F9FA')
gs = GridSpec(2, 2, figure=fig, hspace=0.45, wspace=0.35)

# 1. Weather sequence strip
ax1 = fig.add_subplot(gs[0, :])
for i, s in enumerate(path):
    ax1.bar(i, 1, color=state_colors[s], width=1.0, linewidth=0)
ax1.set_xlim(0, 365)
ax1.set_ylim(0, 1)
ax1.set_xlabel('Day', fontsize=11)
ax1.set_title('Task 1 — 365-Day Weather Sequence (starting Sunny)', fontsize=13, fontweight='bold')
ax1.set_yticks([])
patches = [mpatches.Patch(color=colors[s], label=s) for s in states]
ax1.legend(handles=patches, loc='upper right', framealpha=0.9)

# 2. Empirical fractions bar chart
ax2 = fig.add_subplot(gs[1, 0])
x = np.arange(3)
bars = ax2.bar(x, empirical, color=state_colors, edgecolor='white', linewidth=1.5, width=0.5)
for bar, val in zip(bars, empirical):
    ax2.text(bar.get_x() + bar.get_width()/2, val + 0.005, f'{val:.4f}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')
ax2.set_xticks(x); ax2.set_xticklabels(states, fontsize=11)
ax2.set_ylabel('Fraction', fontsize=11)
ax2.set_ylim(0, max(empirical) * 1.2)
ax2.set_title('Task 2 — Empirical Fractions\n(1000 × 365-day simulations)', fontsize=12, fontweight='bold')
ax2.set_facecolor('#FAFAFA'); ax2.grid(axis='y', alpha=0.4)

# 3. Stationary vs empirical comparison
ax3 = fig.add_subplot(gs[1, 1])
w = 0.35
x = np.arange(3)
b1 = ax3.bar(x - w/2, pi,       width=w, color=['#FF8C00','#5F9EA0','#1E4D8C'],
             label='Stationary π', edgecolor='white')
b2 = ax3.bar(x + w/2, empirical, width=w, color=state_colors,
             label='Empirical', edgecolor='white', alpha=0.85)
for bar, val in zip(list(b1)+list(b2), list(pi)+list(empirical)):
    ax3.text(bar.get_x() + bar.get_width()/2, val + 0.003, f'{val:.4f}',
             ha='center', va='bottom', fontsize=8.5)
ax3.set_xticks(x); ax3.set_xticklabels(states, fontsize=11)
ax3.set_ylabel('Fraction', fontsize=11)
ax3.set_ylim(0, max(max(pi), max(empirical)) * 1.25)
ax3.set_title('Stationary π  vs  Empirical\n(πP = π)', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9); ax3.set_facecolor('#FAFAFA'); ax3.grid(axis='y', alpha=0.4)

plt.suptitle('Markov Chain Weather Model', fontsize=15, fontweight='bold', y=1.01)
plt.show()
print("Stationary distribution:", {s: round(pi[i], 6) for i, s in enumerate(states)})
print("Empirical fractions:    ", {s: round(empirical[i], 6) for i, s in enumerate(states)})