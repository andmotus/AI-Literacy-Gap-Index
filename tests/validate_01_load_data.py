"""
validate_01_load_data.py
========================
Pipeline validation for 01_load_data.ipynb outputs.

Run from the project root:
    python tests/validate_01_load_data.py

Exits with code 0 if all checks pass, code 1 if any check fails.
Each check prints PASS, FAIL, or WARN.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
RAW_DIR = PROJECT_DIR / "data" / "raw"

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


# ── FILE EXISTENCE ────────────────────────────────────────────────────────────

print("\n=== FILE EXISTENCE ===")

expected_files = [
    "unemployment_rate_education_region_tidy.csv",
    "demographics_age_structure_tidy.csv",
    "digital_skills_nuts1_tidy.csv",
    "digital_skills_nuts1_labeled.csv",
    "digital_skills_nuts1_labeled_filtered.csv",
    "digital_skills_indicator_overview.csv",
    "poverty_social_exclusion_tidy.csv",
    "poverty_social_exclusion_labeled.csv",
    "poverty_social_exclusion_mapped.csv",
    "poverty_social_exclusion_nuts1_weighted.csv",
    "poverty_social_exclusion_nuts1_comparison.csv",
    "population_nuts2_total_long.csv",
    "nuts1_lookup.csv",
    "nuts2_lookup.csv",
    "nuts2_to_nuts1_lookup.csv",
    "education_attainment_tidy.csv",
    "education_attainment_labeled.csv",
    "lifelong_learning_tidy.csv",
    "lifelong_learning_labeled.csv",
    "unemployment_education_region_tidy.csv",
    "unemployment_education_region_labeled.csv",
    "enterprise_ai_adoption_tidy.csv",
    "enterprise_ai_adoption_labeled.csv",
    "project_data_catalog.csv",
]

for fname in expected_files:
    check(fname, (PROCESSED_DIR / fname).exists(), f"File not found: {PROCESSED_DIR / fname}")

# ── NUTS LOOKUPS ──────────────────────────────────────────────────────────────

print("\n=== NUTS LOOKUPS ===")

nuts1 = pd.read_csv(PROCESSED_DIR / "nuts1_lookup.csv")
nuts2 = pd.read_csv(PROCESSED_DIR / "nuts2_lookup.csv")
nuts2_map = pd.read_csv(PROCESSED_DIR / "nuts2_to_nuts1_lookup.csv")

check("nuts1_lookup has geo column", "geo" in nuts1.columns)
check("nuts2_lookup has geo column", "geo" in nuts2.columns)
check("nuts1_lookup non-empty (>=100 regions)", nuts1["geo"].nunique() >= 100,
      f"Only {nuts1['geo'].nunique()} NUTS-1 codes found")
check("nuts2_lookup non-empty (>=250 regions)", nuts2["geo"].nunique() >= 250,
      f"Only {nuts2['geo'].nunique()} NUTS-2 codes found")
check("nuts2_to_nuts1_lookup has parent_nuts1 column", "parent_nuts1" in nuts2_map.columns)
check("All NUTS-2 parent codes are 3 chars",
      (nuts2_map["parent_nuts1"].dropna().str.len() == 3).all(),
      "Some parent_nuts1 codes are not 3 characters")
check("No duplicate NUTS-1 codes in lookup", nuts1["geo"].nunique() == len(nuts1),
      "Duplicate geo codes in nuts1_lookup")

# ── DIGITAL SKILLS ────────────────────────────────────────────────────────────

print("\n=== DIGITAL SKILLS ===")

dsk = pd.read_csv(PROCESSED_DIR / "digital_skills_nuts1_labeled_filtered.csv")

check("digital_skills has required columns",
      all(c in dsk.columns for c in ["geo", "year", "indic_is", "unit", "value"]))
check("digital_skills has 2025 data", 2025 in dsk["year"].unique(),
      f"Years present: {sorted(dsk['year'].unique())}")
check("I_DSK2_BAB + PC_IND present",
      ((dsk["indic_is"] == "I_DSK2_BAB") & (dsk["unit"] == "PC_IND")).any(),
      "Selected indicator/unit combination not found")

dsk_2025 = dsk[(dsk["year"] == 2025) & (dsk["indic_is"] == "I_DSK2_BAB") & (dsk["unit"] == "PC_IND")]
check("digital_skills 2025: >=80 NUTS-1 regions", dsk_2025["geo"].nunique() >= 80,
      f"Only {dsk_2025['geo'].nunique()} regions in 2025")
check("digital_skills 2025: no missing values", dsk_2025["value"].isna().sum() == 0,
      f"{dsk_2025['value'].isna().sum()} missing values")
check("digital_skills 2025: values in plausible range (0-100)",
      dsk_2025["value"].between(0, 100).all(),
      f"Range: {dsk_2025['value'].min():.1f}–{dsk_2025['value'].max():.1f}")

# Known: TR/RS present (candidate countries from GISCO — removed in 02_EDA EU27 filter)
non_eu_in_filter = dsk[dsk["geo"].str[:2].isin(["TR", "RS"])]["geo"].nunique()
check("TR/RS regions present in filtered file (known, removed in EU27 filter)",
      non_eu_in_filter == 14, f"Expected 14, found {non_eu_in_filter}",
      level="warn")

# ── POPULATION WEIGHTS ────────────────────────────────────────────────────────

print("\n=== POPULATION WEIGHTS ===")

pop = pd.read_csv(PROCESSED_DIR / "population_nuts2_total_long.csv")

check("population file has required columns",
      all(c in pop.columns for c in ["geo", "year", "population", "parent_nuts1"]))
check("population has 2025 data", 2025 in pop["year"].unique(),
      f"Max year: {pop['year'].max()}")
pop_2025 = pop[pop["year"] == 2025]
check("population 2025: >=250 NUTS-2 regions", pop_2025["geo"].nunique() >= 250,
      f"Only {pop_2025['geo'].nunique()} regions")
check("population 2025: no missing values", pop_2025["population"].isna().sum() == 0,
      f"{pop_2025['population'].isna().sum()} missing")
eu27 = {"AT","BE","BG","CY","CZ","DE","DK","EE","EL","ES","FI","FR",
        "HR","HU","IE","IT","LT","LU","LV","MT","NL","PL","PT","RO","SE","SI","SK"}
pop_2025_eu27 = pop_2025[pop_2025["parent_nuts1"].str[:2].isin(eu27)]
check("population values positive (EU27 NUTS-2 regions)",
      (pop_2025_eu27["population"] > 0).all(),
      f"Non-positive values: {pop_2025_eu27[pop_2025_eu27['population'] <= 0][['geo','population']].to_string()}")

# ── POVERTY WEIGHTING FORMULA ─────────────────────────────────────────────────

print("\n=== POVERTY WEIGHTING (spot-checks) ===")

pov_result = pd.read_csv(PROCESSED_DIR / "poverty_social_exclusion_nuts1_weighted.csv")
pov_mapped = pd.read_csv(PROCESSED_DIR / "poverty_social_exclusion_mapped.csv")

pov_nuts2_2025 = pov_mapped[
    (pov_mapped["parent_nuts1"].notna()) &
    (pov_mapped["year"] == 2025)
].copy()
if "unit" in pov_nuts2_2025.columns:
    pov_nuts2_2025 = pov_nuts2_2025[pov_nuts2_2025["unit"] == "PC_POP"]

pop_weights = pop[["geo", "year", "population", "parent_nuts1"]].copy()
joined = pov_nuts2_2025.merge(pop_weights, on=["geo", "year", "parent_nuts1"], how="left")

check("poverty 2025: all NUTS-2 rows have population match",
      joined["population"].isna().sum() == 0,
      f"{joined['population'].isna().sum()} rows without population match")

pov_2025 = pov_result[pov_result["year"] == 2025]
check("poverty 2025: no coverage > 1.0", (pov_2025["population_coverage_share"] <= 1.001).all(),
      "Coverage share exceeds 1.0 — denominator error")
check("poverty 2025: no coverage <= 0", (pov_2025["population_coverage_share"] > 0).all())

# Spot-check formula for DE1 and FR1
for nuts1_code in ["DE1", "FR1"]:
    row = pov_2025[pov_2025["geo"] == nuts1_code]
    if row.empty:
        check(f"poverty spot-check {nuts1_code}: present in result", False,
              f"{nuts1_code} not in poverty result")
        continue
    stored = row["poverty_social_exclusion_rate"].iloc[0]
    children = joined[
        (joined["parent_nuts1"] == nuts1_code) &
        joined["population"].notna() &
        joined["value"].notna()
    ]
    if children.empty:
        check(f"poverty spot-check {nuts1_code}: child regions found", False)
        continue
    manual = (children["value"] * children["population"]).sum() / children["population"].sum()
    check(f"poverty spot-check {nuts1_code}: formula correct",
          abs(manual - stored) < 0.01,
          f"Stored={stored:.4f}, Manual={manual:.4f}")

# ── POVERTY COVERAGE ─────────────────────────────────────────────────────────

print("\n=== POVERTY COVERAGE ===")

check("poverty result 2025: >=80 regions", pov_2025["geo"].nunique() >= 80,
      f"Only {pov_2025['geo'].nunique()} regions")
check("FI1 present with coverage ~75%",
      not pov_2025[pov_2025["geo"] == "FI1"].empty and
      abs(pov_2025[pov_2025["geo"] == "FI1"]["population_coverage_share"].iloc[0] - 0.75) < 0.02,
      "FI1 coverage unexpected")
check("FRY present with coverage ~86%",
      not pov_2025[pov_2025["geo"] == "FRY"].empty and
      abs(pov_2025[pov_2025["geo"] == "FRY"]["population_coverage_share"].iloc[0] - 0.857) < 0.02,
      "FRY coverage unexpected")

# ── DATA CATALOG ──────────────────────────────────────────────────────────────

print("\n=== DATA CATALOG ===")

catalog = pd.read_csv(PROCESSED_DIR / "project_data_catalog.csv")
expected_codes = ["isoc_r_dskl_i", "tgs00107", "demo_r_d2jan",
                  "edat_lfse_04", "trng_lfse_04", "lfst_r_lfu3pers", "isoc_r_eb_ain2",
                  "lfst_r_lfu3rt", "demo_r_pjanaggr3"]
for code in expected_codes:
    check(f"catalog contains {code}", code in catalog["dataset_code"].values)

check("catalog has downloaded_at column", "downloaded_at" in catalog.columns)
check("catalog: all downloaded_at values present",
      catalog["downloaded_at"].notna().all(),
      f"{catalog['downloaded_at'].isna().sum()} entries missing timestamp")
check("catalog: all files exist on disk",
      all((PROCESSED_DIR / f).exists() for f in catalog["processed_file"]),
      "One or more catalog files not found on disk")

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
