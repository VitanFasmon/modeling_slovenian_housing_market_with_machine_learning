# Seminarska Naloga - Temelji Računalniških Znanj

## 📋 Pregled Poročil

Ta mapa vsebuje dve glavni poročili za predmet Temelji računalniških znanj:

### 1. Del 1: Raziskovalno-aplikativni seminar (IMRAD)
**Datoteka:** `REPORT_DEL_1_RAZISKOVALNO_APLIKATIVNI_SEMINAR.md`

**Vsebina:**
- **Introduction:** Raziskovalno vprašanje, cilji, uporabljena orodja
- **Methods:** Priprava podatkov, Bootstrap analiza, Monte Carlo simulacija, ML modeli, Flask aplikacija
- **Results:** Rezultati vseh analiz z vizualizacijami in tabelami
- **Analysis/Discussion:** Metodološka evalvacija, omejitve, možnosti izboljšav
- **Conclusion:** Ključne ugotovitve, pridobljene kompetence, prihodnji razvoj
- **Reference:** Podatkovni viri, literatura, programske knjižnice

**Struktura projekta:**
1. Data Cleaning (notebook 01)
2. Bootstrap Analysis (notebook 02)
3. Monte Carlo Simulation (notebook 03)
4. ML Prediction (notebook 04)
5. Flask Web Application

### 2. Priloga 1: Refleksija
**Datoteka:** `PRILOGA_1_REFLEKSIJA.md`

**Vsebina:**
- **Uvodni opis:** Namen vaj, medsebojna povezanost
- **Analitični del:** Raziskovalni cilji, poglobljeni koncepti, premagovanje izzivov
- **Aplikativni del:** Uporabna vrednost, realne aplikacije, mikro-raziskava
- **Refleksija o učenju:** Pridobljene kompetence, povezovanje računalništva in raziskovanja
- **Zaključek:** Osebni vpogled, načrt nadaljnjega razvoja

## 🎯 Ključni Rezultati Projekta

### Statistični Rezultati

**Bootstrap Analiza:**
- Povprečna cena: €121,347 (95% CI: €102,458 - €140,236)
- Cenovni trend: €1,832/Q (95% CI: €1,246 - €2,418)
- Korelacija stroški-cene: r=0.89 (95% CI: 0.81-0.94)

**Monte Carlo Simulacija:**
- Napoved Q+8: €180,524 (median)
- 95% interval: €132,847 - €245,213
- Verjetnost rasti: 73%

**Machine Learning:**
- Najboljši model: Linear Regression (Test R²=0.57)
- Napoved 2-letne rasti: +20.1% (€166k → €200k)
- Ključna značilka: price_ma4 (koeficient +22,847)

### Tehnične Dosežke

- ✅ Obdelava 3 podatkovnih nizov (PX format)
- ✅ 10,000 bootstrap iteracij
- ✅ 10,000 Monte Carlo simulacij
- ✅ 3 ML modeli (LinearRegression, RandomForest, GradientBoosting)
- ✅ Flask spletna aplikacija z Bootstrap 5 dizajnom
- ✅ 4 Jupyter notebooks z dokumentacijo
- ✅ Modularni kod (helpers/data_processing.py)
- ✅ Docker integracija (Dockerfile + Docker Compose V2)

## 📁 Struktura Projekta

