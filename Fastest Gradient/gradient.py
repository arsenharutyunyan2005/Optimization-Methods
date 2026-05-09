import sympy as sp

x1, x2 = sp.symbols('x1 x2')

def Func(x1, x2):
    return x1**2 - 2*x1*x2 + 6*x2**2 + x1 - x2

def IsSatisfied(expr, point: dict, threshold=0.01):
    listOfPartial = []
    satisfied = True

    for var in point:
        partial = sp.diff(expr, var)
        value = float(partial.subs(point))
        listOfPartial.append(partial)
        if abs(value) > threshold:
            satisfied = False

    return satisfied, listOfPartial

def FindOptimalStep(expr, point: dict, partials: list):
    alpha = sp.Symbol('a')
    vars = list(point.keys())

    new_point = {
        vars[0]: point[vars[0]] - alpha * float(partials[0].subs(point)),
        vars[1]: point[vars[1]] - alpha * float(partials[1].subs(point)),
    }

    phi = expr.subs(new_point)
    phi_prime = sp.diff(phi, alpha)
    alpha_opt = sp.solve(phi_prime, alpha)[0]
    return float(alpha_opt)

def SteepestDescent(expr, point: dict, threshold=0.01, max_iter=1000):
    print(f"{'Iter':<6} {'x1':>12} {'x2':>12} {'f(x)':>14} {'alpha':>10} {'|df/dx1|':>12} {'|df/dx2|':>12}")
    print("-" * 80)

    alpha_opt = None

    for k in range(max_iter):
        vars = list(point.keys())
        f_val = float(expr.subs(point))

        satisfied, partials = IsSatisfied(expr, point, threshold)

        df1 = float(partials[0].subs(point))
        df2 = float(partials[1].subs(point))

        alpha_str = f"{alpha_opt:>10.6f}" if alpha_opt is not None else f"{'—':>10}"
        print(f"{k:<6} {float(point[vars[0]]):>12.6f} {float(point[vars[1]]):>12.6f} {f_val:>14.6f} {alpha_str} {abs(df1):>12.6f} {abs(df2):>12.6f}")

        if satisfied:
            print(f"\nConverged at iteration {k}")
            break

        alpha_opt = FindOptimalStep(expr, point, partials)

        point = {
            vars[0]: float(point[vars[0]]) - alpha_opt * df1,
            vars[1]: float(point[vars[1]]) - alpha_opt * df2,
        }
    else:
        print(f"\nDid not converge in {max_iter} iterations")

    print(f"\nMinimum at: x1 = {float(point[vars[0]]):.6f}, x2 = {float(point[vars[1]]):.6f}")
    print(f"f(x) = {float(expr.subs(point)):.6f}")
    return point


expr = Func(x1, x2)
point = {x1: 1, x2: 1}

result = SteepestDescent(expr, point)