import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Simulateur OBPPC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS minimal : uniquement marges + typo titres ---
st.markdown("""
<style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; max-width: 100%; }
    h1, h2, h3 { letter-spacing: -0.01em; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; border-bottom: 1px solid #21262d; }
    .stTabs [data-baseweb="tab"] { font-size: 0.85rem; padding: 0.5rem 1rem; }
    div[data-testid="stDataFrame"] { border: 1px solid #21262d; border-radius: 6px; }
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

    for item in energie_data + boisson_data + eaux_data + biere_data:
        for i, key in enumerate(data.keys()):
            data[key].append(item[i])
    return pd.DataFrame(data)


df_initial = load_initial_data()
ALL_SEGMENTS = list(df_initial['Segment'].unique())
ALL_BRANDS = sorted(df_initial['Marque'].unique())


# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------
def check_index_status(idx, role):
    if role == 'Entry (Entrée de gamme)':
        return 'OK' if 101 <= idx <= 110 else 'KO'
    if role == 'Frequency (Cœur de gamme)':
        return 'OK' if idx == 100 else 'KO'
    if role == 'Upsize (Grand format)':
        return 'OK' if 90 <= idx <= 99 else 'KO'
    if role in ['Upscale (Premium)', 'Upscale (Super-Premium Niche)']:
        return 'OK' if idx >= 111 else 'KO'
    return '—'


def target_label(role):
    return {
        'Entry (Entrée de gamme)': '101–110',
        'Frequency (Cœur de gamme)': '100',
        'Upsize (Grand format)': '90–99',
        'Upscale (Premium)': '≥111',
        'Upscale (Super-Premium Niche)': '≥111',
    }.get(role, '—')


# -----------------------------------------------------------------------------
# Sidebar — Filtres simples
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Simulateur OBPPC")
    st.caption("Occasion · Brand · Package · Price · Channel")

    st.markdown("---")

    segments = st.multiselect(
        "Segments",
        options=ALL_SEGMENTS,
        default=ALL_SEGMENTS,
    )

    available_brands = (
        sorted(df_initial[df_initial['Segment'].isin(segments)]['Marque'].unique())
        if segments else []
    )
    brands = st.multiselect(
        "Marques",
        options=available_brands,
        default=available_brands,
    )

    st.markdown("---")
    st.caption(f"**{len(segments)}** segments · **{len(brands)}** marques")


# -----------------------------------------------------------------------------
# Filtrage
# -----------------------------------------------------------------------------
if segments and brands:
    df = df_initial[
        (df_initial['Segment'].isin(segments)) & (df_initial['Marque'].isin(brands))
    ].copy()
else:
    df = df_initial.iloc[0:0].copy()

if not df.empty:
    df['P_Litre_Ar'] = df['PVF_Ar'] / df['Volume_L']


# -----------------------------------------------------------------------------
# Onglets
# -----------------------------------------------------------------------------
if df.empty:
    st.warning("Sélectionnez au moins un segment et une marque dans la sidebar.")
    st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["Simulateur", "Pyramide", "Grille tarifaire", "Diagnostic"])


# =============================================================================
# TAB 1 — SIMULATEUR
# =============================================================================
with tab1:
    st.subheader("Portefeuille — Édition")
    st.caption("Ajustez les valeurs, puis cliquez sur Recalculer.")

    edited = st.data_editor(
        df[['Segment', 'Marque', 'Occasion', 'Role_OBPPC',
            'Description', 'Volume_L', 'PVF_Ar']],
        column_config={
            "Segment": st.column_config.SelectboxColumn(
                "Segment", options=ALL_SEGMENTS, required=True, width="small"),
            "Marque": st.column_config.SelectboxColumn(
                "Marque", options=ALL_BRANDS, required=True, width="small"),
            "Occasion": st.column_config.SelectboxColumn(
                "Occasion",
                options=['IC (VER)', 'IC (PET)', 'FC (VER)', 'FC (PET)', 'Upscale', ''],
                required=False, width="small"),
            "Role_OBPPC": st.column_config.SelectboxColumn(
                "Rôle OBPPC",
                options=['Entry (Entrée de gamme)', 'Frequency (Cœur de gamme)',
                         'Upsize (Grand format)', 'Upscale (Premium)',
                         'Upscale (Super-Premium Niche)'],
                required=True, width="medium"),
            "Description": st.column_config.TextColumn("Format", width="medium"),
            "Volume_L": st.column_config.NumberColumn(
                "Volume (L)", min_value=0.1, step=0.01, format="%.2f", required=True),
            "PVF_Ar": st.column_config.NumberColumn(
                "PVF (Ar)", min_value=0, step=100, format="%d", required=True),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        height=min(600, 80 + 35 * len(df)),
        key="editor",
    )

    if st.button("Recalculer les index", type="primary"):
        e = edited.copy()
        e['P_Litre_Ar'] = e['PVF_Ar'] / e['Volume_L']

        freq = e[e['Role_OBPPC'].str.contains('Frequency', na=False)]
        base = freq['P_Litre_Ar'].mean() if len(freq) else e['P_Litre_Ar'].mean()

        e['Index'] = (e['P_Litre_Ar'] / base * 100).round(0).astype(int)
        e['Cible'] = e['Role_OBPPC'].apply(target_label)
        e['Statut'] = e.apply(lambda r: check_index_status(r['Index'], r['Role_OBPPC']), axis=1)

        result = pd.DataFrame({
            'Marque': e['Marque'],
            'Format': e['Description'],
            'Rôle OBPPC': e['Role_OBPPC'],
            'Volume (L)': e['Volume_L'],
            'PVF (Ar)': e['PVF_Ar'].round(0).astype(int),
            'Prix / L (Ar)': e['P_Litre_Ar'].round(0).astype(int),
            'Index': e['Index'],
            'Cible': e['Cible'],
            'Statut': e['Statut'],
        })

        st.markdown("#### Résultats")

        c1, c2, c3 = st.columns(3)
        c1.metric("SKU analysés", len(result))
        c2.metric("Conformes", int((result['Statut'] == 'OK').sum()))
        c3.metric("Non conformes", int((result['Statut'] == 'KO').sum()))

        st.dataframe(
            result,
            use_container_width=True,
            height=min(600, 80 + 35 * len(result)),
            column_config={
                "Volume (L)": st.column_config.NumberColumn(format="%.2f"),
                "PVF (Ar)": st.column_config.NumberColumn(format="%d"),
                "Prix / L (Ar)": st.column_config.NumberColumn(format="%d"),
                "Index": st.column_config.NumberColumn(format="%d"),
            },
            hide_index=True,
        )

        st.download_button(
            "Télécharger les résultats (CSV)",
            data=result.to_csv(index=False),
            file_name="simulation_obppc.csv",
            mime="text/csv",
        )


# =============================================================================
# TAB 2 — PYRAMIDE
# =============================================================================
with tab2:
    st.subheader("Pyramide OBPPC")
    st.caption("Répartition des SKU par rôle tarifaire.")

    seg_choice = st.radio(
        "Segment", ['Tous'] + sorted(df['Segment'].unique().tolist()),
        horizontal=True, label_visibility="collapsed",
    )
    sub = df if seg_choice == 'Tous' else df[df['Segment'] == seg_choice]

    # Rôles simplifiés
    def simpl(role):
        if role in ['Upscale (Premium)', 'Upscale (Super-Premium Niche)']:
            return 'Upscale'
        if role == 'Entry (Entrée de gamme)':
            return 'Entry'
        if role == 'Frequency (Cœur de gamme)':
            return 'Frequency'
        if role == 'Upsize (Grand format)':
            return 'Upsize'
        return 'Autre'

    sub = sub.copy()
    sub['Role'] = sub['Role_OBPPC'].apply(simpl)

    role_stats = sub.groupby('Role').agg(
        SKU=('Marque', 'count'),
        Prix_moyen=('P_Litre_Ar', 'mean'),
    ).round(0)

    # Ordre pyramidale
    order = ['Upscale', 'Entry', 'Frequency', 'Upsize']
    role_stats = role_stats.reindex([r for r in order if r in role_stats.index])

    if not role_stats.empty:
        max_sku = role_stats['SKU'].max()
        for role, row in role_stats.iterrows():
            pct = int(row['SKU'] / role_stats['SKU'].sum() * 100)
            st.markdown(f"**{role}** — {int(row['SKU'])} SKU ({pct}%)")
            st.progress(
                float(row['SKU'] / max_sku),
                text=f"Prix moyen / L : {row['Prix_moyen']:,.0f} Ar",
            )
            st.write("")


# =============================================================================
# TAB 3 — GRILLE
# =============================================================================
with tab3:
    st.subheader("Grille tarifaire")
    st.caption("Prix de vente (PVF) par marque et format.")

    seg3 = st.selectbox("Segment", sorted(df['Segment'].unique()), key="grid_seg")
    sub3 = df[df['Segment'] == seg3].copy()

    def parse_vol(col):
        nums = [int(s) for s in ''.join(c if c.isdigit() else ' ' for c in col).split()]
        return nums[0] if nums else 999

    pivot = sub3.pivot_table(
        index='Marque', columns='Description',
        values='PVF_Ar', aggfunc='mean',
    ).round(0)
    pivot = pivot[sorted(pivot.columns, key=parse_vol)]

    st.markdown("**Prix (PVF en Ar)**")
    st.dataframe(
        pivot,
        use_container_width=True,
        height=min(500, 80 + 35 * len(pivot)),
    )

    st.markdown("**Prix au litre (Ar)**")
    pivot_pl = sub3.pivot_table(
        index='Marque', columns='Description',
        values='P_Litre_Ar', aggfunc='mean',
    ).round(0)
    pivot_pl = pivot_pl[sorted(pivot_pl.columns, key=parse_vol)]

    st.dataframe(
        pivot_pl,
        use_container_width=True,
        height=min(400, 80 + 35 * len(pivot_pl)),
    )

    st.download_button(
        "Exporter la grille (CSV)",
        data=pivot.to_csv(),
        file_name=f"grille_{seg3.lower()}.csv",
        mime="text/csv",
    )


# =============================================================================
# TAB 4 — DIAGNOSTIC
# =============================================================================
with tab4:
    st.subheader("Diagnostic de conformité")
    st.caption("Écart à la cible OBPPC, base = moyenne des produits Frequency.")

    d = df.copy()
    freq = d[d['Role_OBPPC'].str.contains('Frequency', na=False)]
    base = freq['P_Litre_Ar'].mean() if len(freq) else d['P_Litre_Ar'].mean()

    d['Index'] = (d['P_Litre_Ar'] / base * 100).round(0).astype(int)
    d['Cible'] = d['Role_OBPPC'].apply(target_label)
    d['Statut'] = d.apply(lambda r: check_index_status(r['Index'], r['Role_OBPPC']), axis=1)

    # Synthèse par segment
    st.markdown("**Conformité par segment**")
    seg_summary = d.groupby('Segment').apply(
        lambda g: pd.Series({
            'Total': len(g),
            'Conformes': (g['Statut'] == 'OK').sum(),
            'Taux (%)': round((g['Statut'] == 'OK').sum() / len(g) * 100, 1),
        })
    )
    st.dataframe(seg_summary, use_container_width=True)

    # Non conformes
    st.markdown("**Positions non conformes**")
    ko = d[d['Statut'] == 'KO'].copy()

    if ko.empty:
        st.success("Toutes les positions respectent la cible OBPPC.")
    else:
        def gap(row):
            i, role = row['Index'], row['Role_OBPPC']
            if role == 'Entry (Entrée de gamme)':
                return max(101 - i, i - 110, 0)
            if role == 'Frequency (Cœur de gamme)':
                return abs(i - 100)
            if role == 'Upsize (Grand format)':
                return max(90 - i, i - 99, 0)
            if role in ['Upscale (Premium)', 'Upscale (Super-Premium Niche)']:
                return max(111 - i, 0)
            return 0

        ko['Écart'] = ko.apply(gap, axis=1)
        ko = ko.sort_values('Écart', ascending=False)

        out = pd.DataFrame({
            'Marque': ko['Marque'],
            'Format': ko['Description'],
            'Rôle': ko['Role_OBPPC'],
            'Prix / L (Ar)': ko['P_Litre_Ar'].round(0).astype(int),
            'Index': ko['Index'],
            'Cible': ko['Cible'],
            'Écart': ko['Écart'].astype(int),
        })

        st.dataframe(
            out,
            use_container_width=True,
            height=min(500, 80 + 35 * len(out)),
            column_config={
                "Prix / L (Ar)": st.column_config.NumberColumn(format="%d"),
                "Index": st.column_config.NumberColumn(format="%d"),
                "Écart": st.column_config.NumberColumn(format="%d"),
            },
            hide_index=True,
        )

    # Verdict global
    total = len(d)
    conf = int((d['Statut'] == 'OK').sum())
    taux = conf / total * 100 if total else 0

    st.markdown("---")
    st.markdown("**Verdict**")

    if taux >= 80:
        st.success(f"Cohérence élevée — {conf}/{total} SKU conformes ({taux:.0f}%).")
    elif taux >= 50:
        st.warning(f"Cohérence partielle — {conf}/{total} SKU conformes ({taux:.0f}%).")
    else:
        st.error(f"Cohérence faible — {conf}/{total} SKU conformes ({taux:.0f}%).")
