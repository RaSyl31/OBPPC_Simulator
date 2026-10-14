import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Simulateur OBPPC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# CSS
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
        --yellow:      #d29922;
    }

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu, footer { visibility: hidden; }
    [data-testid="stHeader"] { display: none !important; height: 0 !important; }
    [data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
    section.main > div { padding-top: 0 !important; }
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem;
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
    }
    .stApp { background: var(--bg); }

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {
        background: var(--panel) !important;
        border-right: 1px solid var(--border);
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1.25rem;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 0.5rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }

    .sidebar-title {
        display: flex;
        align-items: center;
        gap: 0.55rem;
        padding-bottom: 0.85rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 1.1rem;
    }
    .sidebar-title .mark {
        width: 26px; height: 26px; border-radius: 6px;
        background: linear-gradient(135deg, var(--accent), var(--accent-2));
        box-shadow: 0 0 20px -5px rgba(139,92,246,0.7);
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 700; color: #fff;
    }
    .sidebar-title h2 {
        margin: 0; font-size: 0.88rem; font-weight: 600;
        color: var(--text-hi); letter-spacing: -0.01em;
    }
    .sidebar-title p {
        margin: 0.1rem 0 0 0; font-size: 0.66rem; color: var(--text-faint);
    }

    .sb-section {
        font-size: 0.66rem;
        font-weight: 600;
        color: var(--text-faint);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin: 1rem 0 0.5rem 0;
    }
    .sb-section:first-of-type { margin-top: 0.3rem; }

    .filter-label {
        font-size: 0.66rem; font-weight: 500; color: var(--text-dim);
        text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 0.4rem;
    }

    .sb-stat {
        background: var(--bg);
        border: 1px solid var(--border-hi);
        border-radius: 6px;
        padding: 0.5rem 0.75rem;
        font-size: 0.72rem;
        color: var(--text-dim);
        font-variant-numeric: tabular-nums;
    }
    .sb-stat .n { color: var(--text-hi); font-weight: 600; }

    /* ---------- MULTISELECT ---------- */
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
        background-color: var(--bg) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 6px !important;
        min-height: 36px; height: auto !important;
        padding: 0.25rem 0.45rem !important;
        align-items: flex-start !important;
        flex-wrap: wrap !important; row-gap: 0.25rem !important;
    }
    div[data-testid="stMultiSelect"] [data-baseweb="select"] > div > div {
        flex-wrap: wrap !important; gap: 0.2rem !important;
    }
    div[data-testid="stMultiSelect"] input {
        background: transparent !important; color: var(--text) !important;
    }
    div[data-testid="stMultiSelect"] svg { fill: var(--text-dim) !important; }

    div[data-baseweb="tag"] {
        background: var(--accent) !important; background-color: var(--accent) !important;
        background-image: none !important; border: none !important;
        color: #fff !important; border-radius: 4px !important;
        font-weight: 500 !important; font-size: 0.7rem !important;
        min-height: 20px !important; height: auto !important;
        padding: 0.1rem 0.4rem !important;
        display: inline-flex !important; align-items: center !important;
    }
    div[data-baseweb="tag"] * { background: transparent !important; color: #fff !important; }
    div[data-baseweb="tag"] svg {
        fill: rgba(255,255,255,0.85) !important;
        width: 10px !important; height: 10px !important;
    }

    div[data-baseweb="popover"], div[data-baseweb="menu"] {
        background-color: var(--panel-2) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 6px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.6) !important;
    }
    div[data-baseweb="menu"] li, div[data-baseweb="menu"] [role="option"] {
        background-color: transparent !important; color: var(--text) !important;
        font-size: 0.8rem !important;
    }
    div[data-baseweb="menu"] li:hover, div[data-baseweb="menu"] [role="option"]:hover,
    div[data-baseweb="menu"] [aria-selected="true"] {
        background-color: var(--accent-soft) !important; color: var(--text-hi) !important;
    }
    div[data-testid="stMultiSelect"] label { display: none !important; }

    /* ---------- TABS ---------- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px; background: transparent;
        border-bottom: 1px solid var(--border);
        padding: 0; margin-bottom: 1rem;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 6px 6px 0 0 !important;
        color: var(--text-dim) !important;
        padding: 0.55rem 1rem !important;
        font-size: 0.8rem !important; font-weight: 500 !important;
        border: none !important;
        border-bottom: 2px solid transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: var(--text-hi) !important;
        border-bottom: 2px solid var(--accent) !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none; }

    /* ---------- SECTION HEAD ---------- */
    .section-head {
        display: flex; align-items: baseline; justify-content: space-between;
        margin: 0.75rem 0 0.5rem 0;
    }
    .section-head h3 {
        margin: 0; font-size: 0.82rem; font-weight: 600; color: var(--text-hi);
    }
    .section-head .hint { font-size: 0.68rem; color: var(--text-faint); }

    /* ---------- BUTTONS ---------- */
    .stButton > button {
        border-radius: 6px; font-weight: 500; font-size: 0.8rem;
        padding: 0.42rem 1rem; border: 1px solid var(--border-hi);
        background: var(--panel); color: var(--text); transition: all 0.15s ease;
    }
    .stButton > button:hover {
        border-color: #484f58; background: var(--panel-2); color: var(--text-hi);
    }
    .stButton > button[kind="primary"] {
        background: var(--accent); border: 1px solid var(--accent); color: #fff;
    }
    .stButton > button[kind="primary"]:hover {
        background: #7c3aed; border-color: #7c3aed;
    }

    /* ---------- DATAFRAMES ---------- */
    [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important; overflow: hidden;
    }

    [data-testid="stDownloadButton"] > button {
        border-radius: 6px; font-size: 0.78rem;
        border: 1px solid var(--border-hi); background: var(--panel); color: var(--text);
    }
    [data-testid="stDownloadButton"] > button:hover {
        border-color: var(--accent); color: var(--accent-2);
    }

    .stAlert {
        background-color: var(--panel) !important;
        border: 1px solid var(--border-hi) !important;
        border-radius: 6px !important; color: var(--text) !important;
    }

    /* ---------- PYRAMIDE ---------- */
    .pyramid-wrap {
        background: linear-gradient(180deg, #131820 0%, #0f141b 100%);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 1rem 0.75rem 0.25rem 0.75rem;
    }
    .pyramid-title {
        font-size: 0.68rem; font-weight: 600; color: var(--text-faint);
        text-transform: uppercase; letter-spacing: 0.08em;
        text-align: center; margin-bottom: 0.4rem;
    }

    .role-card {
        background: var(--panel); border: 1px solid var(--border);
        border-left: 3px solid var(--c, var(--accent));
        border-radius: 6px; padding: 0.6rem 0.8rem; margin-bottom: 0.45rem;
    }
    .role-card .name {
        font-size: 0.68rem; color: var(--text-faint); text-transform: uppercase;
        letter-spacing: 0.06em; font-weight: 600;
    }
    .role-card .val {
        font-size: 1.05rem; font-weight: 700; color: var(--text-hi);
        line-height: 1.2; margin-top: 0.15rem;
        font-variant-numeric: tabular-nums;
    }
    .role-card .sub { font-size: 0.68rem; color: var(--text-dim); margin-top: 0.1rem; }

    hr { border-color: var(--border); margin: 0.85rem 0; }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Données
# -----------------------------------------------------------------------------
@st.cache_data
def load_initial_data():
    data = {"Segment": [], "Marque": [], "Occasion": [], "Role_OBPPC": [],
            "Description": [], "Volume_L": [], "PVF_Ar": []}

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
        ('Boisson Gazeuse', 'COCA', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'COCA', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'COCA', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'COCA', 'FC (PET)', 'Upsize (Grand format)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'WOCO', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'WOCO', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'WOCO', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'WOCO', 'FC (PET)', 'Upsize (Grand format)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'FC (VER)', 'Upsize (Grand format)', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'FANTA', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35', 0.35, 1500),
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
# Helpers
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


def normalize_role(role):
    if role in ['Upscale (Premium)', 'Upscale (Super-Premium Niche)']:
        return 'Upscale'
    if role == 'Entry (Entrée de gamme)':
        return 'Entry'
    if role == 'Frequency (Cœur de gamme)':
        return 'Frequency'
    if role == 'Upsize (Grand format)':
        return 'Upsize'
    return 'Autre'


ROLE_COLORS = {
    'Upscale':   '#a855f7',
    'Entry':     '#3b82f6',
    'Frequency': '#10b981',
    'Upsize':    '#f59e0b',
    'Autre':     '#6e7681',
}
ROLE_ORDER = ['Upscale', 'Entry', 'Frequency', 'Upsize']


def status_dot(status):
    if status == 'Conforme':
        return '🟢 Conforme'
    if status == 'Non conforme':
        return '🔴 Non conforme'
    return '⚪ —'


def build_pyramid_svg(role_counts):
    W, H = 520, 380
    apex_y = 30
    base_y = H - 20
    cx = W / 2
    base_half = 190
    total_h = base_y - apex_y

    counts = [(r, role_counts.get(r, 0)) for r in ROLE_ORDER]
    total = sum(c for _, c in counts) or 1

    def half_w(y):
        return base_half * (y - apex_y) / total_h

    svg = [f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" '
           f'style="width:100%; max-width:520px; display:block; margin:0 auto;">']

    y_cur = apex_y
    for role, count in counts:
        share = count / total
        h = share * total_h
        y_next = y_cur + h

        hw_top = half_w(y_cur)
        hw_bot = half_w(y_next)
        color = ROLE_COLORS[role]

        pts = (f"{cx - hw_top:.1f},{y_cur:.1f} "
               f"{cx + hw_top:.1f},{y_cur:.1f} "
               f"{cx + hw_bot:.1f},{y_next:.1f} "
               f"{cx - hw_bot:.1f},{y_next:.1f}")

        svg.append(f'<polygon points="{pts}" fill="{color}" fill-opacity="0.9" '
                   f'stroke="#0d1117" stroke-width="2.5"/>')

        label_y = (y_cur + y_next) / 2
        if h >= 42:
            svg.append(f'<text x="{cx}" y="{label_y - 4}" text-anchor="middle" '
                       f'fill="#ffffff" font-family="Inter,sans-serif" font-size="13" '
                       f'font-weight="700">{role}</text>')
            svg.append(f'<text x="{cx}" y="{label_y + 12}" text-anchor="middle" '
                       f'fill="#ffffff" font-family="Inter,sans-serif" font-size="10" '
                       f'font-weight="500" opacity="0.9">{count} SKU · {share*100:.1f}%</text>')

        y_cur = y_next

    svg.append('</svg>')
    return ''.join(svg)


# -----------------------------------------------------------------------------
# SIDEBAR — Titre + Filtres
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <div class="mark">OB</div>
        <div>
            <h2>Simulateur OBPPC</h2>
            <p>Occasion · Brand · Package · Price · Channel</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sb-section">Segments</div>', unsafe_allow_html=True)
    segments = st.multiselect(
        "Segments", options=ALL_SEGMENTS, default=ALL_SEGMENTS,
        placeholder="Tous les segments", label_visibility="collapsed",
    )

    st.markdown('<div class="sb-section">Marques</div>', unsafe_allow_html=True)
    available_brands = (
        sorted(df_initial[df_initial['Segment'].isin(segments)]['Marque'].unique())
        if segments else []
    )
    brands = st.multiselect(
        "Marques", options=available_brands, default=available_brands,
        placeholder="Toutes les marques", label_visibility="collapsed",
    )

    st.markdown('<div class="sb-section">Périmètre</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="sb-stat">
        <span class="n">{len(segments)}</span> segments
        &nbsp;·&nbsp;
        <span class="n">{len(brands)}</span> marques
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

df_filtered['P_Litre_Ar'] = df_filtered['PVF_Ar'] / df_filtered['Volume_L']
df_filtered['Role_Simple'] = df_filtered['Role_OBPPC'].apply(normalize_role)


# -----------------------------------------------------------------------------
# Onglets
# -----------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Simulateur", "Pyramide OBPPC", "Grille tarifaire", "Diagnostic",
])


# =============================================================================
# TAB 1 — SIMULATEUR
# =============================================================================
with tab1:
    st.markdown('<div class="section-head"><h3>Portefeuille — Édition</h3>'
                '<span class="hint">Ajustez puis recalculez</span></div>',
                unsafe_allow_html=True)

    if df_filtered.empty:
        st.info("Aucune donnée. Sélectionnez au moins un segment et une marque.")
    else:
        editor_height = min(480, 42 + 36 * len(df_filtered))

        edited_df = st.data_editor(
            df_filtered[['Segment', 'Marque', 'Occasion', 'Role_OBPPC',
                         'Description', 'Volume_L', 'PVF_Ar']],
            column_config={
                "Segment": st.column_config.SelectboxColumn(
                    "Segment", options=ALL_SEGMENTS, required=True, width=100),
                "Marque": st.column_config.SelectboxColumn(
                    "Marque", options=ALL_BRANDS, required=True, width=130),
                "Occasion": st.column_config.SelectboxColumn(
                    "Occasion",
                    options=['IC (VER)', 'IC (PET)', 'FC (VER)', 'FC (PET)', 'Upscale', ''],
                    required=False, width=100),
                "Role_OBPPC": st.column_config.SelectboxColumn(
                    "Rôle OBPPC",
                    options=['Entry (Entrée de gamme)', 'Frequency (Cœur de gamme)',
                             'Upsize (Grand format)', 'Upscale (Premium)',
                             'Upscale (Super-Premium Niche)'],
                    required=True, width=180),
                "Description": st.column_config.TextColumn(
                    "Format / Description", width=190),
                "Volume_L": st.column_config.NumberColumn(
                    "Volume (L)", min_value=0.1, step=0.01, format="%.2f",
                    required=True, width=90),
                "PVF_Ar": st.column_config.NumberColumn(
                    "PVF (Ar)", min_value=0, step=100, format="%d",
                    required=True, width=110),
            },
            hide_index=True, use_container_width=True, num_rows="fixed",
            key="data_editor", height=editor_height, row_height=34,
        )

        col_btn, _ = st.columns([1, 4])
        with col_btn:
            calculate_button = st.button("Recalculer les index",
                                         type="primary", use_container_width=True)

        if calculate_button:
            e = edited_df.copy()
            e['P_Litre_Ar'] = e['PVF_Ar'] / e['Volume_L']

            freq_all = e[e['Role_OBPPC'].str.contains('Frequency', na=False)]
            base_pl = freq_all['P_Litre_Ar'].mean() if len(freq_all) else e['P_Litre_Ar'].mean()

            e['Index_P_Litre'] = (e['P_Litre_Ar'] / base_pl * 100).round(0).astype(int)
            e['Statut'] = e.apply(
                lambda r: check_index_status(r['Index_P_Litre'], r['Role_OBPPC']), axis=1)

            display_df = pd.DataFrame({
                'Marque': e['Marque'],
                'Occasion': e['Occasion'],
                'Rôle OBPPC': e['Role_OBPPC'],
                'Format': e['Description'],
                'Volume (L)': e['Volume_L'].astype(float),
                'PVF (Ar)': e['PVF_Ar'].round(0).astype(int),
                'Prix / L (Ar)': e['P_Litre_Ar'].round(0).astype(int),
                'Index P/L': e['Index_P_Litre'],
                'Cible': e['Role_OBPPC'].apply(target_label),
                'Statut': e['Statut'].apply(status_dot),
            })

            st.dataframe(
                display_df,
                use_container_width=True,
                height=min(520, 42 + 35 * len(display_df)),
                column_config={
                    "Volume (L)": st.column_config.NumberColumn(
                        "Volume (L)", format="%.2f"),
                    "PVF (Ar)": st.column_config.NumberColumn(
                        "PVF (Ar)", format="%d"),
                    "Prix / L (Ar)": st.column_config.NumberColumn(
                        "Prix / L (Ar)", format="%d"),
                    "Index P/L": st.column_config.NumberColumn(
                        "Index P/L", format="%d"),
                    "Statut": st.column_config.TextColumn("Statut", width="small"),
                },
                hide_index=True,
            )

            csv = display_df.to_csv(index=False)
            st.download_button("Télécharger les résultats (CSV)", data=csv,
                               file_name="simulation_obppc.csv", mime="text/csv")


# =============================================================================
# TAB 2 — PYRAMIDE
# =============================================================================
with tab2:
    st.markdown('<div class="section-head"><h3>Pyramide OBPPC</h3>'
                '<span class="hint">Répartition des SKU par rôle</span></div>',
                unsafe_allow_html=True)

    if df_filtered.empty:
        st.info("Aucune donnée à afficher.")
    else:
        seg_options = ['Tous'] + sorted(df_filtered['Segment'].unique().tolist())
        seg_choice = st.radio(
            "Segment", seg_options, horizontal=True,
            label_visibility="collapsed", key="pyr_seg",
        )
        sub = df_filtered if seg_choice == 'Tous' else df_filtered[df_filtered['Segment'] == seg_choice]
        role_counts = sub['Role_Simple'].value_counts().to_dict()

        col_pyr, col_stats = st.columns([1.4, 1], gap="large")

        with col_pyr:
            pyramid_svg = build_pyramid_svg(role_counts)
            st.markdown(f"""
            <div class="pyramid-wrap">
                <div class="pyramid-title">Pyramide tarifaire — {seg_choice if seg_choice != 'Tous' else 'Portefeuille global'}</div>
                {pyramid_svg}
            </div>
            """, unsafe_allow_html=True)

        with col_stats:
            st.markdown('<div class="section-head"><h3>Détail par rôle</h3></div>',
                        unsafe_allow_html=True)
            total_roles = sum(role_counts.values()) or 1
            for role in ROLE_ORDER:
                cnt = role_counts.get(role, 0)
                share = cnt / total_roles * 100
                sub_role = sub[sub['Role_Simple'] == role]
                avg_price = sub_role['P_Litre_Ar'].mean() if len(sub_role) else 0
                target = {'Upscale': '≥ 111', 'Entry': '101 – 110',
                          'Frequency': '100', 'Upsize': '90 – 99'}[role]
                st.markdown(f"""
                <div class="role-card" style="--c:{ROLE_COLORS[role]};">
                    <div class="name">{role}</div>
                    <div class="val">{cnt} SKU <span style="color:var(--text-dim); font-size:0.8rem;">· {share:.1f}%</span></div>
                    <div class="sub">Prix moyen / L : {avg_price:,.0f} Ar · Cible {target}</div>
                </div>
                """, unsafe_allow_html=True)


# =============================================================================
# TAB 3 — GRILLE TARIFAIRE
# =============================================================================
with tab3:
    st.markdown('<div class="section-head"><h3>Grille tarifaire</h3>'
                '<span class="hint">Marques × formats · Prix en Ar</span></div>',
                unsafe_allow_html=True)

    if df_filtered.empty:
        st.info("Aucune donnée à afficher.")
    else:
        seg_options3 = sorted(df_filtered['Segment'].unique().tolist())
        seg3 = st.selectbox("Segment", seg_options3, key="grid_seg",
                            label_visibility="collapsed")
        sub3 = df_filtered[df_filtered['Segment'] == seg3].copy()

        def parse_vol(col):
            nums = [int(s) for s in ''.join(c if c.isdigit() else ' ' for c in col).split()]
            return nums[0] if nums else 999

        pivot = sub3.pivot_table(
            index='Marque', columns='Description', values='PVF_Ar', aggfunc='mean'
        )
        pivot = pivot[sorted(pivot.columns, key=parse_vol)]
        pivot = pivot.round(0)

        fmt_cols = {c: st.column_config.NumberColumn(c, format="%d") for c in pivot.columns}
        st.dataframe(
            pivot.reset_index(),
            use_container_width=True,
            height=min(500, 42 + 35 * len(pivot)),
            column_config=fmt_cols,
            hide_index=True,
        )

        st.markdown(
            '<div style="font-size:0.7rem; color:var(--text-dim); margin:0.5rem 0 1rem 0;">'
            'Les cellules vides correspondent à des formats non proposés par la marque.</div>',
            unsafe_allow_html=True,
        )

        csv = pivot.to_csv()
        st.download_button("Exporter la grille (CSV)", data=csv,
                           file_name=f"grille_{seg3.lower().replace(' ', '_')}.csv",
                           mime="text/csv")

        st.markdown('<div class="section-head"><h3>Prix au litre</h3>'
                    '<span class="hint">Comparaison économique</span></div>',
                    unsafe_allow_html=True)

        pivot_pl = sub3.pivot_table(
            index='Marque', columns='Description', values='P_Litre_Ar', aggfunc='mean'
        )
        pivot_pl = pivot_pl[sorted(pivot_pl.columns, key=parse_vol)].round(0)

        fmt_cols_pl = {c: st.column_config.NumberColumn(c, format="%d") for c in pivot_pl.columns}
        st.dataframe(
            pivot_pl.reset_index(),
            use_container_width=True,
            height=min(400, 42 + 35 * len(pivot_pl)),
            column_config=fmt_cols_pl,
            hide_index=True,
        )


# =============================================================================
# TAB 4 — DIAGNOSTIC
# =============================================================================
with tab4:
    st.markdown('<div class="section-head"><h3>Diagnostic de conformité</h3>'
                '<span class="hint">Index P/L vs référence Frequency</span></div>',
                unsafe_allow_html=True)

    if df_filtered.empty:
        st.info("Aucune donnée à afficher.")
    else:
        diag = df_filtered.copy()

        freq_all = diag[diag['Role_OBPPC'].str.contains('Frequency', na=False)]
        base_global = freq_all['P_Litre_Ar'].mean() if len(freq_all) else diag['P_Litre_Ar'].mean()

        base_by_seg = (
            diag[diag['Role_OBPPC'].str.contains('Frequency', na=False)]
            .groupby('Segment')['P_Litre_Ar'].mean().to_dict()
        )

        diag['Base_Ref'] = diag['Segment'].map(base_by_seg).fillna(base_global)
        diag['Index'] = (diag['P_Litre_Ar'] / diag['Base_Ref'] * 100).round(0).astype(int)
        diag['Statut'] = diag.apply(
            lambda r: check_index_status(r['Index'], r['Role_OBPPC']), axis=1)
        diag['Cible'] = diag['Role_OBPPC'].apply(target_label)

        st.markdown('<div class="section-head"><h3>Conformité par segment</h3></div>',
                    unsafe_allow_html=True)

        seg_stats = []
        for s in sorted(diag['Segment'].unique()):
            sub_s = diag[diag['Segment'] == s]
            tot = len(sub_s)
            conf = (sub_s['Statut'] == 'Conforme').sum()
            seg_stats.append({'Segment': s, 'Total': tot, 'Conformes': conf,
                              'Taux': conf / tot * 100 if tot else 0})

        for s in seg_stats:
            pct = s['Taux']
            color = '#3fb950' if pct >= 70 else '#d29922' if pct >= 40 else '#f85149'
            st.markdown(f"""
            <div style="display:flex; align-items:center; gap:1rem; margin-bottom:0.4rem;">
                <div style="width:130px; font-size:0.8rem; color:var(--text-hi); font-weight:500;">
                    {s['Segment']}
                </div>
                <div style="flex:1; height:18px; background:var(--panel);
                            border:1px solid var(--border); border-radius:4px; overflow:hidden;">
                    <div style="height:100%; width:{pct:.1f}%; background:{color};
                                opacity:0.9;"></div>
                </div>
                <div style="width:170px; text-align:right; font-size:0.75rem;
                            color:var(--text-dim); font-variant-numeric:tabular-nums;">
                    <span style="color:{color}; font-weight:600;">{s['Taux']:.0f}%</span>
                    &nbsp;·&nbsp; {s['Conformes']}/{s['Total']} SKU
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<hr>', unsafe_allow_html=True)

        st.markdown('<div class="section-head"><h3>Positions à réviser</h3>'
                    '<span class="hint">Triées par écart à la cible</span></div>',
                    unsafe_allow_html=True)

        non_conf_df = diag[diag['Statut'] == 'Non conforme'].copy()

        if len(non_conf_df) == 0:
            st.success("Toutes les positions respectent la cible OBPPC.")
        else:
            def compute_gap(row):
                idx = row['Index']; role = row['Role_OBPPC']
                if role == 'Entry (Entrée de gamme)':
                    return max(0, 101 - idx, idx - 110)
                if role == 'Frequency (Cœur de gamme)':
                    return abs(idx - 100)
                if role == 'Upsize (Grand format)':
                    return max(0, 90 - idx, idx - 99)
                if role in ['Upscale (Premium)', 'Upscale (Super-Premium Niche)']:
                    return max(0, 111 - idx)
                return 0

            non_conf_df['Écart'] = non_conf_df.apply(compute_gap, axis=1)
            non_conf_df = non_conf_df.sort_values('Écart', ascending=False)

            issues_df = pd.DataFrame({
                'Marque': non_conf_df['Marque'],
                'Format': non_conf_df['Description'],
                'Rôle': non_conf_df['Role_OBPPC'],
                'Prix / L (Ar)': non_conf_df['P_Litre_Ar'].round(0).astype(int),
                'Index': non_conf_df['Index'],
                'Cible': non_conf_df['Cible'],
                'Écart': non_conf_df['Écart'].astype(int),
                'Statut': non_conf_df['Statut'].apply(status_dot),
            })

            st.dataframe(
                issues_df,
                use_container_width=True,
                height=min(400, 42 + 35 * len(issues_df)),
                column_config={
                    "Prix / L (Ar)": st.column_config.NumberColumn(
                        "Prix / L (Ar)", format="%d"),
                    "Index": st.column_config.NumberColumn("Index", format="%d"),
                    "Écart": st.column_config.NumberColumn("Écart", format="%d"),
                    "Statut": st.column_config.TextColumn("Statut", width="small"),
                },
                hide_index=True,
            )

        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<div class="section-head"><h3>Recommandations</h3></div>',
                    unsafe_allow_html=True)

        total = len(diag)
        conf = (diag['Statut'] == 'Conforme').sum()
        taux = conf / total * 100 if total else 0

        if taux >= 80:
            verdict = ("Portefeuille globalement cohérent. Les écarts résiduels "
                       "relèvent d'ajustements fins plutôt que de repositionnements.")
            color = '#3fb950'
        elif taux >= 50:
            verdict = ("Cohérence partielle. Plusieurs références s'écartent de leur "
                       "rôle cible : revoir les prix au litre ou repositionner les rôles.")
            color = '#d29922'
        else:
            verdict = ("Cohérence faible. La structure tarifaire ne respecte pas la "
                       "logique OBPPC : arbitrage prix / rôle à reprendre en priorité.")
            color = '#f85149'

        st.markdown(f"""
        <div style="background:var(--panel); border:1px solid var(--border);
                    border-left:3px solid {color}; border-radius:6px;
                    padding:0.9rem 1.1rem;">
            <div style="font-size:0.68rem; text-transform:uppercase;
                        letter-spacing:0.08em; color:var(--text-faint);
                        font-weight:600;">Verdict</div>
            <div style="font-size:0.88rem; color:var(--text-hi); margin-top:0.4rem;
                        line-height:1.5;">{verdict}</div>
            <div style="font-size:0.75rem; color:var(--text-dim); margin-top:0.5rem;
                        font-variant-numeric:tabular-nums;">
                {conf} SKU conformes sur {total} · taux global {taux:.0f}%
            </div>
        </div>
        """, unsafe_allow_html=True)
