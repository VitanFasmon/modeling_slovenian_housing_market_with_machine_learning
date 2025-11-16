# Priloga 1: Refleksija - Temelji računalniških znanj

**Avtor:** [Ime in priimek]  
**Program:** Magistrski program Spletna znanost in tehnologije  
**Predmet:** Temelji računalniških znanj  
**Datum:** november 2025

---

## 1. Uvodni opis

### 1.1 Namen in potek vaj

V okviru predmeta Temelji računalniških znanj sem izvedel celovit projekt analize slovenskega trga nepremičnin, ki je obsegal štiri ključne komponente:

**Vaja 1: Obdelava in čiščenje podatkov (Data Cleaning)**
- **Namen:** Pridobiti, očistiti in združiti odprte podatke iz SURS
- **Potek:** Nalaganje PX datotek, pretvorba datumov, agregacija mesečnih v četrtletne podatke, združevanje treh podatkovnih nizov
- **Rezultat:** Čist dataset 48 četrtletij z 5 ključnimi spremenljivkami

**Vaja 2: Bootstrap analiza (Statistična inferenca)**
- **Namen:** Oceniti intervale zaupanja za tržne metrike brez parametričnih predpostavk
- **Potek:** Implementacija bootstrap resampling algoritma, izračun 10.000 vzorčenih porazdelitev, vizualizacija intervalov zaupanja
- **Rezultat:** Robustne ocene povprečnih cen (€102k-€140k), cenovnih trendov (€1,246-€2,418/Q), korelacij (r=0.81-0.94)

**Vaja 3: Monte Carlo simulacija (Verjetnostno modeliranje)**
- **Namen:** Napovedati prihodnje cene z verjetnostnimi intervali
- **Potek:** Ocenjevanje GBM parametrov (drift, volatilnost), simulacija 10.000 scenarijev, izračun percentilnih intervalov
- **Rezultat:** Verjetnostna napoved Q+8: median €180k, 95% CI €133k-€245k

**Vaja 4: Strojno učenje (Predictive Modeling)**
- **Namen:** Zgraditi napovedne modele z uporabo scikit-learn
- **Potek:** Feature engineering (lags, moving averages), trening 3 modelov (LR, RF, GB), evalvacija, 8-četrtletna napoved
- **Rezultat:** Linearna regresija dosega Test R²=0.57, napoved rasti 20% v 2 letih

**Vaja 5: Flask spletna aplikacija (Data Visualization)**
- **Namen:** Integrirati vse analize v interaktivno spletno aplikacijo
- **Potek:** Flask routing, Jinja2 templating, Bootstrap responsive design, serviranje slik in CSV datotek
- **Rezultat:** Dashboard z 4 sekcijami, dostopen prek brskalnika

### 1.2 Izbor teme in medsebojna povezanost

**Zakaj stanovanjski trg?**

Izbral sem analizo slovenskega trga nepremičnin iz več razlogov:
1. **Relevantnost:** Stanovanjska problematika je aktualna družbena tema
2. **Dostopnost podatkov:** SURS ponuja kakovostne odprte podatke
3. **Kompleksnost:** Zadostno število spremenljivk za multivariatno analizo
4. **Časovna komponenta:** Četrtletni podatki omogočajo časovno-serijske metode

**Kako se vaje med seboj povezujejo?**

Projekt sledi logični progresiji od podatkov do vpogledov:

```
Surovi podatki (PX datoteke)
    ↓
[Vaja 1] Čiščenje in priprava
    ↓
Čist dataset (48 četrtletij)
    ↓           ↓                ↓
[Vaja 2]    [Vaja 3]        [Vaja 4]
Bootstrap   Monte Carlo     ML modeli
    ↓           ↓                ↓
Intervali    Verjetnostne   Deterministične
zaupanja     napovedi       napovedi
    ↓           ↓                ↓
         [Vaja 5] Flask
              ↓
    Interaktivni dashboard
```

Vsaka vaja gradi na prejšnjih:
- **Bootstrap** uporablja očiščene podatke iz Vaje 1
- **Monte Carlo** uporablja parametre ocenjene iz zgodovinskih podatkov
- **ML modeli** kombinirajo vse spremenljivke iz združenega dataseta
- **Flask** prikazuje rezultate vseh metod v enotnem vmesniku

