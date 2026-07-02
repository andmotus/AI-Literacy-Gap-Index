# AI Literacy Gap Index

A regional, proxy-based risk index identifying where AI literacy gaps may reinforce
existing inequalities across **87 NUTS-1 regions of the EU-27** (reference year 2025).
Built entirely from official **Eurostat** open data.

Contributing to **SDG 10** (Reduced Inequalities), **SDG 4** (Quality Education) and
**SDG 16** (Peace, Justice and Strong Institutions).

> 📄 **Full write-up — problem, methodology, results, recommendations — is in
> [`DOCUMENTATION.md`](DOCUMENTATION.md).** This README only covers how to run the project.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

Run the notebooks in order — each reads the previous one's output:

```bash
jupyter notebook notebooks/01_load_data.ipynb   # download raw Eurostat data → tidy CSVs
#                02_EDA.ipynb                    # cleaning, weighting → pillar_feature_table.csv
#                03_index_construction.ipynb     # normalisation + PCA weighting → index CSV
#                04_clustering.ipynb             # K-Means risk typology → clustered CSV
#                05_index_mapping.ipynb          # GeoJSON export for the web map
```

Then launch the interactive dashboard (the final data product):

```bash
streamlit run Streamlit_app/app.py
```

## Structure

```
notebooks/        analysis pipeline (run 01 → 05 in order)
data/processed/   all intermediate and final CSVs + figures
Streamlit_app/    interactive dashboard (final product)
web/              public static web map + optimised GeoJSON
DOCUMENTATION.md  full project write-up
```

**Note:** the processed data is not committed to the repository — simply run the full
pipeline once (`01` → `05`, a few seconds), and `01` downloads the raw Eurostat data
automatically. Because Eurostat revises its figures over time, the numbers may shift
slightly on a fresh run: the results reported in `DOCUMENTATION.md` reflect the data
snapshot of **2 July 2026**.
