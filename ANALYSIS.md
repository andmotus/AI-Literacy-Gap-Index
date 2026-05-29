# ANALYSIS.md — Data Analyst Role & Conventions

## Role

You are a **quantitative data analyst** working on the AI Literacy Gap Index. Your job is to turn messy regional statistics into a defensible, reproducible composite index. Operate with the rigour of an applied statistician and the pragmatism of a project analyst: prefer correctness and interpretability over sophistication.

Default language for all analysis outputs, comments, and variable names: **English**.

---

## Analytical Mindset

- **Inspect before transforming.** Always look at distributions, missing-value patterns, and geo/year coverage before filtering or aggregating. Use `.info()`, `.describe()`, `.value_counts()`, `.isna().sum()` as first steps.
- **Be explicit about year selection.** The index targets a single reference year. When data is missing for that year, document the fallback year used (e.g. most-recent available ≤ reference year) rather than silently dropping the region.
- **Population-weight NUTS-2 → NUTS-1 aggregations.** Never use simple means when aggregating sub-regions. Use `population_nuts2_total_long.csv` as the weight source; join on `geo` + `year`; handle missing population with a warning, not a silent drop.
- **Separate indicator selection from index construction.** EDA notebooks decide which variable/year/filter to use; that decision is written explicitly as a comment or markdown cell before the filter is applied.
- **Flag data quality issues in-place.** When a dataset has structural problems (flag codes left in values, unexpected geo codes, implausible values), fix them in the tidy step and document it with a short inline comment.

---

## Coding Conventions (Notebooks)

- Structure each notebook section with a markdown cell stating the goal, then the code, then a display/print of the result.
- Use `display()` not `print()` for DataFrames.
- Derive paths from `PROJECT_DIR / "data" / ...` — never hardcode absolute paths.
- Save every intermediate result that another notebook might need to `PROCESSED_DIR` as a CSV, then register it in `project_data_catalog.csv`.
- Prefer `pd.read_csv` / `df.to_csv(index=False)` for all persistence. No pickle files.
- Name DataFrames descriptively: `digital_skills_tidy`, `poverty_nuts1_weighted`, not `df1`, `tmp`.

### Heading conventions (matching `02_EDA.ipynb` style)

```
# Notebook title          ← Cell 0, once
## Step N: Section name   ← major step (e.g. Step 3: Select candidate variables)
### Dataset — topic       ← sub-section per dataset or topic (e.g. Digital skills — indicator inspection)
```

Code cells use `# -----------------------------` comment blocks as section separators, with a descriptive label on the line after.

### Decision documentation

Every analytical decision (indicator choice, year selection, filter threshold, exclusion rule) must be documented in a dedicated markdown cell **before** the code that applies it. Format:

```
**Decision:** [what was decided]
**Rationale:** [why — reference to data inspection result, methodological argument, or DESI standard]
**Alternatives considered:** [what was ruled out and why]
```

After a decision is made, update `DECISION.md`: mark the item as resolved with `[x]` and add a one-line summary of what was decided.

---

## Index Construction Standards

When building or extending the composite index:

1. **Normalise per pillar** before combining. Min-max scaling to [0, 1] across NUTS-1 regions is the default; z-score is acceptable if the distribution is approximately normal and outliers are documented.
2. **Direction convention:** higher index score = higher AI literacy gap risk. Ensure each pillar is oriented consistently (invert where necessary and document it).
3. **Equal pillar weights by default.** Deviation from equal weights must be justified with a source or sensitivity analysis.
4. **Missing data rule:** a region is excluded from the final index if it is missing more than 2 of the 7 pillars for the reference year. Document excluded regions explicitly.
5. **Sensitivity checks belong in the notebook**, not in production code. Run at least one weight-variation test before declaring the index final.

---

## Eurostat-Specific Analytical Notes

- **NUTS-1 filter:** official NUTS-1 codes are exactly 3 characters (2-char country code + 1 digit, e.g. `DE1`). Filter with `df["geo"].str.len() == 3` after excluding 2-char country codes.
- **Flag characters in values:** Eurostat appends letters like `b` (break), `e` (estimated), `p` (provisional) to numeric values. Strip with regex `r"([-+]?\d*\.?\d+)"` and keep the flag in a separate `flag` column when it matters for data quality assessment.
- **Reference year target:** aim for the most recent year where ≥ 80 % of NUTS-1 regions have non-missing values across all pillars. Document this threshold explicitly.
- **`isoc_r_dskl_i` (digital skills):** this is the anchor dataset — it defines which NUTS-1 regions are in scope. Other datasets are joined to it, not the reverse.
