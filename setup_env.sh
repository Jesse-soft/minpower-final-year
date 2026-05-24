#!/bin/bash

# =============================================================
# Minpower Environment Setup Script
# Sets up everything needed to run Minpower from scratch
# Run this from the root of the minpower-final-year repo
# =============================================================

set -e

echo ""
echo "========================================"
echo "   Minpower Setup — EEE592 Final Year  "
echo "   University of Nigeria, Nsukka       "
echo "========================================"
echo ""

# -----------------------------------------------
# Step 1: Check conda is installed
# -----------------------------------------------
echo "🔍 Checking for conda..."

if ! command -v conda &> /dev/null; then
    echo ""
    echo "❌ conda not found."
    echo ""
    echo "Please install Miniconda first:"
    echo "  👉 https://docs.conda.io/en/latest/miniconda.html"
    echo ""
    echo "After installing, close and reopen your terminal, then run this script again."
    exit 1
fi

echo "✅ conda found: $(conda --version)"
echo ""

# -----------------------------------------------
# Step 2: Create conda environment
# -----------------------------------------------
echo "🐍 Creating conda environment 'minpower' (Python 3.10 + pandas 1.5.3)..."
echo "   This may take a few minutes..."
echo ""

if conda env list | grep -q "^minpower "; then
    echo "⚠️  Environment 'minpower' already exists — skipping creation."
    echo "   To recreate it, run: conda env remove -n minpower"
else
    conda create -n minpower python=3.10 pandas=1.5.3 matplotlib pyomo -c conda-forge -y
    echo "✅ Environment created."
fi

echo ""

# -----------------------------------------------
# Step 3: Activate environment
# -----------------------------------------------
echo "⚡ Activating minpower environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate minpower
echo "✅ Activated."
echo ""

# -----------------------------------------------
# Step 4: Install CBC solver
# -----------------------------------------------
echo "🔧 Installing CBC solver..."
conda install -c conda-forge coincbc -y
echo "✅ CBC solver installed."
echo ""

# -----------------------------------------------
# Step 5: Install Python dependencies
# -----------------------------------------------
echo "📦 Installing Python dependencies..."
pip install cylp tables xarray setuptools --quiet
echo "✅ Dependencies installed."
echo ""

# -----------------------------------------------
# Step 6: Install minpower package
# -----------------------------------------------
echo "📦 Installing minpower package..."
pip install -e . --quiet
echo "✅ Minpower installed."
echo ""

# -----------------------------------------------
# Step 7: Configure environment permanently
# -----------------------------------------------
echo "⚙️  Configuring environment settings..."

# Add to bashrc if not already there
if ! grep -q "conda activate minpower" ~/.bashrc; then
    echo "conda activate minpower" >> ~/.bashrc
    echo "   Added: conda activate minpower → ~/.bashrc"
fi

if ! grep -q "MPLBACKEND=Agg" ~/.bashrc; then
    echo "export MPLBACKEND=Agg" >> ~/.bashrc
    echo "   Added: export MPLBACKEND=Agg → ~/.bashrc"
fi

export MPLBACKEND=Agg
echo "✅ Environment configured."
echo ""

# -----------------------------------------------
# Step 8: Run test solve
# -----------------------------------------------
echo "🧪 Running test solve (Economic Dispatch — Wood & Wollenberg Example 3-7)..."
echo ""

minpower minpower/tests/ed-WW-3-7/ --solver cbc

echo ""
echo "========================================"
echo "✅ Setup complete!"
echo ""
echo "To run problems:"
echo "  minpower minpower/tests/ed-WW-3-7/ --solver cbc   # Economic Dispatch"
echo "  minpower minpower/tests/opf-WW-6-2/ --solver cbc  # Optimal Power Flow"
echo "  minpower minpower/tests/uc/ --solver cbc           # Unit Commitment"
echo ""
echo "Results (CSV + PNG) are saved in each problem folder."
echo "========================================"
echo ""
