# DOCUMENTATION.md — Decisions, Findings, and Change Log

This file serves as the single source of truth for all analytical decisions, code review findings, and pipeline changes made throughout the project.

Sections 1–8 document the original analytical decisions made during EDA (in German, as authored).
Sections 9+ document subsequent findings and changes (in English, per project language convention in ANALYSIS.md).

---

## Original analytical decisions (EDA phase)

---

## 1. Referenzjahr

**Situation:** Das Anker-Dataset (`isoc_r_dskl_i`) hat ausschließlich 2025-Daten. Der Index wird daher eine Querschnittsanalyse, kein Trendprodukt.

**Entscheidung nötig:** Für alle anderen Datasets (Poverty, Education, Lifelong Learning, Unemployment, AI Adoption) muss ein Referenzjahr festgelegt werden. Fallback-Regel bei fehlenden Werten für das Referenzjahr definieren (z.B. most-recent available ≤ Referenzjahr).

**Status:** [x] entschieden — 2025

**Begründung:** Digital Skills (Anker-Dataset) ist ausschließlich in 2025 verfügbar. Alle anderen Datasets werden auf 2025 gefiltert, um Zeitversatz zu vermeiden. Einzig die Schweiz (CH0) fehlt in Poverty 2025 vs. 2024 — als Nicht-EU-Land für den Index nicht kritisch.

---

## 2. Unit in Digital Skills: `PC_IND` vs. `PC_IND_IU3`

**Situation:** Das Digital-Skills-Dataset enthält zwei konzeptuell verschiedene Nenner:
- `PC_IND` — Anteil aller Individuen (inkl. Nicht-Internet-Nutzer)
- `PC_IND_IU3` — Anteil der Individuen, die das Internet in den letzten 3 Monaten genutzt haben

**Empfehlung:** `PC_IND` für den Gap-Index, weil Nicht-Internet-Nutzer Teil der Lücke sind, nicht Ausnahmen davon. `PC_IND_IU3` wäre geeignet für eine Analyse der Skill-Qualität unter aktiven Nutzern.

**Indikator-Empfehlung:** `I_DSK2_BAB` (basic or above basic) als DESI-Standardindikator, oder `I_DSK2_AB` (above basic only) für einen strengeren Maßstab.

**Status:** [x] entschieden — `I_DSK2_BAB` + `PC_IND`

**Begründung:** Nicht-Internet-Nutzer sind Teil der AI Literacy Gap, nicht außerhalb davon. `PC_IND` zählt sie im Nenner mit. `I_DSK2_BAB` (DESI-Standard) bietet die größte regionale Spreizung (19–85 %) und ist international etabliert.

---

## 3. Poverty: Coverage-Cutoff und Datenqualitäts-Flags

**Situation:** Im Referenzjahr 2025 haben nur zwei Regionen eine Coverage unter 100 %:

| Region | Coverage | Fehlende NUTS-2-Region | Poverty-Wert (berechnet) |
|---|---|---|---|
| FI1 — Manner-Suomi | 75.0 % | FI19 Länsi-Suomi | 16.7 % |
| FRY — Régions Ultrapériphériques | 85.7 % | FRY5 Mayotte | 41.4 % |

**Status:** [x] entschieden

**FI1 — kein Flag, Wert wird unverändert verwendet**
Länsi-Suomi (Westfinnland, Tampere/Turku) ist wirtschaftlich und sozial homogen mit den drei abgedeckten Regionen. Die geschätzte Abweichung vom wahren Wert beträgt < 0.5 Prozentpunkte. Der berechnete Wert ist eine valide Näherung.

**FRY — Flag erforderlich, Wert wird mit Caveat verwendet**
Die fehlende Region Mayotte ist das ärmste französische Territorium (bekannt aus INSEE-Berichten, jedoch ohne verifizierte EU-SILC-konforme Rate). Die abgedeckten Regionen liegen bei 31–55 % — Mayotte liegt strukturell deutlich darüber. Der berechnete Wert von 41.4 % unterschätzt die wahre NUTS-1-Armutsrate wahrscheinlich signifikant. Externe Daten werden nicht ergänzt, da eine nicht-EU-SILC-Quelle die methodische Konsistenz des Index brechen würde.

**→ Hinweis für UI / Kollege Kartendarstellung:**
FRY muss in der Karte visuell markiert werden (z.B. Schraffur, Sternchen, Tooltip). Empfohlener Hinweistext: *"Daten basieren auf 4 von 5 Subregionen. Mayotte fehlt — tatsächliche Armutsrate wahrscheinlich signifikant höher (Mayotte ist das ärmste französische Territorium, EU-SILC-konforme Rate nicht verfügbar)."*

---

## 4. AI Adoption: Pflicht-Pillar oder optional?

**Situation:** Kritischer Scope-Konflikt zwischen den Datasets:

