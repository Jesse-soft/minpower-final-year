# Minpower — Power Systems Optimization Toolkit

A Python-based toolkit for solving power systems optimization problems, adapted and modernized for academic use at the Department of Electrical and Electronics Engineering.

This project builds on the open-source [Minpower](https://github.com/adamgreenhall/minpower) toolkit originally developed by Adam Greenhall, extending it with a structured setup guide, worked examples for Nigerian power system contexts, and compatibility updates for Python 3.12 and modern dependencies.

---

## What It Does

Minpower solves three classical power systems optimization problems:

| Problem | Description |
|--------|-------------|
| **Economic Dispatch (ED)** | Allocates generation across units at minimum cost for a single time period |
| **Optimal Power Flow (OPF)** | ED with transmission network (line flow) constraints |
| **Unit Commitment (UC)** | Schedules generator on/off status and dispatch over multiple time periods |

Problems are defined entirely in CSV spreadsheets — no optimization code required from the user.

---

## Requirements

- Python 3.9–3.12
- A solver: [GLPK](https://www.gnu.org/software/glpk/) (free), or Gurobi/CPLEX (free academic license)

### Install dependencies

```bash
pip install -r requirements.txt
```

### Install the package

```bash
pip install -e .
```

### Install GLPK (Windows, via Conda)

```bash
conda install -c conda-forge glpk
```

Or download directly from [winglpk.sourceforge.net](http://winglpk.sourceforge.net/).

---

## Usage

All problems follow the same pattern:

```bash
minpower <path_to_problem_folder> --solver glpk
```

Minpower reads the CSV files in the folder, detects the problem type automatically, solves it, and outputs:
- A results spreadsheet (`.csv`)
- A Matplotlib plot of the dispatch or commitment schedule

---

## Problem Folder Structure

Each problem lives in its own folder containing CSV files:

| File | Required for | Description |
|------|-------------|-------------|
| `generators.csv` | ED, OPF, UC | Generator parameters (pmin, pmax, cost curve, etc.) |
| `loads.csv` | ED, OPF, UC | Load demand (MW) |
| `lines.csv` | OPF only | Transmission line parameters |
| `initial.csv` | UC only | Initial generator on/off status |

---

## Examples

### Economic Dispatch

Solve a 3-generator, 500 MW load dispatch problem from Wood & Wollenberg (Example 3-7):

```bash
minpower minpower/tests/ed-WW-3-7/ --solver glpk
```

**generators.csv** (excerpt):
```
heat rate equation,P min,P max,fuel cost
225+8.4P+0.0025P^2,45,450,0.8
729+6.3P+0.0081P^2,45,350,1.02
400+7.5P+0.0025P^2,47.5,450,0.9
```

---

### Optimal Power Flow

```bash
minpower minpower/tests/opf-WW-6-2/ --solver glpk
```

Add a `lines.csv` to the folder to activate OPF mode automatically.

---

### Unit Commitment

```bash
minpower minpower/tests/uc/ --solver glpk
```

UC mode activates when the load spans multiple time periods. An `initial.csv` sets the starting on/off state for each generator.

---

## Project Structure

```
minpower/
├── get_data.py         # CSV ingestion (Input module)
├── generators.py       # Generator models
├── powersystems.py     # Bus, Load, Line, PowerSystem models
├── optimization.py     # Pyomo abstraction layer (Model/Solver module)
├── solve.py            # Main entry point and CLI
├── results.py          # Output: CSV results + Matplotlib plots
├── config.py           # Configuration and solver settings
├── standalone.py       # Multi-stage rolling UC support
├── bidding.py          # Piecewise cost curve handling
├── stochastic.py       # Stochastic UC with scenario trees
└── tests/              # 15+ test cases (ED, OPF, UC variants)
```

---

## Configuration

Solver and run options can be passed at the command line or set in a `minpower.cfg` file in your home directory:

```bash
# Use CPLEX with 10% reserve and 5 cost curve breakpoints
minpower my_problem/ --solver cplex --reserve_load_fraction 0.10 --breakpoints 5
```

Run `minpower --help` for the full list of options.

---

## Compatibility Notes

This version has been updated from the original to run on **Python 3.12** and **pandas ≥ 1.5**. Changes made:

- `SafeConfigParser` → `ConfigParser` (removed in Python 3.12)
- `pd.read_csv(squeeze=True)` → manual squeeze (removed in pandas 2.0)
- `.iterkv()` → `.items()` (removed from pandas)
- `DataFrame.append()` → `pd.concat()` (removed in pandas 2.0)
- IPython import path updated for modern IPython
- Regex strings in `bidding.py` corrected to raw strings

---

## Credits

- Original Minpower toolkit: [Adam Greenhall](https://github.com/adamgreenhall/minpower) — MIT License
- Adaptation, documentation, and modernization: Onyedire Jesse Kenneth — EEE592 Final Year Project, Department of Electrical Engineering, Faculty of Engineering, University of Nigeria, Nsukka, 2025

---

## License

MIT License — see `LICENSE` for details.
