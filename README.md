# Optimization Methods Labs

This repository contains Python implementations of various optimization methods studied in university lab exercises. Each folder corresponds to a different optimization method.

## Folder Structure

- **Golden Ratio Method/** – Implementation of the Golden Ratio (φ ≈ 1.618) optimization method. Efficiently narrows the search interval by reusing one evaluation point per iteration.
- **Options Method/** – Implementation of the Options optimization method. Divides the interval into n equal segments and evaluates the function at each division point to find the minimum.
- **Section Division Method/** – Implementation of the Section Division (Segmentation) method. Splits the interval using two symmetric points around the midpoint and iteratively narrows the search.

## How to Run

Each method can be run individually:
```bash
python "Golden Ratio Method/golden_ratio_method.py"
python "Options Method/options_method.py"
python "Section Division Method/section_division_method.py"
```

Or run all three at once to compare results and automatically plot the most accurate method:
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