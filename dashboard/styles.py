import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@500;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
        }

        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"],
        .main,
        [data-testid="stAppViewContainer"] > .main,
        .block-container,
        [data-testid="stAppViewBlockContainer"] {
            background: linear-gradient(135deg, #050505 0%, #0D0D0D 50%, #050505 100%) !important;
        }

        [data-testid="stHeader"] {
            background-color: #0A0A0A !important;
            height: 3rem !important;
        }
        /* Hide only the Deploy button + app menu, keep the rest of the
        toolbar (sidebar collapse control) clickable. */
        [data-testid="stAppDeployButton"] {
            display: none !important;
        }
        [data-testid="stDecoration"] {
            display: none !important;
        }
        #MainMenu {
            visibility: hidden !important;
        }
        .block-container {
            padding-top: 1rem !important;
        }

        section[data-testid="stSidebar"] {
            background: linear-gradient(180deg, #030303 0%, #0A0A0A 100%);
            border-right: 1px solid rgba(34, 211, 238, 0.2);
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: #F1F1F1 !important;
            font-weight: 500;
        }

        section[data-testid="stSidebar"] a {
    border-radius: 8px !important;
    padding: 8px 14px !important;
    transition: all 0.2s ease;
}
section[data-testid="stSidebar"] a:hover {
    background: rgba(34, 211, 238, 0.12) !important;
    border-left: 3px solid #22D3EE;
}
section[data-testid="stSidebar"] a[aria-current="page"] {
    background: rgba(255, 214, 10, 0.12) !important;
    border-left: 3px solid #FFD60A;
    font-weight: 700 !important;
}

        h1 {
            background: linear-gradient(90deg, #22D3EE, #FFD60A);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900 !important;
            font-size: 2.9rem !important;
            letter-spacing: -0.5px;
            text-align: center;
            filter: drop-shadow(0 0 20px rgba(34, 211, 238, 0.25));
        }

        h2 {
            color: #FFD60A;
            font-weight: 800 !important;
            border-left: 5px solid #22D3EE;
            padding-left: 14px;
            font-size: 1.7rem !important;
        }

        h3 {
            color: #22D3EE !important;
            font-weight: 700 !important;
        }

        h4 {
            font-weight: 700 !important;
            color: #F1F1F1 !important;
        }

        p, li {
            color: #F1F1F1;
            font-weight: 400;
        }

        strong, b {
            color: #FFD60A;
            font-weight: 700;
        }

        div[data-testid="stMetric"] {
            background: #141414;
            border-radius: 14px;
            padding: 20px;
            border: 1.5px solid rgba(34, 211, 238, 0.35);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
        }

        div[data-testid="stMetricValue"],
        div[data-testid="stMetricValue"] * {
            color: #22D3EE !important;
            opacity: 1 !important;
            font-weight: 800 !important;
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.7rem !important;
        }

        div[data-testid="stMetricLabel"],
        div[data-testid="stMetricLabel"] * {
            color: #FFD60A !important;
            opacity: 1 !important;
            text-transform: uppercase;
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            letter-spacing: 1.2px;
        }

        div[data-testid="stMetricDelta"],
        div[data-testid="stMetricDelta"] * {
            color: #67E8F9 !important;
            opacity: 1 !important;
            font-weight: 700 !important;
        }

        .stButton>button {
            background: linear-gradient(90deg, #22D3EE, #FFD60A);
            color: #0A0A0A;
            border-radius: 10px;
            border: none;
            font-weight: 700;
        }

        div[data-testid="stAlert"] {
            border-radius: 12px;
            border: 1.5px solid rgba(255, 214, 10, 0.4);
            font-weight: 500;
            background: #141414;
        }
        div[data-testid="stAlert"] p {
            color: #F1F1F1 !important;
        }

        hr {
            border: none;
            height: 4px;
            background: linear-gradient(90deg, #22D3EE, #FFD60A);
            border-radius: 10px;
            margin: 1.6rem 0;
        }

        .caption-text {
            color: #9CA3AF;
            font-size: 0.9rem;
            font-weight: 500;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            background: #141414;
            border-radius: 8px 8px 0 0;
            color: #F1F1F1;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(34, 211, 238, 0.2) !important;
            color: #22D3EE !important;
            font-weight: 800;
        }

        .dj-card {
            background: #141414;
            border-radius: 14px;
            padding: 18px;
            border: 1.5px solid rgba(34, 211, 238, 0.3);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.45);
        }

        [data-testid="stExpander"] {
            background-color: #141414 !important;
            border: 1.5px solid rgba(34, 211, 238, 0.3) !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        }

        [data-testid="stExpander"] summary {
            background-color: #0D0D0D !important;
        }

        [data-testid="stExpander"] summary p {
            font-size: 1.15rem !important;
            font-weight: 800 !important;
            color: #FFD60A !important;
        }

        [data-testid="stExpanderDetails"] {
            background-color: #141414 !important;
        }

        [data-testid="stExpanderDetails"] p,
        [data-testid="stExpanderDetails"] li {
            color: #F1F1F1 !important;
        }

        [data-testid="stExpander"] summary svg,
        [data-testid="stExpander"] svg,
        [data-testid="stExpanderToggleIcon"],
        [data-testid="stExpanderToggleIcon"] svg,
        details summary svg {
            fill: #22D3EE !important;
            stroke: #22D3EE !important;
            color: #22D3EE !important;
            opacity: 1 !important;
        }

        [data-testid="stExpander"] summary path,
        details summary path {
            fill: #22D3EE !important;
            stroke: #22D3EE !important;
        }

        [data-testid="stExpander"] summary::marker,
        details summary::marker {
            color: #22D3EE !important;
        }

        /* Sidebar collapse control -- covers every testid variant Streamlit
        has used across versions (name isn't stable, and it's invisible by
        default on a dark theme). */
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="baseButton-header"],
        [data-testid="stHeader"] button,
        [data-testid*="ollapse" i],
        button[kind="header"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            z-index: 999999 !important;
        }
        [data-testid="collapsedControl"],
        [data-testid="stSidebarCollapsedControl"] {
            position: fixed !important;
            top: 12px !important;
            left: 12px !important;
            background: #141414 !important;
            border: 1.5px solid rgba(34, 211, 238, 0.4) !important;
            border-radius: 8px !important;
            padding: 4px !important;
        }
        [data-testid="collapsedControl"] svg,
        [data-testid="stSidebarCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="baseButton-header"] svg,
        [data-testid="stHeader"] button svg,
        button[kind="header"] svg {
            fill: #22D3EE !important;
            stroke: #22D3EE !important;
            opacity: 1 !important;
        }
        </style>
    """, unsafe_allow_html=True)


PALETTE = {
    "navy": "#22D3EE",
    "cyan": "#67E8F9",
    "green": "#FFD60A",
    "mint": "#FFEB3B",
    "risk": "#22D3EE",
    "text_dark": "#F1F1F1",
    "text_muted": "#9CA3AF",
    "card_bg": "#141414",
}