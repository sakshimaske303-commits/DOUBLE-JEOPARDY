import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        .stApp {
            background: #ffffff;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #072a4d 0%, #14213d 100%);
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #ffffff !important;
            font-weight: 500;
        }

        h1 {
            background: linear-gradient(90deg, #072a4d, #0096c7, #1b4332);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900 !important;
            font-size: 2.9rem !important;
            letter-spacing: -0.5px;
        }

        h2 {
            color: #072a4d !important;
            font-weight: 800 !important;
            border-left: 5px solid #0096c7;
            padding-left: 14px;
            font-size: 1.7rem !important;
        }

        h3 {
            color: #1b4332 !important;
            font-weight: 700 !important;
        }

        h4 {
            font-weight: 700 !important;
        }

        p, li {
            color: #14213d;
            font-weight: 400;
        }

        strong, b {
            color: #072a4d;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: linear-gradient(135deg, #e8f7fb, #d4eef5);
            border-radius: 14px;
            padding: 20px;
            border: 1.5px solid rgba(0, 150, 199, 0.35);
            box-shadow: 0 6px 18px rgba(7, 42, 77, 0.12);
        }

        div[data-testid="stMetricValue"] {
            color: #072a4d !important;
            font-weight: 800 !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.7rem !important;
        }

        div[data-testid="stMetricLabel"] {
            color: #1b4332 !important;
            text-transform: uppercase;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 1.2px;
        }

        .stButton>button {
            background: linear-gradient(90deg, #0096c7, #1b4332);
            color: white;
            border-radius: 10px;
            border: none;
            font-weight: 700;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
            border: 1.5px solid rgba(0, 150, 199, 0.3);
            font-weight: 500;
        }

        hr {
            border: none;
            height: 4px;
            background: linear-gradient(90deg, #072a4d, #0096c7, #1b4332);
            border-radius: 10px;
            margin: 1.6rem 0;
        }

        .caption-text {
            color: #6c757d;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background: #e8f7fb;
            border-radius: 8px 8px 0 0;
            color: #072a4d;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(0, 150, 199, 0.2) !important;
            color: #072a4d !important;
            font-weight: 800;
        }

        .dj-card {
            background: linear-gradient(135deg, #e8f7fb, #f0faf5);
            border-radius: 14px;
            padding: 18px;
            border: 1.5px solid rgba(0, 150, 199, 0.3);
            box-shadow: 0 4px 14px rgba(7, 42, 77, 0.08);
        }

        [data-testid="stExpander"] {
            background-color: #ffffff !important;
            border: 1.5px solid rgba(0,150,199,0.3) !important;
            border-radius: 10px !important;
        }

        [data-testid="stExpander"] summary {
            background-color: #e8f7fb !important;
        }

        [data-testid="stExpander"] summary p {
            font-size: 1.15rem !important;
            font-weight: 800 !important;
            color: #072a4d !important;
        }

        [data-testid="stExpanderDetails"] {
            background-color: #ffffff !important;
        }

        [data-testid="stExpanderDetails"] p,
        [data-testid="stExpanderDetails"] li {
            color: #14213d !important;
        }

        /* Force the expander arrow/chevron icon to be black and visible,
           covering multiple possible internal Streamlit selectors since
           the exact DOM structure varies by version */
        [data-testid="stExpander"] summary svg,
        [data-testid="stExpander"] svg,
        [data-testid="stExpanderToggleIcon"],
        [data-testid="stExpanderToggleIcon"] svg,
        details summary svg {
            fill: #000000 !important;
            stroke: #000000 !important;
            color: #000000 !important;
            opacity: 1 !important;
        }

        [data-testid="stExpander"] summary path,
        details summary path {
            fill: #000000 !important;
            stroke: #000000 !important;
        }

        [data-testid="stExpander"] summary::marker,
        details summary::marker {
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)


PALETTE = {
    "navy": "#072a4d",
    "cyan": "#0096c7",
    "green": "#1b4332",
    "mint": "#2d8659",
    "risk": "#d62839",
    "text_dark": "#14213d",
    "text_muted": "#6c757d",
    "card_bg": "#e8f7fb",
}