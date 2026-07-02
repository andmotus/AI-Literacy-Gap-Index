"""
edvancing — AI Literacy Gap Index
Single-page app: Map, Insights and About are all on this page,
reachable via in-page anchor links in the navbar (#map, #insights, #about).
"""

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from case_studies import (
    CASE_STUDIES,
    CLUSTER_ORDER,
    EU27_AVERAGE,
    FEATURES,
    PILLAR_NAMES,
    PILLAR_SHORT,
)
from edv_theme import (
    BLUE,
    BLUE_DARK,
    BLUE_LIGHT,
    INK_MID,
    SURFACE,
    WHITE,
    inject_edvancing_style,
    render_navbar,
)

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="edvancing — AI Literacy Gap Index",
    page_icon="📊",
    layout="wide",
)

inject_edvancing_style()
render_navbar()

DATA_DIR = Path(__file__).parent / "data"

# Explicit brand color mapping per cluster name, as specified.
CLUSTER_COLORS_BRAND = {
    "Education & Poverty Trap": "#D45C00",        # orange
    "Digital & Retraining Deficit": "#E8A020",    # yellow
    "Ageing Workforce & Training Gap": "#6DB33F", # light green
    "Selective Labour Exclusion": "#00A878",      # dark green
    "Low Structural Risk": "#0085CA",             # blue (brand / best status)
}


# -----------------------------
# Map helpers
# -----------------------------
@st.cache_data
def load_geojson(path: str | None = None):
    p = Path(path) if path else DATA_DIR / "nuts1_ai_literacy_gap.geojson"
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def build_cluster_map(df, geojson, highlight_cluster: str | None = None):
    geo_to_cluster = dict(zip(df["geo"], df["cluster_label"]))
    geo_to_index = dict(zip(df["geo"], df["ai_literacy_gap_index"]))
    geo_to_name = dict(zip(df["geo"], df["nuts1_name"]))

    locations = []
    z = []
    text = []
    cluster_to_z = {c: i for i, c in enumerate(CLUSTER_ORDER)}

    for feature in geojson["features"]:
        geo = feature["properties"].get("NUTS_ID") or feature["properties"].get("geo")
        cluster = geo_to_cluster.get(geo)

        locations.append(geo)

        if cluster is None:
            z.append(-1)
            text.append(f"<b>{feature['properties'].get('NAME_LATN', geo)}</b><br>No index data")
            continue

        if highlight_cluster and cluster != highlight_cluster:
            z.append(-1)
        else:
            z.append(cluster_to_z[cluster])

        idx = geo_to_index.get(geo)
        name = geo_to_name.get(geo, geo)
        text.append(
            f"<b>{name}</b> ({geo})<br>"
            f"Cluster: {cluster}<br>"
            f"AI Literacy Gap Index: {idx:.2f}"
        )

    n = len(CLUSTER_ORDER)
    colors = ["#E5E9ED"] + [CLUSTER_COLORS_BRAND[c] for c in CLUSTER_ORDER]
    span = n + 1
    colorscale = []
    for i, c in enumerate(colors):
        frac = i / span
        colorscale.append([frac, c])
        colorscale.append([(i + 1) / span, c])

    fig = go.Figure(
        go.Choropleth(
            geojson=geojson,
            locations=locations,
            z=z,
            featureidkey="properties.NUTS_ID",
            colorscale=colorscale,
            zmin=-1,
            zmax=n - 1,
            showscale=False,
            text=text,
            hovertemplate="%{text}<extra></extra>",
            marker_line_color=WHITE,
            marker_line_width=0.6,
        )
    )

    fig.update_geos(
        scope="europe",
        projection_type="natural earth",
        showcountries=True,
        countrycolor="rgba(150,150,150,0.4)",
        showland=True,
        landcolor="#EDF1F5",
        showocean=True,
        oceancolor=SURFACE,
        showlakes=True,
        lakecolor=SURFACE,
        showcoastlines=True,
        coastlinecolor="rgba(150,150,150,0.5)",
        coastlinewidth=0.5,
        lataxis_range=[33, 71],
        lonaxis_range=[-12, 35],
        bgcolor="rgba(0,0,0,0)",
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=560,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        dragmode=False,
        font=dict(family="DM Sans, sans-serif", color=INK_MID),
    )

    return fig


# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_DIR / "ai_literacy_gap_index_clustered.csv")
    return df


df = load_data()

try:
    geojson = load_geojson()
except FileNotFoundError:
    geojson = None


# ════════════════════════════════════════════════════════════════
# SECTION: MAP
# ════════════════════════════════════════════════════════════════
st.markdown('<div id="map"></div>', unsafe_allow_html=True)

st.title("AI Literacy Gap Index")
st.markdown(
    """
    <div class="edv-section-intro">
    A composite risk index across 87 EU27 NUTS-1 regions, built from 6 pillars:
    digital skills, poverty, education, lifelong learning, unemployment
    (low-educated), and demographics. Regions are grouped into <b>5 clusters</b>
    by <i>risk profile type</i> — not just <i>risk level</i>. Use the map below
    to explore individual regions, and scroll down to <b>Insights</b> for the
    full cluster-by-cluster breakdown, or <b>About</b> for the project
    background and methodology.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="edv-info-card">
    <b>How to use this map</b><br>
    Hover or click a region to see its index score, cluster, and pillar breakdown.
    Each cluster is shown in a different color — the legend below explains what
    each color stands for. For the full explanation of why each cluster scores
    as it does, scroll down to <b>Insights</b>.
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Regions covered", "87")
c2.metric("Clusters", "5")
c3.metric("Highest index score", f"{df['ai_literacy_gap_index'].max():.3f}", "Isole (ITG) — most at risk")
c4.metric("Lowest index score", f"{df['ai_literacy_gap_index'].min():.3f}", "West-Nederland (NL3) — least at risk")

st.markdown("## Map of Europe — by cluster")
st.markdown(
    """
    <div class="edv-section-intro">
    This map shows all 87 NUTS-1 regions colored by their assigned cluster.
    edvancing's brand blue marks the strongest-performing cluster; colors
    shift toward orange for clusters with higher structural risk. Click any
    region to see its score, cluster, and pillar breakdown.
    </div>
    """,
    unsafe_allow_html=True,
)

if geojson is not None:
    fig_map = build_cluster_map(df, geojson)
    map_event = st.plotly_chart(
        fig_map,
        use_container_width=True,
        on_select="rerun",
        selection_mode="points",
        key="overview_map",
    )

    legend_cols = st.columns(len(CLUSTER_ORDER))
    for col, cname in zip(legend_cols, CLUSTER_ORDER):
        col.markdown(
            f'<div class="edv-legend-chip">'
            f'<span style="display:inline-block;width:12px;height:12px;'
            f'background-color:{CLUSTER_COLORS_BRAND[cname]};border-radius:3px;"></span>'
            f'{cname}</div>',
            unsafe_allow_html=True,
        )

    selected_points = map_event.selection.get("points", []) if map_event else []
    if selected_points:
        clicked_geo = selected_points[0].get("location")
        region_row = df[df["geo"] == clicked_geo]
        if not region_row.empty:
            r = region_row.iloc[0]
            cluster_color = CLUSTER_COLORS_BRAND[r["cluster_label"]]
            st.markdown(
                f"""
                <div class="edv-region-card" style="--cluster-color: {cluster_color};">
                <div class="edv-region-name">
                    {r['nuts1_name']} ({r['geo']}, {r['country']})
                </div>
                <div class="edv-region-meta">
                    AI Literacy Gap Index: <b>{r['ai_literacy_gap_index']:.3f}</b>
                    &nbsp;&middot;&nbsp; Rank {int(r['rank'])} of 87
                </div>
                <div class="edv-region-meta">
                    Cluster: <b>{r['cluster_label']}</b>
                    &mdash; <i>{CASE_STUDIES[r['cluster_label']]['headline']}</i>
                </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            pillar_str = "  &nbsp;|&nbsp;  ".join(
                f"{PILLAR_SHORT[f]}: {r[f]:.2f}" for f in FEATURES
            )
            st.markdown(
                f'<div class="edv-region-pillars">{pillar_str}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f"For the full explanation of why **{r['cluster_label']}** regions "
                f"score as they do — including example regions and policy "
                f"suggestions — scroll down to **Insights**."
            )
    else:
        st.caption("Click any region on the map to see its index score, cluster, and pillar breakdown.")

else:
    st.info(
        "Map data not found. Copy `web/data/nuts1_ai_literacy_gap.geojson` "
        "into `Streamlit_app/data/` to enable the map view."
    )


# ════════════════════════════════════════════════════════════════
# SECTION: INSIGHTS
# ════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div id="insights"></div>', unsafe_allow_html=True)

st.title("Insights")
st.markdown(
    """
    <div class="edv-section-intro">
    Each cluster groups regions with a <b>similar risk profile shape</b> —
    not just a similar overall score. The chart for each cluster shows its
    mean pillar scores against the EU27 average, which is the basis for the
    "why" explanation below. Use the tabs to explore each of the 5 clusters,
    see representative regions, and read a suggested policy angle.
    </div>
    """,
    unsafe_allow_html=True,
)

tabs = st.tabs(CLUSTER_ORDER)

for tab, cluster_choice in zip(tabs, CLUSTER_ORDER):
    with tab:
        case = CASE_STUDIES[cluster_choice]
        color = CLUSTER_COLORS_BRAND[cluster_choice]

        st.markdown(f"### {cluster_choice}")
        st.markdown(f"*{case['headline']}*")

        m1, m2, m3 = st.columns(3)
        m1.metric("Regions in cluster", case["n_regions"])
        m2.metric("Mean index score", f"{case['mean_index']:.3f}")
        m3.metric(
            "Rank among 5 clusters",
            f"{CLUSTER_ORDER.index(cluster_choice) + 1} of 5",
            help="1 = highest mean risk, 5 = lowest",
        )

        col_chart, col_drivers = st.columns([2, 1])

        with col_chart:
            cluster_df = df[df["cluster_label"] == cluster_choice]
            cluster_means = cluster_df[FEATURES].mean()

            fig = go.Figure()
            fig.add_trace(
                go.Bar(
                    x=[PILLAR_SHORT[f] for f in FEATURES],
                    y=[EU27_AVERAGE[f] for f in FEATURES],
                    name="EU27 average",
                    marker_color="#D9DEE3",
                )
            )
            fig.add_trace(
                go.Bar(
                    x=[PILLAR_SHORT[f] for f in FEATURES],
                    y=[cluster_means[f] for f in FEATURES],
                    name=cluster_choice,
                    marker_color=color,
                )
            )
            fig.update_layout(
                barmode="group",
                yaxis=dict(title="Risk score (0-1)", range=[0, 1], gridcolor="#EDF1F5"),
                xaxis=dict(gridcolor="#EDF1F5"),
                height=380,
                legend=dict(orientation="h", y=-0.2),
                margin=dict(t=10),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans, sans-serif", color=INK_MID),
            )
            st.plotly_chart(fig, use_container_width=True, key=f"bar_{cluster_choice}")

        with col_drivers:
            st.markdown("**Main risk drivers**")
            if case["drivers"]:
                for d in case["drivers"]:
                    st.markdown(
                        f'<span class="driver-tag">{PILLAR_NAMES[d]}</span>',
                        unsafe_allow_html=True,
                    )
                st.caption("Pillars where this cluster sits clearly above the EU27 average.")
            else:
                st.markdown("*None — all pillars at or below EU27 average.*")

        st.markdown("#### Why this score?")
        st.markdown(case["why"])

        st.markdown("#### What it means")
        st.markdown(case["what_it_means"])

        st.markdown("#### Where this cluster is")
        st.markdown(
            """
            <div class="edv-section-intro" style="margin-bottom:0.5rem;">
            Highlighted regions belong to this cluster; all other regions are
            shown in grey for context.
            </div>
            """,
            unsafe_allow_html=True,
        )
        if geojson is not None:
            fig_cluster_map = build_cluster_map(df, geojson, highlight_cluster=cluster_choice)
            st.plotly_chart(fig_cluster_map, use_container_width=True, key=f"map_{cluster_choice}")
        else:
            st.info(
                "Map data not found. Copy `web/data/nuts1_ai_literacy_gap.geojson` "
                "into `Streamlit_app/data/` to enable the map view."
            )

        st.markdown("#### Representative regions")
        for geo, name, note in case["example_regions"]:
            st.markdown(
                f'<div class="region-card"><b>{name}</b> ({geo})<br>{note}</div>',
                unsafe_allow_html=True,
            )

        st.markdown("#### Policy angle")
        st.info(case["policy_angle"])

        with st.expander(f"All {case['n_regions']} regions in this cluster"):
            member_df = (
                df[df["cluster_label"] == cluster_choice]
                .sort_values("ai_literacy_gap_index", ascending=False)
                [["rank", "geo", "country", "nuts1_name", "ai_literacy_gap_index"]]
                .rename(columns={
                    "rank": "Rank",
                    "geo": "NUTS-1",
                    "country": "Country",
                    "nuts1_name": "Region",
                    "ai_literacy_gap_index": "Index score",
                })
            )
            st.dataframe(member_df, use_container_width=True, hide_index=True)

# Cross-cluster comparison
st.markdown("## Cross-cluster comparison")
st.markdown(
    """
    <div class="edv-section-intro">
    These two charts put all clusters side by side: a scatter plot ranking
    all 87 regions by their index score, and a heatmap showing each
    cluster's average score on every pillar.
    </div>
    """,
    unsafe_allow_html=True,
)

with st.expander("All regions scatter & cluster fingerprints", expanded=True):
    st.markdown("#### All 87 regions, by cluster")
    fig_scatter = px.scatter(
        df,
        x="rank",
        y="ai_literacy_gap_index",
        color="cluster_label",
        category_orders={"cluster_label": CLUSTER_ORDER},
        color_discrete_map=CLUSTER_COLORS_BRAND,
        hover_data={"geo": True, "country": True, "nuts1_name": True, "rank": False},
        labels={
            "rank": "Rank (1 = highest risk)",
            "ai_literacy_gap_index": "AI Literacy Gap Index",
            "cluster_label": "Cluster",
        },
        height=480,
    )
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.85, line=dict(width=0.5, color=WHITE)))
    fig_scatter.update_layout(
        legend=dict(orientation="h", y=-0.2),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=INK_MID),
        xaxis=dict(gridcolor="#EDF1F5"),
        yaxis=dict(gridcolor="#EDF1F5"),
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("#### Cluster fingerprints — mean pillar scores")
    st.caption("0 = no risk on this dimension, 1 = maximum risk. This is the basis for each case study.")

    profile = (
        df.groupby("cluster_label")[FEATURES]
        .mean()
        .reindex(CLUSTER_ORDER)
        .rename(columns=PILLAR_SHORT)
    )
    fig_heatmap = go.Figure(
        data=go.Heatmap(
            z=profile.values,
            x=profile.columns,
            y=profile.index,
            colorscale=[[0, BLUE_LIGHT], [0.5, BLUE], [1, "#C0392B"]],
            zmin=0,
            zmax=1,
            text=profile.round(2).values,
            texttemplate="%{text}",
            colorbar=dict(title="Risk"),
        )
    )
    fig_heatmap.update_layout(
        height=350,
        yaxis=dict(autorange="reversed"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="DM Sans, sans-serif", color=INK_MID),
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)


