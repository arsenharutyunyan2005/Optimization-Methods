import numpy as np

salaries     = np.array([150, 200, 250, 300, 400, 500])
probs        = np.array([0.15, 0.25, 0.30, 0.15, 0.10, 0.05])
beta         = 0.95          
c            = 120           
weeks            = 8             

def accept_value(w):
    return w / (1 - beta)

V_next = sum(p * accept_value(w) for w, p in zip(salaries, probs))

reservation_wages = {}
expected_values   = {}

for t in range(weeks, 0, -1):
    reject_value = c + beta * V_next

    w_star = reject_value * (1 - beta)
    reservation_wages[t] = w_star

    V_t = sum(
        p * max(accept_value(w), reject_value)
        for w, p in zip(salaries, probs)
    )
    expected_values[t] = V_t
    V_next = V_t

print("=" * 55)
print(f"{'Week':>6}  {'Reservation Wage':>18}  {'Expected Value':>15}")
print("-" * 55)
for t in range(1, weeks + 1):
    print(f"{t:>6}  {reservation_wages[t]:>17.2f}  {expected_values[t]:>15.2f}")
print("=" * 55)

print("\nOptimal policy (accept if w >= reservation wage):")
for t in range(1, weeks + 1):
    w_star = reservation_wages[t]
    accept = [int(w) for w in salaries if w >= w_star]
    reject = [int(w) for w in salaries if w < w_star]
    print(f"  Week {t}: accept {accept}, reject {reject}")

print("\nProbability of accepting at each week (given still searching):")
for t in range(1, weeks + 1):
    p_accept = sum(p for w, p in zip(salaries, probs) if w >= reservation_wages[t])
    print(f"  Week {t}: {p_accept:.4f}")