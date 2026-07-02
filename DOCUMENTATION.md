# AI Literacy Gap Index

## A Regional Risk Index for Inequality in the Age of Artificial Intelligence

 **SDG Data Science Project | Contributing to:** 

- **SDG 10** (Reduced Inequalities)
- **SDG 4** (Quality Education)
- **SDG 16** (Peace, Justice and Strong Institutions)

Reference year: **2025** · Geographic scope: **87 NUTS-1 regions across the EU-27** · Data source: **Eurostat** (official open data)

[https://github.com/andmotus/AI-Literacy-Gap-Index](https://github.com/andmotus/AI-Literacy-Gap-Index)

---

## Executive Summary

Artificial intelligence is being adopted across Europe faster than the population’s ability to understand, question, and use it. Where that gap between *exposure to AI* and *the literacy to engage with it critically* opens widest, it does not fall evenly: it falls on the regions and populations that are already disadvantaged, the low-educated, the income-poor, the long-term unemployed, the ageing workforce. 

***If left unaddressed, AI does amplify existing inequalities further.***

This project builds the **AI Literacy Gap Index** — a regional, proxy-based composite index that identifies *where in Europe AI literacy gaps are most likely to reinforce existing inequalities*. It combines seven candidate dimensions of official Eurostat data — finalised as **six pillars** — across 87 NUTS-1 regions of the EU-27 for 2025.

The index is deliberately not a direct measurement of AI literacy (no such regional dataset exists in 2025). It is a **structural risk index**: it measures the conditions under which an AI literacy gap becomes a driver of inequality.

**Headline findings:**

- **Risk is geographically concentrated and structurally patterned.** The highest-risk regions are the islands and the south of Italy (ITG *Isole* = 0.731, ITF *Sud* = 0.700), north-eastern Bulgaria (BG3), Romania (RO2) and the French overseas regions (FRY). The lowest-risk regions are the Netherlands, Denmark and Ireland (NL3 *West-Nederland* = 0.219).
The index spans a range of **0.51 on a 0–1 scale.** This wide spread, confirms that the AI literacy gap is a genuine cohesion problem, not statistical noise.
- **There is no single “risk axis”.** Principal Component Analysis shows the first component explains only **34.5 %** of total variance, what proofs that the six pillars measure *different risk-*dimensions. **A region can be at high risk for several structurally distinct reasons.**
- **Five risk types exist, not one.** Unsupervised clustering (K-Means, k = 5) reveals five qualitatively different “risk fingerprints”, from a deep *High Poverty & Low Education* to a counter-intuitive *Low-Skill Unemployment* profile. **Each type requires a different policy response** — a one-size-fits-all AI-skills programme would fail most of Europe.

The final deliverable is an **interactive dashboard** including a **map**, designed so that a policymaker can locate their region of interest, see which of the five risk profiles it belongs to, and conclude the specific intervention it implies.

---

## Table of Contents

1. [Introduction and Problem Definition](about:blank#1-introduction-and-problem-definition)
2. [Research Question and Hypotheses](about:blank#2-research-question-and-hypotheses)
3. [Data Collection and Preprocessing](about:blank#3-data-collection-and-preprocessing)
4. [Data Quality and Reliability](about:blank#4-data-quality-and-reliability)
5. [Exploratory Data Analysis](about:blank#5-exploratory-data-analysis)
6. [Model Building and Evaluation](about:blank#6-model-building-and-evaluation)
7. [Interpretation and Insight Generation](about:blank#7-interpretation-and-insight-generation)
8. [Actionable Recommendations](about:blank#8-actionable-recommendations)
9. [The Final Data Product](about:blank#9-the-final-data-product)
10. [Impact, Limitations and Future Steps](about:blank#10-impact-limitations-and-future-steps)
11. [Reproducibility and Project Structure](about:blank#11-reproducibility-and-project-structure)
12. [Bibliography](https://app.notion.com/p/AI-Literacy-Gap-Index-38f5687c77bf80169f71ed897ef9e084?pvs=21)

---

## 1. Introduction and Problem Definition

### 1.1 The challenge

Between 2023 and 2025, generative AI moved from research labs into the daily infrastructure of work, public services and information. The EU AI Act entered into force (European Parliament and Council 2024), the Digital Decade targets set a **goal of 80 % of people aged 16–74 with at least basic digital skills by 2030** (European Parliament and Council 2022), and enterprises across Europe began deploying AI systems at scale, with adoption among enterprises (10+ employees) rising from 13.5 % in 2024 to 20 % in 2025 (Eurostat 2025). The technology arrived almost everywhere at once.

***The capacity to engage with it did not.***

**AI literacy,** the ability to understand what AI systems do, to use them productively, and to critically evaluate their outputs, is distributed extremely unevenly. And it is not distributed randomly: it tracks the existing fault lines of European society. A person with low formal education, in a low-income household, in a region with weak adult-learning infrastructure, is far less likely to acquire AI literacy and far more likely to be *exposed* to AI’s downsides: algorithmic decisions in hiring and benefits, automation of low-skill work, and AI-generated disinformation.

This is the precise challenge the project addresses:

> **AI literacy gaps threaten to convert an existing, well-documented pattern of regional inequality into a new, self-reinforcing one. The populations least equipped to benefit from AI are the same populations most exposed to its risks — and we currently have no regional instrument to see where this is happening.**
> 

This is fundamentally a **distributional** problem, which is why it sits at the intersection of three Sustainable Development Goals.

### 1.2 Relevance to the SDGs

This project is anchored in **SDG 10, SDG 4 and SDG 16:**

**SDG 10 — Reduced Inequalities *(primary)***

SDG 10 calls to "empower and promote the social, economic and political inclusion of all, irrespective of … economic or other status" (Target 10.2) and to "ensure equal opportunity and reduce inequalities of outcome" (Target 10.3) (United Nations 2015). The AI Literacy Gap Index is, at its core, an **inequality-amplification early-warning system**. Its entire purpose is to identify where a new technology will widen the gap between Europe's strong and vulnerable regions. The pillars of poverty (P2), low education (P3) and unemployment among the low-qualified (P5) are direct measures of the "economic and other status" that SDG 10 seeks to decouple from opportunity.

**SDG 4 — Quality Education *(core mechanism)***

SDG 4, Target 4.4, calls to "substantially increase the number of youth and adults who have relevant skills, including technical … skills, for employment, decent jobs and entrepreneurship", and Target 4.6 addresses functional literacy for all (United Nations 2015). AI literacy is the contemporary frontier of "relevant skills". Two index pillars measure this directly: **P1 (digital skills)** captures current competence, and **P4 (lifelong learning)** captures the system's capacity to keep adults' skills current, exactly the adult-learning dimension SDG 4 emphasises.

**SDG 16 — Peace, Justice and Strong Institutions *(the civic stake)***

SDG 16 is the least obvious but arguably the most forward-looking link. Target 16.10 concerns public access to information, and Targets 16.6/16.7 concern effective, accountable institutions and inclusive decision-making (United Nations 2015). AI literacy is now a precondition for all three:

- A population that cannot distinguish AI-generated disinformation from genuine information cannot exercise informed democratic choice. Low AI literacy is a direct vulnerability to **algorithmic manipulation of the public sphere** (European Parliament 2023).
- As public administrations adopt AI for benefits, policing and resource allocation, citizens without the literacy to understand or contest these systems lose **effective access to justice and accountable institutions.**
- The regions our index flags as highest-risk are therefore not only economically vulnerable, but also **democratically** vulnerable. The AI literacy gap is a resilience gap for the institutions of SDG 16.

In short: **SDG 10 is the *what* (inequality), SDG 4 is the *mechanism* (skills and learning), and SDG 16 is the *stake* (the integrity of democratic institutions).** The index quantifies all three through a single regional lens.

---

## 2. Research Question and Hypotheses

### 2.1 Primary research question

> **Where in the European Union are AI literacy gaps most likely to reinforce existing social and economic inequalities, and what *structural profile* of risk does each region face?**
> 

The question has two deliberately distinct parts:

- **“Where” (magnitude)** — answered by the composite **index** (Section 6.1–6.2): a single 0–1 risk score per region.
- **“What profile” (kind)** — answered by **unsupervised clustering** (Section 6.3): a typology of *risk fingerprints*. Two regions can share the same risk score for completely different reasons, and the appropriate intervention depends on the reason, not just the score.

This two-part design is what allows the project to move from *measurement* to *actionable, differentiated recommendations;* the difference between “Region X is at risk” and “Region X is at risk *because of A and B*, and therefore needs intervention *C*”.

### 2.2 Hypotheses

| # | Hypothesis | Status after analysis |
| --- | --- | --- |
| **H1** | AI literacy gap risk is **not random** but concentrates in regions already disadvantaged on classic cohesion indicators (income, education, employment). | **Supported.** Highest-risk regions (S. Italy, Bulgaria, Romania, French overseas) are long-standing EU cohesion priority regions. |
| **H2** | Risk is **multidimensional,** no single indicator captures it; the pillars measure distinct dimensions. | **Supported.** PCA: first component explains only 34.5 % of variance; no dominant axis. |
| **H3** | Regions cluster into **qualitatively distinct risk types** requiring different policy responses. | **Supported.** Five robust, interpretable clusters identified. |

### 2.3 Relevance of the question to the SDGs

The research question operationalises the SDG ambition into something *measurable and locatable*. SDG 10 is a global aspiration; “*West-Nederland scores 0.219 while Isole scores 0.731, and they belong to different risk types*” is an actionable fact a regional authority can use. The index is the bridge between the goal and the intervention.

---

## 3. Data Collection and Preprocessing

### 3.1 Design principle: official, open, comparable, regional

Every dataset in the index satisfies four constraints, chosen specifically to make the product **credible to a policy audience and aligned with the SDG framework**:

1. **Official** — sourced exclusively from **Eurostat**, the EU’s statistical authority. No scraped, modelled or proprietary data. This is essential because cohesion policy decisions cannot rest on unofficial numbers.
2. **Open** — every series is downloadable from the Eurostat dissemination API; the entire pipeline is reproducible from raw source (Section 11).
3. **Comparable** — all series follow harmonised EU survey methodologies (EU-LFS, EU-SILC), making cross-regional comparison methodologically valid.
4. **Regional** — a sub-national resolution gives the index more differentiation potential than country averages, which cannot show variation within a country; NUTS-1 specifically is the level of our anchor dataset (P1), to which the NUTS-2 pillars are aggregated up (Section 3.4).

### 3.2 Data sources and pillars

The index was designed around **seven** candidate pillars and finalised with **six** (the rationale for dropping the seventh is in Section 3.6).

| Pillar | Concept | Eurostat dataset | Indicator selected | Level |
| --- | --- | --- | --- | --- |
| **P1** | Digital readiness | `isoc_r_dskl_i` | Basic-or-above digital skills, % of all individuals (`I_DSK2_BAB`, `PC_IND`) | NUTS-1 |
| **P2** | Social vulnerability | `tgs00107` (+ `ilc_peps01n` for 5 states) | At risk of poverty or social exclusion (AROPE), % | NUTS-2 |
| **P3** | Education | `edat_lfse_04` | Population with at most lower-secondary education (ED0-2), age 25–64, % | NUTS-2 |
| **P4** | Adult learning | `trng_lfse_04` | Participation in education/training, age 25–64, % | NUTS-2 |
| **P5** | Labour-market vulnerability | `lfst_r_lfu3rt` | Unemployment rate among low-educated (ED0-2), age 15–74, % | NUTS-2 |
| **P6** | Demographics | `demo_r_d2jan`, `demo_r_pjanaggr3` | Share of population aged 65+, % | NUTS-2 |
| ~~P7~~ | ~~Enterprise AI exposure~~ | `~~isoc_r_eb_ain2~~` | *Dropped — see 3.6* | NUTS-2 |

**Why each indicator was chosen**

Each Eurostat dataset is not a single ready-made figure — it is a multi-dimensional cube. For one and the same dataset, Eurostat offers a choice of **indicator variants** (e.g. "basic-or-above" vs. "above-basic" digital skills), **units or denominators** (e.g. share of all individuals vs. share of internet users; rates vs. absolute counts), **age bands** (e.g. Y25-64 vs. Y18-64), and **sex breakdowns.** Building the index therefore required selecting, for every pillar, one specific combination out of many possible ones — a decision that materially shapes what the pillar measures. The choices we made, and the alternatives we rejected, are set out below.

- **P1 — Digital skills.** We use the share of people with at least basic digital skills, the EU DESI standard (I_DSK2_BAB), measured against everyone in the region rather than only internet users (PC_IND, not PC_IND_IU3), so that people who are offline, the group most exposed to the gap, stay inside the measure (an SDG-10 choice). It is internationally established and spreads regions widest (≈19–85 %), separating them most clearly.
- **P2 — Poverty.** We use the EU's standard at-risk-of-poverty-or-social-exclusion rate (AROPE, tgs00107); for five countries missing from the regional file we substitute the identical national figure (ilc_peps01n), which is exact because each is a single region.
- **P3 — Education.** We measure the share of adults aged 25–64 with only a low level of schooling (no qualification beyond lower-secondary school). People with little formal education are most likely to struggle in the digital and AI transition, so a higher share directly means a bigger gap.
- **P4 — Lifelong learning.** We use participation in adult education or training among 25–64-year-olds (trng_lfse_04), chosen over the 18–64 band for consistency with P3 (under-25s are often still in initial education); higher participation = lower risk (inverted). *Limitation: it only captures the last four weeks, so it is a snapshot.*
- **P5 — Labour market.** We use the unemployment rate among the low-qualified (lfst_r_lfu3rt) rather than the raw count of unemployed persons (lfst_r_lfu3pers), because rates are comparable across differently sized regions; it links low qualification (P3) to actual labour-market exclusion.
- **P6 — Demographics.** We use the share of people aged 65+ (demo_r_d2jan) to capture workforce ageing — *kept for completeness, but a weak differentiator, since Europe ages almost uniformly.*

### 3.3 Reference year

All pillars are filtered to **2025**, the only year available for the anchor dataset (P1 digital skills), making the index a **cross-sectional** snapshot rather than a trend product. We deliberately **do not back-fill missing 2025 values** with older years, as that would break the cross-sectional design; instead each gap is handled explicitly. The five countries missing from the regional poverty file take their identical 2025 national figure (Section 3.2), and the seven regions without a reliable 2025 unemployment rate are carried as missing in the index itself — they are imputed only downstream for the clustering step (Section 6.3.1), not in the base data. The one remaining gap, Switzerland in poverty, is out of scope (non-EU).

### 3.4 The NUTS hierarchy problem and population weighting

The pillars arrive at **mixed geographic levels**: P1 is natively NUTS-1, but P2–P6 are NUTS-2 (a finer subdivision). To build a coherent NUTS-1 index, the NUTS-2 series must be **aggregated up** to NUTS-1 — and this cannot be a naive average, because a region’s sub-areas have very different populations.

The pipeline therefore uses **population-weighted aggregation**:

$$
\text{value}_{\text{NUTS-1}} = \frac{\sum_i \text{value}_i \times \text{pop}_i}{\sum_i \text{pop}_i}
$$

where *i* ranges over the NUTS-2 sub-regions, and population weights come from `demo_r_d2jan`. This correctly gives a city-region more weight than a sparsely populated rural sub-area within the same NUTS-1 region. The formula was independently spot-checked for DE1 and FR1 during the code audit (Section 4.3) and confirmed accurate.

### 3.5 Country-code and coverage harmonisation

Two technical harmonisations were needed to achieve full EU-27 coverage:

- **13 single-region countries** (e.g. Denmark) report digital skills under a 2-character country code (`DK`) rather than the 3-character NUTS-1 code (`DK0`). A mapping was applied. For Finland, `FI` → `FI1` (Manner-Suomi, 99.5 % of population; the Åland Islands FI2 are excluded as negligible).
- **5 countries** (CY, EE, LU, LV, MT) are absent from the regional poverty dataset `tgs00107`. They were filled from `ilc_peps01n` (the *national* AROPE rate, identical EU-SILC methodology and reference year). Because each of these countries is a single NUTS-1 region, the national value *is* the regional value.

### 3.6 Scope decision: dropping the enterprise-AI pillar

The seventh candidate pillar, enterprise AI adoption (`isoc_r_eb_ain2`), was  **removed**. This is the project’s most important scope decision and is documented below:

**Two reasons:**

1. **Conceptual** — enterprise AI adoption measures *business behaviour*, not *human AI literacy*. It is a different level of analysis (the demand-side “exposure pressure”) from the other six human-centred pillars.
2. **Data integrity** — the dataset covers only 38 of 88 NUTS-1 regions, and Germany, France, Italy and the Netherlands are *entirely absent* because they do not report at NUTS-1 level. A missing value here would be read by the index as “no AI exposure = no risk”, which is **substantively false** — the gap is methodological, not real. Including it would have cut the index from 87 to 32 regions (−64 %) and injected a systematic falsehood.

The demand-side perspective is retained as a documented scope exclusion and a candidate for future work (Section 10.3).

### 3.7 Final scope

After EU-27 filtering and the P5 exclusions (Section 4.2), the index covers **87 NUTS-1 regions across all 27 member states**. Non-EU regions (UK, NO, CH, TR, RS, etc.) are excluded so that every region shares the **same legal and policy framework** (EU AI Act, Digital Decade), which is what makes the recommendations *actionable* within a single governance system.

---

## 4. Data Quality and Reliability

A central claim of this project is that its honesty about data limitations is a *strength*, not a weakness. Every quality issue was investigated, decided, and documented rather than silently smoothed over.

### 4.1 Coverage and the population-weighting caveat (P2 poverty)

Two NUTS-1 regions have a sub-region missing from the poverty aggregation:

| Region | Coverage | Missing sub-region | Decision |
| --- | --- | --- | --- |
| FI1 Manner-Suomi | 75 % | FI19 Länsi-Suomi | **No flag.** Länsi-Suomi (~25 % of Manner-Suomi's population) is missing. For its omission to shift the regional poverty rate by more than 0.5 pp, its own rate would have to differ from the three covered sub-regions (which span 15.5–17.9 %) by more than ~2 pp. This is implausible for an economically comparable mainland Finnish region. The value is therefore a reliable approximation and used without a flag. |
| FRY French overseas | 86 % | FRY5 Mayotte | **Flagged.** Mayotte is the poorest French territory, with no EU-SILC-compliant rate available. The computed 41.4 % almost certainly *underestimates* true poverty. Documented as a data-quality flag to be shown in the dashboard. |

### 4.2 Missing values and honest exclusion (P5 unemployment)

P5 is the only pillar with missing data: **7 regions** (DE8, FRM, PL2, PL7, PL8, PL9, PT3) lack a reliable unemployment rate for the low-educated, because the EU-LFS sample is too small to disaggregate by education at NUTS-1. These are recorded in a machine-readable artifact, `excluded_regions.csv`.

A tempting “fix” — substituting the *total* unemployment rate (available for all 7) — was **rejected**: low-educated unemployment is structurally always *higher* than the total, so the fallback would have systematically portrayed these regions as *less* vulnerable than they are. **`NaN` is the methodologically honest choice**. (For the *clustering* step only, a country-peer mean is imputed — see Section 6.3.1.)

---

## 5. Exploratory Data Analysis

EDA was conducted on the assembled `pillar_feature_table.csv` (87 EU-27 NUTS-1 regions × 6 pillars). Three findings shaped the entire downstream modelling strategy.

### 5.1 Pillar distributions

| Pillar | Min | Median | Max | Std | Finding |
| --- | --- | --- | --- | --- | --- |
| P1 Digital skills | 27.1 | 62.0 | 85.2 | 12.3 | Healthy, wide spread |
| P2 Poverty | 10.8 | 19.9 | 41.4 | 6.5 | Healthy spread |
| P3 Education (low) | 3.4 | 15.0 | **56.7** | 10.9 | **Outlier: PT2 = 56.7 %** |
| P4 Lifelong learning | 3.3 | 12.8 | 40.3 | 7.3 | Healthy spread |
| P5 Unemployment (low-ed) | 4.1 | 12.6 | 38.3 | 6.2 | Healthy spread |
| P6 Demographics (65+) | 13.0 | 21.7 | 28.4 | **3.0** | **Very low variance** |

**Two anomalies stand out and were each investigated:**

**Anomaly 1 — the PT2 education outlier**

PT2 (the Azores) has 56.7 % of working-age adults with at most lower-secondary education — almost four times the EU median of 15.0 % and the highest of any region (the next-highest are Madeira at 48.7 % and southern Italy/Isole at 43.3 %). This is not a data error. It reflects the genuine structural reality of historically isolated Atlantic island economies dominated by tourism and agriculture, sectors that traditionally required no formal qualifications.

Unemployment supports this: PT2's unemployment among the low-educated is only 5.5 % (5th-lowest of 80 regions) — the low-educated population is employed, not jobless. The data is correct and the outlier is meaningful, so PT2 is retained unmodified — capping or removing a genuine EU region simply because it is statistically inconvenient would undermine the very purpose of the index.

**Anomaly 2 — the demographics pillar has very low variance**

 P6 (share aged 65+) has a standard deviation of just 3.0 pp; the middle 50 % of regions fall within a 4-point band (20.0–23.9 %). Europe ages almost uniformly. This is itself an insight: demographic ageing is a universal pressure, not a differentiating one. P6 is retained (the signal is real and SDG-relevant) but its low discriminating power shows up in its near-zero loading on the main risk axis (Section 6.4).

### 5.2 Correlation structure — the pillars are largely independent

Pearson correlations between the six pillars (computed on the raw pillar values):

![correlation_matrix.png](AI%20Literacy%20Gap%20Index/correlation_matrix.png)

*(P1 = digital skills, P2 = poverty, P3 = low education, P4 = lifelong learning, P5 = low-skill unemployment, P6 = ageing. Correlations are on the raw values, so a positive sign means the two raw indicators move together.)*

- The only notable correlation is **P1 ↔ P4 = +0.61** (digital skills and lifelong learning move together — competent regions also keep learning). This is moderate, not redundant: the two pillars measure conceptually distinct things (current competence vs. active learning behaviour), so both are retained.
- **Every other pillar pair has |r| < 0.5** (the next-highest is P2 ↔ P3 = 0.47). The pillars are measuring **largely independent dimensions** of risk.

This is the empirical foundation for the entire composite-index design: if the pillars were highly correlated, a single indicator would suffice. They are not — so a **multidimensional** index is justified.

### 5.3 Visual EDA

Key EDA and result visualisations produced by the pipeline:

**PCA Biplot**

![plot_pca_biplot.png](AI%20Literacy%20Gap%20Index/plot_pca_biplot.png)

*Shows how pillars load onto the two main variance axes → visual proof of multidimensionality*

---

**Elbow & Silhouette Curve**

![plot_elbow_silhouette.png](AI%20Literacy%20Gap%20Index/plot_elbow_silhouette.png)

*Used for cluster-count selection diagnostics*

---

**Cluster Profiles Heatmap**

![plot_cluster_profiles.png](AI%20Literacy%20Gap%20Index/plot_cluster_profiles.png)

*Shows the five risk “fingerprints” side by side*

---

**Cluster Profiles Heatmap | k=4 vs. k=5**

![plot_exploratory_heatmap_k4_k5.png](AI%20Literacy%20Gap%20Index/plot_exploratory_heatmap_k4_k5.png)

*Proves that k=5 splits two genuinely different high-risk types*

---

## 6. Model Building and Evaluation

The analytical core is **two complementary models**, each answering a different question. This layered design — measure, then typologise, then attribute — is what lets the project deliver differentiated, actionable insight rather than a single ranking.

| Model | Type | Question it answers |
| --- | --- | --- |
| **Composite index** (PCA-weighted) | Unsupervised (dimensionality / weighting) | *How much* risk does each region face? |
| **K-Means clustering** (k=5) | Unsupervised (typology) | *What kind* of risk does each region face? |

### 6.1 The composite index — construction

All six pillars are **Min-Max normalised to [0, 1]** and direction-aligned so that **1 always means highest risk** (P1 digital skills and P4 lifelong learning are inverted, since high skills/learning mean low risk). Min-Max was chosen over Z-score and Robust Scaling after an explicit comparison: it is interpretable, bounded, and consistent between the index and the clustering step. 

Counter-intuitively, it is also the least distorting representation of the PT2 education outlier. Measured as distance from the centre of the P3 distribution, PT2 sits at 1.000 under Min-Max (simply the maximum of the bounded scale), but **3.60 standard deviations under Z-score** and **3.97 IQR-units under Robust Scaling,** i.e. Robust Scaling, often recommended precisely for outliers, actually makes PT2 the most extreme, because P3's inter-quartile range is narrow (10.5 pp). Min-Max keeps the outlier bounded and therefore least disruptive to the composite.

**Weighting — three variants tested for robustness.** Rather than assert a single weighting, three were computed and compared:

1. **Baseline (equal weights)** — each pillar 1/6 ≈ 16.7 %. The OECD/HDI/DESI standard
and a neutral reference point.
2. **Expert weights** — domain-driven (P1 35 %, P3 22 %, …). **Subsequently removed from
scope**: while reasoned, the exact percentages (why 35 and not 30?) cannot be defended
with empirical rigour. Documented for transparency.
3. **PCA weights (data-driven)** — derived from the variance structure of the data
itself. **Selected for the final index.**

**The final index uses “All-PC” PCA weights**, defined as

$$
w_j = \frac{\sum_{k=1}^{6} \lambda_k \,\lvert \text{loading}_{jk}\rvert}{\sum_j \sum_{k=1}^{6} \lambda_k \,\lvert \text{loading}_{jk}\rvert}
$$

i.e. each pillar’s loading summed across *all* principal components, weighted by each component’s explained variance. This avoids the trap of PC1-only weights, which would near exclude P5 (whose variance is orthogonal to PC1) by ignoring 65.5 % of the variance structure.

### 6.2 The index — key result and its meaning

**PC1 explains only 34.5 % of total variance.** This single number is one of the most important results in the project:

- If one component had explained 80 %+, the pillars would be **redundant** — a single index would be measuring one underlying thing.
- 34.5 % means **every pillar contributes unique information**; risk is genuinely multidimensional (confirming **H2**).
- Consequently the **All-PC weights converge almost exactly to equal weights** (every pillar lands between 14.8 % and 18.4 %). This convergence is a *substantive* finding: the data *empirically validates* the equal-weights baseline rather than us *assuming* it. The final index is therefore both data-grounded **and** robust to the weighting choice — the strongest possible position for a composite index.

**Final index range:** **0.219 (NL3 West-Nederland) to 0.731 (ITG Isole)** — a span of
0.51 on the 0–1 scale, i.e. the most at-risk region carries more than three times the
gap-risk of the least. The full ranked table is in `ai_literacy_gap_index.csv`.

**Top and bottom of the ranking:**

| Rank | Region | Country | Index | Cluster |
| --- | --- | --- | --- | --- |
| 1 | ITG — Isole | Italy | 0.731 | High Poverty & 
Low Education |
| 2 | ITF — Sud | Italy | 0.700 | High Poverty & 
Low Education |
| 3 | BG3 — Severna i Yugoiztochna | Bulgaria | 0.651 | Low Digital Skills |
| 4 | RO2 — Macroregiunea Doi | Romania | 0.648 | High Poverty & 
Low Education |
| 5 | FRY — Régions Ultrapériphériques | France | 0.643 | High Poverty & 
Low Education |
| … |  |  |  |  |
| 85 | DK0 — Danmark | Denmark | 0.245 | Broadly Resilient |
| 86 | NL2 — Oost-Nederland | Netherlands | 0.229 | Broadly Resilient |
| 87 | NL3 — West-Nederland | Netherlands | 0.219 | Broadly Resilient |

**The geographic pattern is itself an external validation of the index (H1).** The index is built entirely from AI-literacy proxies — digital skills, education, poverty, lifelong learning, unemployment and demographics — **with no input from regional GDP or cohesion-policy classifications.** Yet its resulting map reproduces the EU's long-established regional-disparity geography almost exactly. 

The highest-risk regions (southern Italy, Bulgaria, Romania, the French outermost regions) are precisely those the European Commission's Ninth Cohesion Report identifies as structurally lagging: "more than one in four people in the EU (28 %) live in a region with GDP per capita below 75 % of the EU average. Most of them live in Eastern Member States, but also in Greece, Portugal, Spain, Southern Italy and outermost regions" (European Commission 2024). The lowest-risk regions (the Netherlands, Denmark, Ireland) are likewise the established north-western core.

That an AI-literacy risk index, assembled from a different set of indicators, converges on a disparity map documented independently over successive EU Cohesion Reports is strong **convergent-validity** evidence: the index captures genuine structural disadvantage, not measurement artefacts. This convergence is partly expected — two pillars (poverty, education) share socioeconomic signal with the GDP-based classification — but the index adds value beyond that binary "lagging vs. developed" map in two ways: it incorporates the specifically **digital dimension** (P1, P4), which the GDP metric ignores, and it resolves the single "lagging" category into **five distinct risk types** (Section 6.3), turning a static disparity map into an actionable typology.

### 6.3 K-Means clustering — the risk typology

The index answers “**how much**”. Clustering answers **“what kind”** — and this is where the project’s policy value is generated.

#### 6.3.1 Preprocessing for clustering

Input is the **six already-normalised pillar scores**. The 7 P5-missing regions are imputed using the **country-peer mean** (the mean P5 of other NUTS-1 regions in the same country), *not* the EU-27 mean. Labour markets are country-specific, so the national peer is a far closer proxy: for Madeira (PT3), the Portuguese mean (0.060) is far more accurate than the EU mean (0.271), correctly reflecting Portugal’s low low-educated unemployment. Imputation is confined to clustering; the index file preserves the original `NaN`.

#### 6.3.2 Choosing k = 5

The number of clusters was selected with the **elbow (inertia)** and **silhouette** diagnostics over k = 2–8:

| k | Inertia | Silhouette |
| --- | --- | --- |
| 2 | 15.78 | 0.278 |
| 4 | 11.09 | 0.189 |
| **5** | **9.73** | **0.200** |
| 6 | 8.74 | 0.178 |

**k = 5 was chosen — and crucially, not purely on the metric.** k = 2 has the highest silhouette but is uselessly coarse. The decisive argument is **analytical quality**: at k = 4, two structurally different high-risk types are merged; at k = 5 they separate into distinct, policy-relevant fingerprints (the *High Poverty & Low Education* vs. the *Low Digital Skills*). The side-by-side k=4/k=5 heatmap (Figure, §5.3) makes this split visible. **Choosing k on *interpretability* over a marginal silhouette gain is the correct methodology for a typology intended for human decision-makers.**

**Configuration:** `KMeans(n_clusters=5, random_state=42, n_init=20)` — 20 initialisations, fixed seed for full determinism/reproducibility. Cluster IDs are assigned first and *named afterwards* from their pillar profiles.

#### 6.3.3 The five risk profiles (results from `ai_literacy_gap_index_clustered.csv`)

| Cluster | n | Avg. index | Defining fingerprint |
| --- | --- | --- | --- |
| **High Poverty & Low Education** | 11 | **0.583** | High P2 (0.68) + high P3 (0.65), with elevated P4. Poverty and low education reinforce each other. |
| **Low Digital Skills** | 20 | 0.520 | High P1 gap (0.69) + very high P4 (0.88) + ageing (P6 0.63). Specifically a digital-competence and skills-updating failure. |
| **Ageing Workforce** | 39 | 0.410 | Elevated P4 (0.74) + P6 (0.64); poverty/education *not* elevated. The large, diffuse “gradual risk” middle of Europe. |
| **Low-Skill Unemployment** | 6 | 0.354 | Highest P5 (0.67) but lowest P3 (0.12) and low P2 — strong societies with one concentrated blind spot. |
| **Broadly Resilient** | 11 | **0.291** | Acute pillars low; lifelong learning and ageing only moderate. Same long-term challenge, far stronger starting position. |
1. **High Poverty & Low Education**
Poverty and low educational attainment reinforce each other here. Many adults never went beyond basic schooling and face financial hardship, so the AI literacy gap is broad and deeply rooted — it can't be closed with digital courses alone.
2. **Low Digital Skills**
These regions aren't held back by low education — the problem is specifically weak digital skills (the highest gap of any cluster) and very little adult retraining to catch up. Skills simply haven't kept pace as technology moved on.
3. **Ageing Workforce**
A largely stable, reasonably well-off region with no acute weakness — but an ageing workforce whose skills gradually risk falling behind. The risk here is slow and diffuse rather than driven by any single sharp gap.
4. **Low-Skill Unemployment**
A strong, well-functioning region with one concentrated blind spot: the small group of people without formal qualifications struggles to find work. The challenge isn't the whole labour market — it's reaching a specific, hard-to-reach minority.
5. **Broadly Resilient**
No single weakness stands out — income, digital skills and employment are all in good shape, and education is around the European average. These regions face the same long-term AI challenges as everyone else, but from a structurally strong starting position.

*The* **Low-Skill Unemployment** *cluster is the analytically richest finding and is discussed in Section 7.2.*

---

## 7. Interpretation and Insight Generation

### 7.1 The central insight: AI risk rides on old inequalities

**The central insight: AI risk rides on existing inequality.** The regions our index ranks highest — southern Italy, Bulgaria, Romania, the French overseas territories — are the same regions EU structural funds have targeted for decades. **This is the core SDG-10 finding: absent intervention, AI will not be a great equaliser; it will deepen the gaps** that already define European inequality.

What the index adds to that familiar geography is the **digital dimension**. Alongside poverty, education and employment it brings in current digital skills (P1) and adult lifelong learning (P4) — the competences that decide who benefits from AI and who is left behind — and combines them into a single AI-literacy risk score. The five risk types (Section 7.2) take it one step further, showing not only where the gap is largest but what kind of gap each region faces.

### 7.2 The most important nuance: risk type, not just risk rank

The clustering reveals that **the same risk score can mean opposite things**, and the clearest example is the **Low-Skill Unemployment**  cluster (6 regions). These regions look *strong* on almost every dimension — low poverty (P2 0.25), the lowest low-education share of any cluster (P3 0.12), decent digital skills, active retraining. Yet unemployment among their few low educated residents is the **highest of all clusters** (P5 0.67). This is a well-functioning society with a **single concentrated blind spot**: the small minority without qualifications falls through every net at once.

The policy implication is the opposite of the high-risk clusters. These regions do **not** need infrastructure-building or broad skills campaigns — they need **targeted outreach to a small, hard-to-reach group**. A national “boost digital skills” programme would largely miss them. This is the project’s strongest argument for *why a typology, not just a ranking, is necessary*: a ranking would file these regions as “moderate risk” and prescribe the wrong medicine.

### 7.3 Linking the three SDGs to the findings

- **SDG 10** — the finished index is a ready-made targeting instrument: it ranks all 87 regions and, validated against the EU cohesion map (§6.2), can prioritise Cohesion-Policy funding directly.
- **SDG 4** — the results pinpoint the lever: digital skills (P1) is the most influential pillar, and the 20-region Low Digital Skills cluster maps exactly where adult-learning systems (Target 4.4) are failing to keep pace.
- **SDG 16** — the regions the index flags as highest-risk are the same ones least equipped to resist AI-enabled disinformation; the index therefore doubles as a democratic-resilience map, showing where AI-literacy investment is also institutional-integrity investment.

---

## 8. Actionable Recommendations

Recommendations are **differentiated by cluster**, because the central finding is that risk *type* dictates the right response. This is what turns the index from a diagnostic into a decision tool.

### 8.1 Cluster-specific interventions

| Cluster (n) | Core problem | Recommended intervention | SDG |
| --- | --- | --- | --- |
| **High Poverty & Low Education** (11) | Self-reinforcing poverty + low education | **Structural, long-horizon**: combine income support with foundational adult education *before* digital upskilling can land. Tie ESF+/cohesion funds to integrated education-poverty programmes. | 10 + 4 |
| **Low Digital Skills** (20) | Digital-competence gap + failing retraining systems | **Adult digital-skills programmes at scale**, targeted at mid-career workers; rebuild lifelong-learning infrastructure. Highest direct SDG-4.4 leverage. | 4 |
| **Ageing Workforce** (39) | Diffuse, gradual — ageing workers under-participating in training | **Preventive, broad**: workplace-based and age-inclusive digital training; embed AI literacy in continuing professional development before the gap becomes acute. | 4 |
| **Low-Skill Unemployment**  (6) | Small excluded low-qualified minority | **Targeted outreach, not broad campaigns**: active labour-market measures and individualised re-engagement for a specific hard-to-reach group. | 10 |
| **Broadly Resilient** (11) | Strong, but not immune | **Maintain and lead**: pilot advanced AI-literacy curricula; act as exporters of best practice to higher-risk regions. | 4 + 16 |

---

## 9. The Final Data Product

The analysis is delivered as an **interactive, decision-maker-facing dashboard**, not a static report — because the core insight (risk *type* over risk *rank*) only lands when a user can explore their own region.

### 9.1 The dashboard (Streamlit)

The primary deliverable is a **Streamlit application** (`Streamlit_app/`) with:

- An **interactive choropleth map** of all 87 NUTS-1 regions, coloured by index score.
- **Region drill-down**: selecting a region reveals its index score, rank, its cluster (risk type), its six pillar values, and — from the cluster profile — *which pillars* drive its risk and *which intervention* its cluster implies.
- **Case studies** (`case_studies.py`) translating the typology into concrete regional narratives.
- Branded theming (`edv_theme.py`) for a polished, presentation-ready interface.

### 9.2 The public web map

A complementary lightweight **static web map** (`web/` — `index.html`, `map.js`, `style.css`) renders the index from optimised GeoJSON (`web/data/`, with multiple simplification levels for fast loading). Its metadata (`nuts1_ai_literacy_gap_metadata.json`) documents 87 regions with index data of 92 total geometries, including correct handling of the 4 outermost regions. This makes the product **publicly shareable** with zero infrastructure — a homepage-ready cohesion-policy communication tool.

### 9.3 Real-world applicability

The product is designed for concrete users:

- **EU Cohesion / Digital Decade coordinators** — a transparent, official-data allocation key for AI-literacy funding.
- **Elected policymakers (MEPs, national legislators)** — an evidence-based case for where to direct AI-literacy mandates and budgets, and a transparent basis for prioritising legislation and funding.
- **National education and labour ministries** — locate their regions, read the cluster-specific intervention.
- **Regional development agencies** — benchmark against structural peers (same cluster, not just same country).
- **Researchers and journalists** — an open, reproducible evidence base on AI-driven inequality.

> *Because the entire pipeline rebuilds from official Eurostat sources, the product is re-runnable each year as new data is published — a living instrument, not a one-off snapshot.*
> 

---

## 10. Impact, Limitations and Future Steps

### 10.1 Potential impact on the SDGs

- **SDG 10** — turns an abstract risk (“AI may worsen inequality”) into a **specific, ranked, typologised regional map** that policy can act on, with a built-in allocation logic.
- **SDG 4** — identifies digital skills and adult learning as the highest-leverage levers and pinpoints the regions where retraining systems are most clearly failing.
- **SDG 16** — reframes AI literacy as democratic-resilience infrastructure and flags where institutional vulnerability is greatest.

### 10.2 Limitations

1. **Proxy, not measurement.** No regional AI-literacy dataset exists for 2025; the index is a *structural-risk proxy* built from adjacent indicators. It identifies *where the conditions for an AI literacy gap are worst*, not direct literacy levels.
2. **Cross-sectional.** Anchored to a single year (2025); it is a snapshot, not a trend.
3. **The 4-week learning window (P4).** The EU-LFS measures training in the *4 weeks* before interview — it under-counts infrequent-but-intensive learners. The 12-month Adult Education Survey would be better but exists only at country level, every ~5 years.
4. **No age breakdown in the anchor.** Digital skills and poverty are total-population only; elderly-specific digital skills are unavailable at NUTS-1.

### 10.3 Future steps

1. **Country-level elderly digital-skills proxy.** `isoc_sk_dskl_i` provides elderly (55–74) digital-skills breakdowns at country level. Because P6 (elderly share) is near-uniform across regions, imputing national elderly-skills values to NUTS-1 would capture genuine *cross-country* differences in elderly digital competence without distorting regional variation — a high-value, low-risk enhancement.
2. **Time series.** As `isoc_r_dskl_i` accrues more years, convert the index from a snapshot to a **trend product** tracking whether gaps are widening or closing — directly measuring progress against the Digital Decade 2030 target.
3. **Direct validation.** Where any regional AI-literacy survey emerges, validate the proxy index against it and recalibrate.
4. **Sub-NUTS-1 / equity drill-down.** Extend toward NUTS-2 and, where data allows,
demographic breakdowns to locate *intra-regional* inequality (deepening the SDG-10 lens).

---

## 11. Reproducibility and Project Structure

The entire project rebuilds from raw Eurostat sources with a documented, validated pipeline.

```
notebooks/
  01_load_data.ipynb          # downloads all raw Eurostat TSVs → tidy CSVs
  02_EDA.ipynb                # cleaning, weighting, EDA → pillar_feature_table.csv
  03_index_construction.ipynb # normalisation + PCA weighting → ai_literacy_gap_index.csv
  04_clustering.ipynb         # K-Means typology → ..._clustered.csv
  05_index_mapping.ipynb      # GeoJSON export for the web map
data/processed/               # all intermediate + final CSVs, figures
tests/                        # validate_01_load_data.py, validate_02_eda.py (67 checks)
Streamlit_app/                # the interactive dashboard (final product)
web/                          # public static web map + optimised GeoJSON
DOCUMENTATION.md              # full decision log (every analytical choice + rationale)
```

**Run order:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/01_load_data.ipynb   # → 02 → 03 → 04 → 05
streamlit run Streamlit_app/app.py              # launch the dashboard
```

---

*All figures are derived from official Eurostat open data, reference year 2025, and are reproducible from the pipeline above.*

---

## 12. Bibliography

European Commission (2024): Ninth report on economic, social and territorial cohesion.
COM(2024) 149 final, Brussels, 27 March 2024.
[https://ec.europa.eu/regional_policy/information-sources/cohesion-report_en](https://ec.europa.eu/regional_policy/information-sources/cohesion-report_en)

European Parliament (2023): Artificial intelligence, democracy and elections.
European Parliamentary Research Service (EPRS), Briefing PE 751.478.
[https://www.europarl.europa.eu/thinktank/en/document/EPRS_BRI(2023)751478](https://www.europarl.europa.eu/thinktank/en/document/EPRS_BRI(2023)751478)

European Parliament and Council of the European Union (2022): Decision (EU) 2022/2481 of
14 December 2022 establishing the Digital Decade Policy Programme 2030. Official Journal of
the European Union, L 323, 19.12.2022, pp. 4–26.
[https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022D2481](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32022D2481)

European Parliament and Council of the European Union (2024): Regulation (EU) 2024/1689 of
13 June 2024 laying down harmonised rules on artificial intelligence (Artificial
Intelligence Act). Official Journal of the European Union, L, 2024/1689, 12.7.2024.
[https://eur-lex.europa.eu/eli/reg/2024/1689/oj](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)

Eurostat (2025): Use of artificial intelligence in enterprises. Statistics Explained,
European Commission.
[https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises](https://ec.europa.eu/eurostat/statistics-explained/index.php?title=Use_of_artificial_intelligence_in_enterprises)

United Nations (2015): Transforming our world: the 2030 Agenda for Sustainable Development.
Resolution A/RES/70/1 adopted by the General Assembly on 25 September 2015.
[https://sdgs.un.org/2030agenda](https://sdgs.un.org/2030agenda)