| | Regionen |
|---|---|
| Digital Skills (Anker) | 88 NUTS-1 |
| Enterprise AI Adoption | 38 NUTS-1 |
| Überschneidung | 32 NUTS-1 |

AI Adoption als Pflicht-Pillar reduziert den Index von 88 auf 32 Regionen (−64 %).

**Optionen:**
- A) AI Adoption optional → Regionen ohne Daten bekommen NaN für diesen Pillar, bleiben im Index
- B) Zwei Index-Versionen: vollständig (32 Regionen, alle 7 Pillars) + ohne AI-Pillar (88 Regionen, 6 Pillars)
- C) AI Adoption nur als Country-Level-Proxy (verliert Regionalität)

**Status:** [x] entschieden — Pillar wird weggelassen

**Begründung:** Zwei Gründe. Konzeptionell misst Enterprise AI Adoption Unternehmensverhalten, nicht menschliche KI-Literacy — das ist eine andere Analyseebene als die übrigen Pillars. Datenseitig fehlen DE, FR, IT, NL komplett, weil diese Länder nicht auf NUTS-1 melden — nicht weil ihre Adoptionsrate null ist. Ein NaN für diese Regionen würde im Index fälschlicherweise "kein Signal" bedeuten, obwohl die Lücke methodisch ist, nicht inhaltlich. Der Index bleibt mit 6 Pillars konzeptionell vollständig. Der Demand-Side-Blickwinkel (Exposure-Druck durch Unternehmens-KI) wird als bewusster Scope-Ausschluss dokumentiert.

---

## 5. Education: Indikator und Altersgruppe

**Status:** [x] entschieden — `ED0-2` + `Y25-64`

**Begründung:** ED0-2 (Anteil der Bevölkerung ohne weiterführende Qualifikation — kein Abschluss bis Realschule) ist der direkteste Risikoindikator für strukturelle Vulnerabilität im digitalen Wandel. Wer nie über die Pflichtschule hinausgegangen ist, hat weniger Übung im Weiterlernen und Umschulen. Der Selektionseffekt stützt dies: lernbereite Realschulabsolventen setzen ihre Ausbildung in der Regel fort und landen in ED3-8. Y25-64 wurde gewählt weil KI-Disruption alle Erwerbstätigen betrifft — nicht nur Junge. Es ist die einzige Altersgruppe die das vollständige Bild der Arbeitsbevölkerung zeigt (EU-Standard). Y20-24 ist verzerrt (viele noch in Ausbildung), Y25-34 und Y30-34 sind zu enge Ausschnitte.

**Richtung:** höherer Wert = mehr Menschen ohne weiterführende Qualifikation = größere AI Literacy Gap → muss beim Index-Bau invertiert werden.

**Alternativen geprüft:** ED3-8 wäre dasselbe Signal mit umgekehrter Richtung (kein inhaltlicher Unterschied). ED5-8 (nur Tertiär) wäre zu streng und würde Berufsausbildung ignorieren.

**Datenlimitation:** Eurostat stellt für diesen Indikator keine Altersgruppe über Y25-64 bereit. Menschen über 65 sind nicht abgedeckt — das ist eine Einschränkung der Quelldaten, keine analytische Wahl. Digital Skills und Poverty enthalten gar keine Altersaufschlüsselung (Gesamtbevölkerung).

---

## 6. Lifelong Learning: Altersgruppe

**Status:** [x] entschieden — `Y25-64` + `PC` + `sex=T`

**Begründung:** Zwei Altersgruppen verfügbar: Y18-64 und Y25-64 — beide mit identischer Coverage (109/123 NUTS-1 in 2025) und r = 0.986 (Pearson) / 0.980 (Spearman). Y25-64 gewählt aus zwei Gründen: (1) Konsistenz mit Education-Pillar (ebenfalls Y25-64, gleiche Zielgruppe); (2) konzeptuelle Reinheit — 18–24-Jährige sind teils noch in Erstausbildung, was die Abgrenzung zu adult learning unschärfer macht.

**Richtung:** höherer Wert = mehr Weiterbildung = geringeres Risiko → muss beim Index-Bau invertiert werden.

**Fehlende Regionen 2025:** 12 UK-Regionen (systematische Lücke post-Brexit), IS0, ME0.

**Datenlimitation — 4-Wochen-Fenster:** Der LFS-Indikator misst, ob jemand in den 4 Wochen vor dem Interview an Bildung oder Training teilgenommen hat. Das ist ein Snapshot — wer intensiv, aber selten lernt (z.B. einmal jährlich eine Woche Blockseminar), wird nicht erfasst, sofern der Befragungszeitpunkt nicht zufällig in dieses Fenster fällt. Ein 12-Monats-Fenster wäre methodisch stärker. Das Adult Education Survey (AES) verwendet dieses längere Fenster, ist aber nur auf **Länderebene** verfügbar (kein NUTS-1) und erscheint nur ca. alle 5 Jahre (2007, 2011, 2016, 2022) — damit für diesen Index nicht nutzbar. `trng_lfse_04` ist die einzige verfügbare regionale Jahreszeitreihe. Der EU-DESI-Standardstatus sichert internationale Vergleichbarkeit. Diese Einschränkung muss in der Interpretation des Index explizit ausgewiesen werden.

