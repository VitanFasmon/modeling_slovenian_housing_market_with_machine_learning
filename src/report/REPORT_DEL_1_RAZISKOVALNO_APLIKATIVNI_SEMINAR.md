# Modeliranje ponudbe stanovanj in gradbenih stroškov v Sloveniji z uporabo Bootstrap analize, Monte Carlo simulacije in strojnega učenja

**Avtor:** Vitan Fašmon 
**Program:** Magistrski program Spletna znanost in tehnologije  
**Predmet:** Temelji računalniških znanj  
**Mentor:** doc. dr. Matej Mertik  
**Datum:** november 2025

---

## 1. Introduction (Uvod)

Trg nepremičnin v Sloveniji se sooča z izzivi omejene ponudbe stanovanjskih enot in rastočih gradbenih stroškov. Razumevanje dinamike med gradbenimi dovoljenji, stroški gradnje in cenami nepremičnin je ključnega pomena za načrtovalce politik, razvijalce nepremičnin in investitorje. V tej nalogi sem želel raziskati, kako lahko z naprednimi statističnimi metodami in strojnim učenjem analiziramo zgodovinske podatke ter napovedujemo prihodnje trende na slovenskem stanovanjskem trgu.

**Raziskovalno vprašanje:** Kako lahko kombinacija statističnih metod (bootstrap, Monte Carlo) in strojnega učenja (regresija, naključni gozdovi) prispeva k boljšemu razumevanju in napovedovanju slovenskega trga nepremičnin?

**Cilji naloge:**
1. Združiti in pripraviti odprte podatke SURS o gradbenih dovoljenjih, stroških gradnje in prodaji nepremičnin
2. Uporabiti bootstrap metodo za ocenjevanje intervalov zaupanja ključnih metrik
3. Implementirati Monte Carlo simulacijo za verjetnostno napoved prihodnjih cen
4. Zgraditi modele strojnega učenja za napovedovanje cen stanovanj
5. Razviti interaktivno Flask spletno aplikacijo za vizualizacijo rezultatov

**Uporabljena orodja in tehnologije:**
- **Python 3.12** kot programski jezik
- **Pandas** za obdelavo in analizo podatkov
- **NumPy & SciPy** za statistične izračune
- **Scikit-learn** za strojno učenje (LinearRegression, RandomForest, GradientBoosting)
- **Matplotlib & Seaborn** za vizualizacijo podatkov
- **Flask + Bootstrap 5** za spletno aplikacijo
- **Jupyter Notebooks** za interaktivno razvijanje in dokumentiranje

---

## 2. Methods (Metode)

### 2.1 Pridobivanje in priprava podatkov

Projekt temelji na treh odprtih podatkovnih zbirkah iz Statističnega urada Republike Slovenije (SURS):

1. **Gradbena dovoljenja** (`building_permits_slovenia.PX`)
   - Frekvenca: mesečna (2013-2024)
   - Ključne spremenljivke: število izdanih gradbenih dovoljen za stanovanjske objekte
   - Uporaba: proxy za prihodnjo stanovanjsko ponudbo

2. **Indeks gradbenih stroškov** (`construction_costs_index.px`)
   - Frekvenca: četrtletna (2013-2024)
   - Bazno leto: 2021 = 100
   - Uporaba: merjenje razvoja stroškov gradnje

3. **Prodaja nepremičnin** (`number_and_value_of_residential_real_estate_sales.px`)
   - Frekvenca: četrtletna
   - Ključne spremenljivke: število prodaj, povprečna cena (EUR/m²)
   - Uporaba: ciljna spremenljivka za napovedovanje

**Proces čiščenja podatkov** (notebook `01_data_cleaning.ipynb`):

```python
# Nalaganje PX datotek
building_permits = load_px_file(BUILDING_PERMITS_PATH)
construction_costs = load_px_file(COSTS_OF_CONSTRUCTION_PATH)
residential_sales = load_px_file(NUMBER_AND_VALUE_OF_BUILDING_SALES)

# Pretvorba mesečnih podatkov v četrtletne
building_permits_monthly = clean_building_permits_data(building_permits)
quarterly_permits = aggregate_to_quarterly(
    building_permits_monthly,
    date_col='date',
    value_col='num_building_permits',
    agg_func='sum'
)

# Združevanje podatkovnih nizov
merged_data = merge_quarterly_data(
    quarterly_permits,
    costs_quarterly,
    residential_sales_quarterly
)
```

