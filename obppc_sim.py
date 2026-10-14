import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="OBPPC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS minimal — uniquement ce qui améliore la lisibilité
st.markdown("""
<style>
    /* Taille de police confortable et interligne aéré */
    html, body, [class*="css"] {
        font-size: 15px;
        line-height: 1.6;
    }

    /* Titres avec de l'air */
    h1 { font-size: 1.8rem !important; margin-bottom: 0.4rem !important; }
    h2 { font-size: 1.35rem !important; margin-top: 1.5rem !important; }
    h3 { font-size: 1.1rem !important; margin-top: 1.2rem !important; }

    /* Les tableaux HTML lisibles */
    .data-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
        margin-top: 0.5rem;
    }
    .data-table th {
        background: #242832;
        color: #cbd5e1;
        padding: 12px 14px;
        text-align: left;
        font-size: 13px;
        font-weight: 600;
        border-bottom: 2px solid #343a4a;
    }
    .data-table td {
        padding: 11px 14px;
        color: #f5f7fa;
        border-bottom: 1px solid #2a2e38;
        font-variant-numeric: tabular-nums;
    }
    .data-table tr:hover td {
        background: #22262f;
    }
    .data-table .num {
        text-align: right;
        font-weight: 500;
    }

    /* Badge de statut */
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .tag-ok   { background: #14351f; color: #4ade80; }
    .tag-ko   { background: #3a1a1a; color: #f87171; }
    .tag-warn { background: #3a2f14; color: #fbbf24; }

    /* Cartes d'indicateurs */
    .info-box {
        background: #242832;
        border-radius: 10px;
        padding: 16px 20px;
        margin-bottom: 12px;
        border-left: 4px solid #a78bfa;
    }
    .info-box .label {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 4px;
    }
    .info-box .value {
        color: #f5f7fa;
        font-size: 22px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Données
# -----------------------------------------------------------------------------
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
ROLE_TARGETS = {'Entry': '101–110', 'Frequency': '100', 'Upsize': '90–99', 'Upscale': '≥111'}
ROLE_INFO = {
    'Entry':     "Prix d'accès à la marque, petit format",
    'Frequency': "Format de référence, prix pivot",
    'Upsize':    "Grand format, prix au litre plus bas",
    'Upscale':   "Format premium, prix au litre plus élevé",
}


def status(idx, role):
    if role == 'Entry':     return 'OK' if 101 <= idx <= 110 else 'KO'
    if role == 'Frequency': return 'OK' if idx == 100 else 'KO'
    if role == 'Upsize':    return 'OK' if 90 <= idx <= 99 else 'KO'
    if role == 'Upscale':   return 'OK' if idx >= 111 else 'KO'
    return '—'


# -----------------------------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## ⚙️ Paramètres")

    st.markdown("##### Filtres")
    segments = st.multiselect(
        "Segment",
        sorted(df['Segment'].unique()),
        default=sorted(df['Segment'].unique()),
        help="Filtrer par type de boisson",
    )

    available_brands = sorted(df[df['Segment'].isin(segments)]['Marque'].unique()) if segments else []
    brands = st.multiselect(
        "Marque",
        available_brands,
        default=available_brands,
        help="Filtrer par marque",
    )

    st.divider()

    st.markdown("##### Canal de vente")
    channel = st.radio(
        "Canal",
        ["GMS (prix de référence)", "Horeca (+35%)", "Traditionnel (+15%)"],
        help="Applique un coefficient aux prix selon le canal",
    )
    coef = {
        "GMS (prix de référence)": 1.00,
        "Horeca (+35%)": 1.35,
        "Traditionnel (+15%)": 1.15,
    }[channel]

    st.divider()

    if st.button("🔄 Réinitialiser les modifications", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith("prix_"):
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
    st.caption("Index 100 = produit de référence (Frequency)")


# -----------------------------------------------------------------------------
# Filtrer
# -----------------------------------------------------------------------------
d = df[(df['Segment'].isin(segments)) & (df['Marque'].isin(brands))].copy()

if d.empty:
    st.warning("⚠️ Aucun produit ne correspond à vos filtres. Élargissez votre sélection.")
    st.stop()

d['PVF_Ajusté'] = (d['PVF_Ar'] * coef).round(0).astype(int)
d['Prix_Litre_Ajusté'] = (d['Prix_Litre'] * coef).round(0).astype(int)

# Référence : moyenne des Frequency par segment × occasion
ref = (d[d['Rôle'] == 'Frequency']
       .groupby(['Segment', 'Occasion'])['Prix_Litre_Ajusté'].mean())
d['Ref'] = d.set_index(['Segment', 'Occasion']).index.map(ref)
d['Ref'] = d['Ref'].fillna(d.groupby(['Segment', 'Occasion'])['Prix_Litre_Ajusté'].transform('mean'))
d['Index'] = (d['Prix_Litre_Ajusté'] / d['Ref'] * 100).round(0).astype(int)
d['Statut'] = d.apply(lambda r: status(r['Index'], r['Rôle']), axis=1)


# =============================================================================
# EN-TÊTE
# =============================================================================
st.markdown("# Simulateur OBPPC")
st.markdown(
    "**Analyse de cohérence** entre les rôles tarifaires (Entry, Frequency, Upsize, Upscale) "
    "et les prix au litre, par marque et par occasion."
)

# Bandeau de synthèse
n_ok = int((d['Statut'] == 'OK').sum())
n_ko = int((d['Statut'] == 'KO').sum())
taux = n_ok / len(d) * 100 if len(d) else 0

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Produits analysés", len(d))
with col2:
    st.metric("✅ Conformes", n_ok)
with col3:
    st.metric("❌ Non conformes", n_ko)
with col4:
    st.metric("Taux de conformité", f"{taux:.0f}%")

if taux >= 80:
    st.success(f"**Cohérence élevée** — {n_ok} produits sur {len(d)} respectent leur cible tarifaire.")
elif taux >= 50:
    st.warning(f"**Cohérence partielle** — {n_ko} produits s'écartent de leur cible. Vérifiez l'onglet Diagnostic.")
else:
    st.error(f"**Cohérence faible** — {n_ko} produits ne respectent pas leur rôle. Arbitrage prix à revoir.")

st.divider()


# =============================================================================
# NAVIGATION
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
        "Ajustez le **prix de vente (PVF)** ou le **volume** d'un produit directement dans le tableau. "
        "Toutes les analyses se recalculent automatiquement."
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
                help="Entry / Frequency / Upsize / Upscale",
            ),
            "Format": st.column_config.TextColumn("Format", disabled=True, width="medium"),
            "Volume_L": st.column_config.NumberColumn(
                "Volume (L)", min_value=0.05, step=0.05, format="%.2f",
                help="Volume du contenant en litres",
            ),
            "PVF_Ar": st.column_config.NumberColumn(
                "Prix de vente (Ar)", min_value=0, step=100, format="%d",
                help="Prix de vente final en Ariary",
            ),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        height=min(600, 100 + 38 * len(editor_df)),
        key="price_editor",
    )

    # Recalcul
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
    st.caption(f"Canal : {channel} · Index 100 = moyenne des Frequency du même segment × occasion")

    # Tableau de résultats propre
    view = d2[['Marque', 'Format', 'Occasion', 'Rôle',
               'Prix_Litre_Ajusté', 'Index', 'Statut']].copy()
    view.columns = ['Marque', 'Format', 'Occasion', 'Rôle',
                    'Prix / L (Ar)', 'Index', 'Statut']
    view['Prix / L (Ar)'] = view['Prix / L (Ar)'].apply(lambda x: f"{x:,}".replace(',', ' '))
    view['Statut'] = view['Statut'].map({
        'OK': '<span class="tag tag-ok">Conforme</span>',
        'KO': '<span class="tag tag-ko">À revoir</span>',
        '—':  '<span class="tag tag-warn">—</span>',
    })

    html = ['<table class="data-table">']
    html.append('<thead><tr>')
    for c in view.columns:
        html.append(f'<th{" class=num" if "Prix" in c or "Index" in c else ""}>{c}</th>')
    html.append('</tr></thead><tbody>')
    for _, row in view.iterrows():
        html.append('<tr>')
        for i, c in enumerate(view.columns):
            cls = ' class="num"' if c in ('Prix / L (Ar)', 'Index') else ''
            html.append(f'<td{cls}>{row[c]}</td>')
        html.append('</tr>')
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)


# =============================================================================
# TAB 2 — VUE D'ENSEMBLE
# =============================================================================
with tab2:
    st.markdown("## 📊 Vue d'ensemble du portefeuille")

    st.markdown("### Couverture des rôles par marque")
    st.markdown(
        "Ce tableau montre quels rôles tarifaires chaque marque occupe. "
        "Une marque bien structurée couvre **au minimum Entry + Frequency**."
    )

    sub = d[d['Occasion'] == st.radio(
        "Occasion", OCCASIONS, horizontal=True, key="vue_occ",
        help="IC = consommation immédiate · FC = consommation future"
    )]

    if sub.empty:
        st.info("Aucun produit sur cette occasion.")
    else:
        brands_in = sorted(sub['Marque'].unique())

        html = ['<table class="data-table"><thead><tr>'
                '<th>Marque</th><th>Entry</th><th>Frequency</th>'
                '<th>Upsize</th><th>Upscale</th><th>Couverture</th>'
                '</tr></thead><tbody>']

        for brand in brands_in:
            bsub = sub[sub['Marque'] == brand]
            html.append(f'<tr><td><b>{brand}</b></td>')
            covered = 0
            for role in ROLES:
                rsub = bsub[bsub['Rôle'] == role]
                if rsub.empty:
                    html.append('<td style="color:#4a5264;">—</td>')
                else:
                    covered += 1
                    formats = ', '.join(rsub['Format'].tolist())
                    html.append(f'<td>{formats}</td>')
            cov_color = '#4ade80' if covered >= 3 else '#fbbf24' if covered == 2 else '#f87171'
            html.append(f'<td><b style="color:{cov_color}">{covered}/4</b></td>')
            html.append('</tr>')

        html.append('</tbody></table>')
        st.markdown(''.join(html), unsafe_allow_html=True)

    st.markdown("### Tous les produits du périmètre")
    st.markdown(
        "Vue tabulaire complète avec le prix au litre, l'index de positionnement "
        "et le statut de conformité."
    )

    view2 = d[['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
               'Volume_L', 'PVF_Ajusté', 'Prix_Litre_Ajusté', 'Index', 'Statut']].copy()
    view2.columns = ['Segment', 'Marque', 'Occasion', 'Rôle', 'Format',
                     'Volume (L)', 'Prix (Ar)', 'Prix / L (Ar)', 'Index', 'Statut']
    view2['Statut'] = view2['Statut'].map({
        'OK': '<span class="tag tag-ok">Conforme</span>',
        'KO': '<span class="tag tag-ko">À revoir</span>',
        '—':  '<span class="tag tag-warn">—</span>',
    })

    html = ['<table class="data-table"><thead><tr>']
    for c in view2.columns:
        html.append(f'<th>{c}</th>')
    html.append('</tr></thead><tbody>')
    for _, row in view2.iterrows():
        html.append('<tr>')
        for c in view2.columns:
            val = row[c]
            cls = ' class="num"' if c in ('Volume (L)', 'Prix (Ar)', 'Prix / L (Ar)', 'Index') else ''
            if c == 'Volume (L)':
                val = f"{val:.2f}"
            elif c in ('Prix (Ar)', 'Prix / L (Ar)'):
                val = f"{int(val):,}".replace(',', ' ')
            html.append(f'<td{cls}>{val}</td>')
        html.append('</tr>')
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)


# =============================================================================
# TAB 3 — DIAGNOSTIC
# =============================================================================
with tab3:
    st.markdown("## 🎯 Diagnostic OBPPC")
    st.markdown(
        "Liste des produits qui **ne respectent pas leur rôle tarifaire**. "
        "L'écart indique de combien de points d'index le produit doit être ajusté."
    )

    ko = d[d['Statut'] == 'KO'].copy()

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

        html = ['<table class="data-table"><thead><tr>'
                '<th>Marque</th><th>Format</th><th>Rôle actuel</th>'
                '<th>Prix / L</th><th>Index</th><th>Cible</th><th>Écart</th>'
                '</tr></thead><tbody>']

        for _, row in ko.iterrows():
            cible = ROLE_TARGETS[row['Rôle']]
            html.append('<tr>')
            html.append(f'<td><b>{row["Marque"]}</b></td>')
            html.append(f'<td>{row["Format"]}</td>')
            html.append(f'<td>{row["Rôle"]}</td>')
            html.append(f'<td class="num">{int(row["Prix_Litre_Ajusté"]):,} Ar</td>'.replace(',', ' '))
            html.append(f'<td class="num">{row["Index"]}</td>')
            html.append(f'<td>{cible}</td>')
            html.append(f'<td class="num"><b style="color:#f87171">+{int(row["Écart"])}</b></td>')
            html.append('</tr>')
        html.append('</tbody></table>')
        st.markdown(''.join(html), unsafe_allow_html=True)

        st.markdown("### Recommandations")

        entry_ko = ko[ko['Rôle'] == 'Entry']
        freq_ko = ko[ko['Rôle'] == 'Frequency']
        up_ko = ko[ko['Rôle'].isin(['Upsize', 'Upscale'])]

        if len(freq_ko):
            st.warning(
                f"**{len(freq_ko)} produits Frequency** ne sont pas à l'index 100. "
                "Le produit de référence doit être ajusté en priorité, car tous les autres index dépendent de lui."
            )
        if len(entry_ko):
            st.info(
                f"**{len(entry_ko)} produits Entry** sont en dehors de la cible 101–110. "
                "Vérifiez le positionnement du format d'accès (petit format)."
            )
        if len(up_ko):
            st.info(
                f"**{len(up_ko)} produits Upsize/Upscale** sont à revoir. "
                "Vérifiez la cohérence entre volume et prix au litre."
            )