---

## 7. Labour Market Vulnerability: Datensatz und Indikator

**Status:** [x] entschieden — `lfst_r_lfu3rt` + `ED0-2` + `Y15-74` + `sex=T`

**Datensatz-Wechsel:** Ursprünglich geplant war `lfst_r_lfu3pers` (Arbeitslose in Tausend Personen). Dieser wurde verworfen, weil absolute Zahlen Regionen unterschiedlicher Größe nicht vergleichbar machen. Ersetzt durch `lfst_r_lfu3rt` (Arbeitslosenrate in %) — gleiches Erhebungsdesign, richtiger Nenner. ~~Datensatz direkt in `02_EDA.ipynb` nachgeladen~~ → moved to `01_load_data.ipynb` (see Section 10).

**Indikator:** Arbeitslosenrate unter Niedrigqualifizierten (ED0-2, Y15-74) — misst, ob eine Region ihre am wenigsten qualifizierte Bevölkerung strukturell vom Arbeitsmarkt ausschließt. Ergänzt Education (Qualifikationsstruktur) und Poverty (Ergebnis) um die Transmissionsebene: wo trifft niedrige Qualifikation auf aktuelle Erwerbslosigkeit?

**Altersgruppe Y15-74:** Beste Coverage (99/109 NUTS-1 in 2025), niedrigste u-Flag-Rate. Engere Altersgruppen haben u-Flag-Raten über 40 %.

**Fehlende Regionen (10):** DE5, DE8, DEC, FI2, FRM, PL2/PL7/PL8/PL9, PT3 — alle u-flagged (kleine Stichprobe). UK komplett absent (post-Brexit).

**Flag-Caveats:** 20 Regionen mit `d`-Flag (Spanien + FRY, Definition abweichend), 12 mit `u`-Flag aber Wert vorhanden — werden mit Hinweis verwendet.

---

## 8. Index-Scope: EU27

**Status:** [x] entschieden — EU27, alle 27 Mitgliedsstaaten

**Begründung:** Gemeinsamer Rechts- und Politikrahmen (EU AI Act, Digital Decade, Kohäsionspolitik) ermöglicht handlungsfähige Empfehlungen. Nicht-EU-Länder (TR, NO, CH, RS, ME, MK, AL, IS, UK) werden ausgeschlossen.

**Datentechnische Lösungen:**
- 13 EU-Länder mit nur einer NUTS-1 Region fehlten im Anker (Digital Skills), weil sie mit 2-stelligem Ländercode (z.B. `DK`) statt 3-stelligem NUTS-1-Code (`DK0`) gemeldet werden. Mapping angewendet. FI→FI1 (Manner-Suomi, 99.5 % der Bevölkerung; FI2/Åland ausgeschlossen).
- 5 EU-Länder (CY, EE, LU, LV, MT) fehlen in Poverty-Dataset `tgs00107`. Ersetzt durch `ilc_peps01n` (nationale AROPE-Rate, selbe EU-SILC-Methodik, selbes Referenzjahr). Da diese Länder je eine einzige NUTS-1 Region haben gilt: nationaler Wert = NUTS-1 Wert.

**Ausgeschlossene Regionen trotz EU-Mitgliedschaft:** 7 Regionen ohne P5 (Unemployment) wegen zu kleiner LFS-Stichprobe: DE8, FRM, PL2, PL7, PL8, PL9, PT3. Alle gehören zu Ländern die durch andere NUTS-1 Regionen weiterhin vertreten sind. Alternative geprüft: TOTAL-Arbeitslosenrate (alle Bildungsniveaus) wäre für alle 7 verfügbar — abgelehnt, weil ED0-2-Raten strukturell immer höher als TOTAL sind und der Fallback diese Regionen systematisch als "weniger vulnerabel" darstellen würde. NaN ist methodisch ehrlicher.

---

## Bonus: Unemployment-Flags (erledigt)

**Status:** [x] geprüft in EDA — `b`-Flags irrelevant für Einzeljahresanalyse. `u`-Flags konzentrieren sich auf schmale Altersgruppen (Y25-34, Y55-64 mit >40 % u-Rate) → Y15-74 als einzig tragfähige Altersgruppe gewählt. Außerdem: `lfst_r_lfu3pers` durch `lfst_r_lfu3rt` ersetzt (Raten statt Absolutzahlen).

---

