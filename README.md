# Minpower — Power Systems Optimization Toolkit

A Python-based toolkit for solving power systems optimization problems, adapted and modernized for academic use at the Department of Electrical Engineering, Faculty of Engineering, University of Nigeria, Nsukka.

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

## Quickstart (Recommended)

The fastest way to get started is the one-command setup script:

```bash
git clone https://github.com/Jesse-soft/minpower-final-year.git
cd minpower-final-year
chmod +x setup_env.sh
./setup_env.sh
```

This sets up everything automatically. See [Setup Script](#setup-script) for details.

---

## Manual Setup

### Requirements

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/download)
- Git

### Step 1 — Clone the repo

```bash
git clone https://github.com/Jesse-soft/minpower-final-year.git
cd minpower-final-year
```

### Step 2 — Create the conda environment

```bash
conda create -n minpower python=3.10 pandas=1.5.3 matplotlib pyomo -c conda-forge -y
conda activate minpower
```

### Step 3 — Install the solver and dependencies

```bash
conda install -c conda-forge coincbc -y
pip install cylp tables xarray setuptools
```

### Step 4 — Install the package

```bash
pip install -e .
```

### Step 5 — Configure matplotlib backend

```bash
echo "export MPLBACKEND=Agg" >> ~/.bashrc
echo "conda activate minpower" >> ~/.bashrc
source ~/.bashrc
```

---

## Usage

Activate the environment first (automatic if you ran the setup script):

```bash
conda activate minpower
```

Then run any problem:

```bash
minpower <path_to_problem_folder> --solver cbc
```

Minpower reads the CSV files in the folder, detects the problem type automatically, solves it, and outputs:
- A results spreadsheet (`.csv`) in the problem folder
- A Matplotlib plot (`.png`) in the problem folder

---

## Problem Folder Structure

| File | Required for | Description |
|------|-------------|-------------|
| `generators.csv` | ED, OPF, UC | Generator parameters (pmin, pmax, cost curve, etc.) |
| `loads.csv` | ED, OPF, UC | Load demand (MW) |
| `lines.csv` | OPF only | Transmission line parameters |
| `initial.csv` | UC only | Initial generator on/off status |

---

## Examples

### Economic Dispatch

```bash
minpower minpower/tests/ed-WW-3-7/ --solver cbc
```

Expected output:
```
objective cost=4866.425
total cost of generation=4866.42507
```

### Optimal Power Flow

```bash
minpower minpower/tests/opf/ --solver cbc
```

### Unit Commitment

```bash
minpower minpower/tests/uc/ --solver cbc
```

---

## Viewing Results

After running, open the problem folder. You will find:

- `dispatch.csv` — numerical results
- `dispatch.png` — visual dispatch chart

In VS Code or GitHub Codespaces, click the `.png` file to preview it inline.

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

## Setup Script

The setup_env.sh script automates the entire installation:

- Checks if conda is installed and guides you if not
- Creates a minpower conda environment with Python 3.10 and pandas 1.5.3
- Installs the CBC solver via conda-forge
- Installs all Python dependencies
- Configures MPLBACKEND=Agg for headless plot saving
- Sets the environment to auto-activate on terminal startup
- Runs a test solve to confirm everything works

---

## Compatibility Notes

This version has been updated from the original. Changes made:

- SafeConfigParser replaced with ConfigParser (removed in Python 3.12)
- squeeze=True removed from pd.read_csv() (removed in pandas 2.0)
- .iterkv() replaced with .items() (removed from pandas)
- DataFrame.append() replaced with pd.concat() (removed in pandas 2.0)
- pkg_resources replaced with importlib.metadata fallback
- freq="H" corrected to freq="h" (pandas 3.x change)
- IPython import path updated for modern IPython
- Regex strings in bidding.py corrected to raw strings

---

## Credits

- Original Minpower toolkit: Adam Greenhall (https://github.com/adamgreenhall/minpower) — MIT License
- Adaptation, documentation, and modernization: Onyedire Jesse Kenneth — EEE592 Final Year Project, Department of Electrical Engineering, Faculty of Engineering, University of Nigeria, Nsukka, 2025

---

## License

MIT License — see LICENSE for details.
