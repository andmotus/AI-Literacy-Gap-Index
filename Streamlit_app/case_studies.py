"""
Cluster case study content for the AI Literacy Gap Index.
Each cluster's narrative explains WHY the cluster scores as it does,
based on which pillars are elevated relative to the EU27 average.

Updated to match the corrected cluster output from 04_clustering.ipynb
(cluster naming fixed to be profile-based rather than cluster_id-based).
Cluster sizes: Education & Poverty Trap (9), Digital & Retraining Deficit (21),
Ageing Workforce & Training Gap (22), Selective Labour Exclusion (7),
Low Structural Risk (28).
"""

PILLAR_NAMES = {
    "P1_norm": "Digital Skills Gap",
    "P2_norm": "Poverty / Social Exclusion",
    "P3_norm": "Low Education",
    "P4_norm": "Lifelong Learning Gap",
    "P5_norm": "Unemployment (low-educated)",
    "P6_norm": "Ageing Population",
}

PILLAR_SHORT = {
    "P1_norm": "P1 Digital Skills",
    "P2_norm": "P2 Poverty",
    "P3_norm": "P3 Low Education",
    "P4_norm": "P4 Lifelong Learning",
    "P5_norm": "P5 Unemployment",
    "P6_norm": "P6 Demographics",
}

FEATURES = ["P1_norm", "P2_norm", "P3_norm", "P4_norm", "P5_norm", "P6_norm"]

CLUSTER_ORDER = [
    "Education & Poverty Trap",
    "Digital & Retraining Deficit",
    "Ageing Workforce & Training Gap",
    "Selective Labour Exclusion",
    "Low Structural Risk",
]

CLUSTER_COLORS = {
    "Education & Poverty Trap": "#d62728",
    "Digital & Retraining Deficit": "#ff7f0e",
    "Ageing Workforce & Training Gap": "#1f77b4",
    "Selective Labour Exclusion": "#2ca02c",
    "Low Structural Risk": "#9467bd",
}