## 9. Pipeline Audit — Code Review Findings (2026-05-29)

A full static and active validation of `01_load_data.ipynb` and `02_EDA.ipynb` was conducted. Both notebooks were executed end-to-end; all processed CSVs were validated against expected shapes, value ranges, and formula correctness.

### No critical analytical errors found

The population-weighting formula, year joins, regex flag extraction, and dimension splitting were all verified correct. Spot-checks for DE1 and FR1 confirmed the weighted poverty rate formula (`sum(value_i × pop_i) / sum(pop_i)`) produces accurate results.

### Findings (non-blocking, addressed in Section 10)

| # | Finding | Severity | Impact |
|---|---|---|---|
| 1 | `lfst_r_lfu3rt` and `demo_r_pjanaggr3` downloaded in `02_EDA.ipynb`, not `01_load_data.ipynb` | Medium | Reproducibility gap — 01 should be the single download source |
| 2 | No `downloaded_at` timestamp in data catalog | Medium | Data version untrackable after Eurostat revisions |
| 3 | Eurostat `u`/`d` flags lost after merge — not carried into feature table | Medium | Index construction has no visibility into flagged values |
| 4 | Excluded regions (7 with NaN in P5) documented only in DECISION.md, not as a machine-readable artifact | Low | Cannot be consumed programmatically by downstream steps |
| 5 | `pillar_feature_table.csv` not registered in `project_data_catalog.csv` | Low | Catalog incomplete as a project registry |
| 6 | `nuts1_lookup` not loaded in `02_EDA.ipynb` setup cell | Bug (fixed) | `NameError` on clean notebook run |
| 7 | `re`, `json`, `io`, `urllib.request` not imported in `02_EDA.ipynb` setup cell | Bug (fixed) | `NameError` on clean notebook run |
| 8 | 14 non-EU NUTS-1 regions (TR, RS) in `digital_skills_nuts1_labeled_filtered.csv` | Informational | Expected (GISCO includes candidate countries); removed by EU27 filter in Step 3.7 |

### Pipeline quality assessment

Overall rating: **B+ / good to very good.** Methodological decision quality is above average. Population weighting is correct. Data gap handling is honest. The pipeline is analytically sound; the findings above are architectural gaps, not errors in the numbers.

---

## 10. Pipeline Improvements Applied (2026-05-29)

All medium-severity findings from Section 9 were addressed. Changes are minimal and additive — no existing notebook cells were modified except to replace live API downloads with `pd.read_csv()` calls.

### Changes to `01_load_data.ipynb`

Three cells added at the end of the notebook, clearly marked with a dated header. The original author's cells are untouched.

- **Download `lfst_r_lfu3rt`** (unemployment rates by education level) using the existing `download_eurostat_tsv` + `reshape_eurostat_tsv` helper functions. Saved as `unemployment_rate_education_region_tidy.csv`.
- **Download `demo_r_pjanaggr3`** (population by broad age group) using the same helpers. Saved as `demographics_age_structure_tidy.csv`.
- **Catalog update**: both datasets registered in `project_data_catalog.csv`; `downloaded_at` timestamp added to all catalog entries.

### Changes to `02_EDA.ipynb`

- **Step 3.5** (cell `dd411e2d`): replaced `urllib` download of `lfst_r_lfu3rt` with `pd.read_csv(...)`. Flag column re-extracted from `value_raw` (format: `"15.3 u"` → `flag="u"`).
- **Step 3.6** (cell `484ae897`): replaced `urllib` download of `demo_r_pjanaggr3` with `pd.read_csv(...)`.
- **Step 4** (cell `3865ea4f`): feature table now includes `unemployment_flag` column (8 columns total). `excluded_regions.csv` saved as a machine-readable artifact. `pillar_feature_table.csv` registered in catalog.

### New files produced

| File | Location | Purpose |
|---|---|---|
| `unemployment_rate_education_region_tidy.csv` | `data/processed/` | Now produced by `01_load_data.ipynb` |
| `demographics_age_structure_tidy.csv` | `data/processed/` | Now produced by `01_load_data.ipynb` |
| `excluded_regions.csv` | `data/processed/` | Machine-readable record of the 7 regions excluded from P5 |

### Validation test scripts added

Two pipeline validation scripts were added to `tests/`:

- `tests/validate_01_load_data.py` — 34 checks covering file existence, NUTS lookups, digital skills coverage, population weighting formula (spot-checks DE1/FR1), poverty coverage, and catalog completeness.
- `tests/validate_02_eda.py` — 33 checks covering feature table structure, NaN patterns, value ranges, all 6 pillar coverages, EU27 scope, single-NUTS1 country mappings, excluded regions, and catalog registration.

Both exit with code 0 on success, code 1 on any failure. Run from project root:
```bash
python tests/validate_01_load_data.py
python tests/validate_02_eda.py
```

