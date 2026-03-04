import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import math as mt

class Gold:
    @staticmethod
    def new_function(x):
        return float(sp.Rational(1, 4)*x**4 + x**2 - 8*x + 12)

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
        print("\n\nGolden ratio method:::::::")
        
        hist_x, hist_y = [], []
        orig_a, orig_b = a, b

        i = 0
        while not cls.is_done(a, b, eps):
            x1 = cls.new_x1(a, b)
            x2 = cls.new_x2(a, b)
            fx1 = cls.new_function(x1)
            fx2 = cls.new_function(x2)
            
            hist_x.extend([x1, x2])
            hist_y.extend([fx1, fx2])

            if fx1 > fx2:
                a = x1
            else:
                b = x2
            i += 1

        x_star = (a + b) / 2
        print(f"final a:{a}, b:{b}")
        print(f"x* = {x_star}")
        
        # Fixed: Defined the smooth curve and plotting logic here
        x_smooth = np.linspace(orig_a - 1, orig_b + 1, 100)
        y_smooth = [cls.new_function(val) for val in x_smooth]
        
        plt.figure(figsize=(9, 5))
        plt.plot(x_smooth, y_smooth, color='orange', label='f(x)', alpha=0.6)
        plt.scatter(hist_x, hist_y, color='purple', label='Evaluated Points', zorder=5)
        plt.axvline(x_star, color='green', linestyle='--', label=f'Final x* ≈ {x_star:.3f}')
        
        plt.title("Golden Ratio Method")
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.legend()
        plt.show()

if __name__ == "__main__":
    a_val = 0.0
    b_val = 2.0
    eps_val = 0.5
  
    
    
    Gold.calc(a_val, b_val, eps_val)