CASE_STUDIES = {
    "Education & Poverty Trap": {
        "headline": "Poverty and low education reinforce each other",
        "n_regions": 9,
        "mean_index": 0.597,
        "drivers": ["P2_norm", "P3_norm", "P4_norm"],
        "why": (
            "This is the highest-risk cluster, and the reason is structural: "
            "these regions combine **high poverty/social exclusion (P2, 0.67)** with "
            "**very high shares of adults without post-compulsory education "
            "(P3, 0.73)**. Low lifelong learning participation (P4, 0.76) is "
            "elevated too — but here it is best understood as a *consequence* of "
            "the other two, not an independent driver. People facing poverty and "
            "low baseline education have far less capacity to engage with "
            "retraining, regardless of what programmes are on offer."
        ),
        "what_it_means": (
            "The AI literacy gap here is broad and deeply embedded in the regional "
            "economy and history, rather than being a recent or isolated issue. "
            "Digital skills (P1, 0.50) and demographics (P6, 0.48) sit close to "
            "the EU27 average — so this is not primarily a 'too few computers' or "
            "'too many retirees' story. It's a socioeconomic one."
        ),
        "example_regions": [
            ("ITG", "Isole (Italy)", "Highest-risk region in the entire index (0.728)"),
            ("ITF", "Sud (Italy)", "Second-highest overall (0.698)"),
            ("FRY", "RUP FR \u2014 Régions Ultrapériphériques Françaises", "Third-highest overall (0.685) \u2014 France's overseas regions"),
        ],
        "policy_angle": (
            "Interventions that treat digital skills in isolation are unlikely to work "
            "here. The entry point is more likely to be basic education and poverty "
            "reduction — digital literacy programmes will only land if they're paired "
            "with broader social support (e.g. embedded in adult education or "
            "active labour market programmes, not standalone IT courses)."
        ),
    },
    "Digital & Retraining Deficit": {
        "headline": "Skills haven't kept up — and the population is ageing",
        "n_regions": 21,
        "mean_index": 0.524,
        "drivers": ["P4_norm", "P1_norm", "P6_norm"],
        "why": (
            "This cluster's risk is driven by a different combination: "
            "**near-absent lifelong learning participation (P4, highest of any "
            "cluster at 0.87)**, **a substantial digital skills gap (P1, 0.70)**, "
            "and an **ageing population (P6, 0.62)**. Poverty (P2, 0.44) and low "
            "education (P3, 0.19) are close to or below the EU27 average — so this "
            "is not a story of general deprivation."
        ),
        "what_it_means": (
            "The risk here is specifically about *currency* of skills: people may "
            "have adequate baseline education, but digital competence hasn't kept "
            "pace, and almost no one is participating in retraining to close that "
            "gap — in a population that is also getting older. This is the largest "
            "of the high-risk clusters (21 regions, spanning Eastern Europe, Greece, "
            "and parts of Germany) — a 'falling behind' pattern rather than a "
            "'never had the foundation' pattern."
        ),
        "example_regions": [
            ("BG3", "Severna i Yugoiztochna Bulgaria", "Highest-risk region in this cluster (0.649)"),
            ("RO2", "Macroregiunea Doi (Romania)", "Second-highest in this cluster (0.648)"),
            ("DEE", "Sachsen-Anhalt (Germany)", "Highest P6 (ageing) in the dataset \u2014 shows this pattern also occurs in wealthier countries"),
        ],
        "policy_angle": (
            "This is arguably the most direct 'AI literacy' target group: people with "
            "reasonable educational foundations who need digital upskilling, but "
            "for whom existing retraining offers are not landing — possibly due to "
            "format, accessibility, or relevance to an older workforce. Targeted, "
            "age-appropriate digital training (rather than generic adult education) "
            "is the more promising lever."
        ),
    },
    "Ageing Workforce & Training Gap": {
        "headline": "A large, moderate-risk cluster with no single dominant driver",
        "n_regions": 22,
        "mean_index": 0.442,
        "drivers": ["P4_norm", "P6_norm"],
        "why": (
            "This cluster spans 22 regions across France, Italy, Germany, and "
            "Eastern Europe. **Lifelong learning gap (P4, 0.76)** and **ageing "
            "population (P6, 0.75 \u2014 the highest of any cluster)** are clearly "
            "elevated, but poverty (P2, 0.28) and low education (P3, 0.28) are "
            "not. No single factor dominates the way it does in the higher-risk "
            "clusters."
        ),
        "what_it_means": (
            "The risk here is diffuse rather than acute. These regions are not in "
            "crisis on any one dimension, but the combination of the EU's oldest "
            "average population profile (P6) and persistently low retraining "
            "participation creates a slow-moving structural drag. Because the "
            "signal is spread across two pillars rather than concentrated in one, "
            "this cluster is harder to characterise with a single narrative — it "
            "is essentially 'demographically older Europe, with training "
            "participation that hasn't kept pace'."
        ),
        "example_regions": [
            ("FRM", "Corse (France)", "Highest-risk region in this cluster (0.598)"),
            ("ES1", "Noroeste (Spain)", "Second-highest in this cluster (0.504)"),
            ("FRH", "Bretagne (France)", "Lowest-risk region in this cluster (0.357)"),
        ],
        "policy_angle": (
            "Because risk is broad-based but shallow, this cluster is well suited "
            "to general-purpose lifelong learning policy (e.g. EU Digital Decade "
            "targets, Erasmus+ adult education strands) rather than targeted "
            "regional intervention. It's also a useful 'mid-range' reference point "
            "against which the other four clusters' deviations can be read."
        ),
    },
    "Selective Labour Exclusion": {
        "headline": "A small, sharply excluded group inside otherwise strong regions",
        "n_regions": 7,
        "mean_index": 0.363,
        "drivers": ["P5_norm"],
        "why": (
            "This is the most counter-intuitive cluster, and the smallest (7 "
            "regions). On almost every dimension these regions look *good*: low "
            "poverty (P2=0.32), the **lowest share of low-educated adults of any "
            "cluster (P3=0.15)**, decent digital skills (P1=0.31, second-best), "
            "and the **lowest lifelong-learning gap of any cluster (P4=0.32)**. "
            "Yet **unemployment among the low-educated (P5=0.66) is the highest "
            "of all five clusters** — including Slovakia at the top of this "
            "cluster's range."
        ),
        "what_it_means": (
            "These are well-functioning labour markets and education systems "
            "for the majority — but the small minority without post-compulsory "
            "education falls through every net. The risk is not systemic; it's "
            "concentrated in a specific, structurally excluded group. This makes "
            "the overall index score for this cluster (0.363, second-lowest) "
            "somewhat misleading on its own — it understates how severe the "
            "problem is *for the people it actually affects*."
        ),
        "example_regions": [
            ("SK0", "Slovensko (Slovakia)", "Highest-risk region in this cluster (0.488) \u2014 driven by P5"),
            ("BE1", "Brussels (Belgium)", "Second-highest in this cluster (0.418) \u2014 high P2 (poverty) compounds the P5 signal"),
            ("SE1/SE2/SE3", "Sweden (all 3 regions)", "All three Swedish NUTS-1 regions fall in this cluster \u2014 a national pattern, not a regional anomaly"),
        ],
        "policy_angle": (
            "Generic digital-skills or education campaigns will largely miss this "
            "group, because the issue isn't education access at the population "
            "level — it's labour-market integration for a specific minority. "
            "Targeted active labour market programmes (subsidised employment, "
            "tailored job-matching for low-educated adults) are more relevant "
            "than broad digital-literacy investment."
        ),
    },
    "Low Structural Risk": {
        "headline": "The largest cluster — strong starting position across the board",
        "n_regions": 28,
        "mean_index": 0.335,
        "drivers": [],
        "why": (
            "This is the largest cluster (28 of 87 regions) and the lowest-risk "
            "overall. All six pillars sit at or below the EU27 average — there is "
            "no elevated driver to point to. It includes the Netherlands (all 4 "
            "NUTS-1 regions), Denmark, Ireland, Luxembourg, and major "
            "capital/metropolitan regions (Berlin, Hamburg, Île-de-France, "
            "Madrid)."
        ),
        "what_it_means": (
            "These regions face the same long-term AI-driven labour market "
            "transition as the rest of Europe, but from a structurally stronger "
            "starting position: better digital infrastructure (P1=0.30), lower "
            "poverty (P2=0.21) and low-education shares (P3=0.20), and lower "
            "unemployment among the low-educated (P5=0.20). This doesn't mean "
            "zero risk — the lowest score in the dataset is still 0.216 "
            "(West-Nederland), not zero — but it's the most favourable starting "
            "point of the five clusters."
        ),
        "example_regions": [
            ("NL3", "West-Nederland (Netherlands)", "Lowest index score in the entire dataset (0.216)"),
            ("FRE", "Hauts-de-France (France)", "Highest-risk region in this cluster (0.449) \u2014 shows the cluster still spans a wide range"),
            ("DK0", "Danmark (Denmark)", "Among the lowest scores in the dataset (0.243)"),
        ],
        "policy_angle": (
            "These regions are reasonable benchmarks/reference points for what "
            "'good' looks like on each pillar — useful for setting realistic "
            "targets for regions in the other four clusters, rather than a "
            "primary intervention target themselves."
        ),
    },
}

EU27_AVERAGE = {
    "P1_norm": 0.440,
    "P2_norm": 0.339,
    "P3_norm": 0.267,
    "P4_norm": 0.711,
    "P5_norm": 0.271,
    "P6_norm": 0.572,
}