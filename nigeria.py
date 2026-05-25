"""
nigeria.py -- Nigerian Power System Extension for Minpower
==========================================================
Extends Minpower with Nigerian-specific analysis output:
  - Costs in both Naira (N) and USD side by side
  - Load shedding analysis (typical of EEDC/Enugu grid)
  - Cost per kWh in Naira vs EERC/NERC tariff
  - Generator fuel type breakdown
  - Voltage level classification (330kV/132kV/33kV/11kV)
  - Enugu State grid context

Usage:
    python3 nigeria.py <problem_folder> --solver cbc [--rate 1600]

Author: Onyedire Jesse Kenneth
        EEE592 Final Year Project
        Department of Electrical Engineering
        University of Nigeria, Nsukka, 2025
"""

import argparse
import os
import subprocess
import pandas as pd
from datetime import datetime

# Update to current CBN rate before running
DEFAULT_EXCHANGE_RATE = 1600.0

# Voltage level thresholds (MW capacity based)
VOLTAGE_LEVELS = {
    "transmission_high": {"label": "Transmission (330 kV)", "min_mw": 100},
    "transmission_low":  {"label": "Transmission (132 kV)", "min_mw": 30},
    "distribution_high": {"label": "Sub-transmission (33 kV)", "min_mw": 5},
    "distribution_low":  {"label": "Distribution (11 kV)", "min_mw": 0},
}

# Fuel type auto-detection keywords
# Includes real Enugu/SE Nigeria plant names
FUEL_TYPES = {
    "coal":   ["coal", "oji", "oji-river", "enugu-coal", "colliery"],
    "gas":    ["gas", "ng", "natural", "ocgt", "ccgt", "thermal",
               "tempo", "fedikore", "ipp", "olorunsogo", "omotosho"],
    "diesel": ["diesel", "hsd", "oil", "emergency", "backup",
               "gen", "standby", "unn", "university"],
    "hydro":  ["hydro", "water", "kainji", "jebba", "shiroro", "dam",
               "anambra", "cross-river"],
    "solar":  ["solar", "pv", "photovoltaic", "rooftop"],
    "wind":   ["wind", "turbine"],
}


def detect_fuel_type(name):
    name_lower = str(name).lower()
    for fuel, keywords in FUEL_TYPES.items():
        if any(kw in name_lower for kw in keywords):
            return fuel
    return "gas"  # most Nigerian plants are gas


def classify_voltage(power_mw):
    if power_mw >= VOLTAGE_LEVELS["transmission_high"]["min_mw"]:
        return VOLTAGE_LEVELS["transmission_high"]["label"]
    elif power_mw >= VOLTAGE_LEVELS["transmission_low"]["min_mw"]:
        return VOLTAGE_LEVELS["transmission_low"]["label"]
    elif power_mw >= VOLTAGE_LEVELS["distribution_high"]["min_mw"]:
        return VOLTAGE_LEVELS["distribution_high"]["label"]
    else:
        return VOLTAGE_LEVELS["distribution_low"]["label"]


def format_ngn(amount):
    return f"N{amount:,.2f}"


def format_usd(amount):
    return f"${amount:,.2f}"


def run_minpower(folder, solver):
    result = subprocess.run(
        ["minpower", folder, "--solver", solver],
        capture_output=False
    )
    return result.returncode


def load_csv(folder, filename):
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        return None
    idx = 0 if filename == "dispatch.csv" else None
    return pd.read_csv(path, index_col=idx)