---

## 2. Analitični del (raziskovalni pristop)

### 2.1 Raziskovalni cilji posameznih vaj

**Vaja 1 - Data Cleaning:**
- **Cilj:** Ugotoviti, ali lahko PX formatu (PC-Axis) učinkovito obdelam z Pandas
- **Hipoteza:** Združevanje treh različnih frekvenc (mesečno, četrtletno) bo zahtevalo agregacijo
- **Metoda:** Pisanje modularnih funkcij za vsak tip podatkov

**Vaja 2 - Bootstrap:**
- **Cilj:** Preveriti, ali bootstrap daje širše intervale zaupanja od parametričnih metod pri majhnih vzorcih
- **Vprašanje:** Kako stabilen je trend rasti cen? Ali je korelacija med stroški in cenami robustna?
- **Pristop:** Primerjava bootstrap CI z normalnim približkom

**Vaja 3 - Monte Carlo:**
- **Cilj:** Raziskati verjetnostno porazdelitev prihodnjih cen - ni nas zanimal samo "point estimate", ampak celotna porazdelitev možnih izidov
- **Vprašanje:** Kako širok je interval negotovosti za 2-letno napoved?
- **Pristop:** GBM z empirično ocenjenimi parametri, 10.000 simulacij

**Vaja 4 - Machine Learning:**
- **Cilj:** Ugotoviti, ali multivariatni pristop (dovoljenja + stroški + zakasnitve) izboljša napovedi
- **Hipoteza:** Kompleksnejši modeli (RF, GB) bodo boljši od linearne regresije
- **Izid:** Presenečenje! Linearna regresija zmagala zaradi preučevanja pri majhnih vzorcih

**Vaja 5 - Flask:**
- **Cilj:** Raziskati, kako lahko rezultate naredim dostopne netehničnim uporabnikom
- **Vprašanje:** Ali lahko dashboard zgradim brez JavaScript frameworkov (React, Vue)?
- **Pristop:** Minimalistična rešitev s Jinja2 in Bootstrap

### 2.2 Koncepti, ki sem jih moral poglobljeno razumeti

**1. Pandas obdelava kompleksnih formatov:**
- PX datoteke niso standardne CSV - vsebujejo metapodatke, nestandardne separatorje
- Moral sem razumeti `pd.read_csv()` parametre: `sep`, `skiprows`, `encoding`
- **Ključni vpogled:** Pandas je dovolj fleksibilen za večino formatov, če razumeš strukturo

**2. Bootstrap statistika:**
- Razlika med "sampling with replacement" vs "without replacement"
- Zakaj bootstrap porazdelitev aproksimira *sampling distribution* statistike
- Kdaj bootstrap odpove (premalo podatkov, extreme outliers)
- **Aha trenutek:** Bootstrap ne povečuje informacije - samo omogoča ocenjevanje varianc

**3. Stohastični procesi (GBM):**
- Razlika med aritmetičnim (ABM) in geometrijskim (GBM) Brownovim gibanjem
- Zakaj log-returns namesto simple returns (aditivnost, simetrija)
- Annualizacija volatilnosti: σ_annual = σ_quarterly × √4 (ne × 4!)
- **Napaka, ki sem jo naredil:** Prvotno sem uporabil simple returns - dobil negativne cene v simulacijah

**4. Scikit-learn pipeline:**
- Zakaj je `fit_transform()` na train, samo `transform()` na test (preprečevanje data leakage)
- Pomen `random_state` za reproduktivnost
- `shuffle=False` pri time series split
- **Kritična lekcija:** Preučevanje (overfitting) je resen problem pri majhnih podatkih - Train R²=0.99 ne pomeni nič, če je Test R²=-5

**5. Flask arhitektura:**
- MVC pattern: Model (podatki) - View (template) - Controller (route)
- Jinja2 template inheritance: `{% extends %}`, `{% block %}`
- Static file serving: `send_from_directory()` vs. `/static` folder
- **Debugging:** Jinja napake so včasih kriptične - potrebna je sistematičnost

