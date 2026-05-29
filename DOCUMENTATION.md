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