---

## 11. Index Construction — Data Inspection and Normalisation Decisions (2026-06-01)

Before building the index in `03_index_construction.ipynb`, a structured data inspection was conducted on `pillar_feature_table.csv` (87 EU27 NUTS-1 regions × 6 pillars). The following findings and decisions were made.

### 11.1 Missing Values

Only P5 (Unemployment) has missing values: 7 regions (8%) — DE8, FRM, PL2, PL7, PL8, PL9, PT3. These were already documented and accepted in Section 8. All other pillars are complete.

### 11.2 Distribution findings

| Pillar | Min | Q25 | Median | Q75 | Max | Std | Finding |
|--------|-----|-----|--------|-----|-----|-----|---------|
| P1 Digital Skills | 27.1 | 51.5 | 62.0 | 67.3 | 85.2 | 12.3 | Healthy spread |
| P2 Poverty | 10.8 | 16.9 | 19.9 | 24.2 | 41.4 | 6.5 | Healthy spread |
| P3 Education | 3.4 | 10.4 | 15.0 | 20.9 | 56.7 | 10.9 | **Outlier: PT2 = 56.7 % vs. median 15 %** |
| P4 Lifelong Learning | 3.3 | 9.0 | 12.8 | 16.8 | 40.3 | 7.3 | Healthy spread |
| P5 Unemployment | 4.1 | 9.4 | 12.6 | 16.1 | 38.3 | 6.2 | Healthy spread |
| P6 Demographics | 13.0 | 20.0 | 21.7 | 23.9 | 28.4 | 3.0 | **Very low variance — IQR only 3.9 pp** |

**P6 note:** 75 % of regions fall within a 4 percentage-point band (20–24 %). P6 provides limited separation between regions in both the index and clustering. It is retained — the demographic signal is real — but its discriminating power is low.

### 11.3 Correlation matrix (Pearson)

| | P1 | P2 | P3 | P4 | P5 | P6 |
|--|--|--|--|--|--|--|
| P1 | 1.00 | -0.39 | -0.05 | **0.61** | -0.11 | -0.15 |
| P2 | | 1.00 | 0.47 | -0.29 | 0.34 | -0.06 |
| P3 | | | 1.00 | -0.04 | -0.14 | -0.05 |
| P4 | | | | 1.00 | 0.27 | -0.22 |
| P5 | | | | | 1.00 | -0.19 |
| P6 | | | | | | 1.00 |

**P1 ↔ P4: r = 0.61 (moderate positive).** Regions with strong digital skills tend to also have higher participation in continuing education. Both pillars are retained: they measure conceptually distinct things (current competence vs. active learning behaviour), and r = 0.61 is not strong enough to justify removal. No multicollinearity concern for the composite index.

All other pillar pairs: |r| < 0.5. The pillars are largely measuring independent dimensions.

### 11.4 PT2 outlier — analysis and decision

**Situation:** PT2 (Região Autónoma da Madeira e Açores) has `low_education_pct` = 56.7 %, against a dataset median of 15.0 % and a next-highest value of 43.3 % (ITG). This is the maximum in the entire dataset on P3 and pulls the min-max scale significantly.

**Is this a data error?** No. PT2's figure reflects the structural reality of historically isolated Atlantic island regions with limited access to post-compulsory education and an economy dominated by tourism and agriculture — sectors that historically required no formal qualifications. P5 confirms this: PT2 has an unemployment rate of only 5.5 % (rank 75/80, nearly the best), meaning the low-education population is nevertheless employed. The data is correct and the outlier is meaningful.

**Concrete impact on the index:** A simulation was run comparing index scores with and without PT2 as the P3 anchor:
- Maximum score shift for any region: **3.0 index points**
- Average score shift: **0.77 index points**
- Total index span: 50.4 points
- No region changes risk class; top rankings are unaffected (ITG stays rank 1 with or without PT2)

**Decision: PT2 is retained in the dataset without modification.**

**Alternatives considered and rejected:**
- *Remove PT2 entirely:* Methodologically dishonest — PT2 is a real EU region with a genuine and severe AI literacy gap risk. Removing it because it is statistically inconvenient would undermine the purpose of the index.
- *Winsorizing (cap P3 at 95th percentile):* Would reduce PT2's P3 value to ~37 %. Given that the concrete impact on scores is only 0–3 index points, this added complexity is not justified. Retained as an option for the sensitivity analysis in Step 5.

### 11.5 Normalisation method — decision for index and clustering

**Context:** Three normalisation methods were evaluated: Min-Max, Z-Score, and Robust Scaling (median/IQR).

**Key finding on Robust Scaling:** Contrary to intuition, Robust Scaling makes the PT2 outlier *more* extreme, not less. The IQR for P3 is only 10.5 pp (the middle 50 % of regions are tightly clustered). PT2 at 56.7 % is therefore 3.97 IQR-units from the median — compared to 3.60 standard deviations under Z-Score, and simply 1.000 (the maximum) under Min-Max. Min-Max is actually the *least* extreme representation of PT2.