def analyze(folder, solver, rate, save_report=True):

    print("\n" + "=" * 65)
    print("  ENUGU STATE POWER SYSTEM ANALYSIS")
    print("  Regulated by EERC | Distributed by EEDC")
    print("  Powered by Minpower -- UNN EEE592")
    print("=" * 65)
    print(f"  Problem folder : {folder}")
    print(f"  Solver         : {solver.upper()}")
    print(f"  Exchange rate  : N{rate:,.0f} / $1 USD (CBN rate)")
    print(f"  Run time       : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

    # Run Minpower
    print("\n[1/5] Running Minpower solver...")
    rc = run_minpower(folder, solver)
    if rc != 0:
        print(f"  Warning: Minpower exited with code {rc}.")

    # Load data
    dispatch = load_csv(folder, "dispatch.csv")
    loads_df = load_csv(folder, "loads.csv")

    if dispatch is None:
        print("\n  ERROR: No dispatch.csv found. Cannot produce analysis.")
        return

    # Generator dispatch summary
    print("\n[2/5] Generator Dispatch Summary")
    print("-" * 65)

    power_cols = list(dispatch.columns)
    total_generated = dispatch[power_cols].sum(axis=1).iloc[0] if len(dispatch) > 0 else 0

    gen_summary = []
    for col in power_cols:
        power = float(dispatch[col].iloc[0]) if len(dispatch) > 0 else 0
        fuel = detect_fuel_type(col)
        voltage = classify_voltage(power)
        gen_summary.append({
            "Generator": col,
            "Output (MW)": round(power, 2),
            "Fuel Type": fuel.capitalize(),
            "Grid Level": voltage,
        })

    gen_df = pd.DataFrame(gen_summary)
    print(gen_df.to_string(index=False))
    print(f"\n  Total Generation: {total_generated:.2f} MW")

    # Fuel breakdown
    print("\n[3/5] Fuel Mix Breakdown")
    print("-" * 65)

    fuel_breakdown = gen_df.groupby("Fuel Type")["Output (MW)"].sum()
    fuel_pct = (fuel_breakdown / total_generated * 100).round(1) if total_generated > 0 else fuel_breakdown * 0

    for fuel, mw in fuel_breakdown.items():
        bar = "=" * int(fuel_pct[fuel] / 2)
        print(f"  {fuel:<12} {mw:>8.2f} MW  ({fuel_pct[fuel]:>5.1f}%)  [{bar}]")

    # Enugu grid context note
    print("\n  Enugu Grid Context:")
    if "Coal" in fuel_breakdown.index:
        print("  - Coal generation present (Oji River coal resources)")
    if "Gas" in fuel_breakdown.index:
        print("  - Gas generation present (EERC-licensed IPP plants)")
    if "Diesel" in fuel_breakdown.index:
        print("  - Diesel backup present (common in Nsukka/UNN campus supply)")

    # Load shedding analysis
    print("\n[4/5] Load & Load Shedding Analysis (EEDC Context)")
    print("-" * 65)

    if loads_df is not None and 'power' in loads_df.columns:
        total_demand = float(loads_df['power'].sum())
    else:
        total_demand = total_generated

    deficit = total_demand - total_generated
    shedding_pct = (deficit / total_demand * 100) if total_demand > 0 else 0

    print(f"  Total Demand         : {total_demand:>10.2f} MW")
    print(f"  Total Generated      : {total_generated:>10.2f} MW")

    if deficit > 0.01:
        print(f"  Load Shedding        : {deficit:>10.2f} MW  [DEFICIT]")
        print(f"  Shedding Percentage  : {shedding_pct:>10.1f}%")
        print(f"\n  WARNING: {deficit:.1f} MW supply deficit detected.")
        print(f"  This reflects the typical EEDC supply gap in Enugu State.")
        print(f"  Nsukka and UNN campus typically receive 4-8 hrs/day supply.")
        print(f"  Recommended: {deficit:.0f} MW additional IPP capacity needed.")
        print(f"  (Reference: Fedikore 10MW IPP and Tempo Power 5MW Gas plant")
        print(f"   are first steps toward closing this gap in Enugu State)")
    else:
        surplus = abs(deficit)
        print(f"  Surplus              : {surplus:>10.2f} MW  [SUPPLY MET]")
        print(f"\n  All load demand met. No load shedding required.")
        print(f"  (This is the optimal dispatch target for EEDC Enugu)")

    # Cost analysis
    print("\n[5/5] Cost Analysis (EERC Regulated Market)")
    print("-" * 65)

    # Try to read objective from log
    log_path = os.path.join(folder, ".log")
    objective_usd = None

    if os.path.exists(log_path):
        with open(log_path, "r") as f:
            for line in f:
                if "objective cost" in line.lower():
                    try:
                        objective_usd = float(line.split("=")[-1].strip())
                        break
                    except ValueError:
                        pass

    if objective_usd is None:
        objective_usd = total_generated * 8.5
        print("  (Estimating cost from generation output)")

    objective_ngn = objective_usd * rate

    if total_generated > 0:
        cost_per_mwh_usd = objective_usd / total_generated
        cost_per_mwh_ngn = cost_per_mwh_usd * rate
        cost_per_kwh_ngn = cost_per_mwh_ngn / 1000
        cost_per_kwh_usd = cost_per_mwh_usd / 1000
    else:
        cost_per_mwh_usd = cost_per_mwh_ngn = cost_per_kwh_ngn = cost_per_kwh_usd = 0

    print(f"\n  {'Metric':<32} {'USD':>13} {'NGN (N)':>20}")
    print(f"  {'-' * 67}")
    print(f"  {'Total Generation Cost':<32} {format_usd(objective_usd):>13} {format_ngn(objective_ngn):>20}")
    print(f"  {'Cost per MWh':<32} {format_usd(cost_per_mwh_usd):>13} {format_ngn(cost_per_mwh_ngn):>20}")
    print(f"  {'Cost per kWh':<32} {format_usd(cost_per_kwh_usd):>13} {format_ngn(cost_per_kwh_ngn):>20}")
    print(f"  {'CBN Exchange Rate Applied':<32} {'$1 USD':>13} {format_ngn(rate):>20}")

    # EERC tariff comparison
    # NERC Band A tariff 2024 (Enugu State / EEDC customers)
    eerc_tariff_ngn = 68.0
    print(f"\n  EERC/NERC Band A Tariff (2024) : N{eerc_tariff_ngn:.2f}/kWh")
    print(f"  (Applicable to EEDC customers in Enugu, Nsukka, Abakaliki)")

    if cost_per_kwh_ngn > 0:
        ratio = cost_per_kwh_ngn / eerc_tariff_ngn
        if ratio < 1:
            print(f"  Generation cost is {(1-ratio)*100:.1f}% BELOW EERC tariff")
            print(f"  Margin available for transmission/distribution losses")
        else:
            print(f"  Generation cost is {(ratio-1)*100:.1f}% ABOVE EERC tariff")
            print(f"  Tariff review may be needed for cost recovery")

    # Save report
    if save_report:
        report_path = os.path.join(folder, "nigeria_report.txt")
        try:
            with open(report_path, "w") as f:
                f.write("ENUGU STATE POWER SYSTEM ANALYSIS REPORT\n")
                f.write("Regulated by EERC | Distributed by EEDC\n")
                f.write("=" * 60 + "\n")
                f.write(f"Generated  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Problem    : {folder}\n")
                f.write(f"Exch. Rate : N{rate:,.0f}/$\n\n")
                f.write("GENERATOR DISPATCH\n")
                f.write(gen_df.to_string(index=False))
                f.write("\n\nFUEL MIX\n")
                for fuel, mw in fuel_breakdown.items():
                    f.write(f"  {fuel}: {mw:.2f} MW ({fuel_pct[fuel]:.1f}%)\n")
                f.write("\nLOAD ANALYSIS\n")
                f.write(f"  Total Demand    : {total_demand:.2f} MW\n")
                f.write(f"  Total Generated : {total_generated:.2f} MW\n")
                f.write(f"  Deficit/Surplus : {-deficit:.2f} MW\n")
                if deficit > 0:
                    f.write(f"  Shedding        : {shedding_pct:.1f}%\n")
                f.write("\nCOST ANALYSIS\n")
                f.write(f"  Total Cost : {format_usd(objective_usd)} / {format_ngn(objective_ngn)}\n")
                f.write(f"  Per MWh    : {format_usd(cost_per_mwh_usd)} / {format_ngn(cost_per_mwh_ngn)}\n")
                f.write(f"  Per kWh    : {format_usd(cost_per_kwh_usd)} / {format_ngn(cost_per_kwh_ngn)}\n")
                f.write(f"  EERC Tariff: N{eerc_tariff_ngn:.2f}/kWh (Band A, 2024)\n")
            print(f"\n  Report saved: {report_path}")
        except Exception as e:
            print(f"\n  Could not save report: {e}")

    print("\n" + "=" * 65)
    print("  Analysis complete.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Nigerian Power System Extension for Minpower (Enugu/Nsukka)"
    )
    parser.add_argument("folder", help="Path to the problem folder")
    parser.add_argument("--solver", default="cbc", help="Solver (default: cbc)")
    parser.add_argument("--rate", type=float, default=DEFAULT_EXCHANGE_RATE,
                        help=f"NGN/USD exchange rate (default: {DEFAULT_EXCHANGE_RATE})")
    parser.add_argument("--no-report", action="store_true",
                        help="Do not save the text report")
    args = parser.parse_args()
    analyze(folder=args.folder, solver=args.solver, rate=args.rate,
            save_report=not args.no_report)