# ════════════════════════════════════════════════════════════════
# SECTION: ABOUT
# ════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown('<div id="about"></div>', unsafe_allow_html=True)

st.title("About edvancing")
st.markdown(
    """
    <div class="edv-section-intro">
    edvancing is a project by students of <b>Tomorrow University of Applied
    Sciences</b>, created by <b>Asel Mamatbekova, Eric Götz, Joshua Kehrer
    and Lukas Müller</b>. The project maps structural gaps in digital and AI
    literacy across the EU27, with the goal of raising awareness about
    unequal access to digital education — and showing where the need for
    AI literacy support is greatest.
    </div>
    """,
    unsafe_allow_html=True,
)

# SDG alignment
st.markdown("## SDG alignment")
st.markdown(
    """
    <div class="edv-section-intro">
    edvancing directly addresses three UN Sustainable Development Goals,
    focusing on educational equity, regional inequality, and the
    institutional capacity needed to act on both.
    </div>
    """,
    unsafe_allow_html=True,
)

sdg1, sdg2, sdg3 = st.columns(3)

with sdg1:
    st.markdown(
        f"""
        <div class="edv-team-card" style="text-align:left;">
        <span class="edv-sdg-badge">SDG 4</span><br>
        <b>Quality Education</b><br><br>
        edvancing measures gaps in digital skills and lifelong learning
        across European regions — the core barriers to equal access to
        AI-related education.
        </div>
        """,
        unsafe_allow_html=True,
    )