### 2.3 Premagovanje meja znanja

**Izziv 1: PX format parsing**
- **Meja:** Ni standardne knjižnice za PX datoteke
- **Rešitev:** Prebral SURS dokumentacijo, eksperimentiral z `pd.read_csv()`, napisal custom parser
- **Viri:** SURS tehnična specifikacija, Stack Overflow

**Izziv 2: Bootstrap convergence**
- **Meja:** Nisem vedel, koliko resamples potrebujem za stabilen CI
- **Rešitev:** Naredil convergence plot (10 - 100.000 bootstraps), izbral 10.000
- **Viri:** Efron & Tibshirani (1994) knjiga, CrossValidated forum

**Izziv 3: GBM parameter estimation**
- **Meja:** Nisem razumel razlike med drift in realized returns
- **Rešitev:** Študij finančne literature, implementacija obeh metod, primerjava
- **Viri:** Hull (2018) *Options, Futures, and Other Derivatives*, YouTube (QuantPy)

**Izziv 4: Model overfitting**
- **Meja:** Random Forest dosegel Train R²=0.99, Test R²=-6.83
- **Rešitev:** Sistematično dodajanje regularizacije (`max_depth`, `min_samples_split`), reduction feature count
- **Eksperiment:** Testiral sem 15 kombinacij hyperparametrov - vsi drevesni modeli so failali
- **Zaključek:** Včasih je bolje priznati, da imaš premalo podatkov

**Izziv 5: Jinja template debugging**
- **Meja:** "TemplateAssertionError: block 'content' defined twice" - ni bilo jasno kje
- **Rešitev:** Prebral celotno base.html, odkril duplikacijo HTML strukture
- **Orodje:** ChatGPT mi je pomagal identificirati duplikat, jaz sem ga ročno odstranil

**Izziv 6: ML forecast jump**
- **Meja:** Model je napovedal €14k skok v Q+1 - izgledalo je kot bug
- **Raziskava:** Kreiral debug cell, analiziral feature values, odkril da je skok v območju zgodovinske volatilnosti (mean + 2σ)
- **Vpogled:** "Bug" je bil legitimen model output - model je zaznal pattern, ki ga jaz nisem

**Kaj sem se naučil o učenju:**
- **Google + ChatGPT + Dokumentacija** so 80% rešitve
- **Eksperimentiranje** je ključno - ne moreš vedeti brez testiranja
- **Stackoverflow** je zlato - večina problemov je že nekdo rešil
- **Peer review** (posvet s sošolci) razkrije blind spots

### 2.4 Možnosti izboljšav z več časa/podatkov

**Z več časa (1-2 tedna):**
1. **Bayesian bootstrap:** Prior beliefs + podatki → robustnejše napovedi pri majhnih vzorcih
2. **SHAP values:** Interpretabilnost ML modelov - zakaj model napove določeno ceno
3. **Interactive plots:** Plotly namesto static Matplotlib - zoom, hover tooltips
4. **Scenario analysis v Flask:** Slider za "kaj če stroški narastejo za X%?"
5. **Docker deployment:** Enostavna reprodukcija okolja

**Z več podatki (mesečni namesto četrtletnih):**
1. **ARIMA/SARIMA modeli:** Časovno-serijske metode za sezonske vzorce
2. **LSTM nevronske mreže:** Deep learning za kompleksne nelinearne vzorce
3. **Regionalna segmentacija:** Ljubljana vs. Maribor vs. ostalo
4. **Dodajanje makro spremenljivk:** BDP, inflacija, obrestne mere ECB
5. **External shocks modeling:** COVID-19, energetska kriza

**Metodološke izboljšave:**
1. **Walk-forward validation:** Bolj realistična evalvacija time-series modelov
2. **Ensemble forecasting:** Kombinacija Bootstrap, Monte Carlo in ML
3. **Uncertainty quantification:** Confidence bands za vsako napoved
4. **Backtesting:** Kako bi modeli delovali v preteklosti?

---

## 3. Aplikativni del (povezava z realnim svetom)

### 3.1 Dejanska uporabna vrednost rešitve