Additionally, Robust Scaling without a secondary rescaling produces unequal feature spreads across pillars (std: 0.76–1.03), which is problematic for K-Means clustering which relies on comparable Euclidean distances. Applying a secondary min-max after robust scaling produces results mathematically identical to pure min-max (two consecutive linear transformations preserve relative distances).

**Decision: Min-Max normalisation [0, 1] for both the composite index and the clustering step.**

| Method | Index | Clustering | Verdict |
|--------|-------|------------|---------|
| Min-Max | ✓ Standard, interpretable, [0,1] | ✓ Consistent with index, PT2 effect negligible | **Selected** |
| Z-Score | Unbounded, harder to interpret | Viable but inconsistent with index | Rejected |
| Robust Scaling | Identical to Min-Max after rescaling | Makes PT2 *more* extreme; unequal feature spreads | Rejected |

---

## 12. Index Construction — Three Weighting Variants (2026-06-01)

### 12.1 Overview

The composite index is built in three weighting variants to validate robustness and support a transparent final selection. All three variants use the same normalised pillar scores (Min-Max, direction-aligned) from Steps 2–3 of `03_index_construction.ipynb`. They differ only in how pillar weights are assigned.

| Variant | Step | Weights | Logic |
|---------|------|---------|-------|
| Baseline | Step 4 | Equal (1/6 per pillar) | No prior assumptions — OECD standard |
| PCA | Step 6 | Data-driven (PC1 loadings) | Algorithm derives weights from variance structure |
| Expert | Step 5 | Domain-knowledge driven | Human judgment about relative pillar importance |

Note: The logical ordering is Baseline → PCA → Expert (objective → data-driven → normative). Step numbering in the notebook follows the order in which they were implemented (Baseline → Expert → PCA), which differs from the conceptual ordering above.

---

### 12.2 Variant 1 — Baseline: Equal weights

All 6 pillars receive equal weight (1/6 ≈ 16.7 %). Index score = simple mean of the 6 normalised pillar scores.

**Role:** Reference point. Not the final index — used to measure how much the other two variants deviate from a neutral starting point. Consistent with DESI, HDI, and standard OECD composite index methodology.

---

### 12.3 Variant 2 — Expert weights

**Weights:** P1 = 35%, P3 = 22%, P2/P4/P5 = 13% each, P6 = 4%

**Rationale per pillar:**
- **P1 (35%):** The only pillar that directly measures digital competence — the conceptual core of the index. All other pillars are structural proxies. Upweighted to reflect its primacy as the anchor dataset.
- **P3 (22%):** The strongest structural predictor of AI literacy vulnerability. Low educational attainment is the root cause that makes gaps persistent across generations.
- **P2 / P4 / P5 (13% each):** Important contextual dimensions with no clear priority ordering between them.
- **P6 (4%):** Retained to keep the demographic dimension in scope, but downweighted to reflect its low discriminating power (IQR = 3.9 pp, std = 3.0). Near-exclusion is intentional and documented.

**Known limitation:** The exact percentage values (35%, 22% etc.) are informed estimates. The precise numbers are inherently subjective — what is defensible is the direction and relative magnitude of the weighting. The robustness comparison in Step 7 tests whether these specific values produce materially different results from the other variants.

---

### 12.4 Variant 3 — PCA weights

**Method:** Principal Component Analysis (PCA) fitted on the 6 normalised pillar scores for the 80 complete-case regions (StandardScaler applied before PCA). Weights = absolute PC1 loadings, normalised to sum to 1.

**What PCA does:** Finds the linear combination of pillars that explains the most variance across regions (PC1 = the "main risk axis"). Pillars that co-vary most strongly with this axis receive higher weights.

**Results:**

| Pillar | PCA weight | PC1 loading | Expert weight |
|--------|-----------|-------------|---------------|
| P1 Digital Skills | 27.3% | +0.570 | 35% |
| P2 Poverty | 25.9% | +0.540 | 13% |
| P4 Lifelong Learning | 25.0% | +0.521 | 13% |
| P3 Education | 15.3% | +0.319 | 22% |
| P6 Demographics | 4.6% | +0.097 | 4% |
| P5 Unemployment | 1.8% | +0.036 | 13% |

**Key finding — PC1 explains only 34.5% of total variance.** This is a meaningful result: it confirms that the 6 pillars measure genuinely different dimensions of risk. There is no single dominant "risk axis". If PC1 explained 80%+, it would indicate pillar redundancy. 34.5% means each pillar contributes unique information — which validates the composite index design. The limitation is that PCA weights derived from PC1 alone ignore 65.5% of the variance when determining relative pillar importance.

