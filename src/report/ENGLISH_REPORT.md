# Modeling the Slovenian Housing Market with Bootstrap, Monte Carlo, and Machine Learning (Flask + Docker)

Author: Vitan Fašmon  
Program: MSc in Web Science and Technologies  
Course: Fundamentals of Computer Science  
Supervisor: Assoc. Prof. Dr. Matej Mertik  
Date: November 2025

---

## Abstract

This project analyzes the Slovenian residential housing market by combining statistical inference (Bootstrap), stochastic simulation (Monte Carlo), and supervised learning (scikit-learn) into a coherent, reproducible workflow. Three public datasets from the Statistical Office of the Republic of Slovenia (SURS)—building permits (supply proxy), construction cost index (input prices), and residential sales (prices and volumes)—were cleaned, aligned quarterly, and merged. We estimate confidence intervals for market metrics with Bootstrap, simulate price paths over eight quarters with a GBM-based Monte Carlo model (10,000 runs), and evaluate three ML models for price forecasting (Linear Regression, Random Forest, Gradient Boosting). Results are exposed in a Flask dashboard and fully containerized with Docker; the container executes notebooks on startup to generate all figures and CSV outputs before serving the app. Key findings: average price €121,347 (95% CI: €102,458–€140,236), strong cost–price correlation (r=0.89), Q+8 Monte Carlo median forecast €180,524 with 95% interval €132,847–€245,213, and best ML generalization from Linear Regression (Test R²=0.57) with an 8-quarter forecast of ~+20%.

---

## 1. Introduction

Housing supply constraints and rising construction costs shape Slovenian price dynamics. We ask:

Research question: How can Bootstrap, Monte Carlo simulation, and machine learning jointly improve understanding and forecasting of housing prices in Slovenia?

Contributions:

- A clean, merged quarterly dataset (2013–2024) from SURS PX sources
- Bootstrap CIs for key market metrics (price level, trend, correlations)
- Monte Carlo (GBM) forecasts with uncertainty bounds over 8 quarters
- Comparative ML forecasting (LR, RF, GB) with robust evaluation
- A Flask dashboard showcasing all results, containerized with Docker

---

## 2. Data and Sources

All data are obtained from SURS:

- Building permits (`building_permits_slovenia.PX`), monthly → aggregated to quarterly
- Construction cost index (`construction_costs_index.px`), quarterly, base year 2021=100
- Residential sales (`number_and_value_of_residential_real_estate_sales.px`), quarterly (price EUR/m², counts)

Final merged dataset: 48 quarters (2013 Q1 – 2024 Q4) with variables:

- num_building_permits, construction_cost_index, num_residential_sales, avg_price_eur

---

## 3. Methodology

### 3.1 Data Processing

- Parse PC-Axis (PX) formats with pandas and custom loaders
- Aggregate monthly building permits to quarterly sums
- Merge datasets on quarter and engineer features:
  - Lags: price_lag1, price_lag4; permits_lag1; sales_lag1
  - 4-quarter moving averages: price_ma4, permits_ma4, cost_ma4

### 3.2 Bootstrap Inference

- Resample n=48 observations with replacement, 10,000 iterations
- Compute statistics per resample; extract 95% percentile CIs
- Metrics: average price, linear trend per quarter, cost–price correlation

Results:

- Average price: €121,347 (95% CI: €102,458–€140,236)
- Growth trend: €1,832 per quarter (95% CI: €1,246–€2,418)
- Cost–price correlation: r=0.89 (95% CI: 0.81–0.94)

### 3.3 Monte Carlo Simulation

We model prices with Geometric Brownian Motion:

$$ dS = \mu S\, dt + \sigma S\, dW $$

- Drift and volatility estimated from historical log-returns
- 10,000 simulations, horizon of 8 quarters

Results:

- Q+8 median: €180,524
- 95% interval: €132,847–€245,213
- P(price increase > 0%): 73%

### 3.4 Machine Learning Forecasting

- Models: Linear Regression, Random Forest, Gradient Boosting
- Train/test split (80/20) preserving temporal order (no shuffling)
- StandardScaler for linear model; evaluation via R², RMSE, MAE, MAPE

Key outcomes:

- Best generalization: Linear Regression (Test R² = 0.57)
- Tree models overfit given small sample size (negative Test R²)
- 8-quarter rolling forecast with a Q+1 smoothing constraint:
  - Historical quarterly change: mean 1.72%, std 5.69%
  - Q+1 capped to ±(mean + 2σ) ≈ ±13.1%; Q+2–Q+8 clipped to ±10% per quarter

---

## 4. Results

Model comparison (concise): Linear Regression generalizes best (Test R² = 0.57); tree-based models overfit the 44-sample training set. The 8-quarter forecast indicates a cumulative ~20% rise, with an initial Q+1 increase of ~8%, which is statistically reasonable within historical volatility (below mean + 2σ).

Dashboard content:

- Original data: time series of permits, costs, sales, and prices
- Bootstrap analysis: distributions and CIs
- Monte Carlo simulation: fan chart with 5–95% bands
- ML predictions: 8-quarter forecast, feature importance, train vs. test

---

## 5. Reproducibility and Docker

The repository is fully containerized. On startup, the container executes the notebooks to generate data and figures before starting Flask.

Quick start (recommended):

```bash
docker compose up --build
```

- App: <http://localhost:5000>
- Entry-point runs notebooks (01→04) if outputs are missing, then executes `app.py`
- Outputs persist if you bind-mount `src/results`, `src/figures`, and `src/data/processed`

See `DOCKER_QUICKSTART.md` and `DOCKER_README.md` for details, healthcheck notes, and troubleshooting.

---

## 6. Discussion

Strengths:

- Triangulation of insights: Bootstrap CIs, Monte Carlo distributions, and ML forecasts
- Transparent, small-data-appropriate modeling with interpretable baselines
- Reproducible end-to-end workflow (requirements, seeds, Docker)

Limitations:

- Small sample (44–48 quarters) limits model complexity and power
- GBM assumes log-normal returns; fat tails could be underrepresented
- ML forecast keeps exogenous drivers stable (permits, costs, sales) → scenario analysis is a natural extension

Improvements:

- Add macro variables (GDP, inflation, interest rates) and regional segmentation
- Walk-forward validation and probabilistic ML (e.g., Bayesian regression)
- Interactive scenario controls in the dashboard (e.g., cost shocks)

---

## 7. Reflection (selected insights)

- Overfitting is a real risk with small time-series datasets—simple linear models can outperform complex ones
- A systematic debugging workflow matters: validate “jumps” against historical volatility before calling them bugs
- Reproducibility (seeds, requirements, Docker) is not optional—it is integral to research quality
- Visualization is part of thinking: convergence plots, feature importance, and forecast bands reveal structure

---

## 8. Conclusion

Combining Bootstrap, Monte Carlo, and ML yields a robust and interpretable view of the Slovenian housing market. Confidence intervals, probabilistic forecasts, and simple predictive baselines align to suggest moderate growth over the next two years. The Flask dashboard and Dockerization make the work accessible and reproducible for technical and non-technical audiences alike.

---

## 9. References

- SURS (Statistical Office of the Republic of Slovenia) Open Data Portal — <https://podatki.gov.si>
- Scikit-learn User Guide — <https://scikit-learn.org/stable/user_guide.html>
- Flask Documentation — <https://flask.palletsprojects.com/>
- Bootstrap Documentation — <https://getbootstrap.com/docs/5.3/>

