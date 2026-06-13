"""
AI Literacy Gap Index — Cluster Case Studies
Streamlit app explaining WHY each of the 5 regional clusters scores as it does.
"""

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

from case_studies import (
    CASE_STUDIES,
    CLUSTER_COLORS,
    CLUSTER_ORDER,
    EU27_AVERAGE,
    FEATURES,
    PILLAR_NAMES,
    PILLAR_SHORT,
)

# -----------------------------
# Page config & light styling
# -----------------------------
st.set_page_config(
    page_title="AI Literacy Gap Index — Cluster Case Studies",
    page_icon="🇪🇺",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main { font-family: 'IBM Plex Sans', sans-serif; }
    h1, h2, h3 { font-family: 'IBM Plex Sans', sans-serif; }
    .driver-tag {
        display: inline-block;
        background-color: #2c3e50;
        color: white;
        border-radius: 4px;
        padding: 2px 10px;
        margin-right: 6px;
        margin-bottom: 6px;
        font-size: 0.85rem;
    }
    .region-card {
        background-color: #f8f9fa;
        border-left: 4px solid #2c3e50;
        border-radius: 4px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Map helpers
# -----------------------------
@st.cache_data
def load_geojson(path: str = "data/nuts1_ai_literacy_gap.geojson"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_cluster_map(df, geojson, highlight_cluster: str | None = None):
    """
    Build a Plotly choropleth of all NUTS-1 regions colored by cluster_label.
    If highlight_cluster is given, regions in other clusters are shown in grey
    and only the selected cluster gets its color.
    """
    # Map geo -> cluster_label and index from our (corrected) dataframe
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
            z.append(-1)  # no index data -> grey
            text.append(f"{feature['properties'].get('NAME_LATN', geo)}<br>No index data")
            continue

        if highlight_cluster and cluster != highlight_cluster:
            z.append(-1)  # not the selected cluster -> grey
        else:
            z.append(cluster_to_z[cluster])

        idx = geo_to_index.get(geo)
        name = geo_to_name.get(geo, geo)
        text.append(
            f"<b>{name}</b> ({geo})<br>"
            f"Cluster: {cluster}<br>"
            f"AI Literacy Gap Index: {idx:.2f}"
        )

    # Build a discrete colorscale: -1 = grey, 0..4 = cluster colors
    n = len(CLUSTER_ORDER)
    colors = ["#d9d9d9"] + [CLUSTER_COLORS[c] for c in CLUSTER_ORDER]
    # colorscale needs values in [0,1]; map -1..n-1 onto that range
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
            marker_line_color="white",
            marker_line_width=0.6,
        )
    )

    fig.update_geos(
        scope="europe",
        projection_type="natural earth",
        showcountries=True,
        countrycolor="rgba(150,150,150,0.5)",
        showland=True,
        landcolor="#f2f0e9",
        showocean=True,
        oceancolor="#dceefb",
        showlakes=True,
        lakecolor="#dceefb",
        showcoastlines=True,
        coastlinecolor="rgba(150,150,150,0.6)",
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

    )

    return fig


# -----------------------------
# Data loading
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/ai_literacy_gap_index_clustered.csv")
    return df


df = load_data()

# Geo data for the map view - falls back gracefully if not present yet
try:
    geojson = load_geojson("data/nuts1_ai_literacy_gap.geojson")
except FileNotFoundError:
    geojson = None

# -----------------------------
# Header
# -----------------------------
st.title("AI Literacy Gap Index")
st.markdown(
    "A composite risk index across 87 EU27 NUTS-1 regions, built from 6 pillars: "
    "digital skills, poverty, education, lifelong learning, unemployment "
    "(low-educated), and demographics. Regions are grouped into **5 clusters** "
    "by *risk profile type* — not just *risk level*."
)

st.markdown(
    """
    <div style="background-color:#eef5fc; border-radius:8px; padding:14px 18px;
                border-left:4px solid #1f77b4; margin-bottom:1rem;">
    <b>How to use this page</b><br>
    1. Hover or click a region on the map below to see its score, cluster, and risk profile.<br>
    2. Scroll down to <b>Cluster case studies</b> and pick a tab to see why that group of
    regions scores as it does, with example regions and policy suggestions.<br>
    3. Open <b>More data</b> at the bottom for the full ranked list and cluster comparisons.
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Regions covered", "87")
c2.metric("Clusters", "5")
c3.metric("Highest index score", f"{df['ai_literacy_gap_index'].max():.3f}", "Isole (ITG) — most at risk")
c4.metric("Lowest index score", f"{df['ai_literacy_gap_index'].min():.3f}", "West-Nederland (NL3) — least at risk")

# -----------------------------
# Map section - click a region for details
# -----------------------------
st.markdown("## Map of Europe — by cluster")
st.caption("Click any region below to see its score, cluster, and pillar breakdown.")

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
            f'<span style="display:inline-block;width:12px;height:12px;'
            f'background-color:{CLUSTER_COLORS[cname]};border-radius:2px;'
            f'margin-right:6px;"></span>{cname}',
            unsafe_allow_html=True,
        )

    selected_points = map_event.selection.get("points", []) if map_event else []
    if selected_points:
        clicked_geo = selected_points[0].get("location")
        region_row = df[df["geo"] == clicked_geo]
        if not region_row.empty:
            r = region_row.iloc[0]
            cluster_color = CLUSTER_COLORS[r["cluster_label"]]
            st.markdown(
                f"""
                <div style="background-color:#f8f9fa; border-radius:8px;
                            padding:16px 20px; margin-top:0.5rem;
                            border-left:5px solid {cluster_color};">
                <div style="font-size:1.1rem; font-weight:600;">
                    {r['nuts1_name']} ({r['geo']}, {r['country']})
                </div>
                <div style="margin-top:4px;">
                    AI Literacy Gap Index: <b>{r['ai_literacy_gap_index']:.3f}</b>
                    &nbsp;&middot;&nbsp; Rank {int(r['rank'])} of 87
                </div>
                <div style="margin-top:4px;">
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
                f'<div style="margin-top:6px; color:var(--color-text-secondary, #666); '
                f'font-size:0.85rem;">{pillar_str}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f"Go to the **{r['cluster_label']}** tab below to see why "
                f"this region scores as it does, with example regions and "
                f"a suggested policy angle."
            )
    else:
        st.caption("Click any region on the map to see its index score, cluster, and pillar breakdown.")

else:
    st.info(
        "Map data not found. Copy `web/data/nuts1_ai_literacy_gap.geojson` "
        "into `Streamlit_app/data/` to enable the map view."
    )

# -----------------------------
# Cluster case studies - tabs
# -----------------------------
st.markdown("## Cluster case studies")
st.markdown(
    "Each cluster groups regions with a **similar risk profile shape** — "
    "not just a similar overall score. The chart for each cluster shows "
    "its mean pillar scores against the EU27 average, which is the basis "
    "for the 'why' explanation below."
)

tabs = st.tabs(CLUSTER_ORDER)

for tab, cluster_choice in zip(tabs, CLUSTER_ORDER):
    with tab:
        case = CASE_STUDIES[cluster_choice]
        color = CLUSTER_COLORS[cluster_choice]

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
                    marker_color="lightgrey",
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
                yaxis=dict(title="Risk score (0-1)", range=[0, 1]),
                height=380,
                legend=dict(orientation="h", y=-0.2),
                margin=dict(t=10),
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

# -----------------------------
# Additional charts (collapsed)
# -----------------------------
with st.expander("More data — all regions scatter & cluster fingerprints"):
    st.markdown("#### All 87 regions, by cluster")
    fig_scatter = px.scatter(
        df,
        x="rank",
        y="ai_literacy_gap_index",
        color="cluster_label",
        category_orders={"cluster_label": CLUSTER_ORDER},
        color_discrete_map=CLUSTER_COLORS,
        hover_data={"geo": True, "country": True, "nuts1_name": True, "rank": False},
        labels={
            "rank": "Rank (1 = highest risk)",
            "ai_literacy_gap_index": "AI Literacy Gap Index",
            "cluster_label": "Cluster",
        },
        height=480,
    )
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.8))
    fig_scatter.update_layout(legend=dict(orientation="h", y=-0.2))
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
            colorscale="YlOrRd",
            zmin=0,
            zmax=1,
            text=profile.round(2).values,
            texttemplate="%{text}",
            colorbar=dict(title="Risk"),
        )
    )
    fig_heatmap.update_layout(height=350, yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("---")
st.caption(
    "Data: Eurostat (isoc_r_dskl_i, tgs00107, edat_lfse_04, trng_lfse_04, "
    "lfst_r_lfu3rt, demo_r_pjanaggr3), 2025."
)