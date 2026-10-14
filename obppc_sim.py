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
# Dark theme — design premium
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg:           #0a0e1a;
        --bg-elev:      #131826;
        --bg-elev-2:    #1a2234;
        --border:       #1f2937;
        --border-soft:  rgba(99,102,241,0.18);
        --text:         #e2e8f0;
        --text-dim:     #94a3b8;
        --text-faint:   #64748b;
        --accent:       #6366f1;
        --accent-2:     #06b6d4;
        --accent-3:     #8b5cf6;
        --success:      #10b981;
        --danger:       #ef4444;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    #MainMenu, footer, header {visibility: hidden;}

    /* ---------- Background global ---------- */
    .stApp {
        background:
            radial-gradient(1200px 700px at 12% -10%, rgba(99,102,241,0.12), transparent 60%),
            radial-gradient(1000px 600px at 95% 0%,   rgba(6,182,212,0.09),  transparent 60%),
            radial-gradient(800px 500px at 50% 100%,  rgba(139,92,246,0.07), transparent 65%),
            #0a0e1a;
        background-attachment: fixed;
    }

    .main .block-container {
        padding-top: 1.25rem;
        padding-bottom: 3rem;
        max-width: 1600px;
    }

    /* ============================================================
       HEADER UNIFIÉ : titre + filtres
       ============================================================ */
    .app-shell {
        position: relative;
        background: linear-gradient(135deg, rgba(30,41,59,0.85), rgba(15,23,42,0.9));
        border: 1px solid rgba(99,102,241,0.28);
        border-radius: 16px;
        padding: 1.5rem 1.75rem 1.35rem 1.75rem;
        margin-bottom: 1.75rem;
        overflow: hidden;
        box-shadow:
            0 0 0 1px rgba(99,102,241,0.06),
            0 30px 60px -25px rgba(99,102,241,0.45);
    }
    .app-shell::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(900px 220px at 0% 0%, rgba(99,102,241,0.30), transparent 60%);
        pointer-events: none;
    }

    .shell-head {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        padding-bottom: 1.15rem;
        border-bottom: 1px dashed rgba(148,163,184,0.18);
        margin-bottom: 1.15rem;
    }
    .shell-head h1 {
        margin: 0;
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        background: linear-gradient(90deg, #ffffff 0%, #c7d2fe 60%, #a5b4fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .shell-head .subtitle {
        margin: 0.35rem 0 0 0;
        color: var(--text-dim);
        font-size: 0.85rem;
        font-weight: 400;
    }
    .shell-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(99,102,241,0.12);
        color: #c7d2fe;
        padding: 0.45rem 0.85rem;
        border-radius: 6px;
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        border: 1px solid rgba(99,102,241,0.35);
        white-space: nowrap;
    }
    .shell-badge .dot {
        width: 6px; height: 6px; border-radius: 50%;
        background: #22d3ee;
        box-shadow: 0 0 10px #22d3ee, 0 0 20px rgba(34,211,238,0.5);
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%      { opacity: 0.55; transform: scale(0.85); }
    }

    .filter-label {
        font-size: 0.68rem;
        font-weight: 700;
        color: #a5b4fc;
        text-transform: uppercase;
        letter-spacing: 0.13em;
        margin-bottom: 0.5rem;
    }

    .filter-stat {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        min-height: 70px;
        padding: 0.75rem 1rem;
        background: rgba(99,102,241,0.08);
        border: 1px solid rgba(99,102,241,0.25);
        border-radius: 10px;
    }
    .filter-stat-label {
        font-size: 0.66rem;
        font-weight: 700;
        color: #a5b4fc;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        margin-bottom: 0.45rem;
    }
    .filter-stat-value {
        font-size: 0.95rem;
        font-weight: 600;
        color: #e2e8f0;
        font-variant-numeric: tabular-nums;
    }
    .filter-stat-value .dim {
        color: #64748b;
        font-weight: 500;
        font-size: 0.85rem;
    }

    /* ---------- Section titles ---------- */
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        font-size: 1.02rem;
        font-weight: 600;
        color: var(--text);
        margin: 1.5rem 0 0.75rem 0;
        letter-spacing: -0.01em;
    }
    .section-title::before {
        content: "";
        width: 3px;
        height: 18px;
        border-radius: 2px;
        background: linear-gradient(180deg, var(--accent), var(--accent-2));
        box-shadow: 0 0 12px rgba(99,102,241,0.6);
    }
    .section-caption {
        font-size: 0.82rem;
        color: var(--text-faint);
        margin-bottom: 1rem;
        padding-left: 0.9rem;
    }

    /* ============================================================
       MULTISELECT
       ============================================================ */
    div[data-testid="stMultiSelect"] { width: 100%; }
    div[data-testid="stMultiSelect"] > div { width: 100%; }

    div[data-testid="stMultiSelect"] [data-baseweb="select"],
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    div[data-testid="stMultiSelect"] [data-baseweb="input"],
    div[data-testid="stMultiSelect"] [data-baseweb="input"] > div {
        background-color: #131826 !important;
        background-image: none !important;
        border-color: rgba(99,102,241,0.3) !important;
        color: #e2e8f0 !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        border: 1px solid rgba(99,102,241,0.3) !important;
        border-radius: 10px !important;
        min-height: 46px;
        height: auto !important;
        padding: 0.4rem 0.55rem !important;
        box-shadow: none !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
        align-items: flex-start !important;
        flex-wrap: wrap !important;
        row-gap: 0.35rem !important;
    }
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div:hover {
        border-color: rgba(99,102,241,0.6) !important;
    }
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div:focus-within {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.22) !important;
    }

    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
        flex-wrap: wrap !important;
        align-items: center !important;
        gap: 0.3rem !important;
        min-height: 26px;
    }

    div[data-testid="stMultiSelect"] input {
        background-color: transparent !important;
        color: #e2e8f0 !important;
        min-height: 26px;
    }
    div[data-testid="stMultiSelect"] input::placeholder {
        color: #64748b !important;
    }

    div[data-testid="stMultiSelect"] svg {
        fill: #94a3b8 !important;
        color: #94a3b8 !important;
    }

    /* -- TAGS -- */
    div[data-baseweb="tag"] {
        background: #6366f1 !important;
        background-color: #6366f1 !important;
        background-image: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        border: 1px solid rgba(165,180,252,0.35) !important;
        color: #ffffff !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
        font-size: 0.78rem !important;
        min-height: 26px !important;
        height: auto !important;
        padding: 0.28rem 0.6rem !important;
        box-shadow: 0 2px 8px -3px rgba(99,102,241,0.7) !important;
        display: inline-flex !important;
        align-items: center !important;
        line-height: 1.15 !important;
        max-width: 100%;
    }
    div[data-baseweb="tag"] * {
        background: transparent !important;
        background-color: transparent !important;
        color: #ffffff !important;
    }
    div[data-baseweb="tag"] svg {
        fill: #e0e7ff !important;
        color: #e0e7ff !important;
        width: 12px !important;
        height: 12px !important;
    }
    div[data-baseweb="tag"] svg:hover {
        fill: #ffffff !important;
    }

    /* -- Dropdown -- */
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] [role="listbox"],
    div[data-baseweb="menu"] {
        background-color: #131826 !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        border-radius: 10px !important;
        color: #e2e8f0 !important;
        box-shadow:
            0 20px 50px -15px rgba(0,0,0,0.9),
            0 0 40px -20px rgba(99,102,241,0.5) !important;
    }
    div[data-baseweb="menu"] li,
    div[data-baseweb="menu"] [role="option"] {
        background-color: transparent !important;
        color: #e2e8f0 !important;
        font-size: 0.85rem !important;
    }
    div[data-baseweb="menu"] li:hover,
    div[data-baseweb="menu"] [role="option"]:hover {
        background-color: rgba(99,102,241,0.18) !important;
        color: #ffffff !important;
    }
    div[data-baseweb="menu"] [aria-selected="true"] {
        background-color: rgba(99,102,241,0.25) !important;
        color: #ffffff !important;
    }

    div[data-testid="stMultiSelect"] label { display: none !important; }

    /* ---------- KPI cards ---------- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 0.9rem;
        margin: 0.5rem 0 1.4rem 0;
    }
    .kpi-card {
        position: relative;
        background: linear-gradient(160deg, rgba(26,34,52,0.9), rgba(15,23,42,0.9));
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.05rem 1.15rem;
        overflow: hidden;
        transition: border-color 0.2s ease, transform 0.2s ease;
    }
    .kpi-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(90deg, var(--accent), var(--accent-2));
        opacity: 0.85;
    }
    .kpi-card:hover {
        border-color: rgba(99,102,241,0.45);
        transform: translateY(-2px);
    }
    .kpi-label {
        font-size: 0.68rem;
        font-weight: 600;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 0.09em;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #ffffff;
        line-height: 1.05;
        letter-spacing: -0.02em;
    }
    .kpi-value .unit {
        font-size: 0.85rem;
        color: var(--text-dim);
        font-weight: 500;
        margin-left: 0.2rem;
    }
    .kpi-sub {
        font-size: 0.72rem;
        color: var(--text-faint);
        margin-top: 0.4rem;
    }

    /* ---------- Boutons ---------- */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.88rem;
        padding: 0.55rem 1.2rem;
        border: 1px solid var(--border-soft);
        background: var(--bg-elev);
        color: var(--text);
        transition: all 0.18s ease;
    }
    .stButton > button:hover {
        border-color: rgba(99,102,241,0.55);
        color: #ffffff;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
        color: #ffffff;
        box-shadow: 0 10px 30px -10px rgba(99,102,241,0.7);
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        box-shadow: 0 14px 35px -10px rgba(99,102,241,0.9);
        transform: translateY(-1px);
    }

    /* ---------- Dataframes & Data editor ---------- */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        border: 1px solid rgba(99,102,241,0.25) !important;
        border-radius: 14px !important;
        overflow: hidden;
        box-shadow:
            0 0 0 1px rgba(99,102,241,0.05),
            0 30px 60px -30px rgba(0,0,0,0.9),
            0 0 80px -40px rgba(99,102,241,0.4);
        background: linear-gradient(160deg, rgba(19,24,38,0.9), rgba(10,14,26,0.9));
    }
    [data-testid="stDataFrame"]::before,
    [data-testid="stDataEditor"]::before {
        content: "";
        display: block;
        height: 2px;
        background: linear-gradient(90deg, #6366f1, #06b6d4, #8b5cf6);
        opacity: 0.9;
    }

    /* ---------- Download button ---------- */
    [data-testid="stDownloadButton"] > button {
        border-radius: 8px;
        font-size: 0.85rem;
        border: 1px solid var(--border-soft);
        background: var(--bg-elev);
        color: var(--text);
    }
    [data-testid="stDownloadButton"] > button:hover {
        border-color: rgba(6,182,212,0.55);
        color: #67e8f9;
    }

    .stAlert {
        background-color: rgba(99,102,241,0.08) !important;
        border: 1px solid rgba(99,102,241,0.3) !important;
        border-radius: 10px !important;
        color: #c7d2fe !important;
    }

    hr { border-color: var(--border); margin: 1.4rem 0; }
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
# HEADER UNIFIÉ — Titre + Filtres
# -----------------------------------------------------------------------------
with st.container():
    st.markdown("""
    <div class="app-shell" style="padding-bottom:1rem; margin-bottom:0.75rem;">
        <div class="shell-head" style="border-bottom:none; padding-bottom:0; margin-bottom:0;">
            <div>
                <h1>Simulateur OBPPC</h1>
                <p class="subtitle">Occasion · Brand · Package · Price · Channel — analyse de cohérence pricing</p>
            </div>
            <div class="shell-badge"><span class="dot"></span>Pricing Analytics</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
        st.markdown('<div class="filter-label">&nbsp;</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="filter-stat">
            <div class="filter-stat-label">Sélection active</div>
            <div class="filter-stat-value">
                {len(segments)} segment{'s' if len(segments) != 1 else ''}
                <span class="dim">·</span>
                {len(brands)} marque{'s' if len(brands) != 1 else ''}
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
# Tableau éditable — HAUTEUR AUGMENTÉE
# -----------------------------------------------------------------------------
st.markdown('<div class="section-title">Portefeuille — Édition</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-caption">Ajustez les volumes, PVF et rôles OBPPC, puis lancez le recalcul.</div>',
    unsafe_allow_html=True,
)

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
        height=650,          # ← 420 avant → 650 maintenant
        row_height=38,       # ← lignes un peu plus aérées
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
        taux = (conformes / total_sku * 100) if total_sku else 0
        prix_moyen_l = edited_df['P_Litre_Ar'].mean() if total_sku else 0

        st.markdown('<div class="section-title">Résultats</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Références analysées</div>
                <div class="kpi-value">{total_sku}</div>
                <div class="kpi-sub">SKU dans le périmètre filtré</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Prix moyen / L</div>
                <div class="kpi-value">{prix_moyen_l:,.0f}<span class="unit">Ar</span></div>
                <div class="kpi-sub">Moyenne tous rôles OBPPC</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Positions conformes</div>
                <div class="kpi-value">{conformes}<span class="unit">/ {total_sku}</span></div>
                <div class="kpi-sub">Respectent la cible OBPPC</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Taux de conformité</div>
                <div class="kpi-value">{taux:.0f}<span class="unit">%</span></div>
                <div class="kpi-sub">Cohérence portefeuille</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        def style_rows(row):
            if row['Statut'] == 'Conforme':
                base = 'background-color: rgba(16,185,129,0.10); color: #d1fae5;'
            elif row['Statut'] == 'Non conforme':
                base = 'background-color: rgba(239,68,68,0.10); color: #fee2e2;'
            else:
                base = 'color: #94a3b8;'
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
                'font-size': '13px',
                'border-color': 'rgba(99,102,241,0.15)',
            })
            .set_table_styles([
                {'selector': 'th', 'props': [
                    ('background-color', '#131826'),
                    ('color', '#a5b4fc'),
                    ('font-weight', '600'),
                    ('font-size', '12px'),
                    ('text-transform', 'uppercase'),
                    ('letter-spacing', '0.05em'),
                    ('border-bottom', '1px solid rgba(99,102,241,0.25)'),
                    ('padding', '10px 12px'),
                ]},
                {'selector': 'td', 'props': [
                    ('padding', '8px 12px'),
                    ('border-bottom', '1px solid rgba(148,163,184,0.08)'),
                ]},
                {'selector': 'tr:hover td', 'props': [
                    ('background-color', 'rgba(99,102,241,0.08)'),
                ]},
            ])
        )

        # Tableau résultats — hauteur augmentée aussi
        st.dataframe(styled, use_container_width=True, height=600)

        csv = display_df.to_csv(index=False)
        st.download_button(
            label="Télécharger les résultats (CSV)",
            data=csv,
            file_name="simulation_obppc.csv",
            mime="text/csv",
        )