Končni združeni nabor podatkov obsega **48 četrtletij** (2013 Q1 - 2024 Q4) z naslednjimi spremenljivkami:
- `date`: četrtletje
- `num_building_permits`: število gradbenih dovoljen
- `construction_cost_index`: indeks gradbenih stroškov
- `num_residential_sales`: število prodaj stanovanj
- `avg_price_eur`: povprečna cena stanovanja (EUR/m²)

### 2.2 Bootstrap analiza intervalov zaupanja

Bootstrap metoda omogoča ocenjevanje intervalov zaupanja brez predpostavke o porazdelitvi podatkov. Implementirana je v notebooku `02_bootstrap_analysis.ipynb`.

**Algoritem:**
1. Iz obstoječih 48 opazovanj naključno izberemo 48 vzorcev z vračanjem (isti kvartal se lahko ponovi)
2. Izračunamo statistiko (npr. povprečno ceno)
3. Ponovimo postopek 10.000-krat
4. Iz porazdelitve 10.000 vzorčenih statistik izračunamo 95% interval zaupanja (2.5. in 97.5. percentil)

```python
def calculate_bootstrap_confidence_interval(
    data, statistic_func, n_bootstrap=10000, alpha=0.05
):
    np.random.seed(42)
    bootstrap_stats = []
    n = len(data)
    
    for _ in range(n_bootstrap):
        resample_idx = np.random.choice(n, size=n, replace=True)
        bootstrap_stats.append(statistic_func(data[resample_idx]))
    
    bootstrap_stats = np.array(bootstrap_stats)
    ci_lower = np.percentile(bootstrap_stats, alpha/2 * 100)
    ci_upper = np.percentile(bootstrap_stats, (1 - alpha/2) * 100)
    
    return ci_lower, ci_upper, bootstrap_stats
```

**Analizirane metrike:**
- Povprečna cena stanovanj
- Naklon cenovnega trenda (rast per četrtletje)
- Korelacija med stroški gradnje in cenami

### 2.3 Monte Carlo simulacija prihodnjih cen

Monte Carlo metoda uporablja stohastično simuliranje za generiranje verjetnostnih napovedi. Implementirana je v `03_montecarlo_simulation.ipynb`.

**Model: Geometric Brownian Motion (GBM)**

Cene modeliramo kot geometrijsko Brownovo gibanje:

```
dS = μS dt + σS dW
```

kjer je:
- S = cena stanovanja
- μ = drift (pričakovana rast)
- σ = volatilnost (standardna deviacija donosov)
- dW = Wienerjevo naključno gibanje

**Parametri, ocenjeni iz zgodovinskih podatkov:**

```python
# Logaritemski donosi
log_returns = np.diff(np.log(prices))

# Drift (trend)
mu_quarterly = np.mean(log_returns)  # 1.26% na četrtletje
mu_annual = mu_quarterly * 4         # 5.04% letno

# Volatilnost
sigma_quarterly = np.std(log_returns)  # 5.69% na četrtletje
sigma_annual = sigma_quarterly * np.sqrt(4)  # 11.38% letno
```

**Simulacijski algoritem:**

```python
n_simulations = 10000
n_quarters = 8  # 2 leti

for sim in range(n_simulations):
    path = [initial_price]
    for quarter in range(n_quarters):
        random_shock = np.random.normal(0, 1)
        price_next = path[-1] * np.exp(
            mu_quarterly + sigma_quarterly * random_shock
        )
        path.append(price_next)
    all_paths.append(path)
```

Iz 10.000 simulacij izračunamo:
- Median (50. percentil) - najbolj verjetna napoved
- 95% interval zaupanja (5. - 95. percentil)
- Verjetnostna porazdelitev cen v vsakem prihodnjem četrtletju

### 2.4 Modeli strojnega učenja

V notebooku `04_ml_prediction.ipynb` sem implementiral tri modele za napovedovanje cen stanovanj.

**Inženiring značilk:**

Iz surovih podatkov sem ustvaril 10 napovednih spremenljivk:
- **Trenutne vrednosti:** število dovoljen, indeks stroškov, število prodaj
- **Zakasnitve (lags):** cena pred 1 četrtletjem, cena pred 4 četrtletji (medletno), dovoljenja pred 1 Q, prodaje pred 1 Q
- **Drseča povprečja (MA4):** 4-četrtletno drseče povprečje za cene, dovoljenja, stroške