**1. Raziskovalne aplikacije:**

**Urbana ekonomija:**
- **Problem:** Razumevanje vzrokov za stanovanjski primanjkljaj
- **Rešitev:** Moj pristop omogoča kvantifikacijo vpliva gradbenih stroškov na ponudbo
- **Uporaba:** Simulacija "kaj če" scenarijev (npr. subvencije gradnje)

**Ekonometrija:**
- **Problem:** Ocenjevanje intervalov zaupanja pri časovnih serijah z majhnimi vzorci
- **Rešitev:** Bootstrap je nepogrešljiv v situacijah, kjer normalna porazdelitev ne velja
- **Primer:** Disertacije o volatilnosti trgov v manjših državah

**2. Poslovne aplikacije:**

**Nepremičninski razvijalci:**
- **Problem:** Kdaj investirati v novi projekt? Ali bodo cene rasle?
- **Rešitev:** Monte Carlo verjetnostne napovedi → kalkulacija ROI scenarijev
- **Dodana vrednost:** Dashboard omogoča hitro ocenjevanje brez Excel spreadsheetov

**Banke in kreditne institucije:**
- **Problem:** Ocenjevanje tveganja hipotekarnih kreditov
- **Rešitev:** Napovedi cen stanovanj → ocena collateral vrednosti
- **Razširitev:** Stress testing portfeljev (kaj če cene padejo za 20%?)

**3. Družbene aplikacije:**

**Stanovanjska politika:**
- **Problem:** Vlada potrebuje podatke za odločanje (neprofitna stanovanja, subvencije)
- **Rešitev:** Model povezuje dovoljenja → ponudbo → cene
- **Vpogledi:** Simulacija učinka povečanja gradbenih dovoljen za 50%

**Osebne finance:**
- **Problem:** Ali kupiti stanovanje zdaj ali čakati?
- **Rešitev:** Verjetnostne napovedi pomagajo pri odločitvi
- **Transparentnost:** Vsi izračuni in podatki javno dostopni

### 3.2 Realni podatki za nadgradnjo

**Makroekonomski podatki (ECB, BSI):**
- Obrestne mere (EURIBOR) - vpliv na affordability
- Inflacija (HICP) - realne vs. nominalne cene
- BDP per capita - kupna moč

**Demografski podatki (SURS):**
- Migracijski saldo - povpraševanje
- Starostna struktura - first-time buyers
- Gospodinjska sestava - velikost stanovanj

**Finančni podatki:**
- Odobreni hipotekarni krediti - indikator likvidnosti
- LTV (loan-to-value) ratios - dostopnost

**Kvalitativni podatki:**
- Sentiment indeksi (consumer confidence)
- Novice in politični dogodki (text mining)

**Prostorski podatki:**
- GIS koordinate - geografska segmentacija
- Oddaljenost od centra - hedonic pricing

### 3.3 Mikro-raziskava / projekt za prakso

**Predlog: "Real-time Housing Market Monitor"**

**Namen:** Avtomatizirani sistem za mesečno ažuriranje napovedi

**Komponente:**
1. **Data pipeline:** Scraping SURS API → avtomatska obdelava
2. **Model retraining:** Vsak mesec re-fit modele z novimi podatki
3. **Alert system:** Email notification pri večjih spremembah
4. **Public API:** Dostop do napovedi za razvijalce

**Implementacija (3-6 mesecev):**
- **Mesec 1-2:** Backend (FastAPI, PostgreSQL baza)
- **Mesec 3-4:** Frontend (React dashboard, real-time charts)
- **Mesec 5:** Deployment (AWS Lambda, CloudWatch scheduling)
- **Mesec 6:** Testing, dokumentacija, open-source release

**Impact:**
- Raziskovalci → dostop do posodobljenih napovedi
- Javnost → transparentnost trga nepremičnin
- Magistrska naloga → real-world deployment izkušnje

---

## 4. Refleksija o učenju

### 4.1 Pridobljene računalniške in raziskovalne kompetence

**Tehnične kompetence:**

