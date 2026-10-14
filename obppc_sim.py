import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# Configuration de la page
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulateur OBPPC",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -----------------------------------------------------------------------------
# Dark dashboard theme — style widgets
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --bg:          #0d1117;
        --panel:       #161b22;
        --panel-2:     #1c2128;
        --border:      #21262d;
        --border-hi:   #30363d;
        --text:        #c9d1d9;
        --text-hi:     #e6edf3;
        --text-dim:    #8b949e;
        --text-faint:  #6e7681;
        --accent:      #8b5cf6;
        --accent-2:    #a78bfa;
        --accent-soft: rgba(139,92,246,0.15);
        --green:       #3fb950;
        --red:         #f85149;
        --blue:        #58a6ff;
        --yellow:      #d29922;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* ---------- Reset top ---------- */
    #MainMenu, footer { visibility: hidden; }

    [data-testid="stHeader"] {
        display: none !important;
        height: 0 !important;
    }
    [data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
    section.main > div { padding-top: 0 !important; }
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem;
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }

    /* ---------- App background ---------- */
    .stApp {
        background: #0d1117;
    }

    /* ---------- Typography ---------- */
    h1, h2, h3, h4 {
        color: var(--text-hi);
        font-weight: 600;
        letter-spacing: -0.01em;
    }

    /* ============================================================
       TOP BAR : titre compact
       ============================================================ */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 0 0.9rem 0;
        margin-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }
    .topbar-title {
        display: flex;
        align-items: center;
        gap: 0.7rem;
    }
    .topbar-mark {
        width: 26px; height: 26px;
        border-radius: 6px;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        box-shadow: 0 0 20px -5px rgba(139,92,246,0.7);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 0.72rem;
        font-weight: 700;
        color: #ffffff;
    }
    .topbar h1 {
        margin: 0;
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--text-hi);
        letter-spacing: -0.01em;
    }
    .topbar-sub {
        margin: 0.15rem 0 0 0;
        font-size: 0.72rem;
        color: var(--text-faint);
    }
    .topbar-meta {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.72rem;
        color: var(--text-dim);
    }
    .topbar-meta .pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.3rem 0.6rem;
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 6px;
        font-size: 0.68rem;
        font-weight: 500;
        color: var(--text-dim);
        letter-spacing: 0.02em;
    }
    .topbar-meta .pill .dot {
        width: 5px; height: 5px; border-radius: 50%;
        background: var(--green);
        box-shadow: 0 0 8px var(--green);
    }

    /* ============================================================
       WIDGET CARD (générique)
       ============================================================ */
    .widget {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.9rem 1rem;
        height: 100%;
    }
    .widget-label {
        font-size: 0.68rem;
        font-weight: 500;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.5rem;
    }
    .widget-title {
        font-size: 0.82rem;
        font-weight: 600;
        color: var(--text-hi);
        margin-bottom: 0.75rem;
    }

    /* ---------- KPI widget (gros chiffre + barre) ---------- */
    .kpi-tile {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 1rem 1.1rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .kpi-tile-label {
        font-size: 0.68rem;
        font-weight: 500;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.6rem;
    }
    .kpi-tile-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: var(--text-hi);
        line-height: 1;
        letter-spacing: -0.03em;
        font-variant-numeric: tabular-nums;
    }
    .kpi-tile-value .unit {
        font-size: 0.85rem;
        color: var(--text-dim);
        font-weight: 500;
        margin-left: 0.25rem;
        letter-spacing: 0;
    }
    .kpi-tile-sub {
        font-size: 0.72rem;
        color: var(--text-dim);
        margin-top: 0.5rem;
    }
    .kpi-tile-bar {
        margin-top: 0.85rem;
        height: 3px;
        background: var(--border);
        border-radius: 2px;
        overflow: hidden;
        position: relative;
    }
    .kpi-tile-bar::after {
        content: "";
        position: absolute;
        inset: 0;
        width: var(--w, 0%);
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        border-radius: 2px;
    }

    /* ============================================================
       FILTER PANEL
       ============================================================ */
    .filter-panel {
        background: var(--panel);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.9rem 1rem 0.4rem 1rem;
        margin-bottom: 1rem;
    }
    .filter-panel-title {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.75rem;
    }
    .filter-panel-title span {
        font-size: 0.68rem;
        font-weight: 600;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .filter-panel-title .stat {
        font-size: 0.68rem;
        color: var(--text-dim);
        font-variant-numeric: tabular-nums;
    }

    .filter-label {
        font-size: 0.68rem;
        font-weight: 500;
        color: var(--text-dim);
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin-bottom: 0.45rem;
    }

    /* ============================================================
       MULTISELECT — style dashboard plat
       ============================================================ */
    div[data-testid="stMultiSelect"] { width: 100%; }
    div[data-testid="stMultiSelect"] > div { width: 100%; }

    div[data-testid="stMultiSelect"] [data-baseweb="select"],
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="input"],
    div[data-testid="stMultiSelect"] [data-baseweb="input"] > div {
        background-color: #0d1117 !important;
        background-image: none !important;
        border-color: var(--border-hi) !important;
        color: var(--text) !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        border: 1px solid var(--border-hi) !important;
        border-radius: 6px !important;
        min-height: 40px;
        height: auto !important;
        padding: 0.3rem 0.5rem !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease;
        align-items: flex-start !important;
        flex-wrap: wrap !important;
        row-gap: 0.3rem !important;
    }
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div:hover {
        border-color: #484f58 !important;
    }
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div:focus-within {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 3px var(--accent-soft) !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
        flex-wrap: wrap !important;
        align-items: center !important;
        gap: 0.25rem !important;
        min-height: 24px;
    }

    div[data-testid="stMultiSelect"] input {
        background-color: transparent !important;
        color: var(--text) !important;
        min-height: 24px;
    }
    div[data-testid="stMultiSelect"] input::placeholder {
        color: var(--text-faint) !important;
    }

    div[data-testid="stMultiSelect"] svg {
        fill: var(--text-dim) !important;
        color: var(--text-dim) !important;
    }

    /* Tags — violet plat (pas de dégradé) */
    div[data-baseweb="tag"] {
        background: var(--accent) !important;
        background-color: var(--accent) !important;
        background-image: none !important;
        border: none !important;
        color: #ffffff !important;
        border-radius: 4px !important;
        font-weight: 500 !important;
        font-size: 0.72rem !important;
        min-height: 22px !important;
        height: auto !important;
        padding: 0.15rem 0.45rem !important;
        display: inline-flex !important;
        align-items: center !important;
        line-height: 1.2 !important;
        max-width: 100%;
    }
    div[data-baseweb="tag"] * {
        background: transparent !important;
        background-color: transparent !important;
        color: #ffffff !important;
    }
    div[data-baseweb="tag"] svg {
        fill: rgba(255,255,255,0.85) !important;
        color: rgba(255,255,255,0.85) !important;
        width: 11px !important;
        height: 11px !important;
    }
    div[data-baseweb="tag"] svg:hover {
        fill: #ffffff !important;
    }

    /* Dropdown */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] [role="listbox"],
    div[data-baseweb="menu"] {
        background-color: var(--panel-2) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
    }
    div[data-baseweb="menu"] li,
    div[data-baseweb="menu"] [role="option"] {
        background-color: transparent !important;
        color: var(--text) !important;
        font-size: 0.8rem !important;
    }
    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="menu"] [role="option"]:hover {
        background-color: var(--accent-soft) !important;
        color: var(--text-hi) !important;
    }
    div[data-baseweb="menu"] [aria-selected="true"] {
        background-color: var(--accent-soft) !important;
        color: var(--text-hi) !important;
    }

    div[data-testid="stMultiSelect"] label { display: none !important; }

    /* ============================================================
       SECTION TITLES
       ============================================================ */
    .section-head {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin: 1.25rem 0 0.6rem 0;
    }
    .section-head h3 {
        margin: 0;
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--text-hi);
        letter-spacing: -0.005em;
    }
    .section-head .hint {
        font-size: 0.7rem;
        color: var(--text-faint);
    }

    /* ============================================================
       BUTTONS
       ============================================================ */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        font-size: 0.82rem;
        padding: 0.45rem 1rem;
        border: 1px solid var(--border-hi);
        background: var(--panel);
        color: var(--text);
        transition: all 0.15s ease;
    }
    .stButton > button:hover {
        border-color: #484f58;
        background: var(--panel-2);
        color: var(--text-hi);
    }
    .stButton > button[kind="primary"] {
        background: var(--accent);
        border: 1px solid var(--accent);
        color: #ffffff;
    }
    .stButton > button[kind="primary"]:hover {
        background: #7c3aed;
        border-color: #7c3aed;
    }

    /* ============================================================
       DATAFRAMES / EDITOR
       ============================================================ */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        overflow: hidden;
        background: var(--panel);
    }

    /* ============================================================
       DOWNLOAD BUTTON
       ============================================================ */
    [data-testid="stDownloadButton"] > button {
        border-radius: 6px;
        font-size: 0.8rem;
        border: 1px solid var(--border-hi);
        background: var(--panel);
        color: var(--text);
    }
    [data-testid="stDownloadButton"] > button:hover {
        border-color: var(--accent);
        color: var(--accent-2);
    }

    .stAlert {
        background-color: var(--panel) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 6px !important;
        color: var(--text) !important;
    }

    hr { border-color: var(--border); margin: 1rem 0; }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Données initiales
