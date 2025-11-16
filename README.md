# 🏘️ Modeling the Slovenian Housing Market

Comprehensive analysis of the residential real estate market in Slovenia using statistical methods (Bootstrap, Monte Carlo) and machine learning.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Project Overview

This project analyzes the Slovenian housing market using a combination of:
- **Data Processing:** Cleaning and merging SURS (Statistical Office of Slovenia) datasets
- **Bootstrap Analysis:** Confidence intervals for market metrics
- **Monte Carlo Simulation:** Probabilistic forecasts of future prices
- **Machine Learning:** Predictive models (Linear Regression, Random Forest, Gradient Boosting)
- **Flask Application:** Interactive dashboard for results visualization

### 🎯 Key Results

- **Bootstrap CI:** Average price €121,347 (95% CI: €102,458-€140,236)
- **Monte Carlo:** Q+8 forecast: €180,524 (median), 95% CI: €132,847-€245,213
- **ML Model:** Test R² = 0.57, 2-year growth forecast: +20.1%

## 🚀 Quick Start

### Option 1: Docker (Recommended) 🐳

**Fastest way to run the application:**

```bash
# Clone the repository

# Run with Docker Compose
docker compose up --build
```

**Application accessible at:** http://localhost:5000

**More about Docker setup:** See [DOCKER_README.md](DOCKER_README.md)

### Option 2: Local Installation 💻

**Prerequisites:**
- Python 3.12+
- pip

**Steps:**

```bash
# 1. Clone the repository

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Flask application
python app.py
```

**Application accessible at:** http://127.0.0.1:5000

### Option 3: Jupyter Notebooks 📓

**For research analysis:**

```bash
# Activate virtual environment
source venv/bin/activate

# Start Jupyter
jupyter notebook src/notebooks/
```

**Execution order:**
1. `01_data_cleaning.ipynb` → Data cleaning
2. `02_bootstrap_analysis.ipynb` → Bootstrap analysis
3. `03_montecarlo_simulation.ipynb` → Monte Carlo simulation
4. `04_ml_prediction.ipynb` → ML models and predictions

## 📁 Project Structure

```
final_project/
├── 🐳 Docker files
│   ├── Dockerfile              # Docker image configuration
│   ├── docker-compose.yml      # Multi-container orchestration
│   ├── .dockerignore           # Files excluded from Docker image
│   └── DOCKER_README.md        # Docker documentation
│
├── 🌐 Flask application
│   ├── app.py                  # Main Flask server
│   ├── templates/              # Jinja2 templates
│   │   ├── base.html           # Bootstrap base template
│   │   └── index.html          # Dashboard page
│   └── requirements.txt        # Python dependencies
│
├── 📊 Analysis and data
│   └── src/
│       ├── notebooks/          # Jupyter notebooks
│       │   ├── 01_data_cleaning.ipynb
│       │   ├── 02_bootstrap_analysis.ipynb
│       │   ├── 03_montecarlo_simulation.ipynb
│       │   └── 04_ml_prediction.ipynb
│       │
│       ├── data/
│       │   ├── raw/            # Raw SURS data (PX format)
│       │   └── processed/      # Cleaned data (CSV)
│       │
│       ├── results/            # Analysis results (CSV)
│       │   ├── bootstrap/
│       │   ├── montecarlo/
│       │   └── ml_prediction/
│       │
│       ├── figures/            # Visualizations (PNG)
│       │   ├── original_data/
│       │   ├── bootstrap/
│       │   ├── montecarlo/
│       │   └── ml_prediction/
│       │
│       ├── helpers/            # Utility functions
│       │   └── data_processing.py
│       │
│       └── report/             # Seminar reports (Slovenian)
│           ├── REPORT_DEL_1_RAZISKOVALNO_APLIKATIVNI_SEMINAR.md
│           ├── PRILOGA_1_REFLEKSIJA.md
│           └── README.md
│
└── 📝 Documentation
    └── README.md (this document)
```

## 🛠 Technologies Used

### Backend
- **Python 3.12** - Programming language
- **Flask 3.0** - Web framework
- **Pandas 2.2** - Data manipulation
- **NumPy 1.26** - Numerical computing
- **SciPy 1.12** - Scientific computing

### Machine Learning
- **Scikit-learn 1.4** - ML models (LinearRegression, RandomForest, GradientBoosting)
- **StandardScaler** - Feature normalization

### Visualization
- **Matplotlib 3.8** - Plotting library
- **Seaborn 0.13** - Statistical visualizations

### Frontend
- **Bootstrap 5.3.3** - CSS framework
- **Jinja2** - Template engine

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📊 Data Sources

All data obtained from the **Statistical Office of the Republic of Slovenia (SURS)**:

1. **Building Permits** (`building_permits_slovenia.PX`)
   - Frequency: Monthly (2013-2024)
   - Metric: Number of issued permits for residential buildings

