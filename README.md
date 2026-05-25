# Minpower — Power Systems Optimization Toolkit

A Python-based toolkit for solving power systems optimization problems, adapted and modernized for academic use at the Department of Electrical Engineering, Faculty of Engineering, University of Nigeria, Nsukka.

This project builds on the open-source [Minpower](https://github.com/adamgreenhall/minpower) toolkit originally developed by Adam Greenhall, extending it with a structured setup guide, Enugu/Nsukka-specific worked examples, compatibility updates for Python 3.12, and an original Nigerian Power System Extension.

---

## What It Does

Minpower solves three classical power systems optimization problems:

| Problem | Description |
|--------|-------------|
| **Economic Dispatch (ED)** | Allocates generation across units at minimum cost |
| **Optimal Power Flow (OPF)** | ED with transmission network constraints |
| **Unit Commitment (UC)** | Schedules generator on/off status over multiple time periods |

Problems are defined entirely in CSV spreadsheets — no coding required.

---

## Nigerian Power System Extension (`nigeria.py`)

An original contribution that wraps Minpower's output with Nigerian and Enugu State-specific analysis:

- Costs in both **Naira (N)** and **USD** side by side
- **Load shedding analysis** reflecting EEDC supply conditions
- **Cost per kWh** compared against EERC/NERC Band A tariff
- **Fuel type breakdown** — Coal, Gas, Diesel, Hydro, Solar
- **Voltage level classification** — 330kV, 132kV, 33kV, 11kV
- Enugu State grid context (EERC regulated, EEDC distributed)
- Saves `nigeria_report.txt` per run

### Usage

```bash
python3 nigeria.py <problem_folder> --solver cbc --rate 1600
```

---

## Quickstart

```bash
git clone https://github.com/Jesse-soft/minpower-final-year.git
cd minpower-final-year
chmod +x setup_env.sh
./setup_env.sh
```

---

## Sample Problems — Enugu State & Nsukka

### 1. Enugu State Economic Dispatch (`enugu-ed/`)

Models Enugu State's generation mix including:
- **Oji River Coal IPP** (350 MW proposed — locally sourced Enugu coal)
- **Fedikore Gas IPP** (10 MW — first IPP licensed by EERC, 2024)
- **Tempo Power Gas** (5 MW — EERC licensed, 2025)
- **EEDC Diesel Backup** (emergency supply)
- **UNN Campus Diesel** (University of Nigeria standby generation)

Loads: Enugu City, Nsukka Township, UNN Campus, 9th Mile Corner, Agbani, Udi, Awgu

```bash
python3 nigeria.py enugu-ed/ --solver cbc --rate 1600
```

---

### 2. Enugu 132kV Transmission Network (`enugu-opf/`)

Models the Enugu State transmission network:
- **Buses:** Oji River, Enugu City, Nsukka
- **Lines:** Oji River–Enugu 132kV, Enugu–Nsukka 132kV, Oji River–Nsukka 33kV

```bash
python3 nigeria.py enugu-opf/ --solver cbc --rate 1600
```

---

### 3. Nsukka Local Supply (`nsukka-ed/`)

A Nsukka/UNN-focused dispatch problem showing the local supply reality:
- EEDC Nsukka Feeder (grid supply)
- UNN Campus Diesel generators
- Nsukka solar rooftop generation
- Proposed local gas IPP

Loads: UNN Academic Area, Halls of Residence, Nsukka Market, Odim Street, Staff Quarters

```bash
python3 nigeria.py nsukka-ed/ --solver cbc --rate 1600
```

---

## Standard Minpower Problems (Wood & Wollenberg Textbook)

```bash
minpower minpower/tests/ed-WW-3-7/ --solver cbc   # 3-generator ED
minpower minpower/tests/opf/ --solver cbc           # 3-bus OPF
```

---

## Creating Your Own Problem

Make a folder and add CSV files:

**generators.csv (ED)**
```
name,heat rate equation,P min,P max,fuel cost
gen1,500+10P+0.02P^2,50,200,1.0
gen2,300+8P+0.015P^2,30,150,0.9
```

**loads.csv**
```
name,power
load,300
```

```bash
python3 nigeria.py my-problem/ --solver cbc --rate 1600
```

Minpower auto-detects ED, OPF, or UC from the files present.

---

## Setup Script

Run `setup_env.sh` to install everything from scratch:

```bash
chmod +x setup_env.sh
./setup_env.sh
```

Installs: conda environment (Python 3.10, pandas 1.5.3), CBC solver, all dependencies.

---

## Project Structure

```
minpower/               # Core Minpower solver (adapted from Greenhall)
nigeria.py              # Nigerian Power System Extension (original)
enugu-ed/               # Enugu State ED problem (Oji River, Fedikore, Tempo)
enugu-opf/              # Enugu 132kV network OPF
nsukka-ed/              # Nsukka/UNN local supply ED
setup_env.sh            # One-command environment setup
deploy_nigeria.sh       # Deploys Nigerian extension
```

---

## Compatibility Notes

Updated from original Minpower for Python 3.10 and modern dependencies:
- `SafeConfigParser` replaced with `ConfigParser` (Python 3.12)
- `squeeze=True` removed from `pd.read_csv()` (pandas 2.0)
- `.iterkv()` replaced with `.items()` (pandas)
- `DataFrame.append()` replaced with `pd.concat()` (pandas 2.0)
- `pkg_resources` fallback to `importlib.metadata`
- `freq="H"` corrected to `freq="h"` (pandas 3.x)

---

## Credits

- Original Minpower toolkit: [Adam Greenhall](https://github.com/adamgreenhall/minpower) — MIT License
- Adaptation, Nigerian extension, and modernization: Onyedire Jesse Kenneth
  EEE592 Final Year Project, Department of Electrical Engineering,
  Faculty of Engineering, University of Nigeria, Nsukka, 2025

---

## License

MIT License — see `LICENSE` for details.