**1. Data wrangling (Pandas):**
- Obvladovanje kompleksnih transformacij: `groupby`, `merge`, `rolling`, `shift`
- Custom parsers za nestandardne formate
- **Pred:** Znal sem osnovne operacije (read_csv, head, describe)
- **Po:** Znam obvladovati kompleksne ETL pipeline

**2. Statistično programiranje (NumPy/SciPy):**
- Implementacija bootstrap algoritma od nič
- Razumevanje random number generation (`np.random.seed`)
- **Pred:** Uporabljal samo prepared funkcije (scipy.stats.ttest)
- **Po:** Znam implementirati custom resampling algoritme

**3. Machine learning workflow (Scikit-learn):**
- Feature engineering pipeline
- Train/test split strategije za time series
- Hyperparameter tuning in regularizacija
- **Pred:** Copy-paste koda iz tutorialov
- **Po:** Razumevanje bias-variance tradeoff, overfitting prepoznavanje

**4. Spletni razvoj (Flask + Bootstrap):**
- MVC arhitektura
- Template inheritance (Jinja2)
- Responsive design (Bootstrap grid)
- **Pred:** Nisem razumel routing koncepta
- **Po:** Znam zgraditi fullstack aplikacijo

**5. Verzioniranje in reproduktivnost (Git + Best practices):**
- Struktura projekta (src/, data/, notebooks/)
- Requirements.txt za dependency management
- Random seeds za reproduktivnost
- **Pred:** Ena datoteka z vsem kodom
- **Po:** Modularna, maintainable codebase

**Raziskovalne kompetence:**

**1. Statistična inferenca:**
- Razumevanje razlike med parametričnimi in neparametričnimi metodami
- Interpretacija intervalov zaupanja vs. prediction intervals
- **Vpogled:** CI pove o negotovosti ocene, ne o porazdelitvi prihodnjih vrednosti

**2. Model validation:**
- Cross-validation strategije
- Metrics selection (kdaj R², kdaj MAE, kdaj MAPE)
- Overfitting detection
- **Lekcija:** Visok Train score brez Test score je rdeča zastava

**3. Verjetnostno razmišljanje:**
- Monte Carlo ne da "ene" napovedi, ampak porazdelitev
- Razumevanje risk vs. uncertainty
- **Sprememba perspektive:** Od "kakšna bo cena?" → "kakšna je verjetnost, da cena presega X?"

**4. Znanstveno komuniciranje:**
- IMRAD struktura
- Vizualizacija rezultatov (katere grafe uporabiti)
- **Izboljšava:** Prej sem samo pokazal rezultate, zdaj znam argumentirati zakaj metoda

### 4.2 Povezovanje računalništva in raziskovalnega razmišljanja

**Pred predmetom:**
- Videl sem programiranje kot "tool" - nekaj, kar rabim za analizo
- Raziskovanje = zbiranje podatkov + statistični test + pisanje
- Excel je bil moj glavni workflow

**Med predmetom:**
- **Aha moment 1:** Programiranje je raziskovalno orodje - omogoča eksperimentiranje
  - Primer: Lahko testiram 100 različnih bootstrap velikosti v 5 minutah
  - V Excelu bi to trajalo ure
  
- **Aha moment 2:** Reproducibility je raziskovalna etika
  - Jupyter notebooks → vsak korak je dokumentiran
  - Random seeds → drugi lahko ponovijo moje rezultate
  - To je bistvo znanstvenega dela!

- **Aha moment 3:** Vizualizacija je raziskovalni proces, ne samo prezentacija
  - Convergence plot mi je pokazal, da potrebujem 10k bootstraps
  - Feature importance graf mi je razkril, da price_lag1 dominira
  - Debugging graf mi je pomagal razumeti "€14k jump bug"

**Po predmetu:**
- **Nova perspektiva:** Računalništvo in raziskovanje sta neločljivo povezana
- Programiranje mi omogoča:
  - **Iteracijo:** Hitro testiranje hipotez
  - **Skaliranje:** Analize, ki bi bile ročno nemogoče
  - **Transparentnost:** Koda je bolj precizna od naravnega jezika
  - **Reproducibilnost:** Drugi lahko preverijo moje delo

**Konkretni primeri integracije:**