**Notable divergences from Expert weights:**
- **P5 (Unemployment): 1.8% vs. 13%** — the near-zero loading means unemployment does not co-vary with the main risk signal. Structurally plausible: low-educated workers are employed in Southern Europe (tourism) and unemployed in Eastern Europe — the signal is region-type-specific, not a general risk factor.
- **P2 (Poverty): 25.9% vs. 13%** — the data shows poverty and digital skills vary strongly together across regions. The PCA treats poverty as an equally primary indicator as digital skills.
- **P4 (Lifelong Learning): 25.0% vs. 13%** — elevated due to its correlation with P1 (r = 0.61).

**All PC1 loadings are positive** — confirming that after direction alignment (Step 3), PC1 points in the high-risk direction for all pillars. No sign-flip correction needed.

---

### 12.5 Expert weights — removed from scope

The expert weighting variant (P1=35%, P3=22%, P2/P4/P5=13%, P6=4%) was removed after further reflection. The specific percentage values, while documented and reasoned, are ultimately informed estimates without a hard empirical basis. The exact numbers (why 35% and not 30%?) cannot be defended with the same rigour as a data-driven approach. Expert weights were removed from the notebook to keep the analysis clean and defensible. The rationale is documented here for transparency.

---

### 12.6 PC1-only vs. All-PC — decision and rationale

Two PCA weighting variants were computed and compared:

**PC1-only weights** use the absolute loadings of the first principal component, normalised to sum to 1. Result: P1=27.3%, P2=25.9%, P4=25.0%, P3=15.3%, P6=4.6%, P5=1.8%. P5 is near-excluded (1.8%) not because it is unimportant, but because its variance pattern is orthogonal to PC1 — it dominates PC2 instead. Using PC1 only ignores 65.5% of the total variance structure.

**All-PC weights** sum absolute loadings across all 6 principal components, each weighted by its explained variance share:

$$w_j = \frac{\sum_{k=1}^{6} \lambda_k \cdot |loading_{jk}|}{\sum_j \sum_{k=1}^{6} \lambda_k \cdot |loading_{jk}|}$$

Result: P1=16.6%, P2=17.6%, P3=17.2%, P4=18.4%, P5=15.5%, P6=14.8%. All pillars land between 14.8% and 18.4%.

**Key finding — convergence to equal weights:** The All-PC approach produces weights nearly identical to the equal-weights baseline (16.7% each). This convergence is a substantive result: every pillar dominates at least one principal component, confirming that each dimension contributes unique information to the variance structure. No pillar is redundant. The equal-weights baseline is therefore not merely a convention — it is empirically validated by the All-PC approach.

**Decision: All-PC PCA weights are used for the final index.**

Rationale: All-PC is methodologically superior to both PC1-only (which ignores 65.5% of variance and near-excludes P5) and equal weights (which is a valid but assumption-based approach). Although All-PC results are numerically close to equal weights, they are grounded in the data rather than in the assumption of equal importance. The equal-weights baseline is retained in the notebook as a reference comparison.

---

### 12.7 Final index

**`pca_all_score` — variance-weighted All-PC PCA index — is the final AI Literacy Gap Index.**

The equal-weights `index_score` is retained as baseline reference. Both are saved in `data/processed/ai_literacy_gap_index.csv`.

---

## 13. Clustering — Risk Profile Typology (2026-06-02)

Clustering is performed in `04_clustering.ipynb`. The goal is to identify **what kind** of AI literacy gap risk a region faces, not how much — that is answered by the index. K-Means is an unsupervised learning method: no target labels are provided; the algorithm finds structure in the pillar profiles autonomously.

**Input:** `data/processed/ai_literacy_gap_index.csv` — P1_norm–P6_norm columns (Min-Max normalised in `03_index_construction.ipynb`, no further normalisation applied in this notebook).

**Output:** `data/processed/ai_literacy_gap_index_clustered.csv` — adds `cluster_label` and `cluster_id` columns.

---

### 13.1 NaN handling — P5 country-level mean imputation

**Decision:** P5_norm missing values (7 regions: DE8, FRM, PL2, PL7, PL8, PL9, PT3) are imputed with the mean P5_norm of other available NUTS-1 regions in the same country, not the EU27 mean.

**Rationale:** Labour market structures are country-specific. The country peer is a much closer proxy than the EU27 average. The difference is largest for PT3 (Madeira): global mean = 0.271 vs. Portuguese mean = 0.060 — a gap of 0.21 normalised units. Portugal's low unemployment among the low-educated (tourism and agricultural employment) should be reflected in the imputed value for Madeira. Imputation is applied only to the clustering step; original NaN values are preserved in the output file.

