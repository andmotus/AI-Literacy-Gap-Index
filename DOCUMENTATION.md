# DOCUMENTATION.md — Decisions, Findings, and Change Log

This file serves as the single source of truth for all analytical decisions, code review findings, and pipeline changes made throughout the project.

---

## Original analytical decisions (EDA phase)

---

## 1. Reference Year

**Situation:** The anchor dataset (`isoc_r_dskl_i`) has data for 2025 only. The index is therefore a cross-sectional analysis, not a trend product.

**Decision needed:** A reference year must be defined for all other datasets (Poverty, Education, Lifelong Learning, Unemployment, AI Adoption). A fallback rule must be defined for missing values in the reference year (e.g. most-recent available ≤ reference year).

**Status:** [x] decided — 2025

**Rationale:** Digital Skills (anchor dataset) is available for 2025 only. All other datasets are filtered to 2025 to avoid temporal misalignment. The only gap is Switzerland (CH0), which is missing from Poverty 2025 vs. 2024 — not critical for the index as a non-EU country.

---

## 2. Unit in Digital Skills: `PC_IND` vs. `PC_IND_IU3`

**Situation:** The Digital Skills dataset contains two conceptually different denominators:
- `PC_IND` — share of all individuals (including non-internet users)
- `PC_IND_IU3` — share of individuals who used the internet in the last 3 months

**Recommendation:** `PC_IND` for the gap index, because non-internet users are part of the gap, not exceptions to it. `PC_IND_IU3` would be suitable for an analysis of skill quality among active users.

**Indicator recommendation:** `I_DSK2_BAB` (basic or above basic) as the DESI standard indicator, or `I_DSK2_AB` (above basic only) for a stricter benchmark.

**Status:** [x] decided — `I_DSK2_BAB` + `PC_IND`

**Rationale:** Non-internet users are part of the AI literacy gap, not outside it. `PC_IND` includes them in the denominator. `I_DSK2_BAB` (DESI standard) offers the widest regional spread (19–85 %) and is internationally established.

---

## 3. Poverty: Coverage Cut-off and Data Quality Flags

**Situation:** In the reference year 2025, only two regions have coverage below 100 %:

| Region | Coverage | Missing NUTS-2 region | Poverty rate (calculated) |
|---|---|---|---|
| FI1 — Manner-Suomi | 75.0 % | FI19 Länsi-Suomi | 16.7 % |
| FRY — Régions Ultrapériphériques | 85.7 % | FRY5 Mayotte | 41.4 % |

**Status:** [x] decided

**FI1 — no flag, value used as-is**
Länsi-Suomi (western Finland, Tampere/Turku) is economically and socially homogeneous with the three covered sub-regions. The estimated deviation from the true value is < 0.5 percentage points. The calculated value is a valid approximation.

**FRY — flag required, value used with caveat**
The missing sub-region Mayotte is the poorest French territory (documented in INSEE reports, but without a verified EU-SILC-compliant rate). The covered sub-regions range from 31–55 % — Mayotte is structurally well above that. The calculated value of 41.4 % likely significantly underestimates the true NUTS-1 poverty rate. No external data will be added, as a non-EU-SILC source would break the methodological consistency of the index.

**→ Note for UI / map visualisation:**
FRY must be visually flagged on the map (e.g. hatching, asterisk, tooltip). Recommended tooltip text: *"Data based on 4 of 5 sub-regions. Mayotte is missing — actual poverty rate likely significantly higher (Mayotte is the poorest French territory; no EU-SILC-compliant rate available)."*

---

## 4. AI Adoption: Mandatory Pillar or Optional?

**Situation:** Critical scope conflict between datasets:

| | Regions |
|---|---|
| Digital Skills (anchor) | 88 NUTS-1 |
| Enterprise AI Adoption | 38 NUTS-1 |
| Overlap | 32 NUTS-1 |

Including AI Adoption as a mandatory pillar reduces the index from 88 to 32 regions (−64 %).

**Options:**
- A) AI Adoption optional → regions without data receive NaN for this pillar but remain in the index
- B) Two index versions: full (32 regions, all 7 pillars) + without AI pillar (88 regions, 6 pillars)
- C) AI Adoption as country-level proxy only (loses regional granularity)

**Status:** [x] decided — pillar dropped

**Rationale:** Two reasons. Conceptually, Enterprise AI Adoption measures business behaviour, not human AI literacy — a different level of analysis from the other pillars. On the data side, DE, FR, IT, and NL are entirely absent because these countries do not report at NUTS-1 level — not because their adoption rate is zero. A NaN for these regions would incorrectly signal "no risk" in the index when the gap is methodological, not substantive. The index remains conceptually complete with 6 pillars. The demand-side perspective (exposure pressure from enterprise AI) is documented as a deliberate scope exclusion.

---

## 5. Education: Indicator and Age Group

**Status:** [x] decided — `ED0-2` + `Y25-64`

**Rationale:** ED0-2 (share of the population without post-compulsory qualifications — no qualification through lower secondary) is the most direct risk indicator for structural vulnerability in the digital transition. Those who never progressed beyond compulsory schooling have had less practice with continuous learning and retraining. The selection effect supports this: school-leavers who are willing to learn typically continue into ED3-8. Y25-64 was chosen because AI disruption affects all working-age adults, not only the young. It is the only age group that provides a complete picture of the working-age population (EU standard). Y20-24 is biased (many still in initial education); Y25-34 and Y30-34 are too narrow a window.