with sdg2:
    st.markdown(
        f"""
        <div class="edv-team-card" style="text-align:left;">
        <span class="edv-sdg-badge">SDG 10</span><br>
        <b>Reduced Inequalities</b><br><br>
        By comparing 87 NUTS-1 regions, edvancing makes regional disparities
        in digital readiness visible — a prerequisite for targeted,
        place-based policy.
        </div>
        """,
        unsafe_allow_html=True,
    )

with sdg3:
    st.markdown(
        f"""
        <div class="edv-team-card" style="text-align:left;">
        <span class="edv-sdg-badge">SDG 16</span><br>
        <b>Strong Institutions</b><br><br>
        The dashboard is designed as a transparent, evidence-based tool for
        policymakers and public institutions to act on AI literacy gaps.
        </div>
        """,
        unsafe_allow_html=True,
    )

# Methodology
st.markdown("## Methodology")
st.markdown(
    """
    <div class="edv-section-intro">
    The AI Literacy Gap Index is a proxy-based risk index, not a direct
    measurement of AI literacy. It is built from six pillars sourced from
    Eurostat, combined into a single composite score per NUTS-1 region.
    </div>
    """,
    unsafe_allow_html=True,
)

method_steps = [
    ("1", "Variable selection", "Six pillars were selected from Eurostat regional datasets: digital skills, "
                                  "at-risk-of-poverty rate, education level, lifelong learning participation, "
                                  "unemployment among the low-educated, and population demographics."),
    ("2", "Normalisation", "All variables are normalised to a 0–1 risk scale. Variables where a higher "
                            "value indicates lower risk are inverted, so that 1 always represents the "
                            "highest structural risk."),
    ("3", "Composite scoring", "The six normalised scores are combined into the AI Literacy Gap Index. "
                                "The methodology and weighting are documented transparently and can be "
                                "adjusted."),
    ("4", "Clustering", "Regions are grouped into five clusters using unsupervised clustering on the "
                         "six underlying pillars — grouping regions by risk profile shape, not just "
                         "overall score."),
]

