#!/bin/bash
set -e

echo "=========================================="
echo "Running Jupyter Notebooks to generate data"
echo "=========================================="

# Navigate to notebooks directory
cd /app/src/notebooks

echo "[1/4] Running 01_data_cleaning.ipynb..."
jupyter nbconvert --to notebook --execute --inplace 01_data_cleaning.ipynb

echo "[2/4] Running 02_bootstrap_analysis.ipynb..."
jupyter nbconvert --to notebook --execute --inplace 02_bootstrap_analysis.ipynb

echo "[3/4] Running 03_montecarlo_simulation.ipynb..."
jupyter nbconvert --to notebook --execute --inplace 03_montecarlo_simulation.ipynb

echo "[4/4] Running 04_ml_prediction.ipynb..."
jupyter nbconvert --to notebook --execute --inplace 04_ml_prediction.ipynb

echo "=========================================="
echo "All notebooks executed successfully!"
echo "Starting Flask application..."
echo "=========================================="

# Return to app root
cd /app

# Start Flask server
exec python app.py
