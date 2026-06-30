"""
edvancing — shared design tokens & styling helper.
Import `inject_edvancing_style()` and `render_navbar()` in every page.
"""

import base64
from pathlib import Path

import streamlit as st

# -----------------------------
# edvancing brand tokens
# -----------------------------
BLUE = "#0085CA"
BLUE_DARK = "#004F7A"
BLUE_LIGHT = "#E0F2FB"
WHITE = "#FFFFFF"
INK = "#1A1A1A"
INK_MID = "#444444"
INK_LIGHT = "#888888"
SURFACE = "#F7FAFE"
BORDER = "rgba(0,133,202,0.12)"

# 6-step EAA-compliant status palette, BLUE = best status, descending
STATUS_COLORS = [
    "#0085CA",  # 1 — best (edvancing brand blue)
    "#00A878",  # 2
    "#6DB33F",  # 3
    "#E8A020",  # 4
    "#D45C00",  # 5
    "#C0392B",  # 6 — worst
]

LOGO_PATH = Path(__file__).parent / "assets" / "edvancing_logo.png"


@st.cache_data
def get_logo_base64(path: Path) -> str | None:
    if not path.exists():
        return None
    return base64.b64encode(path.read_bytes()).decode()


def inject_edvancing_style():
    """Inject the shared edvancing CSS. Call once at the top of every page."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&display=swap');

        @font-face {{
            font-family: 'Futura';
            src: local('Futura');
        }}

        html, body, [class*="css"] {{
            font-family: 'DM Sans', 'Futura', 'Century Gothic', sans-serif;
            color: {INK};
        }}

        h1, h2, h3, h4 {{
            font-family: 'Futura', 'Century Gothic', 'DM Sans', sans-serif !important;
            font-weight: 600 !important;
            color: {INK} !important;
            letter-spacing: -0.01em;
        }}

        .stApp {{
            background-color: {SURFACE};
        }}

        /* ── Main content max-width & responsive padding ────── */
        .block-container {{
            max-width: 1280px;
            padding-left: clamp(12px, 4vw, 48px);
            padding-right: clamp(12px, 4vw, 48px);
            padding-top: clamp(12px, 2vw, 32px);
        }}

        /* ── Top nav bar ─────────────────────────────── */
        .edv-navbar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 16px;
            background-color: {WHITE};
            border-radius: 14px;
            padding: 20px clamp(12px, 3vw, 32px);
            margin-bottom: 28px;
            border: 1px solid {BORDER};
            box-shadow: 0 2px 16px rgba(0,133,202,0.06);
        }}
        .edv-navbar-logo {{
            display: flex;
            align-items: center;
            flex-shrink: 0;
        }}
        .edv-navbar-logo img,
        .edv-navbar img {{
            height: 220px !important;
            max-height: none !important;
            max-width: 100% !important;
            width: auto !important;
            display: block !important;
        }}
        .edv-navbar-links {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            justify-content: center;
            flex: 1;
        }}
        .edv-navlink,
        a.edv-navlink,
        [data-testid="stMarkdownContainer"] a.edv-navlink,
        div[data-testid="stMarkdownContainer"] .edv-navbar a.edv-navlink {{
            font-family: 'Futura', 'Century Gothic', 'DM Sans', sans-serif !important;
            font-size: 18px;
            font-weight: 600;
            color: {INK_MID} !important;
            padding: 10px 22px;
            border-radius: 8px;
            text-decoration: none !important;
            border-bottom: none !important;
            letter-spacing: 0.01em;
            transition: background-color .12s, color .12s;
        }}
        .edv-navlink:link, .edv-navlink:visited, .edv-navlink:active,
        [data-testid="stMarkdownContainer"] a.edv-navlink:link,
        [data-testid="stMarkdownContainer"] a.edv-navlink:visited {{
            text-decoration: none !important;
            border-bottom: none !important;
        }}
        .edv-navlink:hover {{
            background-color: {BLUE_LIGHT};
            color: {BLUE} !important;
            text-decoration: none !important;
        }}
        .edv-navbar-right {{
            font-size: 12px;
            color: {INK_LIGHT};
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 500;
            text-align: right;
            white-space: nowrap;
        }}

        /* ── Responsive: stack navbar on narrow screens ──────── */
        @media (max-width: 900px) {{
            .edv-navbar-right {{
                display: none;
            }}
            .edv-navlink {{
                font-size: 15px;
                padding: 8px 14px;
            }}
            .edv-navbar-logo img,
            .edv-navbar img {{
                height: 140px !important;
            }}
        }}
        @media (max-width: 640px) {{
            .edv-navbar {{
                justify-content: center;
                text-align: center;
            }}
            .edv-navbar-logo {{
                width: 100%;
                justify-content: center;
            }}
            .edv-navbar-links {{
                width: 100%;
                justify-content: center;
            }}
            .edv-navlink {{
                font-size: 13px;
                padding: 8px 12px;
            }}
            .edv-navbar-logo img,
            .edv-navbar img {{
                height: 110px !important;
            }}
            h1 {{
                font-size: 1.6rem !important;
            }}
            h2 {{
                font-size: 1.25rem !important;
            }}
        }}

        /* ── Section intro text ──────────────────────── */
        .edv-section-intro {{
            font-size: 14px;
            color: {INK_MID};
            line-height: 1.7;
            margin-bottom: 1rem;
            max-width: 760px;
        }}

        /* ── Info / how-to card ──────────────────────── */
        .edv-info-card {{
            background-color: {BLUE_LIGHT};
            border-radius: 12px;
            padding: 16px 20px;
            border-left: 4px solid {BLUE};
            margin-bottom: 1.25rem;
            font-size: 13px;
            color: {BLUE_DARK};
            line-height: 1.7;
        }}
        .edv-info-card b {{
            color: {INK};
        }}

        /* ── Metric cards ────────────────────────────── */
        div[data-testid="stMetric"] {{
            background-color: {WHITE} !important;
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 14px 18px;
            box-shadow: 0 2px 12px rgba(0,133,202,0.05);
        }}
        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] > div {{
            font-family: 'Futura', 'Century Gothic', sans-serif;
            color: {BLUE} !important;
            font-weight: 600 !important;
        }}
        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] > div,
        div[data-testid="stMetricLabel"] p {{
            color: {INK} !important;
            font-size: 12px !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700 !important;
            opacity: 1 !important;
            visibility: visible !important;
            display: block !important;
        }}
        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] > div {{
            color: {INK_MID} !important;
        }}

        /* ── Region detail card (on map click) ──────── */
        .edv-region-card {{
            background-color: {WHITE};
            border-radius: 12px;
            padding: 18px 22px;
            margin-top: 0.75rem;
            border: 1px solid {BORDER};
            border-left: 5px solid var(--cluster-color, {BLUE});
            box-shadow: 0 4px 20px rgba(0,133,202,0.08);
        }}
        .edv-region-name {{
            font-size: 1.05rem;
            font-weight: 600;
            font-family: 'Futura', 'Century Gothic', sans-serif;
            color: {INK};
        }}
        .edv-region-meta {{
            margin-top: 4px;
            font-size: 13px;
            color: {INK_MID};
        }}
        .edv-region-pillars {{
            margin-top: 8px;
            font-size: 0.85rem;
            color: {INK_LIGHT};
        }}

        /* ── Driver tags ─────────────────────────────── */
        .driver-tag {{
            display: inline-block;
            background-color: {BLUE};
            color: {WHITE};
            border-radius: 100px;
            padding: 3px 12px;
            margin-right: 6px;
            margin-bottom: 6px;
            font-size: 0.78rem;
            font-weight: 500;
            letter-spacing: 0.02em;
        }}

        /* ── Representative region cards ────────────── */
        .region-card {{
            background-color: {WHITE};
            border-left: 4px solid {BLUE};
            border: 1px solid {BORDER};
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 8px;
            font-size: 13px;
            color: {INK_MID};
        }}
        .region-card b {{
            color: {INK};
        }}

        /* ── Tabs styling ────────────────────────────── */
        button[data-baseweb="tab"] {{
            font-family: 'Futura', 'Century Gothic', sans-serif;
            font-weight: 500;
            font-size: 13px;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: {BLUE} !important;
        }}
        div[data-baseweb="tab-highlight"] {{
            background-color: {BLUE} !important;
        }}

        /* ── Policy angle box ────────────────────────── */
        div[data-testid="stAlert"] {{
            background-color: {BLUE_LIGHT};
            border-radius: 10px;
            border: 1px solid {BORDER};
            color: {BLUE_DARK};
        }}

        /* ── Caption / footer text ───────────────────── */
        .stCaption, [data-testid="stCaptionContainer"] {{
            color: {INK_LIGHT} !important;
        }}

        /* ── Cluster legend chips ────────────────────── */
        .edv-legend-chip {{
            font-size: 12px;
            color: {INK_MID};
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* ── Team / about cards ──────────────────────── */
        .edv-team-card {{
            background-color: {WHITE};
            border: 1px solid {BORDER};
            border-radius: 12px;
            padding: 14px 18px;
            text-align: center;
            font-size: 13px;
            font-weight: 500;
            color: {INK};
        }}
        .edv-sdg-badge {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background-color: {BLUE_LIGHT};
            color: {BLUE_DARK};
            border-radius: 100px;
            padding: 6px 16px;
            font-size: 13px;
            font-weight: 600;
            margin-right: 8px;
            margin-bottom: 8px;
        }}

        /* ── Force readable dark text in Plotly charts ───────── */
        .js-plotly-plot .plotly text,
        .js-plotly-plot .plotly .xtick text,
        .js-plotly-plot .plotly .ytick text,
        .js-plotly-plot .plotly .legend text,
        .js-plotly-plot .plotly .gtitle,
        .js-plotly-plot .plotly .g-xtitle,
        .js-plotly-plot .plotly .g-ytitle {{
            fill: {INK} !important;
        }}
        /* Keep gridlines light, only override text/labels above */
        .js-plotly-plot .plotly .xgrid,
        .js-plotly-plot .plotly .ygrid {{
            stroke: #D8E0E8 !important;
        }}
        .js-plotly-plot .plotly .xaxislayer-above path,
        .js-plotly-plot .plotly .yaxislayer-above path,
        .js-plotly-plot .plotly .domain {{
            stroke: {INK_MID} !important;
        }}

        /* ── Force readable dark text in dataframes / tables ──── */
        div[data-testid="stDataFrame"],
        div[data-testid="stTable"] {{
            color: {INK} !important;
        }}
        div[data-testid="stDataFrame"] * ,
        div[data-testid="stTable"] * {{
            color: {INK} !important;
        }}
        div[data-testid="stDataFrame"] {{
            border: 1px solid {BORDER};
            border-radius: 8px;
        }}

        /* ── Hide default Streamlit sidebar nav (we use top navbar) ── */
        [data-testid="stSidebarNav"] {{
            display: none;
        }}

        /* ── Anchor scroll offset (so sections aren't hidden under navbar) ── */
        #map, #insights, #about {{
            display: block;
            scroll-margin-top: 20px;
        }}

        /* ── Responsive: charts, legend, cards on narrow screens ──── */
        .js-plotly-plot, .plot-container {{
            width: 100% !important;
        }}
        @media (max-width: 640px) {{
            div[data-testid="stHorizontalBlock"] {{
                flex-wrap: wrap;
            }}
            .edv-legend-chip {{
                font-size: 11px;
                margin-bottom: 6px;
            }}
            .edv-team-card, .edv-info-card, .edv-section-intro {{
                font-size: 12px;
            }}
            .edv-region-card {{
                padding: 14px 16px;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_navbar():
    """
    Render the edvancing top navigation bar with plain in-page anchor
    links (#map, #insights, #about). All content lives on one page,
    so this avoids Streamlit's multipage routing entirely.
    """
    logo_b64 = get_logo_base64(LOGO_PATH)

    if logo_b64:
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" alt="edvancing logo" '
            f'style="height:220px !important; width:auto !important; max-width:100% !important; display:block !important;"/>'
        )
    else:
        logo_html = (
            f'<span style="font-family:\'Futura\',\'Century Gothic\',sans-serif;'
            f'font-size:96px;font-weight:600;color:{BLUE};letter-spacing:-0.02em;">'
            f'edvancing</span>'
        )

    st.markdown(
        f"""
        <div class="edv-navbar">
            <div class="edv-navbar-logo">{logo_html}</div>
            <div class="edv-navbar-links">
                <a class="edv-navlink" href="#map">Map</a>
                <a class="edv-navlink" href="#insights">Insights</a>
                <a class="edv-navlink" href="#about">About</a>
            </div>
            <div class="edv-navbar-right">EU27 · NUTS-1 · 2025</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