1. **Raziskovalno vprašanje:** "Ali je bootstrap CI širši od parametričnega?"
   - **Računalniški pristop:** Implementiraj obe metodi, primerjaj v loopu
   - **Rezultat:** Bootstrap je ~15% širši pri n=48

2. **Raziskovalno vprašanje:** "Koliko simulacij potrebujem?"
   - **Računalniški pristop:** Convergence analysis (plot variance vs. n_sims)
   - **Rezultat:** Stabilizacija pri ~5,000, izbral 10,000 za safety margin

3. **Raziskovalno vprašanje:** "Zakaj model preučuje?"
   - **Računalniški pristop:** Grid search hyperparameters, plot learning curves
   - **Rezultat:** Premalo podatkov (44/10 = 4.4 samples/feature)

### 4.3 Sprememba razumevanja programiranja v mojem strokovnem delu

**Pred:**
- Programiranje = tehničen tool za implementacijo rešitev
- "Plačal bom razvijalca, da to naredi"
- Fokus na rezultate, ne proces

**Zdaj:**
- Programiranje = raziskovalno orodje za raziskovanje vprašanj
- "Moram razumeti kodo, da razumem omejitve metode"
- Fokus na reproducibilnost, transparentnost, validacijo

**Konkretne spremembe v pristopu:**

**1. Od blackbox do whitebox:**
- **Prej:** Uporabljal sem Excel statistične funkcije brez razumevanja
- **Zdaj:** Implementiral sem bootstrap od nič → razumem vsak korak

**2. Od static do iterative:**
- **Prej:** Enkratna analiza → poročilo
- **Zdaj:** Jupyter notebook omogoča iteracijo in dokumentiranje misli

**3. Od individualnega do reproducibilnega:**
- **Prej:** Analiza, ki jo samo jaz lahko ponovim
- **Zdaj:** GitHub repo, requirements.txt → kdorkoli lahko podvoji

**Aplikacija na magistrsko delo:**

Moja magistrska tema: [Primer - Spletne tehnologije v izobraževanju]

**Kako bom uporabil naučeno:**
1. **Data collection:** Scraping, API calls (ne več ročno kopiranje)
2. **Analysis:** Statistical tests v Python (ne Excel)
3. **Visualization:** Interactive dashboards (ne statični PowerPoint)
4. **Validation:** Cross-validation, bootstrapping za robustnost
5. **Dissemination:** GitHub repo + dokumentacija (ne samo PDF)

---

## 5. Zaključek: Osebni vpogled in načrt nadaljnjega razvoja

### 5.1 Naslednja razvojna stopnja

**Kratkoročno (3-6 mesecev):**

1. **Deep dive v time series:**
   - Knjiga: "Forecasting: Principles and Practice" (Hyndman & Athanasopoulos)
   - Implementacija ARIMA, SARIMA, Prophet
   - Uporaba: Nadgradnja magistrskega projekta

2. **Bayesian statistics:**
   - Online tečaj: "Bayesian Statistics" (Coursera)
   - PyMC3 library za probabilistic programming
   - Cilj: Robustnejše napovedi pri majhnih vzorcih

3. **Advanced ML:**
   - LightGBM, XGBoost (optimizirani gradient boosting)
   - Feature engineering automation (FeatureTools)
   - Hyperparameter optimization (Optuna)

**Dolgoročno (1-2 leti):**

1. **Magistrska naloga:**
   - Tema: "Predictive Analytics for [moja domena]"
   - Uporaba vseh naučenih metod
   - Real-world deployment z metrikami uspešnosti

2. **Open-source contributions:**
   - Prispevati k scikit-learn ali pandas
   - Razviti Python package za slovensko-specifične podatke (surs-api)

3. **Profesionalni razvoj:**
   - Data Science certifikat (AWS, Google Cloud)
   - Portfolio projektov na GitHub
   - Eventual cilj: ML Engineer ali Research Scientist

### 5.2 Vključitev znanja v magistrski projekt / prakso

**Magistrski projekt - konkretni plan:**

**Faza 1: Research design**
- Uporaba IMRAD strukture (naučene v tej nalogi)
- Literatura review z Bootstrap CI za meta-analizo
- Power analysis za določanje sample size