**Direction:** higher value = more people without post-compulsory qualifications = larger AI literacy gap → must be inverted during index construction.

**Alternatives considered:** ED3-8 carries the same signal with the opposite direction (no substantive difference). ED5-8 (tertiary only) would be too strict and would ignore vocational qualifications.

**Data limitation:** Eurostat does not provide an age group above Y25-64 for this indicator. People over 65 are not covered — this is a source data constraint, not an analytical choice. Digital Skills and Poverty contain no age breakdown at all (total population).

---

## 6. Lifelong Learning: Age Group

**Status:** [x] decided — `Y25-64` + `PC` + `sex=T`

**Rationale:** Two age groups are available: Y18-64 and Y25-64 — both with identical coverage (109/123 NUTS-1 in 2025) and r = 0.986 (Pearson) / 0.980 (Spearman). Y25-64 was chosen for two reasons: (1) consistency with the Education pillar (also Y25-64, same target population); (2) conceptual clarity — 18–24 year-olds are partly still in initial education, which blurs the boundary with adult learning.

**Direction:** higher value = more participation in continuing education = lower risk → must be inverted during index construction.

**Missing regions 2025:** 12 UK regions (systematic gap post-Brexit), IS0, ME0.

**Data limitation — 4-week window:** The LFS indicator measures whether a person participated in education or training in the 4 weeks before the interview. This is a snapshot — someone who learns intensively but infrequently (e.g. one week of block seminars per year) will not be captured unless the interview happens to fall within that window. A 12-month window would be methodologically stronger. The Adult Education Survey (AES) uses this longer window but is only available at **country level** (no NUTS-1) and is published approximately every 5 years (2007, 2011, 2016, 2022) — making it unsuitable for this index. `trng_lfse_04` is the only available regional annual time series. Its EU-DESI standard status ensures international comparability. This limitation must be stated explicitly in the interpretation of the index.

---

## 7. Labour Market Vulnerability: Dataset and Indicator

**Status:** [x] decided — `lfst_r_lfu3rt` + `ED0-2` + `Y15-74` + `sex=T`

**Dataset change:** The original plan used `lfst_r_lfu3pers` (unemployed persons in thousands). This was rejected because absolute counts are not comparable across regions of different sizes. Replaced by `lfst_r_lfu3rt` (unemployment rate in %) — same survey design, correct denominator. ~~Dataset loaded directly in `02_EDA.ipynb`~~ → moved to `01_load_data.ipynb` (see Section 10).

**Indicator:** Unemployment rate among the low-qualified (ED0-2, Y15-74) — measures whether a region structurally excludes its least-qualified population from the labour market. Complements Education (qualification structure) and Poverty (outcome) with the transmission layer: where does low qualification meet current unemployment?

**Age group Y15-74:** Best coverage (99/109 NUTS-1 in 2025), lowest `u`-flag rate. Narrower age groups have `u`-flag rates above 40 %.

**Missing regions (10):** DE5, DE8, DEC, FI2, FRM, PL2/PL7/PL8/PL9, PT3 — all `u`-flagged (small sample). UK entirely absent (post-Brexit).

**Flag caveats:** 20 regions with `d`-flag (Spain + FRY, non-standard definition), 12 with `u`-flag but value present — used with a caveat note.

---

## 8. Index Scope: EU27

**Status:** [x] decided — EU27, all 27 member states

**Rationale:** A shared legal and policy framework (EU AI Act, Digital Decade, Cohesion Policy) enables actionable recommendations. Non-EU countries (TR, NO, CH, RS, ME, MK, AL, IS, UK) are excluded.

**Technical data solutions:**
- 13 EU countries with only one NUTS-1 region were missing from the anchor dataset (Digital Skills) because they report using a 2-character country code (e.g. `DK`) rather than the 3-character NUTS-1 code (`DK0`). A mapping was applied. FI→FI1 (Manner-Suomi, 99.5 % of population; FI2/Åland excluded).
- 5 EU countries (CY, EE, LU, LV, MT) are absent from the poverty dataset `tgs00107`. Replaced with `ilc_peps01n` (national AROPE rate, same EU-SILC methodology, same reference year). As these countries each have a single NUTS-1 region, the national value equals the NUTS-1 value.

**Regions excluded despite EU membership:** 7 regions without P5 (Unemployment) due to an LFS sample too small to produce reliable estimates: DE8, FRM, PL2, PL7, PL8, PL9, PT3. All belong to countries that remain represented through other NUTS-1 regions. Alternative considered: the TOTAL unemployment rate (all education levels) would be available for all 7 — rejected because ED0-2 rates are structurally always higher than TOTAL, so the fallback would systematically represent these regions as "less vulnerable". NaN is the methodologically honest choice.

---

## Bonus: Unemployment Flags (resolved)

**Status:** [x] reviewed in EDA — `b`-flags are irrelevant for a single-year analysis. `u`-flags are concentrated in narrow age groups (Y25-34, Y55-64 with > 40 % `u`-rate) → Y15-74 selected as the only viable age group. Additionally: `lfst_r_lfu3pers` replaced by `lfst_r_lfu3rt` (rates instead of absolute counts).

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
