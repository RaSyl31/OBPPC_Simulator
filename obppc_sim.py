import streamlit as st
import pandas as pd

# =============================================================================
# CONFIGURATION
# =============================================================================
st.set_page_config(
    page_title="Simulateur OBPPC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =============================================================================
# CSS — dark bleu partout (dropdowns, menus, éditeur, onglets)
# =============================================================================
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-size: 15px;
        line-height: 1.55;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0a1929 !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #0e2338 !important;
        border-right: 1px solid #1e4976;
    }
    section[data-testid="stSidebar"] * { color: #ffffff !important; }

    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; }
    p, span, div, label, li { color: #ffffff; }
    [data-testid="stCaptionContainer"] p,
    .stCaption { color: #a8c0dd !important; }

    /* ---------- INPUTS / SELECT ---------- */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
    }
    [data-baseweb="select"] div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="input"] input {
        color: #ffffff !important;
    }
    [data-baseweb="select"] input::placeholder,
    [data-baseweb="input"] input::placeholder {
        color: #a8c0dd !important;
        opacity: 1 !important;
    }
    [data-baseweb="select"] svg,
    [data-testid="stMultiSelect"] svg {
        fill: #a8c0dd !important;
        color: #a8c0dd !important;
    }

    /* ---------- TAGS MULTISELECT ---------- */
    [data-baseweb="tag"] {
        background-color: #4a9eff !important;
        color: #ffffff !important;
        border: none !important;
    }
    [data-baseweb="tag"] *,
    [data-baseweb="tag"] span,
    [data-baseweb="tag"] div,
    [data-baseweb="tag"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
        background-color: transparent !important;
    }

    /* ---------- DROPDOWN / POPOVER ---------- */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] [role="dialog"],
    [data-baseweb="menu"],
    [data-baseweb="menu"] > div,
    div[role="listbox"],
    ul[role="listbox"] {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
    }
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"],
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] [role="option"],
    div[role="option"],
    li[role="option"] {
        background-color: #132f4c !important;
        color: #ffffff !important;
        font-size: 0.9rem !important;
    }
    [data-baseweb="menu"] li *,
    [data-baseweb="menu"] [role="option"] *,
    [data-baseweb="popover"] li *,
    [data-baseweb="popover"] [role="option"] *,
    [role="option"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] [role="option"]:hover,
    [role="option"]:hover {
        background-color: #1e4976 !important;
        color: #ffffff !important;
    }
    [data-baseweb="menu"] [aria-selected="true"],
    [data-baseweb="popover"] [aria-selected="true"],
    [role="option"][aria-selected="true"] {
        background-color: #4a9eff !important;
        color: #ffffff !important;
    }
    [role="option"][aria-selected="true"] * {
        color: #ffffff !important;
    }

    /* ---------- RADIO / CHECKBOX ---------- */
    .stRadio label, .stCheckbox label,
    .stRadio > div > label > div { color: #ffffff !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #ffffff !important; }

    /* ---------- BOUTONS ---------- */
    .stButton > button,
    [data-testid="stDownloadButton"] > button {
        background-color: #132f4c !important;
        color: #ffffff !important;
        border: 1px solid #1e4976 !important;
        border-radius: 6px;
    }
    .stButton > button:hover,
    [data-testid="stDownloadButton"] > button:hover {
        background-color: #1e4976 !important;
        border-color: #4a9eff !important;
        color: #ffffff !important;
    }

    /* ---------- METRICS ---------- */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"] { color: #ffffff !important; }

    /* ---------- TABS ---------- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #1e4976;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a8c0dd !important;
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"] * { color: inherit !important; }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #4a9eff !important;
    }

    /* ---------- DATAFRAME / DATA EDITOR ---------- */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        border-radius: 8px;
    }
    [data-testid="stDataEditor"] [data-testid="stElementToolbar"] button,
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"] button {
        background-color: transparent !important;
        color: #ffffff !important;
        border-color: #1e4976 !important;
    }
    [data-testid="stDataEditor"] [data-testid="stElementToolbar"] button:hover {
        background-color: #1e4976 !important;
    }
    [data-testid="stDataEditor"] canvas,
    [data-testid="stDataFrame"] canvas {
        background-color: #132f4c !important;
    }

    /* ---------- ALERTS ---------- */
    .stAlert {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
    }
    .stAlert *, .stAlert p { color: #ffffff !important; }

    /* ---------- DIVERS ---------- */
    hr { border-color: #1e4976 !important; }
    strong, b { color: #ffffff !important; }
    a { color: #4a9eff !important; }

    [role="listbox"] *,
    [role="option"] *,
    [role="dialog"] * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DONNÉES
# =============================================================================
@st.cache_data
def load_data():
    rows = [
        # --- ENERGIE ---
        ('Energie', 'Red Bull', 'IC', 'Upscale', 'CAN 25', 0.25, 9900),
        ('Energie', 'Monster', 'IC', 'Upscale', 'CAN 50', 0.50, 9900),
        ('Energie', 'FOSA', 'IC', 'Upscale', 'CAN 50', 0.50, 5000),
        ('Energie', 'XXL', 'IC', 'Entry', 'VC 30', 0.30, 2500),
        ('Energie', 'XXL', 'IC', 'Frequency', 'PET 35', 0.35, 3500),
        ('Energie', 'XXL', 'IC', 'Frequency', 'PET 50', 0.50, 5000),
        ('Energie', 'XXL', 'IC', 'Upscale', 'CAN 33', 0.33, 4000),
        ('Energie', 'DYNAMIC', 'IC', 'Upscale', 'CAN 25', 0.25, 3500),
        ('Energie', 'BOOST VITALITY', 'IC', 'Upscale', 'CAN 33', 0.33, 4000),

        # --- BOISSON GAZEUSE ---
        ('Boisson Gazeuse', 'COCA', 'IC', 'Entry', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'COCA', 'IC', 'Frequency', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'COCA', 'IC', 'Upscale', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'COCA', 'FC', 'Upsize', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'IC', 'Entry', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'WOCO', 'IC', 'Frequency', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'WOCO', 'IC', 'Upscale', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'WOCO', 'IC', 'Entry', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'WOCO', 'FC', 'Upsize', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'FC', 'Upsize', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'FANTA', 'IC', 'Entry', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'FANTA', 'IC', 'Frequency', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'FANTA', 'FC', 'Upsize', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Frequency', 'PET 35', 0.35, 1500),  # RÉFÉRENCE BG
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Frequency', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Upscale', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Entry', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'CAPRICE', 'FC', 'Upsize', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'CAPRICE', 'FC', 'Upsize', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'TONIC', 'IC', 'Entry', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'TONIC', 'FC', 'Upsize', 'VC 100', 1.00, 3000),

        # --- EAUX ---
        ('Eaux', 'Cristal', 'IC', 'Entry', 'Cristal 30 VER', 0.30, 1500),
        ('Eaux', 'Cristal', 'IC', 'Frequency', 'Cristal 50 VER', 0.50, 2200),
        ('Eaux', 'Cristal', 'FC', 'Upsize', 'Cristal 100 VER', 1.00, 3800),
        ('Eaux', 'Cristal', 'FC', 'Upsize', 'Cristal 150 PET', 1.50, 5500),
        ('Eaux', 'RANOVISY', 'IC', 'Entry', 'RANOVISY 33 PET', 0.33, 1000),
        ('Eaux', 'RANOVISY', 'IC', 'Frequency', 'RANOVISY 50 PET', 0.50, 2400),
        ('Eaux', 'RANOVISY', 'IC', 'Upsize', 'RANOVISY 75 PET', 0.75, 3000),
        ('Eaux', 'VISY GASY', 'IC', 'Entry', 'VISY GASY 60 PET', 0.60, 2500),
        ('Eaux', 'VISY GASY', 'FC', 'Upsize', 'VISY GASY 100 PET', 1.00, 3000),
        ('Eaux', 'Eau vive', 'IC', 'Entry', 'Eau vive 50 PET', 0.50, 1600),
        ('Eaux', 'Eau vive', 'FC', 'Upsize', 'Eau vive 150 PET', 1.50, 3300),
        ('Eaux', 'Eau vive', 'IC', 'Frequency', 'Eau vive 50 VER', 0.50, 2200),
        ('Eaux', 'Cristalline', 'FC', 'Frequency', 'Cristalline 100 PET', 1.00, 2100),  # RÉFÉRENCE EAUX
        ('Eaux', 'Cristalline', 'FC', 'Upsize', 'Cristalline 200 PET', 2.00, 3600),
        ('Eaux', 'OLYMPIKO', 'IC', 'Entry', 'OLYMPIKO 50', 0.50, 1500),
        ('Eaux', 'OLYMPIKO', 'FC', 'Frequency', 'OLYMPIKO 100', 1.00, 2000),
        ('Eaux', 'OLYMPIKO', 'FC', 'Upsize', 'OLYMPIKO 150', 1.50, 2500),
        ('Eaux', 'NATUR EAU', 'IC', 'Entry', 'NATUR EAU 50', 0.50, 1500),
        ('Eaux', 'NATUR EAU', 'FC', 'Frequency', 'NATUR EAU 100', 1.00, 2000),
        ('Eaux', 'NATUR EAU', 'FC', 'Upsize', 'NATUR EAU 150', 1.50, 2500),

        # --- BIERE ---
        ('Bière', 'Beaufort', 'IC', 'Frequency', 'Beaufort 33 VER', 0.33, 4000),
        ('Bière', 'Beaufort', 'IC', 'Upscale', 'Beaufort 33 CAN', 0.33, 5000),
        ('Bière', 'Gold', 'IC', 'Entry', 'Gold Blanche 33 VER', 0.33, 3500),
        ('Bière', 'Gold', 'FC', 'Entry', 'Gold 8 50 VER', 0.50, 4500),
        ('Bière', 'Gold', 'FC', 'Frequency', 'Gold Blanche 50 VER', 0.50, 4500),
        ('Bière', 'Gold', 'FC', 'Frequency', 'Gold Blonde 50 VER', 0.50, 4500),
        ('Bière', 'Gold', 'FC', 'Frequency', 'Gold Blonde 65 VER', 0.65, 5000),
        ('Bière', 'Gold', 'IC', 'Upscale', 'Gold 8 50 CAN', 0.50, 6000),
        ('Bière', 'Gold', 'IC', 'Upscale', 'Gold Blanche 50 CAN', 0.50, 6000),
        ('Bière', 'Gold', 'IC', 'Upscale', 'Gold Blonde 50 CAN', 0.50, 6000),
        ('Bière', 'THB', 'IC', 'Entry', 'THB Pilsener 33 VER', 0.33, 2500),
        ('Bière', 'THB', 'IC', 'Frequency', 'THB Pilsener 65 VER', 0.65, 4500),  # RÉFÉRENCE BIERE
        ('Bière', 'THB', 'IC', 'Upscale', 'THB Pilsener 50 CAN', 0.50, 5000),
        ('Bière', 'Queen', 'FC', 'Entry', 'Queen s 65 VER', 0.65, 4000),
        ('Bière', 'Fresh', 'IC', 'Entry', 'Fresh 33 VER', 0.33, 2500),
        ('Bière', 'Fresh', 'FC', 'Frequency', 'Fresh 65 VER', 0.65, 4000),
        ('Bière', 'Fresh', 'IC', 'Upscale', 'Fresh 33 CAN', 0.33, 3500),
    ]
    df = pd.DataFrame(rows, columns=['Segment', 'Marque', 'Occasion',
                                      'Rôle', 'Format', 'Volume_L', 'PVF_Ar'])
    df['Prix_Litre'] = (df['PVF_Ar'] / df['Volume_L']).round(0).astype(int)
    return df


df = load_data()

# =============================================================================
# RÉFÉRENCE PAR SEGMENT
# =============================================================================
REFERENCE_PRODUCTS = {
    'Energie':         ('XXL',         'PET 50'),
    'Boisson Gazeuse': ('CAPRICE',     'PET 35'),
    'Eaux':            ('Cristalline', 'Cristalline 100'),
    'Bière':           ('THB',         'THB Pilsener 65'),
}

OCCASIONS = ['IC', 'FC']
ROLES = ['Entry', 'Frequency', 'Upsize', 'Upscale']
ROLE_TARGETS = {
    'Entry':     '101–110',
    'Frequency': '100',
    'Upsize':    '90–99',
    'Upscale':   '≥111',
}
ROLE_INDEX_RANGE = {
    'Entry':     (101, 110),
    'Frequency': (100, 100),
    'Upsize':    (90, 99),
    'Upscale':   (111, 999),
}


def find_reference(df_full, segment, coef):
    if segment not in REFERENCE_PRODUCTS:
        return None, None
    marque, fmt_pattern = REFERENCE_PRODUCTS[segment]
    mask = (df_full['Segment'] == segment) & (df_full['Marque'] == marque)
    sub = df_full[mask]
    if sub.empty:
        return None, None
    for _, row in sub.iterrows():
        if fmt_pattern.lower() in str(row['Format']).lower():
            pl_adj = (row['PVF_Ar'] / row['Volume_L']) * coef
            return f"{row['Marque']} — {row['Format']}", round(pl_adj)
    row = sub.iloc[0]
    pl_adj = (row['PVF_Ar'] / row['Volume_L']) * coef
    return f"{row['Marque']} — {row['Format']}", round(pl_adj)


def status(idx, role):
    if role == 'Entry':     return 'Conforme' if 101 <= idx <= 110 else 'À revoir'
    if role == 'Frequency': return 'Conforme' if idx == 100 else 'À revoir'
    if role == 'Upsize':    return 'Conforme' if 90 <= idx <= 99 else 'À revoir'
    if role == 'Upscale':   return 'Conforme' if idx >= 111 else 'À revoir'
    return '—'


def compute_target(row, coef):
    current_pvf = row['PVF_Ar']
    idx = row['Index']
    role = row['Rôle']
    ref = row['Ref']
    vol = row['Volume_L']

    if row['Statut'] == 'Conforme':
        return {'action': 'conforme', 'pvf_min': current_pvf,
                'pvf_max': current_pvf, 'msg': '— conforme —'}

    idx_min, idx_max = ROLE_INDEX_RANGE[role]
    pl_min_cible = (idx_min * ref / 100) / coef
    pl_max_cible = (idx_max * ref / 100) / coef
    pvf_min_cible = pl_min_cible * vol
    pvf_max_cible = pl_max_cible * vol

    pvf_min = max(pvf_min_cible, current_pvf)
    pvf_max = max(pvf_max_cible, pvf_min)

    if idx < idx_min:
        action = 'augmenter'
        msg = f"{int(pvf_min):,} – {int(pvf_max):,} Ar".replace(',', ' ')
    else:
        action = 'au-dessus'
        msg = '⚠️ Prix déjà au-dessus de la cible'

    return {'action': action, 'pvf_min': pvf_min, 'pvf_max': pvf_max, 'msg': msg}


def style_status(series):
    out = []
    for v in series:
        if v == 'Conforme':
            out.append('color: #4ade80; font-weight: 700;')
        elif v == 'À revoir':
            out.append('color: #ff6b6b; font-weight: 700;')
        else:
            out.append('color: #a8c0dd;')
    return out


def style_couverture(series):
    out = []
    for v in series:
        if v in ('4/4', '3/4'):
            out.append('color: #4ade80; font-weight: 700;')
        elif v == '2/4':
            out.append('color: #fbbf24; font-weight: 700;')
        elif v == '1/4':
            out.append('color: #ff6b6b; font-weight: 700;')
        else:
            out.append('')
    return out


def style_proposition(series):
    out = []
    for v in series:
        s = str(v)
        if 'conforme' in s.lower():
            out.append('color: #a8c0dd; font-style: italic;')
        elif 'au-dessus' in s.lower():
            out.append('color: #fbbf24; font-weight: 600;')
        else:
            out.append('color: #4ade80; font-weight: 700;')
    return out


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Paramètres")

    st.markdown("##### Filtres")
    segments = st.multiselect(
        "Segment",
        sorted(df['Segment'].unique()),
        default=sorted(df['Segment'].unique()),
    )

    available_brands = (
        sorted(df[df['Segment'].isin(segments)]['Marque'].unique())
        if segments else []
    )
    brands = st.multiselect(
        "Marque",
        available_brands,
        default=available_brands,
    )

    st.divider()

    st.markdown("##### Canal de vente")
    channel = st.radio(
        "Canal",
        ["GMS (prix de référence)", "Horeca (+35%)", "Traditionnel (+15%)"],
    )
    coef = {
        "GMS (prix de référence)": 1.00,
        "Horeca (+35%)": 1.35,
        "Traditionnel (+15%)": 1.15,
    }[channel]

    st.divider()

    if st.button("🔄 Réinitialiser les modifications", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith("price_editor"):
                del st.session_state[k]
        st.rerun()

    st.divider()

    st.markdown("##### 📖 Cibles d'index")
    st.markdown(f"""
    - **Entry** — {ROLE_TARGETS['Entry']}
    - **Frequency** — {ROLE_TARGETS['Frequency']}
    - **Upsize** — {ROLE_TARGETS['Upsize']}
    - **Upscale** — {ROLE_TARGETS['Upscale']}
    """)


# =============================================================================
# FILTRAGE + CALCUL
# =============================================================================
d = df[(df['Segment'].isin(segments)) & (df['Marque'].isin(brands))].copy()

if d.empty:
    st.warning("⚠️ Aucun produit ne correspond à vos filtres. Élargissez votre sélection.")
    st.stop()

d['PVF_Ajusté'] = (d['PVF_Ar'] * coef).round(0).astype(int)
d['Prix_Litre_Ajusté'] = (d['Prix_Litre'] * coef).round(0).astype(int)

ref_by_segment = {}
ref_label_by_segment = {}
for segment in d['Segment'].unique():
    label, pl = find_reference(d, segment, coef)
    if pl is None:
        freq = d[(d['Segment'] == segment) & (d['Rôle'] == 'Frequency')]
        if len(freq):
            pl = freq['Prix_Litre_Ajusté'].mean()
            label = f"(fallback) Moyenne Frequency {segment}"
        else:
            pl = d[d['Segment'] == segment]['Prix_Litre_Ajusté'].mean()
            label = f"(fallback) Moyenne {segment}"
    ref_by_segment[segment] = pl
    ref_label_by_segment[segment] = label

d['Ref'] = d['Segment'].map(ref_by_segment)
d['Index'] = (d['Prix_Litre_Ajusté'] / d['Ref'] * 100).round(0).astype(int)
d['Statut'] = d.apply(lambda r: status(r['Index'], r['Rôle']), axis=1)

with st.sidebar:
    st.divider()
    st.markdown("##### 🎯 Références actives")
    for seg in sorted(ref_label_by_segment.keys()):
        st.caption(
            f"**{seg}** · {ref_label_by_segment[seg]}  \n"
            f"Index 100 = {int(ref_by_segment[seg]):,} Ar/L".replace(',', ' ')
        )


# =============================================================================
# EN-TÊTE + MÉTRIQUES
# =============================================================================
st.markdown("# Simulateur OBPPC")
st.markdown(
    "**Analyse de cohérence** entre les rôles tarifaires et les prix au litre, "
    "avec **proposition d'intervalle de prix à la hausse** pour chaque produit sous-évalué. "
    "La référence (index 100) est **fixe par segment**."
)

n_ok = int((d['Statut'] == 'Conforme').sum())
n_ko = int((d['Statut'] == 'À revoir').sum())
taux = n_ok / len(d) * 100 if len(d) else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Produits analysés", len(d))
col2.metric("✅ Conformes", n_ok)
col3.metric("❌ Non conformes", n_ko)
col4.metric("Taux de conformité", f"{taux:.0f}%")

if taux >= 80:
    st.success(f"**Cohérence élevée** — {n_ok} produits sur {len(d)} respectent leur cible tarifaire.")
elif taux >= 50:
    st.warning(f"**Cohérence partielle** — {n_ko} produits s'écartent de leur cible. Voir l'onglet Diagnostic.")
else:
    st.error(f"**Cohérence faible** — {n_ko} produits ne respectent pas leur rôle. Arbitrage prix à revoir.")

st.divider()


# =============================================================================
# ONGLETS
# =============================================================================
tab1, tab2, tab3 = st.tabs([
    "①  ✏️  Modifier les prix",
    "②  📊  Vue d'ensemble",
    "③  🎯  Diagnostic",
])


# =============================================================================
# TAB 1 — MODIFIER LES PRIX
# =============================================================================
with tab1:
    st.markdown("## ✏️ Modifier les prix")
    st.markdown(
        "Ajustez le **prix de vente (PVF)** ou le **volume** d'un produit directement "
        "dans le tableau. Toutes les analyses se recalent automatiquement."
    )

    editor_df = d[['Segment', 'Marque', 'Occasion', 'Rôle',
                   'Format', 'Volume_L', 'PVF_Ar']].copy()

    edited = st.data_editor(
        editor_df,
        column_config={
            "Segment": st.column_config.TextColumn("Segment", disabled=True, width="small"),
            "Marque": st.column_config.TextColumn("Marque", disabled=True, width="small"),
            "Occasion": st.column_config.TextColumn("Occasion", disabled=True, width="small"),
            "Rôle": st.column_config.SelectboxColumn(
                "Rôle tarifaire", options=ROLES, required=True, width="medium",
            ),
            "Format": st.column_config.TextColumn("Format", disabled=True, width="medium"),
            "Volume_L": st.column_config.NumberColumn(
                "Volume (L)", min_value=0.05, step=0.05, format="%.2f",
            ),
            "PVF_Ar": st.column_config.NumberColumn(
                "Prix de vente (Ar)", min_value=0, step=100, format="%d",
            ),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        height=min(600, 100 + 38 * len(editor_df)),
        key="price_editor",
    )

    d2 = edited.copy()
    d2['PVF_Ajusté'] = (d2['PVF_Ar'] * coef).round(0).astype(int)
    d2['Prix_Litre_Ajusté'] = ((d2['PVF_Ar'] / d2['Volume_L']) * coef).round(0).astype(int)

    ref2_by_segment = {}
    for segment in d2['Segment'].unique():
        label, pl = find_reference(d2, segment, coef)
        if pl is None:
            freq = d2[(d2['Segment'] == segment) & (d2['Rôle'] == 'Frequency')]
            pl = freq['Prix_Litre_Ajusté'].mean() if len(freq) else d2[d2['Segment'] == segment]['Prix_Litre_Ajusté'].mean()
        ref2_by_segment[segment] = pl

    d2['Ref'] = d2['Segment'].map(ref2_by_segment)
    d2['Index'] = (d2['Prix_Litre_Ajusté'] / d2['Ref'] * 100).round(0).astype(int)
    d2['Statut'] = d2.apply(lambda r: status(r['Index'], r['Rôle']), axis=1)

    proposals = d2.apply(lambda r: compute_target(r, coef), axis=1)
    d2['Action'] = proposals.apply(lambda x: x['action'])
    d2['PVF_min'] = proposals.apply(lambda x: x['pvf_min'])
    d2['PVF_max'] = proposals.apply(lambda x: x['pvf_max'])
    d2['Proposition'] = proposals.apply(lambda x: x['msg'])

    st.markdown("### Résultats en direct")
    st.caption(f"Canal : **{channel}** · Index 100 = référence fixe par segment")

    result = d2[['Marque', 'Format', 'Occasion', 'Rôle',
                 'PVF_Ar', 'Prix_Litre_Ajusté', 'Index',
                 'Statut', 'Proposition']].copy()
    result.columns = ['Marque', 'Format', 'Occasion', 'Rôle',
                      'Prix actuel (Ar)', 'Prix / L (Ar)', 'Index',
                      'Statut', '💡 Proposition']

    styled_result = (
        result.style
        .apply(style_status, subset=['Statut'])
        .apply(style_proposition, subset=['💡 Proposition'])
        .format({
            'Prix actuel (Ar)': '{:,.0f}',
            'Prix / L (Ar)':    '{:,.0f}',
            'Index':            '{:d}',
        })
    )

    st.dataframe(
        styled_result,
        use_container_width=True,
        height=min(500, 80 + 35 * len(result)),
        hide_index=True,
        column_config={
            'Prix actuel (Ar)': st.column_config.NumberColumn(
                "Prix actuel (Ar)",
                help="Prix de vente (PVF) saisi dans le tableau d'édition",
                format="%d",
            ),
            'Prix / L (Ar)': st.column_config.NumberColumn(
                "Prix / L (Ar)",
                help="Prix au litre ajusté selon le canal sélectionné",
                format="%d",
            ),
            'Index': st.column_config.NumberColumn(format="%d"),
            '💡 Proposition': st.column_config.TextColumn(
                "💡 Proposition",
                help="Intervalle de prix à appliquer (jamais en dessous du prix actuel).",
                width="large",
            ),
        },
    )

    n_augment = int((d2['Action'] == 'augmenter').sum())
    n_above = int((d2['Action'] == 'au-dessus').sum())

    if n_augment or n_above:
        msg = f"💡 **{n_augment} produit(s)** sous-évalué(s) à augmenter · "
        msg += f"**{n_above} produit(s)** au-dessus de la cible"
        st.info(msg + ". Voir les détails dans l'onglet **③ Diagnostic**.")
    else:
        st.success("✅ Tous les produits sont conformes à leur rôle tarifaire.")


# =============================================================================
# TAB 2 — VUE D'ENSEMBLE
# =============================================================================
with tab2:
    st.markdown("## 📊 Vue d'ensemble du portefeuille")

    st.markdown("### Couverture des rôles par marque")
    st.markdown(
        "Ce tableau indique quels rôles tarifaires chaque marque occupe. "
        "Une marque bien structurée couvre **au minimum Entry + Frequency**."
    )

    occ_filter = st.radio("Occasion", OCCASIONS, horizontal=True, key="vue_occ")
    sub = d[d['Occasion'] == occ_filter]

    if sub.empty:
        st.info("Aucun produit sur cette occasion.")
    else:
        rows_cov = []
        for brand in sorted(sub['Marque'].unique()):
            bsub = sub[sub['Marque'] == brand]
            row = {'Marque': brand}
            covered = 0
            for role in ROLES:
                rsub = bsub[bsub['Rôle'] == role]
                if rsub.empty:
                    row[role] = '—'
                else:
                    covered += 1
                    row[role] = ' · '.join(rsub['Format'].tolist())
            row['Couverture'] = f"{covered}/4"
            rows_cov.append(row)

        cov_df = pd.DataFrame(rows_cov)

        styled_cov = cov_df.style.apply(style_couverture, subset=['Couverture'])

        st.dataframe(
            styled_cov,
            use_container_width=True,
            height=min(600, 80 + 38 * len(cov_df)),
            hide_index=True,
        )

    st.markdown("### Tous les produits du périmètre")

    view2 = d.copy()
    props = view2.apply(lambda r: compute_target(r, coef), axis=1)
    view2['Proposition'] = props.apply(lambda x: x['msg'])

    view2_final = view2[['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
                          'Volume_L', 'PVF_Ajusté', 'Prix_Litre_Ajusté',
                          'Index', 'Statut', 'Proposition']].copy()
    view2_final.columns = ['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
                            'Volume (L)', 'Prix (Ar)', 'Prix / L (Ar)',
                            'Index', 'Statut', '💡 Proposition']

    styled_view2 = (
        view2_final.style
        .apply(style_status, subset=['Statut'])
        .apply(style_proposition, subset=['💡 Proposition'])
        .format({
            'Volume (L)': '{:.2f}',
            'Prix (Ar)': '{:,.0f}',
            'Prix / L (Ar)': '{:,.0f}',
            'Index': '{:d}',
        })
    )

    st.dataframe(
        styled_view2,
        use_container_width=True,
        height=min(700, 80 + 35 * len(view2_final)),
        hide_index=True,
        column_config={
            'Volume (L)': st.column_config.NumberColumn(format="%.2f"),
            'Prix (Ar)': st.column_config.NumberColumn(format="%d"),
            'Prix / L (Ar)': st.column_config.NumberColumn(format="%d"),
            'Index': st.column_config.NumberColumn(format="%d"),
            '💡 Proposition': st.column_config.TextColumn(
                "💡 Proposition",
                help="Proposition de prix à la hausse",
            ),
        },
    )


# =============================================================================
# TAB 3 — DIAGNOSTIC
# =============================================================================
with tab3:
    st.markdown("## 🎯 Diagnostic OBPPC")
    st.markdown(
        "Liste des produits **non conformes** avec l'intervalle de prix à la hausse. "
        "⚠️ Aucune proposition de baisse n'est faite."
    )

    ko = d[d['Statut'] == 'À revoir'].copy()

    if ko.empty:
        st.success("✅ Tous les produits respectent leur cible tarifaire.")
    else:
        proposals = ko.apply(lambda r: compute_target(r, coef), axis=1)
        ko['Action'] = proposals.apply(lambda x: x['action'])
        ko['PVF_min'] = proposals.apply(lambda x: x['pvf_min'])
        ko['PVF_max'] = proposals.apply(lambda x: x['pvf_max'])
        ko['Proposition'] = proposals.apply(lambda x: x['msg'])

        to_increase = ko[ko['Action'] == 'augmenter'].copy()
        above_target = ko[ko['Action'] == 'au-dessus'].copy()

        if not to_increase.empty:
            def ecart_index(row):
                i = row['Index']
                imin, imax = ROLE_INDEX_RANGE[row['Rôle']]
                return imin - i if i < imin else 0

            to_increase['Écart'] = to_increase.apply(ecart_index, axis=1)
            to_increase = to_increase.sort_values('Écart', ascending=False)

            st.markdown(f"### ⬆️ {len(to_increase)} produits à augmenter")
            st.caption(
                "Produits **sous-évalués**. L'intervalle proposé est toujours supérieur au prix actuel."
            )

            diag = to_increase[[
                'Segment', 'Marque', 'Format', 'Occasion', 'Rôle',
                'PVF_Ar', 'Prix_Litre_Ajusté', 'Index',
                'PVF_min', 'PVF_max',
            ]].copy()
            diag.columns = [
                'Segment', 'Marque', 'Format', 'Occasion', 'Rôle',
                'PVF actuel', 'Prix / L actuel', 'Index actuel',
                'PVF cible min', 'PVF cible max',
            ]

            styled_diag = (
                diag.style
                .apply(lambda s: ['color: #ff6b6b; font-weight: 700;'] * len(s),
                       subset=['Index actuel'])
                .apply(lambda s: ['color: #4ade80; font-weight: 700;'] * len(s),
                       subset=['PVF cible min', 'PVF cible max'])
                .format({
                    'PVF actuel':       '{:,.0f}',
                    'Prix / L actuel':  '{:,.0f}',
                    'Index actuel':     '{:d}',
                    'PVF cible min':    '{:,.0f}',
                    'PVF cible max':    '{:,.0f}',
                })
            )

            st.dataframe(
                styled_diag,
                use_container_width=True,
                height=min(600, 80 + 40 * len(diag)),
                hide_index=True,
                column_config={
                    'PVF actuel':       st.column_config.NumberColumn(format="%d Ar"),
                    'Prix / L actuel':  st.column_config.NumberColumn(format="%d Ar"),
                    'Index actuel':     st.column_config.NumberColumn(format="%d"),
                    'PVF cible min':    st.column_config.NumberColumn(format="%d Ar"),
                    'PVF cible max':    st.column_config.NumberColumn(format="%d Ar"),
                },
            )

        if not above_target.empty:
            st.markdown("---")
            st.markdown(f"### ⚠️ {len(above_target)} produits au-dessus de la cible")
            st.caption(
                "Index **supérieur** à la cible du rôle. **Aucune baisse n'est proposée**."
            )

            diag_above = above_target[[
                'Segment', 'Marque', 'Format', 'Occasion', 'Rôle',
                'PVF_Ar', 'Prix_Litre_Ajusté', 'Index',
            ]].copy()
            diag_above.columns = [
                'Segment', 'Marque', 'Format', 'Occasion', 'Rôle',
                'PVF actuel', 'Prix / L actuel', 'Index actuel',
            ]

            styled_above = (
                diag_above.style
                .apply(lambda s: ['color: #fbbf24; font-weight: 700;'] * len(s),
                       subset=['Index actuel'])
                .format({
                    'PVF actuel':       '{:,.0f}',
                    'Prix / L actuel':  '{:,.0f}',
                    'Index actuel':     '{:d}',
                })
            )

            st.dataframe(
                styled_above,
                use_container_width=True,
                height=min(500, 80 + 40 * len(diag_above)),
                hide_index=True,
                column_config={
                    'PVF actuel':       st.column_config.NumberColumn(format="%d Ar"),
                    'Prix / L actuel':  st.column_config.NumberColumn(format="%d Ar"),
                    'Index actuel':     st.column_config.NumberColumn(format="%d"),
                },
            )

        st.markdown("---")
        st.markdown("### Export du diagnostic")
        export_diag = ko[[
            'Segment', 'Marque', 'Format', 'Occasion', 'Rôle',
            'PVF_Ar', 'Prix_Litre_Ajusté', 'Index',
            'Action', 'PVF_min', 'PVF_max',
        ]].copy()
        export_diag.columns = [
            'Segment', 'Marque', 'Format', 'Occasion', 'Rôle',
            'PVF actuel (Ar)', 'Prix/L actuel (Ar)', 'Index actuel',
            'Action', 'PVF cible min (Ar)', 'PVF cible max (Ar)',
        ]
        csv_diag = export_diag.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "📥 Télécharger le diagnostic (CSV)",
            data=csv_diag,
            file_name=f"diagnostic_obppc_{channel.split()[0].lower()}.csv",
            mime="text/csv",
        )

    st.markdown("---")
    st.markdown("### Export global")
    csv = d[['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
             'Volume_L', 'PVF_Ajusté', 'Prix_Litre_Ajusté',
             'Index', 'Statut']].to_csv(index=False).encode('utf-8-sig')

    st.download_button(
        "📥 Télécharger l'analyse complète (CSV)",
        data=csv,
        file_name=f"analyse_obppc_{channel.split()[0].lower()}.csv",
        mime="text/csv",
    )