```python
# Zakasnitve za zajemanje momentum-a
df['price_lag1'] = df['avg_price_eur'].shift(1)
df['price_lag4'] = df['avg_price_eur'].shift(4)

# Drseča povprečja za glajenje šuma
df['price_ma4'] = df['avg_price_eur'].rolling(window=4).mean()
df['permits_ma4'] = df['num_building_permits'].rolling(window=4).mean()
```

**Trenirani modeli:**

1. **Linearna regresija** (baseline):
   - Standardizacija značilk (StandardScaler)
   - Koeficienti razkrivajo vpliv posameznih značilk
   
2. **Random Forest Regressor**:
   - 50 dreves, max_depth=5 (regularizacija proti preučenju)
   - Nelinearne interakcije med spremenljivkami
   
3. **Gradient Boosting Regressor**:
   - 50 iteracij, learning_rate=0.05
   - Sekvenčno učenje napak

**Delitev podatkov:**
- 80% učna množica (35 četrtletij)
- 20% testna množica (9 četrtletij)
- Brez mešanja (ohranjanje časovnega zaporedja)

**Evaluacijske metrike:**
- R² (koeficient determinacije) - delež pojasnjene variance
- RMSE (Root Mean Squared Error) - povprečna velikost napake
- MAE (Mean Absolute Error) - povprečno absolutno odstopanje
- MAPE (Mean Absolute Percentage Error) - povprečno procentualno odstopanje

**8-četrtletna napoved z rolling horizon:**

```python
# Začetne značilke iz zadnjega opazovanja
current_features = last_row_features.copy()
current_price = last_price

for quarter_ahead in range(1, 9):
    # Napoved z najboljšim modelom
    if best_model == 'Linear Regression':
        scaled = scaler.transform([current_features])
        pred_price = model.predict(scaled)[0]
    else:
        pred_price = model.predict([current_features])[0]
    
    # Q+1 glajenje: omejitev na ±13.1% (mean + 2σ iz zgodovine)
    if quarter_ahead == 1:
        max_change = historical_mean + 2 * historical_std
        pred_price = np.clip(pred_price, 
                            current_price * (1 - max_change),
                            current_price * (1 + max_change))
    else:
        # Q+2-8: ±10% per quarter (stabilizacija)
        pred_price = np.clip(pred_price, 
                            current_price * 0.9, 
                            current_price * 1.1)
    
    # Posodobitev značilk za naslednje četrtletje
    current_features[3] = pred_price  # price_lag1
    current_features[4] = current_features[3]  # price_lag4
    current_features[7] = (current_features[7] * 3 + pred_price) / 4
    
    current_price = pred_price
```

### 2.5 Flask spletna aplikacija

Spletna aplikacija (`app.py`) združuje vse rezultate v interaktivni dashboard z Bootstrap 5 oblikovanjem.

**Arhitektura:**
- **Backend:** Flask (Python mikrookvir)
- **Frontend:** Jinja2 predloge + Bootstrap 5.3.3
- **Struktura:**
  - `templates/base.html` - osnovna predloga (navbar, footer)
  - `templates/index.html` - glavna stran z 4 sekcijami
  - `/figures/<section>/<file>` - serviranje slik
  - `/results/<section>/<file>` - serviranje CSV datotek

**Sekcije dashboarda:**
1. **Izvirni podatki:** časovne vrste gradbenih dovoljen, stroškov, cen
2. **Bootstrap analiza:** porazdelitve, intervali zaupanja
3. **Monte Carlo simulacija:** verjetnostne napovedi, območja zaupanja
4. **ML napovedi:** primerjava modelov, napoved 8 četrtletij, pomembnost značilk

```python
@app.route("/")
def index():
    # Nalaganje podatkov za vsako sekcijo
    bootstrap_table = pd.read_csv("results/bootstrap/bootstrap_summary.csv")
    ml_forecast = pd.read_csv("results/ml_prediction/price_forecast.csv")
    
    context = {
        "bootstrap_table": bootstrap_table,
        "ml_forecast": ml_forecast,
        "bootstrap_images": list_images("figures/bootstrap"),
        # ... ostale sekcije
    }
    return render_template("index.html", **context)
```

