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
# CSS MINIMAL — typographie uniquement, la palette est gérée par config.toml
# =============================================================================
st.markdown("""
<style>
    html, body, [class*="css"] {
        font-size: 15px;
        line-height: 1.55;
        color: #ffffff;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #ffffff;
    }
    h1 { font-size: 1.75rem !important; margin-bottom: 0.3rem !important; }
    h2 { font-size: 1.3rem !important; margin-top: 1.4rem !important; }
    h3 { font-size: 1.05rem !important; margin-top: 1.1rem !important; }

    /* Caption légèrement atténué mais lisible */
    [data-testid="stCaptionContainer"] p,
    .stCaption {
        color: #a8c0dd !important;
    }
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


def status(idx, role):
    if role == 'Entry':     return 'Conforme' if 101 <= idx <= 110 else 'À revoir'
    if role == 'Frequency': return 'Conforme' if idx == 100 else 'À revoir'
    if role == 'Upsize':    return 'Conforme' if 90 <= idx <= 99 else 'À revoir'
    if role == 'Upscale':   return 'Conforme' if idx >= 111 else 'À revoir'
    return '—'


# =============================================================================
# STYLERS compatibles toutes versions pandas
# =============================================================================
def style_status_col(series):
    """Retourne une liste de styles CSS pour la colonne Statut."""
    styles = []
    for val in series:
        if val == 'Conforme':
            styles.append('color: #4ade80; font-weight: 700;')
        elif val == 'À revoir':
            styles.append('color: #ff6b6b; font-weight: 700;')
        else:
            styles.append('color: #a8c0dd;')
    return styles


def style_couverture_col(series):
    styles = []
    for val in series:
        if val in ('4/4', '3/4'):
            styles.append('color: #4ade80; font-weight: 700;')
        elif val == '2/4':
            styles.append('color: #fbbf24; font-weight: 700;')
        elif val == '1/4':
            styles.append('color: #ff6b6b; font-weight: 700;')
        else:
            styles.append('')
    return styles


def style_ecart_col(series):
    styles = []
    for val in series:
        try:
            v = int(str(val).replace('+', ''))
            if v >= 20:
                styles.append('color: #ff6b6b; font-weight: 700;')
            elif v >= 10:
                styles.append('color: #fbbf24; font-weight: 700;')
            else:
                styles.append('color: #ffffff;')
        except Exception:
            styles.append('')
    return styles


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
    "**Analyse de cohérence** entre les rôles tarifaires (Entry, Frequency, Upsize, Upscale) "
    "et les prix au litre, par marque et par occasion."
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
        "dans le tableau. Toutes les analyses se recalculent automatiquement."
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

    st.markdown("### Résultats en direct")
    st.caption(f"Canal : **{channel}** · Index 100 = moyenne des Frequency du même segment × occasion")

    result = d2[['Marque', 'Format', 'Occasion', 'Rôle',
                 'Prix_Litre_Ajusté', 'Index', 'Statut']].copy()
    result.columns = ['Marque', 'Format', 'Occasion', 'Rôle',
                      'Prix / L (Ar)', 'Index', 'Statut']

    # Utilisation de Styler.apply (compatible pandas 1.x et 2.x/3.x)
    styled_result = (
        result.style
        .apply(style_status_col, subset=['Statut'])
        .format({
            'Prix / L (Ar)': '{:,.0f}',
            'Index': '{:d}',
        })
        .set_properties(**{
            'font-family': 'Inter, sans-serif',
            'font-size': '14px',
            'color': '#ffffff',
        })
    )

    st.dataframe(
        styled_result,
        use_container_width=True,
        height=min(500, 80 + 35 * len(result)),
        hide_index=True,
        column_config={
            'Prix / L (Ar)': st.column_config.NumberColumn(format="%d"),
            'Index': st.column_config.NumberColumn(format="%d"),
        },
    )


# =============================================================================
# TAB 2 — VUE D'ENSEMBLE
# =============================================================================
with tab2:
    st.markdown("## 📊 Vue d'ensemble du portefeuille")

    # ---- Couverture des rôles ----
    st.markdown("### Couverture des rôles par marque")
    st.markdown(
        "Ce tableau indique quels rôles tarifaires chaque marque occupe. "
        "Une marque bien structurée couvre **au minimum Entry + Frequency**."
    )

    occ_filter = st.radio(
        "Occasion", OCCASIONS, horizontal=True, key="vue_occ",
    )
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
            .apply(style_couverture_col, subset=['Couverture'])
            .set_properties(**{
                'font-family': 'Inter, sans-serif',
                'font-size': '13px',
                'color': '#ffffff',
            })
        )

        st.dataframe(
            styled_cov,
            use_container_width=True,
            height=min(600, 80 + 38 * len(cov_df)),
            hide_index=True,
        )

    # ---- Tous les produits ----
    st.markdown("### Tous les produits du périmètre")
    st.markdown(
        "Vue tabulaire complète avec le prix au litre, l'index de positionnement "
        "et le statut de conformité."
    )

    view2 = d[['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
               'Volume_L', 'PVF_Ajusté', 'Prix_Litre_Ajusté',
               'Index', 'Statut']].copy()
    view2.columns = ['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
                     'Volume (L)', 'Prix (Ar)', 'Prix / L (Ar)',
                     'Index', 'Statut']

    styled_view2 = (
        view2.style
        .apply(style_status_col, subset=['Statut'])
        .format({
            'Volume (L)': '{:.2f}',
            'Prix (Ar)': '{:,.0f}',
            'Prix / L (Ar)': '{:,.0f}',
            'Index': '{:d}',
        })
        .set_properties(**{
            'font-family': 'Inter, sans-serif',
            'font-size': '13px',
            'color': '#ffffff',
        })
    )

    st.dataframe(
        styled_view2,
        use_container_width=True,
        height=min(700, 80 + 35 * len(view2)),
        hide_index=True,
        column_config={
            'Volume (L)': st.column_config.NumberColumn(format="%.2f"),
            'Prix (Ar)': st.column_config.NumberColumn(format="%d"),
            'Prix / L (Ar)': st.column_config.NumberColumn(format="%d"),
            'Index': st.column_config.NumberColumn(format="%d"),
        },
    )


# =============================================================================
# TAB 3 — DIAGNOSTIC
# =============================================================================
with tab3:
    st.markdown("## 🎯 Diagnostic OBPPC")
    st.markdown(
        "Liste des produits qui **ne respectent pas leur rôle tarifaire**. "
        "L'écart indique de combien de points d'index le produit doit être ajusté."
    )

    ko = d[d['Statut'] == 'À revoir'].copy()

    if ko.empty:
        st.success("✅ Tous les produits respectent leur cible tarifaire.")
    else:
        def ecart(row):
            i, role = row['Index'], row['Rôle']
            if role == 'Entry':     return max(101 - i, i - 110, 0)
            if role == 'Frequency': return abs(i - 100)
            if role == 'Upsize':    return max(90 - i, i - 99, 0)
            if role == 'Upscale':   return max(111 - i, 0)
            return 0

        ko['Écart'] = ko.apply(ecart, axis=1)
        ko = ko.sort_values('Écart', ascending=False)

        st.markdown(f"**{len(ko)} produits à réviser** — triés par écart décroissant :")

        diag = ko[['Marque', 'Format', 'Occasion', 'Rôle',
                   'Prix_Litre_Ajusté', 'Index', 'Écart']].copy()
        diag.columns = ['Marque', 'Format', 'Occasion', 'Rôle',
                        'Prix / L (Ar)', 'Index', 'Écart']

        styled_diag = (
            diag.style
            .apply(style_ecart_col, subset=['Écart'])
            .format({
                'Prix / L (Ar)': '{:,.0f}',
                'Index': '{:d}',
                'Écart': '+{:d}',
            })
            .set_properties(**{
                'font-family': 'Inter, sans-serif',
                'font-size': '13px',
                'color': '#ffffff',
            })
        )

        st.dataframe(
            styled_diag,
            use_container_width=True,
            height=min(500, 80 + 35 * len(diag)),
            hide_index=True,
            column_config={
                'Prix / L (Ar)': st.column_config.NumberColumn(format="%d"),
                'Index': st.column_config.NumberColumn(format="%d"),
                'Écart': st.column_config.NumberColumn(format="%d"),
            },
        )

        # ---- Recommandations ----
        st.markdown("### Recommandations")

        entry_ko = ko[ko['Rôle'] == 'Entry']
        freq_ko = ko[ko['Rôle'] == 'Frequency']
        up_ko = ko[ko['Rôle'].isin(['Upsize', 'Upscale'])]

        if len(freq_ko):
            st.warning(
                f"**{len(freq_ko)} produits Frequency** ne sont pas à l'index 100. "
                "Le produit de référence doit être ajusté en priorité : "
                "tous les autres index dépendent de lui."
            )
        if len(entry_ko):
            st.info(
                f"**{len(entry_ko)} produits Entry** sont en dehors de la cible 101–110. "
                "Vérifiez le positionnement du format d'accès (petit format)."
            )
        if len(up_ko):
            st.info(
                f"**{len(up_ko)} produits Upsize / Upscale** sont à revoir. "
                "Vérifiez la cohérence entre volume et prix au litre."
            )

    # ---- Export ----
    st.markdown("### Export")
    csv = d[['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
             'Volume_L', 'PVF_Ajusté', 'Prix_Litre_Ajusté',
             'Index', 'Statut']].to_csv(index=False)

    st.download_button(
        "📥 Télécharger l'analyse (CSV)",
        data=csv,
        file_name=f"analyse_obppc_{channel.split()[0].lower()}.csv",
        mime="text/csv",
    )