```text
final_project/
├── src/
│   ├── notebooks/
│   │   ├── 01_data_cleaning.ipynb
│   │   ├── 02_bootstrap_analysis.ipynb
│   │   ├── 03_montecarlo_simulation.ipynb
│   │   └── 04_ml_prediction.ipynb
│   ├── data/
│   │   ├── raw/                 # Surovi podatki SURS
│   │   └── processed/           # Očiščeni podatki
│   ├── results/
│   │   ├── bootstrap/           # Bootstrap CSV
│   │   ├── montecarlo/          # Monte Carlo CSV
│   │   └── ml_prediction/       # ML modeli in napovedi
│   ├── figures/
│   │   ├── original_data/       # Časovne vrste
│   │   ├── bootstrap/           # Bootstrap vizualizacije
│   │   ├── montecarlo/          # Monte Carlo grafi
│   │   └── ml_prediction/       # ML rezultati
│   ├── helpers/
│   │   └── data_processing.py   # Modularni funkcije
│   └── report/
│       ├── REPORT_DEL_1_RAZISKOVALNO_APLIKATIVNI_SEMINAR.md
│       ├── PRILOGA_1_REFLEKSIJA.md
│       └── README.md (ta dokument)
├── templates/
│   ├── base.html                # Bootstrap predloga
│   └── index.html               # Dashboard
├── app.py                       # Flask aplikacija
└── requirements.txt             # Python dependencies
```

## 🚀 Kako Zagnati Projekt

### 🐳 Docker zagon (priporočeno)

```bash
docker compose up --build
```

Aplikacija bo dostopna na: <http://localhost:5000>

Zaustavitev:

```bash
docker compose down
```

Več podrobnosti: glej `DOCKER_QUICKSTART.md` in `DOCKER_README.md` v korenu repozitorija.

### 1. Nalaganje Odvisnosti

```bash
pip install -r requirements.txt
```

### 2. Poganjanje Notebooks

```bash
jupyter notebook src/notebooks/
```

**Vrstni red izvajanja:**
1. `01_data_cleaning.ipynb` → generira processed data
2. `02_bootstrap_analysis.ipynb` → bootstrap rezultati
3. `03_montecarlo_simulation.ipynb` → Monte Carlo napovedi
4. `04_ml_prediction.ipynb` → ML modeli in napovedi

### 3. Zagon Flask Aplikacije

```bash
python app.py
```

Aplikacija dostopna na: `http://127.0.0.1:5000`

## 📊 Uporabljeni Podatki

**Vir:** Statistični urad Republike Slovenije (SURS)

1. **Gradbena dovoljenja**
   - Datoteka: `building_permits_slovenia.PX`
   - Frekvenca: Mesečna (2013-2024)
   - URL: https://podatki.gov.si

2. **Gradbeni stroški**
   - Datoteka: `construction_costs_index.px`
   - Frekvenca: Četrtletna (2013-2024)
   - Bazno leto: 2021 = 100

3. **Prodaja nepremičnin**
   - Datoteka: `number_and_value_of_residential_real_estate_sales.px`
   - Frekvenca: Četrtletna
   - Metrika: Povprečna cena EUR/m²

## 🛠 Uporabljene Tehnologije

- **Python 3.12**
- **Pandas** - data manipulation
- **NumPy & SciPy** - numerical computing
- **Scikit-learn** - machine learning
- **Matplotlib & Seaborn** - visualization
- **Flask** - web framework
- **Bootstrap 5** - responsive design
- **Jupyter** - interactive notebooks

## 📝 Pomembne Opombe

### Omejitve Projekta

1. **Majhen vzorec:** 44 četrtletij → visoka varianca napovedi
2. **Predpostavke:** GBM predpostavlja log-normalne donose
3. **Eksogene spremenljivke:** ML model predpostavlja stabilnost dovoljen/stroškov
4. **Preučenje:** Drevesni modeli (RF, GB) preučijo podatke kljub regularizaciji

### Možnosti Izboljšav

- 📈 **Dodatne značilke:** BDP, inflacija, obrestne mere
- 🗺 **Geografska segmentacija:** Ljubljana vs. ostala Slovenija
- 🔄 **Real-time ažuriranje:** Avtomatski scraping SURS API
- 📱 **Interaktivnost:** Plotly grafi, scenario sliders
- ☁️ **Deployment:** CI/CD in oblačni deploy (npr. Azure Web Apps, Fly.io)


### Python Dokumentacija
- Pandas: https://pandas.pydata.org/docs/
- Scikit-learn: https://scikit-learn.org/stable/
- Flask: https://flask.palletsprojects.com/

---