### 2.6 Docker integracija in reproducibilnost

Za zagotovitev ponovljivosti rezultatov in enostavnega zagona aplikacije je projekt kontejneriziran z Docker in orkestriran z Docker Compose (V2).

**Zakaj Docker?**

- Enotno okolje (Python 3.12-slim + vse knjižnice iz `requirements.txt`)
- Hitro postavljanje in deljenje (1 ukaz za zagon celotne aplikacije)
- Reproducibilni rezultati (fiksne verzije paketov, brez »works on my machine«)

**Ključne tehnične podrobnosti:**

- Osnovna slika: `python:3.12-slim`
- Vstopna točka: `python app.py` (Flask)
- Mapa dela v kontejnerju: `/app`
- Objavljen port: `5000` (host) → `5000` (container)
- Volumni (read-only):
    - `./src/figures:/app/src/figures:ro` (slike za dashboard)
    - `./src/results:/app/src/results:ro` (CSV rezultati analiz)

**Hiter zagon (priporočeno):**

```bash
docker compose up --build
```

Aplikacija je nato dostopna na: <http://localhost:5000>

**Zaustavitev:**

```bash
docker compose down
```

**Zdravstveni pregled (healthcheck):**

- Compose konfiguracija periodično preverja, ali je endpoint `/` odziven, kar pomaga pri diagnostiki ob zagonu.

**Reproducibilnost:**

- Fiksni `requirements.txt` in nastavljeni `random_state`/`np.random.seed` v analizah
- Kontejner zagotavlja identično okolje ne glede na OS (Linux/Mac/Windows)

**Dodatna dokumentacija:**

- Podrobna navodila: `DOCKER_README.md`
- Kratka navodila: `DOCKER_QUICKSTART.md`

---

## 3. Results (Rezultati)

### 3.1 Bootstrap rezultati

**Povprečna cena stanovanj:**
- Točkovna ocena: **€121,347**
- 95% interval zaupanja: **€102,458 - €140,236**
- Relativna napaka: ±15.6%

**Cenovni trend (naklon regresije):**
- Rast: **€1,832 na četrtletje**
- 95% interval zaupanja: **€1,246 - €2,418**
- To pomeni letno rast okoli **€7,328** oz. **6.0% nominalno**

**Korelacija med stroški gradnje in cenami:**
- Pearsonov koeficient: **r = 0.89** (zelo močna pozitivna povezava)
- 95% interval zaupanja: **0.81 - 0.94**
- Interpretacija: višji gradbeni stroški močno napovedujejo višje cene stanovanj

### 3.2 Monte Carlo rezultati

**Napoved za Q+8 (2 leti naprej):**
- Median: **€180,524**
- 95% interval zaupanja: **€132,847 - €245,213**
- Trenutna cena (Q0): **€166,796**
- Pričakovana rast: **+8.2%** (median)

**Verjetnostna porazdelitev:**
- P(rast > 0%) = 73%
- P(rast > 10%) = 45%
- P(padec > 10%) = 12%

**Konvergenca simulacije:**
- Stabilizacija medianske napovedi pri ~5,000 simulacijah
- Končno število simulacij: 10,000 za zanesljive intervale zaupanja

### 3.3 Rezultati strojnega učenja

**Primerjava modelov:**

| Model               | Train R² | Test R² | RMSE     | MAE      |
|---------------------|----------|---------|----------|----------|
| Linear Regression   | 0.9300   | 0.5713  | €20,438  | €16,924  |
| Random Forest       | 0.7900   | -6.8300 | €87,273  | €72,155  |
| Gradient Boosting   | 0.7800   | -5.6800 | €80,667  | €65,438  |

**Interpretacija:**
- **Linearna regresija** dosega najboljšo generalizacijo (Test R² = 0.57)
- Drevesni modeli kažejo hudo preučenje (negativen Test R²) kljub regularizaciji
- Majhna učna množica (35 vzorcev, 10 značilk = 3.5 vzorcev/značilko) omejuje kompleksne modele

**Pomembnost značilk (Linear Regression koeficienti):**
1. **price_ma4** (+22,847): 4-četrtletno drseče povprečje ima največji vpliv
2. **cost_ma4** (+4,128): drseče povprečje stroškov
3. **permits_lag1** (+3,256): dovoljenja iz prejšnjega četrtletja
4. **price_lag1** (-2,845): negativen koeficient kaže mean reversion
5. **construction_cost_index** (-2,134): trenutni stroški negativno vplivajo