for num, title, text in method_steps:
    c_num, c_text = st.columns([0.06, 0.94])
    with c_num:
        st.markdown(
            f"""
            <div style="width:32px;height:32px;border-radius:8px;background-color:{BLUE_LIGHT};
                        color:{BLUE_DARK};display:flex;align-items:center;justify-content:center;
                        font-weight:600;font-size:14px;">{num}</div>
            """,
            unsafe_allow_html=True,
        )
    with c_text:
        st.markdown(f"**{title}**")
        st.markdown(f'<div class="edv-section-intro" style="margin-top:-4px;">{text}</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="edv-info-card">
    <b>Note:</b> This index is a <b>proxy-based risk measure</b>, not a direct
    measurement of AI literacy. It reflects structural conditions that
    correlate with AI literacy outcomes.
    </div>
    """,
    unsafe_allow_html=True,
)

# Data sources
st.markdown("## Data sources")
st.markdown(
    """
    <div class="edv-section-intro">
    All data is sourced from Eurostat regional statistics (NUTS-1 level, EU27, 2025):
    </div>
    """,
    unsafe_allow_html=True,
)

sources = [
    ("isoc_r_dskl_i", "Individuals' level of digital skills"),
    ("tgs00107", "People at risk of poverty or social exclusion"),
    ("edat_lfse_04", "Population by educational attainment level"),
    ("trng_lfse_04", "Participation in education and training (lifelong learning)"),
    ("lfst_r_lfu3rt", "Unemployment rate by educational attainment"),
    ("demo_r_pjanaggr3", "Population by broad age group"),
]

for code, desc in sources:
    st.markdown(
        f'<div class="region-card"><b>{code}</b><br>{desc}</div>',
        unsafe_allow_html=True,
    )

st.markdown("---")
st.caption(
    "edvancing · Tomorrow University of Applied Sciences · 2025. "
    "Data: Eurostat (isoc_r_dskl_i, tgs00107, edat_lfse_04, trng_lfse_04, "
    "lfst_r_lfu3rt, demo_r_pjanaggr3), 2025."
)