**Faza 2: Data collection**
- Python scraping namesto ročnega zbiranja
- PostgreSQL za storage namesto Excel
- Git verzioniranje podatkovnih transformacij

**Faza 3: Analysis**
- Jupyter notebooks za eksplorativno analizo
- Scikit-learn za predictive modeling
- Bootstrap za robustnost intervalov zaupanja

**Faza 4: Validation**
- Cross-validation strategije (ne samo single split)
- Monte Carlo simulacije za sensitivity analysis
- Statistical tests za significance

**Faza 5: Dissemination**
- Flask dashboard za interaktivno prezentacijo
- GitHub repository za reproducibilnost
- Open data sharing (kjer etično dovoljeno)

**Poklicna praksa:**

**Scenario 1: Raziskovalec v akademiji**
- Vsi naučeni pristopi direktno aplicabilni
- Publikacije bodo imeli open-source kodo
- Reproduktivnost = competitive advantage

**Scenario 2: Data Scientist v industriji**
- Flask dashboards za stakeholder reports
- ML pipelines za production deployment
- Statistical rigor za business decisions

**Scenario 3: Consultant**
- Monte Carlo za risk analysis klientov
- Bootstrap CI za robustne ocene
- Professional dashboards za presentations

### 5.3 Ena poved: Kaj mi je ta predmet omogočil razumeti

**"Ta predmet mi je omogočil razumeti, da programiranje ni samo tehničen tool za implementacijo rešitev, ampak raziskovalno orodje, ki spreminja način razmišljanja - od statičnega eksperimentiranja do iterativne, reproducibilne in transparentne znanstvene raziskave."**

**Dodatni vpogled:**

Največja sprememba je bila **mindset shift** od:
- "Kako lahko to izračunam?" → "Kako lahko to avtomatiziram in validiram?"
- "Kakšen je rezultat?" → "Kako zanesljiv je ta rezultat?"
- "Znam uporabljati orodje" → "Razumem omejitve orodja"

**Osebna rast:**

Pred predmetom sem bil **pasiven uporabnik** statističnih metod.  
Po predmetu sem **kritičen raziskovalec**, ki razume matematiko, implementacijo in omejitve.

To je razlika med operaterjem in strokovnjakom.

---

## 6. Docker integracija: reproducibilnost in prenosljivost

### 6.1 Kaj sem implementiral

- **Dockerfile** z osnovo `python:3.12-slim` in namestitvijo vseh odvisnosti iz `requirements.txt`
- **Docker Compose (V2)** za orkestracijo aplikacije, mapiranje porta `5000:5000` in read-only volumne za rezultate/figure
- **Healthcheck** v `docker-compose.yml`, ki preverja odzivnost aplikacije

### 6.2 Kako Docker izboljša moj potek dela

- **Reproducibilnost:** Enako okolje na vsakem računalniku (brez konflikta verzij)
- **Onboarding:** Kdor klonira repo, lahko zažene celotno aplikacijo z enim ukazom
- **Pariteta dev/prod:** Enaka konfiguracija lokalno in v produkciji
- **Čisto okolje:** Ni potrebe po lokalnih virtualnih okoljih ali globalnih namestitvah

### 6.3 Hiter zagon

```bash
docker compose up --build
```

Aplikacija je nato dostopna na: <http://localhost:5000>

Za zaustavitev:

```bash
docker compose down
```

### 6.4 Izzivi in rešitve pri integraciji

- Prehod na **Docker Compose V2** (ukaz `docker compose` namesto `docker-compose`)
- **Port 5000**: konflikt z obstoječimi procesi (rešitev: sprememba porta ali kill procesa)
- **Volumni**: read-only mounti za `src/results` in `src/figures` zagotavljajo integriteto izhodov

### 6.5 Dokumentacija

- Kratka navodila: `DOCKER_QUICKSTART.md`
- Podrobna navodila in troubleshooting: `DOCKER_README.md`

---

**Zahvala:**

Zahvaljujem se mentorju doc. dr. Mateju Mertiku za strukturiran pristop k predmetu, ki povezuje teorijo in prakso.

---