**8-četrtletna napoved:**

| Četrtletje | Napoved (EUR) | Sprememba (EUR) | Sprememba (%) |
|------------|---------------|-----------------|---------------|
| Q+1        | 180,938       | +14,142         | +8.0%         |
| Q+2        | 182,197       | +1,258          | +9.2%         |
| Q+3        | 184,628       | +2,432          | +10.7%        |
| Q+4        | 187,709       | +3,081          | +12.5%        |
| Q+8        | 200,330       | +33,535         | +20.1%        |

**Glajenje Q+1:**
Model napoveduje 8% skok v prvem četrtletju. Analiza zgodovinske volatilnosti pokaže:
- Povprečna četrtletna sprememba: **1.72%**
- Standardni odklon: **5.69%**
- Meja razumnosti (μ + 2σ): **13.1%**

Ker je 8% < 13.1%, je napoved **statistično sprejemljiva** - model zaznava odboj po začasnem padcu iz €168k (Q-1) na €167k (Q0).

### 3.4 Flask aplikacija

Spletna aplikacija je dostopna na `http://127.0.0.1:5000` in vključuje:
- **4 interaktivne sekcije** z vizualizacijami in tabelami
- **Responziven dizajn** (Bootstrap grid sistem)
- **Povečane slike** (400px višina na desktop, 320px na mobilnih)
- **Dinamično serviranje** CSV in PNG datotek

Primer vizualizacije:
- Zgodovinske cene + Monte Carlo napoved s 95% intervalom zaupanja
- ML napoved z ločenimi barvami za zgodovino (modra) in napoved (zelena)
- Feature importance grafi za interpretabilnost modelov

---

## 4. Analysis / Discussion (Analiza in razprava)

### 4.1 Metodološka izvedba

**Prednosti pristopa:**

1. **Bootstrap omogoča robust ocenjevanje** brez parametričnih predpostavk - primerno za majhne vzorce in neznane porazdelitve
2. **Monte Carlo zajema stohastično naravo** finančnih trgov - verjetnostne napovedi so realističnejše od točkovnih
3. **Kombinacija metod daje triangulacijo** - različni pristopi potrjujejo trende
4. **Flask integracija** omogoča enostaven dostop do rezultatov brez tehnične ekspertize

**Omejitve in izzivi:**

1. **Majhna učna množica** (44 opazovanja po čiščenju):
   - Ratio 3.5 vzorcev/značilko je pod priporočenim pragom 20
   - Drevesni modeli močno preučijo podatke (Test R² < 0)
   - Rešitev: uporaba regularizacije, izbira bolj robustnega linearnega modela

2. **Časovna odvisnost podatkov**:
   - Tradicionalne CV metode niso primerne (bi povzročile data leakage)
   - Uporaba time-series split brez shuffling
   - Forecast uporablja rolling horizon z ažuriranjem značilk

3. **Parametrične predpostavke GBM**:
   - Predpostavka log-normalnih donosov morda ni izpolnjena
   - Alternativa: empirični bootstrap iz zgodovinskih donosov (bi ohranil repe porazdelitve)

4. **Eksogene spremenljivke konstantne**:
   - ML napoved predpostavlja, da dovoljenja, stroški in prodaje ostanejo stabilne
   - Realistična nadgradnja: scenarijska analiza (kaj če stroški narastejo za 10%?)

### 4.2 Primerjava z obstoječimi rešitvami

**Akademska literatura:**
- OECD Economic Surveys uporabljajo ARIMA modele za cene nepremičnin
- Naš pristop dodaja:
  - Stohastično simuliranje (Monte Carlo)
  - Multivariatne značilke (dovoljenja, stroški)
  - Interpretabilnost skozi bootstrap intervale zaupanja

**Komercialne napovedi (Eurostat, ECB):**
- Uporabljajo kompleksne DSGE modele z makroekonomskimi povezavami
- Naš pristop je **bolj transparenten** in **lažji za razumevanje**
- Primeren za hitro prototipiranje in raziskovalne študije

### 4.3 Možnosti izboljšav

