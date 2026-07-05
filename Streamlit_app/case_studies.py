"""
Cluster case study content for the AI Literacy Gap Index.

Five clusters describe different structural risk profiles across
87 EU27 NUTS-1 regions. Each entry explains which pillars drive
the risk in that cluster, with representative regions and a
suggested policy angle.

Note: clusters represent types of structural risk, not a ranking.
Colors and order do not imply one cluster is worse than another —
each describes a different pattern of risk drivers.
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

# Clusters listed as types — order does not imply risk ranking
CLUSTER_ORDER = [
    "High Poverty & Low Education",
    "Low Digital Skills",
    "Ageing Workforce",
    "Low-Skill Unemployment",
    "Broadly Resilient",
]

CLUSTER_COLORS = {
    "High Poverty & Low Education": "#d62728",
    "Low Digital Skills": "#ff7f0e",
    "Ageing Workforce": "#1f77b4",
    "Low-Skill Unemployment": "#2ca02c",
    "Broadly Resilient": "#9467bd",
}

CASE_STUDIES = {
    "High Poverty & Low Education": {
        "headline": (
            "Poverty and low educational attainment reinforce each other "
            "\u2014 the gap can\u2019t be closed with digital courses alone"
        ),
        "n_regions": 9,
        "mean_index": 0.597,
        "drivers": ["P2_norm", "P3_norm", "P4_norm"],
        "why": (
            "These regions combine **high poverty/social exclusion (P2, 0.67)** "
            "with **very high shares of adults without post-compulsory education "
            "(P3, 0.73)**. Low lifelong learning participation (P4, 0.76) is "
            "elevated too \u2014 but here it is best understood as a *consequence* "
            "of the other two, not an independent driver. People facing poverty and "
            "low baseline education have far less capacity to engage with "
            "retraining, regardless of what programmes are on offer."
        ),
        "what_it_means": (
            "The AI literacy gap here is broad and deeply embedded in the regional "
            "economy and history, rather than being a recent or isolated issue. "
            "Digital skills (P1, 0.50) and demographics (P6, 0.48) sit close to "
            "the EU27 average \u2014 so this is not primarily a \u2018too few computers\u2019 or "
            "\u2018too many retirees\u2019 story. It\u2019s a socioeconomic one."
        ),
        "example_regions": [
            ("ITG", "Isole (Italy)",
             "Rank 1 \u2014 highest index score in the entire dataset (0.728)"),
            ("ITF", "Sud (Italy)",
             "Rank 2 \u2014 second-highest overall (0.698)"),
            ("FRY", "RUP FR \u2014 R\u00e9gions Ultrep\u00e9riph\u00e9riques Fran\u00e7aises",
             "Rank 3 (0.685) \u2014 Note: Mayotte data missing, actual poverty likely higher"),
        ],
        "policy_angle": (
            "Structural, long-horizon response needed: combine income support with "
            "foundational adult education before digital upskilling can land. "
            "Tie ESF+/cohesion funds to integrated education-poverty programmes. "
            "(SDG 10 + 4)"
        ),
    },
    "Low Digital Skills": {
        "headline": (
            "Weak digital skills and very little adult retraining "
            "\u2014 skills haven\u2019t kept pace as technology moved on"
        ),
        "n_regions": 21,
        "mean_index": 0.524,
        "drivers": ["P4_norm", "P1_norm", "P6_norm"],
        "why": (
            "This cluster\u2019s risk is driven by: "
            "**near-absent lifelong learning participation (P4, 0.87 \u2014 highest of "
            "any cluster)**, **a substantial digital skills gap (P1, 0.70)**, "
            "and an **ageing population (P6, 0.62)**. Poverty (P2, 0.44) and low "
            "education (P3, 0.19) are close to or below the EU27 average \u2014 so this "
            "is not a story of general deprivation."
        ),
        "what_it_means": (
            "The risk here is specifically about *currency* of skills: people may "
            "have adequate baseline education, but digital competence hasn\u2019t kept "
            "pace, and almost no one is participating in retraining to close that "
            "gap \u2014 in a population that is also getting older. With 21 regions "
            "spanning Eastern Europe, Greece, and parts of Germany, it is the "
            "largest of the higher-risk clusters."
        ),
        "example_regions": [
            ("BG3", "Severna i Yugoiztochna Bulgaria",
             "Rank 4 \u2014 highest in this cluster (0.649)"),
            ("RO2", "Macroregiunea Doi (Romania)",
             "Rank 5 (0.648)"),
            ("DEE", "Sachsen-Anhalt (Germany)",
             "Rank 14 (0.569) \u2014 shows this pattern also occurs in wealthier countries"),
        ],
        "policy_angle": (
            "Adult digital-skills programmes at scale, targeted at mid-career workers; "
            "rebuild lifelong-learning infrastructure. This cluster has the highest "
            "direct SDG 4.4 leverage of all five types. (SDG 4)"
        ),
    },
    "Ageing Workforce": {
        "headline": (
            "A largely stable region with no acute weakness "
            "\u2014 but an ageing workforce gradually at risk of falling behind"
        ),
        "n_regions": 22,
        "mean_index": 0.442,
        "drivers": ["P4_norm", "P6_norm"],
        "why": (
            "This cluster spans 22 regions across France, Italy, Germany, and "
            "Eastern Europe. **Lifelong learning gap (P4, 0.76)** and **ageing "
            "population (P6, 0.75 \u2014 highest of any cluster)** are clearly "
            "elevated, but poverty (P2, 0.28) and low education (P3, 0.28) are "
            "not. No single factor dominates the way it does in the other clusters."
        ),
        "what_it_means": (
            "The risk here is diffuse rather than acute. These regions are not in "
            "crisis on any one dimension, but the combination of the EU\u2019s oldest "
            "average population profile (P6) and persistently low retraining "
            "participation creates a slow-moving structural drag. This cluster is "
            "best understood as \u2018demographically older Europe, with training "
            "participation that hasn\u2019t kept pace\u2019 \u2014 a gradual challenge "
            "rather than an immediate crisis."
        ),
        "example_regions": [
            ("FRM", "Corse (France)",
             "Rank 8 \u2014 highest in this cluster (0.598)"),
            ("ES1", "Noroeste (Spain)",
             "Rank 21 (0.504)"),
            ("FRH", "Bretagne (France)",
             "Rank 68 \u2014 lowest in this cluster (0.357)"),
        ],
        "policy_angle": (
            "Preventive, broad response: workplace-based and age-inclusive digital "
            "training; embed AI literacy in continuing professional development "
            "before the gap becomes acute. (SDG 4)"
        ),
    },
    "Low-Skill Unemployment": {
        "headline": (
            "A well-functioning region with one concentrated blind spot "
            "\u2014 the low-qualified minority falls through every net"
        ),
        "n_regions": 7,
        "mean_index": 0.363,
        "drivers": ["P5_norm"],
        "why": (
            "This is the most counter-intuitive cluster (7 regions). On almost "
            "every dimension these regions look *good*: low poverty (P2=0.32), "
            "**lowest share of low-educated adults of any cluster (P3=0.15)**, "
            "decent digital skills (P1=0.31), and the **lowest lifelong-learning "
            "gap of any cluster (P4=0.32)**. Yet **unemployment among the "
            "low-educated (P5=0.66) is the highest of all five clusters**."
        ),
        "what_it_means": (
            "These are well-functioning labour markets and education systems "
            "for the majority \u2014 but the small minority without post-compulsory "
            "education falls through every net. The risk is not systemic; it is "
            "concentrated in a specific, structurally excluded group. "
            "A ranking would file these regions as \u2018moderate risk\u2019 and prescribe "
            "the wrong medicine \u2014 which is exactly why a typology matters."
        ),
        "example_regions": [
            ("SK0", "Slovensko (Slovakia)",
             "Rank 25 \u2014 highest in this cluster (0.488), driven by P5"),
            ("BE1", "Brussels (Belgium)",
             "Rank 48 (0.418) \u2014 high poverty compounds the P5 signal"),
            ("SE1/SE2/SE3", "Sweden (all 3 regions)",
             "All three Swedish NUTS-1 regions in this cluster \u2014 a national pattern"),
        ],
        "policy_angle": (
            "Targeted outreach, not broad campaigns: active labour-market measures "
            "and individualised re-engagement for a specific hard-to-reach group. "
            "A national \u2018boost digital skills\u2019 programme would largely miss them. "
            "(SDG 10)"
        ),
    },
    "Broadly Resilient": {
        "headline": (
            "No single weakness stands out \u2014 same long-term AI challenges "
            "as everyone else, but from a structurally stronger starting position"
        ),
        "n_regions": 28,
        "mean_index": 0.335,
        "drivers": [],
        "why": (
            "This is the largest cluster (28 of 87 regions). All six pillars sit "
            "at or below the EU27 average \u2014 there is no elevated driver to point "
            "to. It includes the Netherlands (all 4 NUTS-1 regions), Denmark, "
            "Ireland, Luxembourg, and major capital/metropolitan regions "
            "(Berlin, Hamburg, \u00cele-de-France, Madrid, Brussels)."
        ),
        "what_it_means": (
            "These regions face the same long-term AI-driven labour market "
            "transition as the rest of Europe, but from a structurally stronger "
            "starting position: better digital infrastructure (P1=0.30), lower "
            "poverty (P2=0.21), lower low-education shares (P3=0.20), and lower "
            "unemployment among the low-educated (P5=0.20). This doesn\u2019t mean "
            "zero risk \u2014 the lowest score in the dataset is still 0.216 "
            "(West-Nederland) \u2014 but it\u2019s the most favourable starting point "
            "of the five cluster types."
        ),
        "example_regions": [
            ("NL3", "West-Nederland (Netherlands)",
             "Rank 87 \u2014 lowest index score in the entire dataset (0.216)"),
            ("FRE", "Hauts-de-France (France)",
             "Rank 35 (0.449) \u2014 highest in this cluster, shows the cluster spans a wide range"),
            ("DK0", "Danmark (Denmark)",
             "Rank 85 (0.243) \u2014 among the lowest scores in the dataset"),
        ],
        "policy_angle": (
            "Maintain and lead: pilot advanced AI-literacy curricula and act as "
            "exporters of best practice to higher-risk regions. These regions are "
            "not immune \u2014 but they are best placed to lead. (SDG 4 + 16)"
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