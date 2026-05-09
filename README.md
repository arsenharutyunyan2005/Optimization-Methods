# Optimization Methods Labs

This repository contains Python implementations of various optimization and simulation methods studied in university lab exercises. Each folder corresponds to a different method or topic.

## Folder Structure

- **Golden Ratio Method/** – Implementation of the Golden Ratio (φ ≈ 1.618) optimization method. Efficiently narrows the search interval by reusing one evaluation point per iteration.

- **Options Method/** – Divides the interval into n equal segments and evaluates the function at each division point to find the minimum.

- **Section Division Method/** – Splits the interval using two symmetric points around the midpoint and iteratively narrows the search.

- **Fastest Gradient/** – Gradient descent with optimal step size selection (steepest descent method) for unconstrained minimization.

- **DP/** – Dynamic Programming approach to optimization problems.

- **Weather Simulation/** – Discrete-time Markov Chain weather simulation. Models sunny, cloudy, and rainy days using a transition matrix. Includes:
  - 365-day path simulation starting from Sunny
  - 1000-run Monte Carlo estimation of empirical state fractions
  - Analytical stationary distribution by solving πP = π
  - Comparison of empirical vs theoretical results

## How to Run

Each method can be run individually, for example:

```bash
python "Golden Ratio Method/golden_ratio_method.py"
python "Options Method/options_method.py"
python "Section Division Method/section_division_method.py"
python "Weather Simulation/weather_forecast.py"
```

Or run all at once:

```bash
python run_all.py
```

## Requirements

- Python 3.x
- NumPy
- Matplotlib
- SymPy

Install all dependencies with:

```bash
pip install numpy matplotlib sympy
```

## Student

Arsen Harutyunyan