2. **Construction Costs** (`construction_costs_index.px`)
   - Frequency: Quarterly (2013-2024)
   - Metric: Construction cost index (base year 2021=100)

3. **Residential Sales** (`number_and_value_of_residential_real_estate_sales.px`)
   - Frequency: Quarterly
   - Metric: Number of sales, average price (EUR/m²)

**Source:** https://podatki.gov.si

## 🔬 Methodology

### 1. Data Processing
- Parsing PX format files
- Aggregating monthly to quarterly data
- Merging three datasets
- Feature engineering (lags, moving averages)

### 2. Bootstrap Analysis
```python
# 10,000 bootstrap iteracij
for i in range(10000):
    resample = np.random.choice(data, size=len(data), replace=True)
    bootstrap_stats.append(calculate_statistic(resample))
    
ci_lower = np.percentile(bootstrap_stats, 2.5)
ci_upper = np.percentile(bootstrap_stats, 97.5)
```

**Results:**
- Average price: €121,347 (95% CI: €102,458-€140,236)
- Growth trend: €1,832/Q (95% CI: €1,246-€2,418)
- Cost-price correlation: r=0.89 (95% CI: 0.81-0.94)

### 3. Monte Carlo Simulation
```python
# Geometric Brownian Motion
for sim in range(10000):
    for t in range(8):  # 8 quarters
        random_shock = np.random.normal(0, 1)
        price_next = price * np.exp(mu + sigma * random_shock)
```

**Results:**
- Q+8 forecast: €180,524 (median)
- 95% interval: €132,847 - €245,213
- Growth probability: 73%

### 4. Machine Learning
```python
# Feature engineering
features = [
    'num_building_permits', 'construction_cost_index', 'num_residential_sales',
    'price_lag1', 'price_lag4', 'permits_lag1', 'sales_lag1',
    'price_ma4', 'permits_ma4', 'cost_ma4'
]

# 80/20 train/test split (time-ordered)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

# Best model: Linear Regression
model = LinearRegression()
model.fit(StandardScaler().fit_transform(X_train), y_train)
```

**Results:**
- Linear Regression: Test R² = 0.57 ✅
- Random Forest: Test R² = -6.83 (overfitting)
- Gradient Boosting: Test R² = -5.68 (overfitting)

## 🖥 Flask Dashboard

The dashboard includes 4 main sections:

### 1. Original Data
- Time series of building permits
- Construction cost index
- Number of sales and prices

### 2. Bootstrap Analysis
- Bootstrap sample distributions
- Confidence intervals
- Statistical tests

### 3. Monte Carlo Simulation
- 10,000 simulations of future prices
- Probability intervals (5%-95%)
- Convergence analysis

### 4. ML Predictions
- Comparison of 3 models
- Feature importance
- 8-quarter forecast
- Train vs Test performance

## 🐛 Troubleshooting

### Problem: Port 5000 already in use

**Solution:**
```bash
# Kill existing process
lsof -i :5000
kill -9 <PID>

# Or change port in docker-compose.yml
ports:
  - "5001:5000"
```

### Problem: Docker container won't start

**Solution:**
```bash
# Check logs
docker compose logs flask-app

# Rebuild without cache
docker compose down
docker compose build --no-cache
docker compose up
```

### Problem: Missing data

**Solution:**
```bash
# Run all notebooks in sequence
cd src/notebooks/
jupyter nbconvert --execute --to notebook 01_data_cleaning.ipynb
jupyter nbconvert --execute --to notebook 02_bootstrap_analysis.ipynb
jupyter nbconvert --execute --to notebook 03_montecarlo_simulation.ipynb
jupyter nbconvert --execute --to notebook 04_ml_prediction.ipynb
```

## 📚 Documentation

- **[DOCKER_README.md](DOCKER_README.md)** - Docker setup and instructions
- **[src/report/README.md](src/report/README.md)** - Overview of seminar reports
- **[src/report/REPORT_DEL_1_RAZISKOVALNO_APLIKATIVNI_SEMINAR.md](src/report/REPORT_DEL_1_RAZISKOVALNO_APLIKATIVNI_SEMINAR.md)** - Research analysis (IMRAD, in Slovenian)
- **[src/report/PRILOGA_1_REFLEKSIJA.md](src/report/PRILOGA_1_REFLEKSIJA.md)** - Personal reflection (in Slovenian)

## 🤝 Contributions

Project developed for the course **Fundamentals of Computer Science**, Master's program in Web Science and Technologies.

**Author:** Vitan Fasmon  
**Mentor:** Assoc. Prof. Dr. Matej Mertik  
**Date:** November 2025

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🔗 Links

- **GitHub Repository:** https://github.com/VitanFasmon/temelji_racunalniskih_znanj_final_project
- **SURS Data:** https://podatki.gov.si
- **Flask Documentation:** https://flask.palletsprojects.com/
- **Scikit-learn:** https://scikit-learn.org/

---

**⭐ If you like this project, give it a star on GitHub!**