| Region | Imputed value (country mean) | Global mean | Difference |
|---|---|---|---|
| PT3 | 0.060 | 0.271 | −0.211 |
| DE8 | 0.187 | 0.271 | −0.084 |
| FRM | 0.310 | 0.271 | +0.039 |
| PL2 / PL7 / PL8 / PL9 | 0.229 | 0.271 | −0.042 |

**Alternatives rejected:** Global mean imputation (methodologically weaker, overestimates unemployment for Portugal and Germany); dropping 7 regions (loses all remaining Polish NUTS-1 regions).

---

### 13.2 Optimal cluster count — k=5

**Method:** Elbow (inertia) and Silhouette score tested for k=2–8 using the country-level imputed feature matrix.

| k | Inertia | Silhouette |
|---|---|---|
| 2 | 15.78 | 0.278 |
| 3 | 12.75 | 0.238 |
| 4 | 11.09 | 0.189 |
| **5** | **9.73** | **0.200** |
| 6 | 8.74 | 0.178 |
| 7 | 8.02 | 0.218 |
| 8 | 7.20 | 0.222 |

**Decision:** k = 5.

**Rationale:** The decisive argument is not the marginal silhouette improvement (0.189 → 0.200) but the analytical quality of the split. k=4 merges two structurally different high-risk types into one cluster. In k=5 these separate into two distinct pillar fingerprints: one characterised by elevated P3+P2 (education-poverty trap) alongside high P4, and another by elevated P1+P6 (digital skills gap and aging demographics) alongside very high P4. These have different policy implications and should not be conflated. The exploratory side-by-side heatmap (k=4 vs. k=5) in the notebook makes this split visually apparent.

**Alternatives rejected:** k=2 (highest silhouette at 0.278 but too coarse); k=4 (conflates the two highest-risk profiles); k=6+ (silhouette does not improve meaningfully, clusters become small and unstable).

---

### 13.3 K-Means configuration

`KMeans(n_clusters=5, random_state=42, n_init=20)` — 20 random initialisations, best result kept. Deterministic due to fixed random seed.

Cluster IDs (0–4) are assigned first; semantic names are derived in a subsequent step after inspecting the pillar profiles, so that names follow from evidence rather than being assumed upfront.

---

### 13.4 Cluster naming — derived from pillar profiles

Names were assigned after inspecting the mean normalised pillar score per cluster (profile table + heatmap in Step 5 of the notebook). Names describe the **structural pattern** of the cluster, not the geographic location of its members — two regions in different parts of Europe with the same pillar fingerprint fall into the same cluster.

| Cluster ID | Dominant pillars | Name assigned |
|---|---|---|
| 0 | P3 (0.74), P4 (0.77), P2 (0.69) | Education & Poverty Trap |
| 3 | P4 (0.87), P1 (0.71), P6 (0.66) | Digital & Retraining Deficit |
| 2 | P4 (0.76), P6 (0.64) elevated; P2, P3, P5 low | Ageing Workforce & Training Gap |
| 1 | P5 (0.66) highest; P1 (0.31) lowest of all clusters | Selective Labour Exclusion |
| 4 | All pillars low | Low Structural Risk |

---

### 13.5 Cluster profiles and interpretations

| Cluster | n | Avg. risk score | Key finding |
|---|---|---|---|
| Education & Poverty Trap | 8 | 0.612 | Poverty and low educational attainment reinforce each other. Low retraining participation (P4) is a consequence, not an independent driver. The AI literacy gap is broad and structurally embedded. |
| Digital & Retraining Deficit | 16 | 0.559 | Core problem is absent digital skills combined with near-zero retraining participation and an aging population. Poverty and low education are not elevated — the risk is specifically about digital competence and failure to update skills over time. |
| Ageing Workforce & Training Gap | 40 | 0.416 | Largest cluster. P4 and P6 are clearly elevated but poverty and low education are not. These regions have not fallen into structural deprivation, but their aging workforce participates less in retraining. Risk is gradual and diffuse rather than acute. |
| Selective Labour Exclusion | 7 | 0.362 | Most counter-intuitive cluster. Low poverty (P2=0.32), lowest low-education share of all clusters (P3=0.15), good digital skills (P1=0.31), and lowest lifelong learning gap (P4=0.32). Yet unemployment among the low-educated (P5=0.66) is the highest of all clusters. A well-functioning society with a concentrated blind spot: the few without qualifications fall through every net. Policy implication: not infrastructure rebuilding but targeted outreach to a small, hard-to-reach group. |
| Low Structural Risk | 16 | 0.321 | Lowest risk across all dimensions. Faces the same long-term challenges as the rest of Europe but from a structurally stronger position. |

**Note on "Selective Labour Exclusion":** This cluster is analytically important precisely because it contradicts the expected pattern. High unemployment among the low-educated coexists with strong overall digital performance, low poverty, and active retraining systems. The risk is not systemic — it is selective and concentrated. This requires a fundamentally different policy response than the other four clusters.
