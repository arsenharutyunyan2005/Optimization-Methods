import numpy as np

offers = np.array([15, 25, 40, 55])
probs  = np.array([0.1, 0.4, 0.3, 0.2])
T      = 7

V     = {}
wstar = {}

V[T]     = np.dot(probs, offers)
wstar[T] = 0.0

for t in range(T - 1, 0, -1):
    V_next   = V[t + 1]
    wstar[t] = V_next
    V[t]     = np.dot(probs, np.maximum(offers, V_next))

print(f"{'Period':>8}  {'w*':>8}  {'V(t)':>8}  {'P(accept)':>10}  Policy")
print("-" * 60)
for t in range(1, T + 1):
    ws       = wstar[t]
    p_accept = probs[offers >= ws].sum()
    accept   = offers[offers >= ws].tolist()
    reject   = offers[offers <  ws].tolist()
    label    = "(final)" if t == T else ""
    print(f"  t={t} {label:<7}  {ws:>8.2f}  {V[t]:>8.2f}  {p_accept:>9.1%}  "
          f"accept {accept}, reject {reject}")