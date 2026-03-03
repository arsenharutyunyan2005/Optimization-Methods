import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import math as mt
xSymbol = sp.Symbol('x')
eps = sp.Rational(1,2)
a = 0
b = 2

def Function(x):
    return sp.Rational(1, 4)*x**4 + x**2 - 8*x + 12


diff = sp.diff(Function(xSymbol), xSymbol)

solutions = sp.solve(diff, xSymbol)

realRoot = [x for x in solutions if x.is_real][0]
print(realRoot.evalf())

def CalculateN(first,last,epsilion):
    sectionRange = sp.Rational(last-first,epsilion)
    return int(sectionRange)

n = CalculateN(a,b,eps)

def OptionsMethod(first,last,sectionRange):
    someXValues = []
    for k in range(0,n+1):
        tempExpr = first+k*sp.Rational(last-first,sectionRange)
        someXValues.append(tempExpr)
    return someXValues


def ValueCheck(realroot, xmin,epsilion):
    if mt.abs(realroot - xmin) < epsilion:
        print('x-min is approximate to real root')
    else:
        print('x-min is not approximate to real root! change epsilion or find another x-min')


someXValues = OptionsMethod(a,b,n)
print(someXValues)

functionValues=[]

functionValues = [Function(xi).evalf() for xi in someXValues]
print(functionValues)

realRootX = float(realRoot)
realRootY = float(Function(realRoot).evalf())

x_smooth = np.linspace(a, b, 200)
f_lamb = sp.lambdify(xSymbol, Function(xSymbol), "numpy")
y_smooth = f_lamb(x_smooth)

plt.figure(figsize=(9,5))
plt.plot(x_smooth, y_smooth,  color='blue', label='f(x)')
plt.scatter(someXValues, functionValues, color='red', label='Division Points')
plt.scatter(realRootX,realRootY, color='green', label='Real Root')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Function Values at Division Points')
plt.grid(True)
plt.legend()
plt.show()