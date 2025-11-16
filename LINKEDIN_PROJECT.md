# Modeling the Slovenian Housing Market — Bootstrap, Monte Carlo & ML (Flask + Docker)

Use this copy on your LinkedIn Project section. Two variants are provided: short (for tight cards) and long (for detailed view), plus skills/tags.

---

## Short description (≈220 characters)

Built a reproducible analytics stack for Slovenia’s housing market: Bootstrap confidence intervals, 10k Monte Carlo simulations, ML forecasting (best Test R²=0.57), and a Flask dashboard—all containerized with Docker.

---

## Long description (≈700–900 characters)

I built an end-to-end, reproducible analysis of the Slovenian housing market combining:

- Bootstrap confidence intervals for key metrics (avg price, trend, correlations)
- 10,000-path Monte Carlo (GBM) forecasts over 8 quarters with fan charts
- Machine Learning models (Linear Regression, Random Forest, Gradient Boosting) with time-aware evaluation; best generalization from Linear Regression (Test R² = 0.57)
- A Flask dashboard for interactive exploration, styled with Bootstrap

Data: SURS building permits (supply proxy), construction cost index, and residential sales (EUR/m²). The project is fully Dockerized; on startup the container executes the notebooks to generate figures and CSVs before serving the app. Results suggest moderate growth and a strong relationship between construction costs and housing prices (r = 0.89).

Repo link: <https://github.com/VitanFasmon/modeling_slovenian_housing_market_with_machine_learning>

---

## Highlights (bullet points)

- Public data pipeline: PX (PC-Axis) → cleaned quarterly dataset (2013–2024)
- Bootstrap CIs for price level, trend (≈€1,832/Q), and cost–price correlation (r = 0.89)
- Monte Carlo: 10k paths, Q+8 median ≈ €180k, 95% interval ≈ €133k–€245k
- ML forecasting: Linear Regression best (Test R² = 0.57), 8-quarter outlook ≈ +20%
- Flask dashboard with four sections and exportable tables/figures
- Docker/Compose: notebooks auto-run on startup; healthcheck, headless plots

---

## Skills / Technologies

Python • Pandas • NumPy • SciPy • scikit-learn • Matplotlib • Seaborn • Flask • Bootstrap • Docker • Docker Compose • Jupyter • Monte Carlo Simulation • Bootstrap Resampling • Time Series • Reproducible Research

---

## Suggested media

- Screenshot of the Flask dashboard (home + one analysis section)
- Feature importance chart
- Monte Carlo fan chart (historical + forecast bands)
- Repo link and/or short screen capture of the Docker quick start