# -----------------------------------------------------------------------------
@st.cache_data
def load_initial_data():
    data = {
        "Segment": [], "Marque": [], "Occasion": [], "Role_OBPPC": [],
        "Description": [], "Volume_L": [], "PVF_Ar": [],
    }

    energie_data = [
        ('Energie', 'Red Bull', 'Upscale', 'Upscale (Premium)', 'CAN 25', 0.25, 9900),
        ('Energie', 'Monster', 'Upscale', 'Upscale (Premium)', 'CAN 50', 0.50, 9900),
        ('Energie', 'FOSA', 'Upscale', 'Upscale (Premium)', 'CAN 50', 0.50, 5000),
        ('Energie', 'XXL', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 2500),
        ('Energie', 'XXL', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 35', 0.35, 3500),
        ('Energie', 'XXL', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 4000),
        ('Energie', 'DYNAMIC', 'Upscale', 'Upscale (Premium)', 'CAN 25', 0.25, 3500),
        ('Energie', 'BOOST VITALITY', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 4000),
    ]

    boisson_data = [
        ('Boisson Gazeuse', 'COCA', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35 (N°1 vente en col)', 0.35, 1500),
        ('Boisson Gazeuse', 'COCA', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'COCA', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'COCA', 'FC (PET)', 'Upsize (Grand format)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'WOCO', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'WOCO', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'WOCO', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'WOCO', 'FC (PET)', 'Upsize (Grand format)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'FC (VER)', 'Upsize (Grand format)', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'FANTA', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35 (N°1 vente en col)', 0.35, 1500),
        ('Boisson Gazeuse', 'FANTA', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'FANTA', 'FC (PET)', 'Upsize (Grand format)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'CAPRICE', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'CAPRICE', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'CAPRICE', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'CAPRICE', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'CAPRICE', 'FC (PET)', 'Upsize (Grand format)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'CAPRICE', 'FC (VER)', 'Upsize (Grand format)', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'TONIC', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'TONIC', 'FC (VER)', 'Upsize (Grand format)', 'VC 100', 1.00, 3000),
    ]

    eaux_data = [
        ('Eaux', 'Cristal', 'IC (VER)', 'Entry (Entrée de gamme)', 'Cristal 30 cl VER', 0.30, 1500),
        ('Eaux', 'Cristal', 'IC (VER)', 'Frequency (Cœur de gamme)', 'Cristal 50 cl VER', 0.50, 2200),
        ('Eaux', 'Cristal', 'FC (VER)', 'Upsize (Grand format)', 'Cristal 100 cl VER', 1.00, 3800),
        ('Eaux', 'Cristal', 'FC (PET)', 'Upsize (Grand format)', 'Cristal 150 cl PET', 1.50, 5500),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Entry (Entrée de gamme)', 'RANOVISY 33 PET', 0.33, 1000),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Frequency (Cœur de gamme)', 'RANOVISY 50 CL PET', 0.50, 2400),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Upsize (Grand format)', 'RANOVISY 75 PET', 0.75, 3000),
        ('Eaux', 'VISY GASY', 'IC (PET)', 'Entry (Entrée de gamme)', 'VISY GASY 60 PET', 0.60, 2500),
        ('Eaux', 'VISY GASY', 'FC (PET)', 'Upsize (Grand format)', 'VISY GASY 100 PET', 1.00, 3000),
        ('Eaux', 'Eau vive', 'IC (PET)', 'Entry (Entrée de gamme)', 'Eau vive 50 cl PET', 0.50, 1600),
        ('Eaux', 'Eau vive', 'FC (PET)', 'Upsize (Grand format)', 'Eau vive 150 cl PET', 1.50, 3300),
        ('Eaux', 'Eau vive', 'IC (VER)', 'Frequency (Cœur de gamme)', 'Eau vive 50 cl VER', 0.50, 2200),
        ('Eaux', 'Cristalline', 'FC (PET)', 'Upsize (Grand format)', 'Cristalline 100 cl PET', 1.50, 2100),
        ('Eaux', 'Cristalline', 'FC (PET)', 'Upsize (Grand format)', 'Cristalline 200 cl PET', 2.00, 3600),
        ('Eaux', 'OLYMPIKO', 'IC (PET)', 'Entry (Entrée de gamme)', 'OLYMPIKO 50', 0.50, 1500),
        ('Eaux', 'OLYMPIKO', 'FC (PET)', 'Frequency (Cœur de gamme)', 'OLYMPIKO 100', 1.00, 2000),
        ('Eaux', 'OLYMPIKO', 'FC (PET)', 'Upsize (Grand format)', 'OLYMPIKO 150', 1.50, 2500),
        ('Eaux', 'NATUR EAU', 'IC (PET)', 'Entry (Entrée de gamme)', 'NATUR EAU 50', 0.50, 1500),
        ('Eaux', 'NATUR EAU', 'FC (PET)', 'Frequency (Cœur de gamme)', 'NATUR EAU 100', 1.00, 2000),
        ('Eaux', 'NATUR EAU', 'FC (PET)', 'Upsize (Grand format)', 'NATUR EAU 150', 1.50, 2500),
    ]

    biere_data = [
        ('Bière', 'Beaufort', '', 'Frequency (Cœur de gamme)', 'Beaufort 33CL VER', 0.33, 4000),
        ('Bière', 'Beaufort', '', 'Upscale (Premium)', 'Beaufort 33 CL CAN', 0.33, 5000),
        ('Bière', 'Gold', '', 'Entry (Entrée de gamme)', 'Gold Blanche 33cl VER', 0.33, 3500),
        ('Bière', 'Gold', '', 'Entry (Entrée de gamme)', 'Gold 8 50 cl VER', 0.50, 4500),
        ('Bière', 'Gold', '', 'Frequency (Cœur de gamme)', 'Gold Blanche 50 cl VER', 0.50, 4500),
        ('Bière', 'Gold', '', 'Frequency (Cœur de gamme)', 'Gold Blonde 50 cl VER', 0.50, 4500),
        ('Bière', 'Gold', '', 'Frequency (Cœur de gamme)', 'Gold Blonde 65 cl VER', 0.65, 5000),
        ('Bière', 'Gold', '', 'Upscale (Premium)', 'Gold 8 50 cl CAN', 0.50, 6000),
        ('Bière', 'Gold', '', 'Upscale (Premium)', 'Gold Blanche 50 cl CAN', 0.50, 6000),
        ('Bière', 'Gold', '', 'Upscale (Premium)', 'Gold Blonde 50 cl CAN', 0.50, 6000),
        ('Bière', 'THB', '', 'Entry (Entrée de gamme)', 'THB Pilsener 33 cl VER', 0.33, 2500),
        ('Bière', 'THB', '', 'Frequency (Cœur de gamme)', 'THB Pilsener 65 cl VER', 0.65, 4500),
        ('Bière', 'THB', '', 'Upscale (Premium)', 'THB Pilsener 50 cl CAN', 0.50, 5000),
        ('Bière', 'Queen', '', 'Entry (Entrée de gamme)', 'Queen s 65 cl VER', 0.65, 4000),
        ('Bière', 'Fresh', '', 'Entry (Entrée de gamme)', 'THB Fresh 33 cl VER', 0.33, 2500),
        ('Bière', 'Fresh', '', 'Frequency (Cœur de gamme)', 'THB Fresh 65 cl VER', 0.65, 4000),
        ('Bière', 'Fresh', '', 'Upscale (Premium)', 'FRESH 33 cl CAN', 0.33, 3500),
    ]

    all_data = energie_data + boisson_data + eaux_data + biere_data
    for item in all_data:
        for i, key in enumerate(data.keys()):
            data[key].append(item[i])
    return pd.DataFrame(data)


df_initial = load_initial_data()
ALL_SEGMENTS = list(df_initial['Segment'].unique())
ALL_BRANDS = sorted(df_initial['Marque'].unique())


# -----------------------------------------------------------------------------
# Logique métier
# -----------------------------------------------------------------------------
def check_index_status(index_value, role):
    if role == 'Entry (Entrée de gamme)':
        return 'Conforme' if 101 <= index_value <= 110 else 'Non conforme'
    if role == 'Frequency (Cœur de gamme)':
        return 'Conforme' if index_value == 100 else 'Non conforme'
    if role == 'Upsize (Grand format)':
        return 'Conforme' if 90 <= index_value <= 99 else 'Non conforme'
    if role in ['Upscale (Premium)', 'Upscale (Super-Premium Niche)']:
        return 'Conforme' if index_value >= 111 else 'Non conforme'
    return '—'


def target_label(role):
    return {
        'Entry (Entrée de gamme)': '101 – 110',
        'Frequency (Cœur de gamme)': '100',
        'Upsize (Grand format)': '90 – 99',
        'Upscale (Premium)': '≥ 111',
        'Upscale (Super-Premium Niche)': '≥ 111',
    }.get(role, '—')


# -----------------------------------------------------------------------------
# TOP BAR
# -----------------------------------------------------------------------------
st.markdown("""
<div class="topbar">
    <div class="topbar-title">
        <div class="topbar-mark">OB</div>
        <div>
            <h1>Simulateur OBPPC</h1>
            <p class="topbar-sub">Occasion · Brand · Package · Price · Channel</p>
        </div>
    </div>
    <div class="topbar-meta">
        <span class="pill"><span class="dot"></span>Pricing Analytics</span>
        <span class="pill">Cohérence portefeuille</span>
    </div>
</div>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# FILTER PANEL
# -----------------------------------------------------------------------------
st.markdown('<div class="filter-panel-title"><span>Filtres</span><span class="stat">Périmètre d\'analyse</span></div>', unsafe_allow_html=True)

col_seg, col_br, col_stat = st.columns([1.4, 2.6, 1.1], gap="medium")

with col_seg:
    st.markdown('<div class="filter-label">Segments</div>', unsafe_allow_html=True)
    segments = st.multiselect(
        "Segments",
        options=ALL_SEGMENTS,
        default=ALL_SEGMENTS,
        placeholder="Tous les segments",
        label_visibility="collapsed",
    )

with col_br:
    if segments:
        available_brands = sorted(
            df_initial[df_initial['Segment'].isin(segments)]['Marque'].unique()
        )
    else:
        available_brands = []

    st.markdown('<div class="filter-label">Marques</div>', unsafe_allow_html=True)
    brands = st.multiselect(
        "Marques",
        options=available_brands,
        default=available_brands,
        placeholder="Toutes les marques",
        label_visibility="collapsed",
    )

with col_stat:
    st.markdown('<div class="filter-label">Périmètre</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="widget" style="padding:0.55rem 0.8rem;">
        <div style="font-size:0.72rem; color:var(--text-dim); font-variant-numeric:tabular-nums;">
            <span style="color:var(--text-hi); font-weight:600;">{len(segments)}</span> segments
            &nbsp;·&nbsp;
            <span style="color:var(--text-hi); font-weight:600;">{len(brands)}</span> marques
        </div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Filtrage
# -----------------------------------------------------------------------------
if segments and brands:
    df_filtered = df_initial[
        (df_initial['Segment'].isin(segments)) & (df_initial['Marque'].isin(brands))
    ].copy()
else:
    df_filtered = df_initial.iloc[0:0].copy()


# -----------------------------------------------------------------------------
# KPI tiles (aperçu portefeuille)
# -----------------------------------------------------------------------------
n_sku = len(df_filtered)
n_seg = df_filtered['Segment'].nunique() if n_sku else 0
n_brand = df_filtered['Marque'].nunique() if n_sku else 0
prix_moy_l = (df_filtered['PVF_Ar'] / df_filtered['Volume_L']).mean() if n_sku else 0

k1, k2, k3, k4 = st.columns(4, gap="medium")

with k1:
    st.markdown(f"""
    <div class="kpi-tile">
        <div>
            <div class="kpi-tile-label">Références</div>
            <div class="kpi-tile-value">{n_sku}</div>
            <div class="kpi-tile-sub">SKU dans le périmètre</div>
        </div>
        <div class="kpi-tile-bar" style="--w:100%"></div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-tile">
        <div>
            <div class="kpi-tile-label">Segments</div>
            <div class="kpi-tile-value">{n_seg}<span class="unit">/ {len(ALL_SEGMENTS)}</span></div>
            <div class="kpi-tile-sub">Catégories actives</div>
        </div>
        <div class="kpi-tile-bar" style="--w:{int(n_seg/max(len(ALL_SEGMENTS),1)*100)}%"></div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-tile">
        <div>
            <div class="kpi-tile-label">Marques</div>
            <div class="kpi-tile-value">{n_brand}<span class="unit">/ {len(ALL_BRANDS)}</span></div>
            <div class="kpi-tile-sub">Marques actives</div>
        </div>
        <div class="kpi-tile-bar" style="--w:{int(n_brand/max(len(ALL_BRANDS),1)*100)}%"></div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-tile">
        <div>
            <div class="kpi-tile-label">Prix moyen / L</div>
            <div class="kpi-tile-value">{prix_moy_l:,.0f}<span class="unit">Ar</span></div>
            <div class="kpi-tile-sub">Moyenne pondérée</div>
        </div>
        <div class="kpi-tile-bar" style="--w:65%"></div>
    </div>
    """, unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Tableau éditable
# -----------------------------------------------------------------------------
st.markdown('<div class="section-head"><h3>Portefeuille — Édition</h3><span class="hint">Ajustez puis recalculez</span></div>', unsafe_allow_html=True)

if df_filtered.empty:
    st.info("Aucune donnée à afficher. Sélectionnez au moins un segment et une marque dans la barre de filtres.")
else:
    edited_df = st.data_editor(
        df_filtered,
        column_config={
            "Segment": st.column_config.SelectboxColumn(
                "Segment", options=ALL_SEGMENTS, required=True, width=110,
            ),
            "Marque": st.column_config.SelectboxColumn(
                "Marque", options=ALL_BRANDS, required=True, width=150, pinned=True,
            ),
            "Occasion": st.column_config.SelectboxColumn(
                "Occasion",
                options=['IC (VER)', 'IC (PET)', 'FC (VER)', 'FC (PET)', 'Upscale', ''],
                required=False, width=120,
            ),
            "Role_OBPPC": st.column_config.SelectboxColumn(
                "Rôle OBPPC",
                options=[
                    'Entry (Entrée de gamme)',
                    'Frequency (Cœur de gamme)',
                    'Upsize (Grand format)',
                    'Upscale (Premium)',
                    'Upscale (Super-Premium Niche)',
                ],
                required=True, width=210,
            ),
            "Description": st.column_config.TextColumn(
                "Format / Description", width=230, help="Format commercial du SKU",
            ),
            "Volume_L": st.column_config.NumberColumn(
                "Volume (L)", min_value=0.1, step=0.01, format="%.2f L",
                required=True, width=110,
            ),
            "PVF_Ar": st.column_config.NumberColumn(
                "PVF (Ar)", min_value=0, step=100, format="%d Ar",
                required=True, width=130,
            ),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        key="data_editor",
        height=600,
        row_height=36,
    )

    col_btn, _ = st.columns([1, 4])
    with col_btn:
        calculate_button = st.button("Recalculer les index", type="primary", use_container_width=True)

    if calculate_button:
        edited_df = edited_df.copy()
        edited_df['P_Litre_Ar'] = edited_df['PVF_Ar'] / edited_df['Volume_L']

        edited_df['Index_PVF'] = 0.0
        edited_df['Index_P_Litre'] = 0.0
        edited_df['Index_PVF_Freq'] = 0.0
        edited_df['Index_P_Litre_Freq'] = 0.0

        for segment in edited_df['Segment'].unique():
            mask = edited_df['Segment'] == segment
            seg = edited_df[mask]
            if len(seg) == 0:
                continue
            base_pvf = seg.iloc[0]['PVF_Ar']
            base_pl = seg.iloc[0]['P_Litre_Ar']
            if base_pvf > 0:
                edited_df.loc[mask, 'Index_PVF'] = (edited_df.loc[mask, 'PVF_Ar'] / base_pvf * 100).round(0).astype(int)
            if base_pl > 0:
                edited_df.loc[mask, 'Index_P_Litre'] = (edited_df.loc[mask, 'P_Litre_Ar'] / base_pl * 100).round(0).astype(int)

        freq = edited_df[edited_df['Role_OBPPC'].str.contains('Frequency', na=False)]
        if len(freq) > 0:
            base_pvf = freq['PVF_Ar'].mean()
            base_pl = freq['P_Litre_Ar'].mean()
        else:
            base_pvf = edited_df['PVF_Ar'].mean()
            base_pl = edited_df['P_Litre_Ar'].mean()

        if base_pvf > 0:
            edited_df['Index_PVF_Freq'] = (edited_df['PVF_Ar'] / base_pvf * 100).round(0).astype(int)
        if base_pl > 0:
            edited_df['Index_P_Litre_Freq'] = (edited_df['P_Litre_Ar'] / base_pl * 100).round(0).astype(int)

        display_df = pd.DataFrame({
            'Marque': edited_df['Marque'],
            'Occasion': edited_df['Occasion'],
            'Rôle OBPPC': edited_df['Role_OBPPC'],
            'Format': edited_df['Description'],
            'Volume (L)': edited_df['Volume_L'],
            'PVF (Ar)': edited_df['PVF_Ar'].round(0).astype(int),
            'Prix / L (Ar)': edited_df['P_Litre_Ar'].round(0).astype(int),
            'Index PVF': edited_df['Index_PVF'].round(0).astype(int),
            'Index P/L': edited_df['Index_P_Litre'].round(0).astype(int),
            'Index PVF / Freq': edited_df['Index_PVF_Freq'].round(0).astype(int),
            'Index P/L / Freq': edited_df['Index_P_Litre_Freq'].round(0).astype(int),
            'Cible': edited_df['Role_OBPPC'].apply(target_label),
            'Statut': edited_df.apply(
                lambda r: check_index_status(r['Index_P_Litre'], r['Role_OBPPC']), axis=1
            ),
        })

        total_sku = len(display_df)
        conformes = (display_df['Statut'] == 'Conforme').sum()
        non_conformes = total_sku - conformes
        taux = (conformes / total_sku * 100) if total_sku else 0

        # ---- KPI tiles résultats ----
        st.markdown('<div class="section-head"><h3>Résultats</h3><span class="hint">Cohérence OBPPC</span></div>', unsafe_allow_html=True)

        r1, r2, r3, r4 = st.columns(4, gap="medium")

        with r1:
            st.markdown(f"""
            <div class="kpi-tile">
                <div>
                    <div class="kpi-tile-label">Références analysées</div>
                    <div class="kpi-tile-value">{total_sku}</div>
                    <div class="kpi-tile-sub">SKU dans le périmètre filtré</div>
                </div>
                <div class="kpi-tile-bar" style="--w:100%"></div>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown(f"""
            <div class="kpi-tile">
                <div>
                    <div class="kpi-tile-label">Positions conformes</div>
                    <div class="kpi-tile-value">{conformes}<span class="unit">/ {total_sku}</span></div>
                    <div class="kpi-tile-sub">Respectent la cible OBPPC</div>
                </div>
                <div class="kpi-tile-bar" style="--w:{int(taux)}%"></div>
            </div>
            """, unsafe_allow_html=True)

        with r3:
            st.markdown(f"""
            <div class="kpi-tile">
                <div>
                    <div class="kpi-tile-label">Non conformes</div>
                    <div class="kpi-tile-value">{non_conformes}</div>
                    <div class="kpi-tile-sub">À réviser</div>
                </div>
                <div class="kpi-tile-bar" style="--w:{100-int(taux)}%"></div>
            </div>
            """, unsafe_allow_html=True)

        with r4:
            st.markdown(f"""
            <div class="kpi-tile">
                <div>
                    <div class="kpi-tile-label">Taux de conformité</div>
                    <div class="kpi-tile-value">{taux:.0f}<span class="unit">%</span></div>
                    <div class="kpi-tile-sub">Cohérence portefeuille</div>
                </div>
                <div class="kpi-tile-bar" style="--w:{int(taux)}%"></div>
            </div>
            """, unsafe_allow_html=True)

        # ---- Tableau de résultats ----
        def style_rows(row):
            if row['Statut'] == 'Conforme':
                base = 'background-color: rgba(63,185,80,0.10); color: #7ee787;'
            elif row['Statut'] == 'Non conforme':
                base = 'background-color: rgba(248,81,73,0.10); color: #ffa198;'
            else:
                base = 'color: #8b949e;'
            return [base] * len(row)

        styled = (
            display_df.style
            .apply(style_rows, axis=1)
            .format({
                'Volume (L)': '{:.2f}',
                'PVF (Ar)': '{:,.0f}',
                'Prix / L (Ar)': '{:,.0f}',
                'Index PVF': '{:d}',
                'Index P/L': '{:d}',
                'Index PVF / Freq': '{:d}',
                'Index P/L / Freq': '{:d}',
            })
            .set_properties(**{
                'font-family': 'Inter, sans-serif',
                'font-size': '12.5px',
                'border-color': 'rgba(48,54,61,0.6)',
            })
            .set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#161b22'),
                    ('color', '#8b949e'),
                    ('font-weight', '600'),
                    ('font-size', '11px'),
                    ('text-transform', 'uppercase'),
                    ('letter-spacing', '0.06em'),
                    ('border-bottom', '1px solid #30363d'),
                    ('padding', '9px 12px'),
                ]},
                {'selector': 'td', 'props': [
                    ('padding', '7px 12px'),
                    ('border-bottom', '1px solid rgba(48,54,61,0.5)'),
                ]},
                {'selector': 'tr:hover td', 'props': [
                    ('background-color', 'rgba(139,92,246,0.06)'),
                ]},
            ])
        )

        st.dataframe(styled, use_container_width=True, height=560)

        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Télécharger les résultats (CSV)",
            data=csv,
            file_name="simulation_obppc.csv",
            mime="text/csv",
        )
