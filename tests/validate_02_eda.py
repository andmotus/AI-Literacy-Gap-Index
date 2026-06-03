"""
validate_02_eda.py
==================
Pipeline validation for 02_EDA.ipynb outputs.

Run from the project root:
    python tests/validate_02_eda.py

Exits with code 0 if all checks pass, code 1 if any check fails.
Each check prints PASS, FAIL, or WARN.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

PASS = "  [PASS]"
FAIL = "  [FAIL]"
WARN = "  [WARN]"

failures = []
warnings = []


def check(name, condition, message="", level="fail"):
    if condition:
        print(f"{PASS} {name}")
    else:
        tag = FAIL if level == "fail" else WARN
        print(f"{tag} {name}")
        if message:
            print(f"         → {message}")
        if level == "fail":
            failures.append(name)
        else:
            warnings.append(name)


EU27 = {
    "AT","BE","BG","CY","CZ","DE","DK","EE","EL","ES","FI","FR",
    "HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"
}

# ── FILE EXISTENCE ────────────────────────────────────────────────────────────

print("\n=== FILE EXISTENCE ===")

expected_files = [
    "pillar_feature_table.csv",
    "unemployment_rate_education_region_tidy.csv",
    "demographics_age_structure_tidy.csv",
    "excluded_regions.csv",
]
for fname in expected_files:
    check(fname, (PROCESSED_DIR / fname).exists(),
          f"File not found: {PROCESSED_DIR / fname}")

# ── FEATURE TABLE ─────────────────────────────────────────────────────────────

print("\n=== FEATURE TABLE (pillar_feature_table.csv) ===")

ft = pd.read_csv(PROCESSED_DIR / "pillar_feature_table.csv")

expected_cols = [
    "geo",
    "digital_skills_pct",
    "poverty_social_exclusion_rate",
    "low_education_pct",
    "lifelong_learning_pct",
    "unemployment_rate_low_edu_pct",
    "share_ge65_pct",
    "unemployment_flag",
]
check("feature_table has all 8 expected columns",
      all(c in ft.columns for c in expected_cols),
      f"Missing: {set(expected_cols) - set(ft.columns)}")
check("feature_table has exactly 8 columns", ft.shape[1] == 8,
      f"Shape: {ft.shape}")
check("feature_table has 87 regions", len(ft) == 87,
      f"Found {len(ft)} regions")

# EU27 only
non_eu = ft[~ft["geo"].str[:2].isin(EU27)]
check("feature_table contains only EU27 regions", len(non_eu) == 0,
      f"Non-EU27 regions found: {sorted(non_eu['geo'].tolist())}")

# No duplicate geos
check("feature_table: no duplicate geo codes",
      ft["geo"].nunique() == len(ft),
      f"Duplicates: {ft[ft['geo'].duplicated()]['geo'].tolist()}")

# P5 NaN: exactly 7 expected regions
expected_nan_p5 = {"DE8", "FRM", "PL2", "PL7", "PL8", "PL9", "PT3"}
actual_nan_p5 = set(ft[ft["unemployment_rate_low_edu_pct"].isna()]["geo"].tolist())
check("P5 NaN: exactly the 7 expected regions",
      actual_nan_p5 == expected_nan_p5,
      f"Expected {sorted(expected_nan_p5)}, got {sorted(actual_nan_p5)}")

# No NaN in other pillars
other_cols = [c for c in expected_cols if c not in ["geo", "unemployment_rate_low_edu_pct", "unemployment_flag"]]
for col in other_cols:
    check(f"No NaN in {col}", ft[col].isna().sum() == 0,
          f"{ft[col].isna().sum()} missing values")

# ── VALUE RANGES ──────────────────────────────────────────────────────────────

print("\n=== VALUE RANGES (plausibility) ===")

ranges = {
    "digital_skills_pct":             (10, 100),
    "poverty_social_exclusion_rate":   (5,  60),
    "low_education_pct":               (0,  70),
    "lifelong_learning_pct":           (0,  50),
    "unemployment_rate_low_edu_pct":   (0,  50),
    "share_ge65_pct":                  (5,  35),
}
for col, (lo, hi) in ranges.items():
    vals = ft[col].dropna()
    in_range = vals.between(lo, hi).all()
    check(f"{col}: range {lo}–{hi}%",
          in_range,
          f"Actual range: {vals.min():.1f}–{vals.max():.1f}")

# ── PILLAR COVERAGE PER DATASET ───────────────────────────────────────────────

print("\n=== INDIVIDUAL PILLAR COVERAGE ===")

# P1 Digital Skills
dsk = pd.read_csv(PROCESSED_DIR / "digital_skills_nuts1_labeled_filtered.csv")
dsk_eu27_2025 = dsk[
    (dsk["year"] == 2025) &
    (dsk["indic_is"] == "I_DSK2_BAB") &
    (dsk["unit"] == "PC_IND") &
    (dsk["geo"].str[:2].isin(EU27))
]
# digital_skills_nuts1_labeled_filtered.csv contains only direct NUTS-1 matches (~74).
# 13 single-NUTS1-countries (DK0, CY0, etc.) are added in Step 3.7 via raw TSV mapping.
# Full EU27 coverage (87 regions) is validated via the feature_table check above.
check("P1 Digital Skills: >=70 direct EU27 NUTS-1 regions in source file",
      dsk_eu27_2025["geo"].nunique() >= 70,
      f"Found {dsk_eu27_2025['geo'].nunique()}")

# P2 Poverty
pov = pd.read_csv(PROCESSED_DIR / "poverty_social_exclusion_nuts1_weighted.csv")
pov_eu27_2025 = pov[(pov["year"] == 2025) & (pov["geo"].str[:2].isin(EU27))]
check("P2 Poverty: >=80 EU27 NUTS-1 regions in 2025",
      pov_eu27_2025["geo"].nunique() >= 80,
      f"Found {pov_eu27_2025['geo'].nunique()}")

# P3 Education
edu = pd.read_csv(PROCESSED_DIR / "education_attainment_labeled.csv")
edu_eu27 = edu[
    (edu["year"] == 2025) &
    (edu["isced11"] == "ED0-2") &
    (edu["age"] == "Y25-64") &
    (edu["sex"] == "T") &
    (edu["unit"] == "PC") &
    (edu["geo"].str.len() == 3) &
    (edu["geo"].str[:2].isin(EU27))
]
check("P3 Education: >=85 EU27 NUTS-1 regions in 2025",
      edu_eu27["geo"].nunique() >= 85,
      f"Found {edu_eu27['geo'].nunique()}")
check("P3 Education: no duplicate geo codes",
      edu_eu27["geo"].nunique() == len(edu_eu27),
      "Duplicate geo codes after NUTS-1 filter")

# P4 Lifelong Learning
ll = pd.read_csv(PROCESSED_DIR / "lifelong_learning_labeled.csv")
ll_eu27 = ll[
    (ll["year"] == 2025) &
    (ll["age"] == "Y25-64") &
    (ll["sex"] == "T") &
    (ll["unit"] == "PC") &
    (ll["geo"].str.len() == 3) &
    (ll["geo"].str[:2].isin(EU27))
]
check("P4 Lifelong Learning: >=75 EU27 NUTS-1 regions in 2025",
      ll_eu27["geo"].nunique() >= 75,
      f"Found {ll_eu27['geo'].nunique()}")
check("P4 Lifelong Learning: no duplicate geo codes",
      ll_eu27["geo"].nunique() == len(ll_eu27),
      "Duplicate geo codes after NUTS-1 filter")

# P5 Unemployment Rate
unemp = pd.read_csv(PROCESSED_DIR / "unemployment_rate_education_region_tidy.csv")
unemp_eu27 = unemp[
    (unemp["year"] == 2025) &
    (unemp["isced11"] == "ED0-2") &
    (unemp["age"] == "Y15-74") &
    (unemp["sex"] == "T") &
    (unemp["geo"].str.len() == 3) &
    (unemp["geo"].str[:2].isin(EU27))
]
check("P5 Unemployment: unit is PC only",
      (unemp["unit"] == "PC").all(),
      f"Units found: {unemp['unit'].unique()}")
unemp_with_val = unemp_eu27[unemp_eu27["value"].notna()]
check("P5 Unemployment: >=78 EU27 NUTS-1 regions with values in 2025",
      unemp_with_val["geo"].nunique() >= 78,
      f"Found {unemp_with_val['geo'].nunique()}")

# P6 Demographics
demo = pd.read_csv(PROCESSED_DIR / "demographics_age_structure_tidy.csv")
demo_eu27 = demo[
    (demo["year"] == 2025) &
    (demo["sex"] == "T") &
    (demo["age"].isin(["TOTAL", "Y_GE65"])) &
    (demo["geo"].str.len() == 3) &
    (demo["geo"].str[:2].isin(EU27))
]
pivot = demo_eu27.pivot_table(index="geo", columns="age", values="value")
check("P6 Demographics: TOTAL and Y_GE65 present",
      "TOTAL" in pivot.columns and "Y_GE65" in pivot.columns)
check("P6 Demographics: no missing TOTAL values",
      pivot["TOTAL"].isna().sum() == 0 if "TOTAL" in pivot.columns else False,
      f"{pivot['TOTAL'].isna().sum()} regions missing TOTAL" if "TOTAL" in pivot.columns else "TOTAL column missing")
check("P6 Demographics: no missing Y_GE65 values",
      pivot["Y_GE65"].isna().sum() == 0 if "Y_GE65" in pivot.columns else False)
share = (pivot["Y_GE65"] / pivot["TOTAL"] * 100).dropna()
check("P6 Demographics: share_ge65 in plausible range (5–35%)",
      share.between(5, 35).all(),
      f"Actual range: {share.min():.1f}–{share.max():.1f}")

# ── EXCLUDED REGIONS ─────────────────────────────────────────────────────────

print("\n=== EXCLUDED REGIONS ===")

excl = pd.read_csv(PROCESSED_DIR / "excluded_regions.csv")
expected_excl = {"DE8", "FRM", "PL2", "PL7", "PL8", "PL9", "PT3"}
actual_excl = set(excl["geo"].tolist())
check("excluded_regions.csv: exactly the 7 expected regions",
      actual_excl == expected_excl,
      f"Expected {sorted(expected_excl)}, got {sorted(actual_excl)}")
check("excluded_regions.csv has required columns",
      all(c in excl.columns for c in ["geo", "missing_pillar", "reason", "included_in_index"]))
check("excluded_regions: all marked as not included in index",
      (excl["included_in_index"] == False).all())

# ── DATA CATALOG ──────────────────────────────────────────────────────────────

print("\n=== DATA CATALOG ===")

catalog = pd.read_csv(PROCESSED_DIR / "project_data_catalog.csv")
check("catalog contains pillar_feature_table",
      "pillar_feature_table" in catalog["dataset_code"].values)
check("catalog has downloaded_at column", "downloaded_at" in catalog.columns)

# ── EU27 SCOPE CHECKS ─────────────────────────────────────────────────────────

print("\n=== EU27 SCOPE ===")

all_eu27_countries_represented = {g[:2] for g in ft["geo"]}
missing_eu27 = EU27 - all_eu27_countries_represented
check("All 27 EU member states represented in feature_table",
      len(missing_eu27) == 0,
      f"Missing countries: {sorted(missing_eu27)}")

# FI mapping: FI1 present, FI2 absent
check("Finland: FI1 present in feature_table",
      "FI1" in ft["geo"].values)
check("Finland: FI2 absent from feature_table (Åland excluded)",
      "FI2" not in ft["geo"].values, level="warn")

# Single-NUTS1 country mappings
single_nuts1 = ["CY0","CZ0","DK0","EE0","HR0","IE0","LT0","LU0","LV0","MT0","SI0","SK0"]
for code in single_nuts1:
    check(f"Single-NUTS1 country {code} present", code in ft["geo"].values)

# ── SUMMARY ───────────────────────────────────────────────────────────────────

print("\n" + "=" * 60)
print(f"RESULT: {len(failures)} failure(s), {len(warnings)} warning(s)")
if failures:
    print("FAILED checks:")
    for f in failures:
        print(f"  - {f}")
if warnings:
    print("WARNINGS (known, non-blocking):")
    for w in warnings:
        print(f"  - {w}")
print("=" * 60)

sys.exit(1 if failures else 0)