**Kratkoročno:**
1. **Dodajanje makroekonomskih spremenljivk**: BDP rast, obrestne mere, inflacija
2. **Regionalna disagregacija**: Ljubljana vs. ostala Slovenija
3. **Interaktivni scenariji v Flask**: slider za stroške, dovoljenja

**Dolgoročno:**
1. **Bayesian approach**: prior distributions + podatki → posterior
2. **LSTM nevronske mreže**: deep learning za časovne vrste
3. **Eksogeni šoki**: COVID-19, energetska kriza, demografija

### 4.4 Uporabnost v raziskovalnem in praktičnem okolju

**Raziskovalno:**
- **Metodološki template** za podobne študije (energetika, transport)
- **Odprtokodna implementacija** (GitHub repository)
- **Reproducibilnost**: seed values, requirements.txt, Docker potencial

**Praktično:**
- **Razvijalci nepremičnin**: hitro ocenjevanje tržnih trendov
- **Državne institucije**: simulacije politik (npr. vpliv neprofitnega gradbeništva)
- **Izobraževanje**: demonstracija statističnih konceptov skozi realne podatke

---

## 5. Conclusion (Zaključek)

Ta naloga demonstrira, kako kombinacija statističnih metod (Bootstrap, Monte Carlo) in strojnega učenja (scikit-learn) omogoča celovito analizo in napovedovanje slovenskega trga nepremičnin.

**Ključne ugotovitve:**

1. **Bootstrap analiza pokaže močno povezavo** (r = 0.89) med gradbenimi stroški in cenami stanovanj z zanesljivimi intervali zaupanja
2. **Monte Carlo simulacija napoveduje** median rasti 8.2% v naslednjih 2 letih, s širokim intervalom zaupanja (€132k - €245k) zaradi velike volatilnosti
3. **Linearna regresija dosega Test R² = 0.57**, kar je sprejemljivo ob majhni učni množici; drevesni modeli preučijo podatke
4. **Flask aplikacija uspešno integrira** vse komponente v dostopen, vizualno privlačen dashboard

**Pridobljene kompetence:**

- **Tehnične**: pandas obdelava PX datotek, scikit-learn pipeline, Flask routing, Bootstrap responsive design
- **Statistične**: razumevanje bootstrap resampling, stohastičnih procesov (GBM), cross-validation strategij
- **Raziskovalne**: strukturiranje IMRAD poročila, interpretacija rezultatov, kritična evalvacija omejitev

**Dodana vrednost pristopa:**

- **Transparentnost**: vsak korak je dokumentiran v Jupyter notebooks
- **Reproduktivnost**: fiksni random seeds, versionirane knjižnice
- **Modularnost**: ločene funkcije v `helpers/data_processing.py`
- **Dostopnost**: spletni vmesnik ne zahteva programerskega znanja

**Prihodnji razvoj:**

Ta projekt bi lahko služil kot osnova za:
1. **Magistrsko raziskavo** o vplivu makroekonomskih politik na stanovanjski trg
2. **Komercialno orodje** za nepremičninske analitike (SaaS model)
3. **Izobraževalni tutorial** o povezavi statistike in programiranja

**Osebni vpogled:**

Največ sem se naučil o **pomenu validacije modelov** - prvotno sem uporabil kompleksne modele, ki so dosegli visok Train R², a katastrofalen Test R². To me je naučilo, da **preprostost in robustnost** pogosto premagata kompleksnost, še posebej pri majhnih podatkovnih množicah.

---

## 6. Reference

**Podatkovni viri:**
- Statistični urad Republike Slovenije (SURS). (2024). *Stavbe, za katere so bila izdana gradbena dovoljenja*. Pridobljeno iz https://podatki.gov.si
- SURS. (2024). *Indeksi gradbenih stroškov za nova stanovanja*. Pridobljeno iz https://podatki.gov.si
- SURS. (2024). *Število in vrednost sklenjenih prodajnih pogodb*. Pridobljeno iz https://podatki.gov.si

**Spletni viri:**
- Bootstrap Documentation. (2024). https://getbootstrap.com/docs/5.3/
- Scikit-learn User Guide. (2024). https://scikit-learn.org/stable/user_guide.html
- Flask Documentation. (2024). https://flask.palletsprojects.com/

**Umetna inteligenca:**
- GitHub Copilot
- ChatGTP 5.0

---

