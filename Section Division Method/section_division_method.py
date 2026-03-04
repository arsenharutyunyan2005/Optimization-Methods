import sympy as sp
import matplotlib.pyplot as plt
import numpy as np
import math as mt

class Segment:
    @staticmethod
    def new_function(x):
        # Added float() to ensure compatibility with plotting libraries
        return float(sp.Rational(1, 4)*x**4 + x**2 - 8*x + 12)

    @staticmethod
    def new_x1(a, b, beta):
        return (a + b) / 2 - beta

    @staticmethod
    def new_x2(a, b, beta):
        return (a + b) / 2 + beta

    @staticmethod
    def is_done(a, b, eps):
        return (b - a) < eps

    @classmethod
    def calc(cls, a, b, eps, beta):
        print("Segmentation method:::\n")
        
        # Track history for plotting
        hist_x, hist_y = [], []
        orig_a, orig_b = a, b
        
        i = 0
        while not cls.is_done(a, b, eps):
            print(f"iteration {i}:::")
            print(f"a = {a}, b = {b}")
            
            x1 = cls.new_x1(a, b, beta)
            x2 = cls.new_x2(a, b, beta)
            fx1 = cls.new_function(x1)
            fx2 = cls.new_function(x2)
            
            hist_x.extend([x1, x2])
            hist_y.extend([fx1, fx2])

            if fx1 > fx2:
                a = x1
            else:
                b = x2
            
            i += 1
            print()

        x_star = (a + b) / 2
        print(f"final a:{a}, b:{b}")
        print(f"x* = {x_star}")
        print(f"I(x*) = {cls.new_function(x_star)}")
        
        cls.plot_results("Segmentation Method", orig_a, orig_b, hist_x, hist_y, x_star)

    @classmethod
    def plot_results(cls, title, a, b, hist_x, hist_y, x_star):
        x_smooth = np.linspace(a - 1, b + 1, 100)
        # Vectorize the function to handle numpy arrays
        y_smooth = [cls.new_function(val) for val in x_smooth]
        
        plt.figure(figsize=(9, 5))
        plt.plot(x_smooth, y_smooth, color='blue', label='f(x)', alpha=0.6)
        plt.scatter(hist_x, hist_y, color='red', label='Evaluated Points', zorder=5)
        plt.axvline(x_star, color='green', linestyle='--', label=f'Final x* ≈ {x_star:.3f}')
        
        plt.title(title)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True, linestyle=':', alpha=0.7)
        plt.legend()
        plt.show()



if __name__ == "__main__":
    a_val = 0.0
    b_val = 2.0
    eps_val = 0.5
    beta_val = 0.1
    
    Segment.calc(a_val, b_val, eps_val, beta_val)
    