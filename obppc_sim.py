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
# CSS — dark bleu partout
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

    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
    }
    [data-baseweb="tag"] {
        background-color: #4a9eff !important;
        color: #ffffff !important;
    }
    [data-baseweb="tag"] span,
    [data-baseweb="tag"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
    }
    [data-baseweb="popover"], [data-baseweb="menu"] {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
    }
    [data-baseweb="menu"] li { color: #ffffff !important; }
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [aria-selected="true"] {
        background-color: #1e4976 !important;
        color: #ffffff !important;
    }
    input { color: #ffffff !important; }

    .stRadio label, .stCheckbox label,
    .stRadio > div > label > div { color: #ffffff !important; }

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
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] { color: #ffffff !important; }

    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #1e4976;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a8c0dd !important;
        background-color: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #4a9eff !important;
    }

    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        border-radius: 8px;
    }

    .stAlert {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
    }
    .stAlert p { color: #ffffff !important; }

    hr { border-color: #1e4976 !important; }
    strong, b { color: #ffffff !important; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DONNÉES
# =============================================================================
@st.cache_data
def load_data():
    rows = [
        ('Energie', 'Red Bull', 'IC', 'Upscale', 'CAN 25', 0.25, 9900),
        ('Energie', 'Monster', 'IC', 'Upscale', 'CAN 50', 0.50, 9900),
        ('Energie', 'FOSA', 'IC', 'Upscale', 'CAN 50', 0.50, 5000),
        ('Energie', 'XXL', 'IC', 'Entry', 'VC 30', 0.30, 2500),
        ('Energie', 'XXL', 'IC', 'Frequency', 'PET 35', 0.35, 3500),
        ('Energie', 'XXL', 'IC', 'Upscale', 'CAN 33', 0.33, 4000),
        ('Energie', 'DYNAMIC', 'IC', 'Upscale', 'CAN 25', 0.25, 3500),
        ('Energie', 'BOOST VITALITY', 'IC', 'Upscale', 'CAN 33', 0.33, 4000),
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
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Entry', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Frequency', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Upscale', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'CAPRICE', 'IC', 'Entry', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'CAPRICE', 'FC', 'Upsize', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'CAPRICE', 'FC', 'Upsize', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'TONIC', 'IC', 'Entry', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'TONIC', 'FC', 'Upsize', 'VC 100', 1.00, 3000),
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
        ('Eaux', 'Cristalline', 'FC', 'Upsize', 'Cristalline 100 PET', 1.50, 2100),
        ('Eaux', 'Cristalline', 'FC', 'Upsize', 'Cristalline 200 PET', 2.00, 3600),
        ('Eaux', 'OLYMPIKO', 'IC', 'Entry', 'OLYMPIKO 50', 0.50, 1500),
        ('Eaux', 'OLYMPIKO', 'FC', 'Frequency', 'OLYMPIKO 100', 1.00, 2000),
        ('Eaux', 'OLYMPIKO', 'FC', 'Upsize', 'OLYMPIKO 150', 1.50, 2500),
        ('Eaux', 'NATUR EAU', 'IC', 'Entry', 'NATUR EAU 50', 0.50, 1500),
        ('Eaux', 'NATUR EAU', 'FC', 'Frequency', 'NATUR EAU 100', 1.00, 2000),
        ('Eaux', 'NATUR EAU', 'FC', 'Upsize', 'NATUR EAU 150', 1.50, 2500),
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
        ('Bière', 'THB', 'FC', 'Frequency', 'THB Pilsener 65 VER', 0.65, 4500),
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


def status(idx, role):
    if role == 'Entry':     return 'Conforme' if 101 <= idx <= 110 else 'À revoir'
    if role == 'Frequency': return 'Conforme' if idx == 100 else 'À revoir'
    if role == 'Upsize':    return 'Conforme' if 90 <= idx <= 99 else 'À revoir'
    if role == 'Upscale':   return 'Conforme' if idx >= 111 else 'À revoir'
    return '—'


def compute_target_prices(ref, vol, role, coef):
    """Retourne (pl_min, pl_max, pvf_min, pvf_max) pour un produit."""
    idx_min, idx_max = ROLE_INDEX_RANGE[role]
    pl_min_adj = idx_min * ref / 100
    pl_max_adj = idx_max * ref / 100
    pl_min = pl_min_adj / coef
    pl_max = pl_max_adj / coef
    pvf_min = pl_min * vol
    pvf_max = pl_max * vol
    return round(pl_min), round(pl_max), round(pvf_min), round(pvf_max)


def format_target_range(row):
    """Format compact 'PVF_min – PVF_max Ar' ou '—' si conforme."""
    if row['Statut'] == 'Conforme':
        return '— conforme —'
    return f"{int(row['PVF_cible_min']):,} – {int(row['PVF_cible_max']):,} Ar".replace(',', ' ')


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


def style_target_col(series):
    """Vert clair sur la colonne des prix cibles si non conforme, gris si conforme."""
    out = []
    for v in series:
        if 'conforme' in str(v).lower():
            out.append('color: #a8c0dd; font-style: italic;')
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
    st.caption("Index 100 = produit de référence (moyenne des Frequency du même segment × occasion)")


# =============================================================================
# FILTRAGE + CALCUL
# =============================================================================
d = df[(df['Segment'].isin(segments)) & (df['Marque'].isin(brands))].copy()

if d.empty:
    st.warning("⚠️ Aucun produit ne correspond à vos filtres. Élargissez votre sélection.")
    st.stop()

d['PVF_Ajusté'] = (d['PVF_Ar'] * coef).round(0).astype(int)
d['Prix_Litre_Ajusté'] = (d['Prix_Litre'] * coef).round(0).astype(int)

ref = (d[d['Rôle'] == 'Frequency']
       .groupby(['Segment', 'Occasion'])['Prix_Litre_Ajusté'].mean())
d['Ref'] = d.set_index(['Segment', 'Occasion']).index.map(ref)
d['Ref'] = d['Ref'].fillna(
    d.groupby(['Segment', 'Occasion'])['Prix_Litre_Ajusté'].transform('mean'))
d['Index'] = (d['Prix_Litre_Ajusté'] / d['Ref'] * 100).round(0).astype(int)
d['Statut'] = d.apply(lambda r: status(r['Index'], r['Rôle']), axis=1)


# =============================================================================
# EN-TÊTE + MÉTRIQUES
# =============================================================================
st.markdown("# Simulateur OBPPC")
st.markdown(
    "**Analyse de cohérence** entre les rôles tarifaires et les prix au litre, "
    "avec **proposition d'intervalle de prix** pour chaque produit non conforme."
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
# TAB 1 — MODIFIER LES PRIX (avec intervalle cible)
# =============================================================================
with tab1:
    st.markdown("## ✏️ Modifier les prix")
    st.markdown(
        "Ajustez le **prix de vente (PVF)** ou le **volume** d'un produit directement "
        "dans le tableau. Toutes les analyses se recalculent automatiquement. "
        "La colonne **💡 Prix cible** indique l'intervalle à viser pour les produits non conformes."
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

    # --- Recalcul
    d2 = edited.copy()
    d2['PVF_Ajusté'] = (d2['PVF_Ar'] * coef).round(0).astype(int)
    d2['Prix_Litre_Ajusté'] = ((d2['PVF_Ar'] / d2['Volume_L']) * coef).round(0).astype(int)

    ref2 = (d2[d2['Rôle'] == 'Frequency']
            .groupby(['Segment', 'Occasion'])['Prix_Litre_Ajusté'].mean())
    d2['Ref'] = d2.set_index(['Segment', 'Occasion']).index.map(ref2)
    d2['Ref'] = d2['Ref'].fillna(
        d2.groupby(['Segment', 'Occasion'])['Prix_Litre_Ajusté'].transform('mean'))
    d2['Index'] = (d2['Prix_Litre_Ajusté'] / d2['Ref'] * 100).round(0).astype(int)
    d2['Statut'] = d2.apply(lambda r: status(r['Index'], r['Rôle']), axis=1)

    # --- Calcul des PVF cibles
    def get_pvf_targets(row):
        pl_min, pl_max, pvf_min, pvf_max = compute_target_prices(
            row['Ref'], row['Volume_L'], row['Rôle'], coef
        )
        return pd.Series({
            'PVF_cible_min': pvf_min,
            'PVF_cible_max': pvf_max,
            'Prix_L_cible_min': pl_min,
            'Prix_L_cible_max': pl_max,
        })

    targets = d2.apply(get_pvf_targets, axis=1)
    d2 = pd.concat([d2, targets], axis=1)

    # --- Colonne compacte : intervalle PVF
    d2['Prix_cible'] = d2.apply(format_target_range, axis=1)

    st.markdown("### Résultats en direct")
    st.caption(f"Canal : **{channel}** · Index 100 = moyenne des Frequency du même segment × occasion")

    result = d2[['Marque', 'Format', 'Occasion', 'Rôle',
                 'Prix_Litre_Ajusté', 'Index', 'Statut', 'Prix_cible']].copy()
    result.columns = ['Marque', 'Format', 'Occasion', 'Rôle',
                      'Prix / L (Ar)', 'Index', 'Statut',
                      '💡 Prix cible (Ar)']

    styled_result = (
        result.style
        .apply(style_status, subset=['Statut'])
        .apply(style_target_col, subset=['💡 Prix cible (Ar)'])
        .format({'Prix / L (Ar)': '{:,.0f}', 'Index': '{:d}'})
    )

    st.dataframe(
        styled_result,
        use_container_width=True,
        height=min(500, 80 + 35 * len(result)),
        hide_index=True,
        column_config={
            'Prix / L (Ar)': st.column_config.NumberColumn(format="%d"),
            'Index': st.column_config.NumberColumn(format="%d"),
            '💡 Prix cible (Ar)': st.column_config.TextColumn(
                "💡 Prix cible (Ar)",
                help="Intervalle de prix de vente à appliquer pour rentrer dans la cible du rôle. "
                     "Uniquement pour les produits non conformes.",
                width="medium",
            ),
        },
    )

    # --- Compteur de non-conformes avec suggestion
    nb_ko = int((d2['Statut'] == 'À revoir').sum())
    if nb_ko > 0:
        st.info(
            f"💡 **{nb_ko} produit(s)** non conforme(s) — voir la colonne "
            "*💡 Prix cible (Ar)* pour l'intervalle exact à appliquer. "
            "Détails par rôle dans l'onglet **③ Diagnostic**."
        )
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

        styled_cov = (
            cov_df.style
            .apply(style_couverture, subset=['Couverture'])
        )

        st.dataframe(
            styled_cov,
            use_container_width=True,
            height=min(600, 80 + 38 * len(cov_df)),
            hide_index=True,
        )

    st.markdown("### Tous les produits du périmètre")
    st.markdown(
        "Vue tabulaire complète avec le prix au litre, l'index de positionnement, "
        "le statut de conformité et le prix cible suggéré."
    )

    # Ajout des cibles dans la vue d'ensemble aussi
    view2 = d.copy()

    def add_targets(row):
        pl_min, pl_max, pvf_min, pvf_max = compute_target_prices(
            row['Ref'], row['Volume_L'], row['Rôle'], coef
        )
        return pd.Series({
            'PVF_cible_min': pvf_min,
            'PVF_cible_max': pvf_max,
        })

    v_targets = view2.apply(add_targets, axis=1)
    view2 = pd.concat([view2, v_targets], axis=1)
    view2['Prix_cible'] = view2.apply(format_target_range, axis=1)

    view2_final = view2[['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
                          'Volume_L', 'PVF_Ajusté', 'Prix_Litre_Ajusté',
                          'Index', 'Statut', 'Prix_cible']].copy()
    view2_final.columns = ['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
                            'Volume (L)', 'Prix (Ar)', 'Prix / L (Ar)',
                            'Index', 'Statut', '💡 Prix cible (Ar)']

    styled_view2 = (
        view2_final.style
        .apply(style_status, subset=['Statut'])
        .apply(style_target_col, subset=['💡 Prix cible (Ar)'])
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
            '💡 Prix cible (Ar)': st.column_config.TextColumn(
                "💡 Prix cible (Ar)",
                help="Intervalle de prix à appliquer (uniquement pour les non-conformes)",
            ),
        },
    )


# =============================================================================
# TAB 3 — DIAGNOSTIC avec propositions de prix détaillées
# =============================================================================
with tab3:
    st.markdown("## 🎯 Diagnostic OBPPC")
    st.markdown(
        "Liste des produits **non conformes** avec l'intervalle de prix cible "
        "pour les remettre en conformité."
    )

    ko = d[d['Statut'] == 'À revoir'].copy()

    if ko.empty:
        st.success("✅ Tous les produits respectent leur cible tarifaire.")
    else:
        # --- Calcul des cibles
        def compute_targets(row):
            pl_min, pl_max, pvf_min, pvf_max = compute_target_prices(
                row['Ref'], row['Volume_L'], row['Rôle'], coef
            )
            return pd.Series({
                'Prix_L_min':  pl_min,
                'Prix_L_max':  pl_max,
                'PVF_min':     pvf_min,
                'PVF_max':     pvf_max,
            })

        targets = ko.apply(compute_targets, axis=1)
        ko = pd.concat([ko, targets], axis=1)

        # --- Écart en points d'index
        def ecart_index(row):
            i = row['Index']
            imin, imax = ROLE_INDEX_RANGE[row['Rôle']]
            if i < imin:
                return imin - i
            if i > imax:
                return i - imax
            return 0

        ko['Écart'] = ko.apply(ecart_index, axis=1)
        ko = ko.sort_values('Écart', ascending=False)

        # --- Tendance
        def tendance(row):
            i = row['Index']
            imin, imax = ROLE_INDEX_RANGE[row['Rôle']]
            if i < imin:
                return '⬆️ Augmenter'
            if i > imax:
                return '⬇️ Baisser'
            return '—'

        ko['Tendance'] = ko.apply(tendance, axis=1)

        st.markdown(f"**{len(ko)} produits à réviser** — triés par écart décroissant :")

        # --- Tableau final
        diag = ko[[
            'Marque', 'Format', 'Occasion', 'Rôle',
            'Prix_Litre_Ajusté', 'Index', 'Tendance',
            'Prix_L_min', 'Prix_L_max',
            'PVF_min', 'PVF_max',
        ]].copy()
        diag.columns = [
            'Marque', 'Format', 'Occasion', 'Rôle',
            'Prix actuel / L', 'Index actuel', 'Action',
            'Prix cible / L min', 'Prix cible / L max',
            'PVF min', 'PVF max',
        ]

        def style_index(series):
            out = []
            for v in series:
                try:
                    n = int(v)
                    if 95 <= n <= 105:
                        out.append('color: #fbbf24; font-weight: 700;')
                    else:
                        out.append('color: #ff6b6b; font-weight: 700;')
                except Exception:
                    out.append('')
            return out

        def style_target_range(series):
            return ['color: #4ade80; font-weight: 600;'] * len(series)

        def style_action(series):
            out = []
            for v in series:
                if 'Augmenter' in str(v):
                    out.append('color: #4ade80; font-weight: 700;')
                elif 'Baisser' in str(v):
                    out.append('color: #fbbf24; font-weight: 700;')
                else:
                    out.append('color: #a8c0dd;')
            return out

        styled_diag = (
            diag.style
            .apply(style_index, subset=['Index actuel'])
            .apply(style_target_range, subset=['Prix cible / L min', 'Prix cible / L max'])
            .apply(style_action, subset=['Action'])
            .format({
                'Prix actuel / L':     '{:,.0f}',
                'Index actuel':        '{:d}',
                'Prix cible / L min':  '{:,.0f}',
                'Prix cible / L max':  '{:,.0f}',
                'PVF min':             '{:,.0f}',
                'PVF max':             '{:,.0f}',
            })
        )

        st.dataframe(
            styled_diag,
            use_container_width=True,
            height=min(600, 80 + 40 * len(diag)),
            hide_index=True,
            column_config={
                'Prix actuel / L':    st.column_config.NumberColumn(format="%d Ar"),
                'Index actuel':       st.column_config.NumberColumn(format="%d"),
                'Prix cible / L min': st.column_config.NumberColumn(format="%d Ar"),
                'Prix cible / L max': st.column_config.NumberColumn(format="%d Ar"),
                'PVF min':            st.column_config.NumberColumn(format="%d Ar"),
                'PVF max':            st.column_config.NumberColumn(format="%d Ar"),
            },
        )

        st.caption(
            "**Lecture** — La colonne *Action* indique s'il faut **augmenter** ou **baisser** le prix. "
            "Les colonnes *Prix cible / L* et *PVF* donnent l'intervalle exact à appliquer "
            "pour rentrer dans la cible du rôle."
        )

        # ---- Recommandations ----
        st.markdown("### Recommandations")

        entry_ko = ko[ko['Rôle'] == 'Entry']
        freq_ko = ko[ko['Rôle'] == 'Frequency']
        up_ko = ko[ko['Rôle'].isin(['Upsize', 'Upscale'])]

        if len(freq_ko):
            st.warning(
                f"**{len(freq_ko)} produits Frequency** ne sont pas à l'index 100. "
                "Le produit de référence doit être ajusté en priorité."
            )
        if len(entry_ko):
            st.info(
                f"**{len(entry_ko)} produits Entry** sont en dehors de la cible 101–110. "
                "Vérifiez le positionnement du format d'accès."
            )
        if len(up_ko):
            st.info(
                f"**{len(up_ko)} produits Upsize / Upscale** sont à revoir. "
                "Vérifiez la cohérence volume / prix au litre."
            )

        # ---- Export du diagnostic ----
        st.markdown("### Export du diagnostic")
        csv_diag = diag.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            "📥 Télécharger le diagnostic (CSV)",
            data=csv_diag,
            file_name=f"diagnostic_obppc_{channel.split()[0].lower()}.csv",
            mime="text/csv",
        )

    # ---- Export global ----
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
