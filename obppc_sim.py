import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="OBPPC", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main .block-container { padding-top: 1.25rem; max-width: 100%; }

    /* Tableau matrice : fond sombre uniforme, seul le bord gauche est coloré */
    .obppc-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
    .obppc-table th {
        background: #161b22; color: #8b949e;
        padding: 8px 10px; font-size: 0.68rem;
        text-transform: uppercase; letter-spacing: 0.05em;
        border: 1px solid #30363d; font-weight: 600; text-align: center;
    }
    .obppc-table th.row-head { text-align: left; min-width: 110px; }
    .obppc-table td {
        border: 1px solid #30363d;
        padding: 8px 10px;
        text-align: center;
        color: #e6edf3;
        background: #0e1117;
        font-variant-numeric: tabular-nums;
        vertical-align: middle;
    }
    .obppc-table td.row-head {
        text-align: left; font-weight: 600; color: #e6edf3;
        background: #161b22;
    }
    .obppc-table td.empty { color: #484f58; background: #0e1117; }
    .obppc-table td.cell {
        border-left: 3px solid var(--c, #30363d);
    }
    .pv { font-weight: 600; font-size: 0.85rem; color: #e6edf3; }
    .idx { font-size: 0.7rem; color: #8b949e; margin-left: 4px; }

    .legend { display: flex; gap: 1rem; margin: 0.75rem 0 1rem 0; flex-wrap: wrap; }
    .legend-item {
        display: flex; align-items: center; gap: 0.4rem;
        font-size: 0.75rem; color: #c9d1d9;
    }
    .legend-swatch {
        width: 10px; height: 10px; border-radius: 2px;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# Données
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    rows = [
        ('Energie', 'Red Bull', 'Upscale', 'Upscale (Premium)', 'CAN 25', 0.25, 9900),
        ('Energie', 'Monster', 'Upscale', 'Upscale (Premium)', 'CAN 50', 0.50, 9900),
        ('Energie', 'FOSA', 'Upscale', 'Upscale (Premium)', 'CAN 50', 0.50, 5000),
        ('Energie', 'XXL', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 2500),
        ('Energie', 'XXL', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 35', 0.35, 3500),
        ('Energie', 'XXL', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 4000),
        ('Energie', 'DYNAMIC', 'Upscale', 'Upscale (Premium)', 'CAN 25', 0.25, 3500),
        ('Energie', 'BOOST VITALITY', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 4000),

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

        ('Eaux', 'Cristal', 'IC (VER)', 'Entry (Entrée de gamme)', 'Cristal 30 VER', 0.30, 1500),
        ('Eaux', 'Cristal', 'IC (VER)', 'Frequency (Cœur de gamme)', 'Cristal 50 VER', 0.50, 2200),
        ('Eaux', 'Cristal', 'FC (VER)', 'Upsize (Grand format)', 'Cristal 100 VER', 1.00, 3800),
        ('Eaux', 'Cristal', 'FC (PET)', 'Upsize (Grand format)', 'Cristal 150 PET', 1.50, 5500),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Entry (Entrée de gamme)', 'RANOVISY 33 PET', 0.33, 1000),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Frequency (Cœur de gamme)', 'RANOVISY 50 PET', 0.50, 2400),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Upsize (Grand format)', 'RANOVISY 75 PET', 0.75, 3000),
        ('Eaux', 'VISY GASY', 'IC (PET)', 'Entry (Entrée de gamme)', 'VISY GASY 60 PET', 0.60, 2500),
        ('Eaux', 'VISY GASY', 'FC (PET)', 'Upsize (Grand format)', 'VISY GASY 100 PET', 1.00, 3000),
        ('Eaux', 'Eau vive', 'IC (PET)', 'Entry (Entrée de gamme)', 'Eau vive 50 PET', 0.50, 1600),
        ('Eaux', 'Eau vive', 'FC (PET)', 'Upsize (Grand format)', 'Eau vive 150 PET', 1.50, 3300),
        ('Eaux', 'Eau vive', 'IC (VER)', 'Frequency (Cœur de gamme)', 'Eau vive 50 VER', 0.50, 2200),
        ('Eaux', 'Cristalline', 'FC (PET)', 'Upsize (Grand format)', 'Cristalline 100 PET', 1.50, 2100),
        ('Eaux', 'Cristalline', 'FC (PET)', 'Upsize (Grand format)', 'Cristalline 200 PET', 2.00, 3600),
        ('Eaux', 'OLYMPIKO', 'IC (PET)', 'Entry (Entrée de gamme)', 'OLYMPIKO 50', 0.50, 1500),
        ('Eaux', 'OLYMPIKO', 'FC (PET)', 'Frequency (Cœur de gamme)', 'OLYMPIKO 100', 1.00, 2000),
        ('Eaux', 'OLYMPIKO', 'FC (PET)', 'Upsize (Grand format)', 'OLYMPIKO 150', 1.50, 2500),
        ('Eaux', 'NATUR EAU', 'IC (PET)', 'Entry (Entrée de gamme)', 'NATUR EAU 50', 0.50, 1500),
        ('Eaux', 'NATUR EAU', 'FC (PET)', 'Frequency (Cœur de gamme)', 'NATUR EAU 100', 1.00, 2000),
        ('Eaux', 'NATUR EAU', 'FC (PET)', 'Upsize (Grand format)', 'NATUR EAU 150', 1.50, 2500),

        ('Bière', 'Beaufort', 'IC (VER)', 'Frequency (Cœur de gamme)', 'Beaufort 33 VER', 0.33, 4000),
        ('Bière', 'Beaufort', 'IC (CAN)', 'Upscale (Premium)', 'Beaufort 33 CAN', 0.33, 5000),
        ('Bière', 'Gold', 'IC (VER)', 'Entry (Entrée de gamme)', 'Gold Blanche 33 VER', 0.33, 3500),
        ('Bière', 'Gold', 'FC (VER)', 'Entry (Entrée de gamme)', 'Gold 8 50 VER', 0.50, 4500),
        ('Bière', 'Gold', 'FC (VER)', 'Frequency (Cœur de gamme)', 'Gold Blanche 50 VER', 0.50, 4500),
        ('Bière', 'Gold', 'FC (VER)', 'Frequency (Cœur de gamme)', 'Gold Blonde 50 VER', 0.50, 4500),
        ('Bière', 'Gold', 'FC (VER)', 'Frequency (Cœur de gamme)', 'Gold Blonde 65 VER', 0.65, 5000),
        ('Bière', 'Gold', 'IC (CAN)', 'Upscale (Premium)', 'Gold 8 50 CAN', 0.50, 6000),
        ('Bière', 'Gold', 'IC (CAN)', 'Upscale (Premium)', 'Gold Blanche 50 CAN', 0.50, 6000),
        ('Bière', 'Gold', 'IC (CAN)', 'Upscale (Premium)', 'Gold Blonde 50 CAN', 0.50, 6000),
        ('Bière', 'THB', 'IC (VER)', 'Entry (Entrée de gamme)', 'THB Pilsener 33 VER', 0.33, 2500),
        ('Bière', 'THB', 'FC (VER)', 'Frequency (Cœur de gamme)', 'THB Pilsener 65 VER', 0.65, 4500),
        ('Bière', 'THB', 'IC (CAN)', 'Upscale (Premium)', 'THB Pilsener 50 CAN', 0.50, 5000),
        ('Bière', 'Queen', 'FC (VER)', 'Entry (Entrée de gamme)', 'Queen s 65 VER', 0.65, 4000),
        ('Bière', 'Fresh', 'IC (VER)', 'Entry (Entrée de gamme)', 'Fresh 33 VER', 0.33, 2500),
        ('Bière', 'Fresh', 'FC (VER)', 'Frequency (Cœur de gamme)', 'Fresh 65 VER', 0.65, 4000),
        ('Bière', 'Fresh', 'IC (CAN)', 'Upscale (Premium)', 'Fresh 33 CAN', 0.33, 3500),
    ]
    df = pd.DataFrame(rows, columns=['Segment', 'Marque', 'Occasion', 'Role_OBPPC',
                                      'Format', 'Volume_L', 'PVF_Ar'])
    df['P_Litre'] = df['PVF_Ar'] / df['Volume_L']

    def occ_group(o):
        if o.startswith('IC'):
            return 'IC (Immédiate)'
        if o.startswith('FC'):
            return 'FC (Future)'
        return 'Hors occasion'
    df['Occ_Group'] = df['Occasion'].apply(occ_group)
    return df


df = load_data()
ALL_SEGMENTS = sorted(df['Segment'].unique())

ROLE_SIMPLE = {
    'Entry (Entrée de gamme)': 'Entry',
    'Frequency (Cœur de gamme)': 'Frequency',
    'Upsize (Grand format)': 'Upsize',
    'Upscale (Premium)': 'Upscale',
    'Upscale (Super-Premium Niche)': 'Upscale',
}
ROLE_COLORS = {
    'Entry':     '#58a6ff',   # bleu clair
    'Frequency': '#3fb950',   # vert
    'Upsize':    '#d29922',   # jaune/orange
    'Upscale':   '#bc8cff',   # violet clair
}
ROLE_TARGET = {'Entry': '101–110', 'Frequency': '100', 'Upsize': '90–99', 'Upscale': '≥111'}


def status(idx, role):
    if role == 'Entry':     return 'OK' if 101 <= idx <= 110 else 'KO'
    if role == 'Frequency': return 'OK' if idx == 100 else 'KO'
    if role == 'Upsize':    return 'OK' if 90 <= idx <= 99 else 'KO'
    if role == 'Upscale':   return 'OK' if idx >= 111 else 'KO'
    return '—'


# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### OBPPC")
    st.caption("Occasion · Brand · Package · Price · Channel")
    st.markdown("---")

    segments = st.multiselect("Segments", ALL_SEGMENTS, default=ALL_SEGMENTS)
    available_brands = (
        sorted(df[df['Segment'].isin(segments)]['Marque'].unique())
        if segments else []
    )
    brands = st.multiselect("Marques", available_brands, default=available_brands)

    st.markdown("---")
    channel = st.radio(
        "Canal", ["GMS", "Horeca (+35%)", "Traditionnel (+15%)"],
    )
    coef_map = {"GMS": 1.00, "Horeca (+35%)": 1.35, "Traditionnel (+15%)": 1.15}
    coef = coef_map[channel]

    st.markdown("---")
    st.caption(
        "**Cibles d'index prix/litre**  \n"
        f"<span style='color:{ROLE_COLORS['Entry']}'>■</span> Entry — 101–110  \n"
        f"<span style='color:{ROLE_COLORS['Frequency']}'>■</span> Frequency — 100  \n"
        f"<span style='color:{ROLE_COLORS['Upsize']}'>■</span> Upsize — 90–99  \n"
        f"<span style='color:{ROLE_COLORS['Upscale']}'>■</span> Upscale — ≥111",
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Filtrage
# -----------------------------------------------------------------------------
d = df[(df['Segment'].isin(segments)) & (df['Marque'].isin(brands))].copy()

if d.empty:
    st.warning("Sélectionnez au moins un segment et une marque.")
    st.stop()

d['PVF_Ajuste'] = d['PVF_Ar'] * coef
d['P_Litre_Ajuste'] = d['P_Litre'] * coef
d['Role'] = d['Role_OBPPC'].map(ROLE_SIMPLE)

ref = (
    d[d['Role'] == 'Frequency']
    .groupby(['Segment', 'Occ_Group'])['P_Litre_Ajuste'].mean()
)
d['Ref_Litre'] = d.set_index(['Segment', 'Occ_Group']).index.map(ref)
d['Ref_Litre'] = d['Ref_Litre'].fillna(
    d.groupby(['Segment', 'Occ_Group'])['P_Litre_Ajuste'].transform('mean')
)
d['Index'] = (d['P_Litre_Ajuste'] / d['Ref_Litre'] * 100).round(0).astype(int)
d['Statut'] = d.apply(lambda r: status(r['Index'], r['Role']), axis=1)


# -----------------------------------------------------------------------------
# En-tête
# -----------------------------------------------------------------------------
st.markdown(f"## Matrice OBPPC — Canal **{channel}**")
st.caption(
    f"{len(d)} SKU · {d['Marque'].nunique()} marques · "
    f"{d['Segment'].nunique()} segments · référence = moyenne des Frequency"
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Matrice OBPPC", "Couverture des rôles", "Échelle de prix", "Diagnostic",
])


# =============================================================================
# TAB 1 — MATRICE OBPPC (fond neutre + bord gauche coloré)
# =============================================================================
with tab1:
    seg_choice = st.selectbox("Segment", sorted(d['Segment'].unique()), key="t1_seg")
    sub = d[d['Segment'] == seg_choice].copy()

    sub['Occ_Order'] = sub['Occ_Group'].map(
        {'IC (Immédiate)': 0, 'FC (Future)': 1, 'Hors occasion': 2}
    )
    sub = sub.sort_values(['Occ_Order', 'Volume_L'])

    cols = sorted(
        sub['Format'].unique(),
        key=lambda f: (
            sub[sub['Format'] == f]['Occ_Order'].iloc[0],
            sub[sub['Format'] == f]['Volume_L'].iloc[0],
        ),
    )
    brands_in = sorted(sub['Marque'].unique())

    html = ['<table class="obppc-table">']
    html.append('<thead><tr><th class="row-head">Marque</th>')
    for c in cols:
        html.append(f'<th>{c}</th>')
    html.append('</tr></thead><tbody>')

    for brand in brands_in:
        html.append(f'<tr><td class="row-head">{brand}</td>')
        bsub = sub[sub['Marque'] == brand]
        for c in cols:
            cell = bsub[bsub['Format'] == c]
            if cell.empty:
                html.append('<td class="empty">—</td>')
            else:
                row = cell.iloc[0]
                color = ROLE_COLORS[row['Role']]
                pv = f'{int(row["PVF_Ajuste"]):,}'
                idx = row['Index']
                # petit indicateur de conformité
                ok = row['Statut'] == 'OK'
                mark = '' if ok else '⚠'
                html.append(
                    f'<td class="cell" style="--c:{color};">'
                    f'<span class="pv">{pv}</span>'
                    f'<span class="idx">·{idx}{mark}</span>'
                    f'</td>'
                )
        html.append('</tr>')
    html.append('</tbody></table>')

    st.markdown(''.join(html), unsafe_allow_html=True)

    st.markdown(
        '<div class="legend">'
        + ''.join([
            f'<div class="legend-item">'
            f'<span class="legend-swatch" style="background:{color};"></span>'
            f'{role} (cible {ROLE_TARGET[role]})</div>'
            for role, color in ROLE_COLORS.items()
        ])
        + '</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Chiffre = PVF ajusté au canal (Ar). Nombre après le point = index prix/litre "
        "(100 = référence Frequency du segment × occasion). ⚠ = non conforme à la cible."
    )


# =============================================================================
# TAB 2 — COUVERTURE DES RÔLES
# =============================================================================
with tab2:
    st.markdown("#### Couverture des rôles par marque")
    st.caption(
        "Une marque bien structurée couvre au minimum **Entry + Frequency** sur une occasion."
    )

    occ_choice = st.radio(
        "Occasion", ['IC (Immédiate)', 'FC (Future)', 'Hors occasion'],
        horizontal=True, key="t2_occ",
    )
    sub2 = d[d['Occ_Group'] == occ_choice]

    if sub2.empty:
        st.info("Aucun SKU sur cette occasion.")
    else:
        pivot = sub2.pivot_table(
            index='Marque', columns='Role',
            values='Format', aggfunc='count',
        ).fillna(0).astype(int)
        for r in ['Entry', 'Frequency', 'Upsize', 'Upscale']:
            if r not in pivot.columns:
                pivot[r] = 0
        pivot = pivot[['Entry', 'Frequency', 'Upsize', 'Upscale']]

        html = ['<table class="obppc-table">']
        html.append(
            '<thead><tr><th class="row-head">Marque</th>'
            '<th>Entry</th><th>Frequency</th><th>Upsize</th><th>Upscale</th>'
            '<th>Couverture</th></tr></thead><tbody>'
        )
        for brand, row in pivot.iterrows():
            covered = (row > 0).sum()
            bar_color = '#3fb950' if covered >= 3 else '#d29922' if covered >= 2 else '#f85149'
            html.append(f'<tr><td class="row-head">{brand}</td>')
            for role in ['Entry', 'Frequency', 'Upsize', 'Upscale']:
                n = row[role]
                if n > 0:
                    color = ROLE_COLORS[role]
                    html.append(
                        f'<td class="cell" style="--c:{color};">'
                        f'<span class="pv">{n}</span></td>'
                    )
                else:
                    html.append('<td class="empty">·</td>')
            html.append(
                f'<td><span style="color:{bar_color}; font-weight:700;">'
                f'{covered}/4</span></td>'
            )
            html.append('</tr>')
        html.append('</tbody></table>')
        st.markdown(''.join(html), unsafe_allow_html=True)

        st.markdown("##### Lacunes détectées")
        missing = pivot[(pivot['Entry'] == 0) | (pivot['Frequency'] == 0)]
        if missing.empty:
            st.success("Toutes les marques couvrent Entry et Frequency sur cette occasion.")
        else:
            for brand, row in missing.iterrows():
                gaps = []
                if row['Entry'] == 0: gaps.append('Entry')
                if row['Frequency'] == 0: gaps.append('Frequency')
                st.warning(f"**{brand}** — manquant : {', '.join(gaps)}")


# =============================================================================
# TAB 3 — ÉCHELLE DE PRIX
# =============================================================================
with tab3:
    st.markdown("#### Échelle de prix par marque")
    st.caption("Progression Entry → Frequency → Upsize → Upscale, par occasion.")

    brand_choice = st.selectbox("Marque", sorted(d['Marque'].unique()), key="t3_brand")
    bsub = d[d['Marque'] == brand_choice].copy()

    order_roles = ['Entry', 'Frequency', 'Upsize', 'Upscale']
    bsub = bsub[bsub['Role'].isin(order_roles)]
    bsub['Role_Order'] = bsub['Role'].map({r: i for i, r in enumerate(order_roles)})
    bsub = bsub.sort_values(['Occ_Group', 'Role_Order'])

    if bsub.empty:
        st.info("Aucune donnée pour cette marque.")
    else:
        fig = go.Figure()
        for occ in bsub['Occ_Group'].unique():
            occ_df = bsub[bsub['Occ_Group'] == occ]
            fig.add_trace(go.Bar(
                x=occ_df['Role'],
                y=occ_df['P_Litre_Ajuste'],
                name=occ,
                text=[f'{int(v):,}' for v in occ_df['P_Litre_Ajuste']],
                textposition='outside',
                textfont=dict(color='#e6edf3', size=11),
                marker_color=[ROLE_COLORS[r] for r in occ_df['Role']],
                marker_line=dict(color='#0e1117', width=1),
            ))

        fig.update_layout(
            barmode='group',
            height=420,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#c9d1d9', family='Inter'),
            yaxis=dict(title='Prix / L (Ar)', gridcolor='#21262d', zeroline=False),
            xaxis=dict(title='', gridcolor='#21262d'),
            legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'),
        )
        st.plotly_chart(fig, use_container_width=True)

        view = bsub[['Occ_Group', 'Role', 'Format', 'Volume_L',
                     'PVF_Ajuste', 'P_Litre_Ajuste', 'Index', 'Statut']].copy()
        view.columns = ['Occasion', 'Rôle', 'Format', 'Volume (L)',
                        'PVF ajusté', 'Prix / L', 'Index', 'Statut']
        view['PVF ajusté'] = view['PVF ajusté'].round(0).astype(int)
        view['Prix / L'] = view['Prix / L'].round(0).astype(int)

        st.dataframe(
            view, use_container_width=True, hide_index=True,
            column_config={
                'Volume (L)': st.column_config.NumberColumn(format="%.2f"),
                'PVF ajusté': st.column_config.NumberColumn(format="%d Ar"),
                'Prix / L': st.column_config.NumberColumn(format="%d Ar"),
                'Index': st.column_config.NumberColumn(format="%d"),
            },
        )


# =============================================================================
# TAB 4 — DIAGNOSTIC
# =============================================================================
with tab4:
    st.markdown("#### Diagnostic OBPPC global")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SKU analysés", len(d))
    c2.metric("Conformes", int((d['Statut'] == 'OK').sum()))
    c3.metric("Non conformes", int((d['Statut'] == 'KO').sum()))
    c4.metric("Taux conformité", f"{(d['Statut'] == 'OK').mean() * 100:.0f}%")

    st.markdown("##### Conformité par segment × occasion")
    summary = (
        d.groupby(['Segment', 'Occ_Group'])
        .apply(lambda g: pd.Series({
            'SKU': len(g),
            'Conformes': (g['Statut'] == 'OK').sum(),
            'Taux (%)': round((g['Statut'] == 'OK').mean() * 100, 1),
        }))
        .reset_index()
    )
    st.dataframe(summary, use_container_width=True, hide_index=True)

    st.markdown("##### Positions à réviser")
    ko = d[d['Statut'] == 'KO'].copy()

    if ko.empty:
        st.success("Toutes les positions sont conformes.")
    else:
        def gap(row):
            i, role = row['Index'], row['Role']
            if role == 'Entry':     return max(101 - i, i - 110, 0)
            if role == 'Frequency': return abs(i - 100)
            if role == 'Upsize':    return max(90 - i, i - 99, 0)
            if role == 'Upscale':   return max(111 - i, 0)
            return 0

        ko['Écart'] = ko.apply(gap, axis=1)
        ko = ko.sort_values('Écart', ascending=False)

        out = ko[['Segment', 'Marque', 'Occ_Group', 'Format', 'Role',
                  'P_Litre_Ajuste', 'Index', 'Écart']].copy()
        out.columns = ['Segment', 'Marque', 'Occasion', 'Format', 'Rôle',
                       'Prix / L', 'Index', 'Écart']
        out['Prix / L'] = out['Prix / L'].round(0).astype(int)
        out['Écart'] = out['Écart'].astype(int)

        st.dataframe(
            out, use_container_width=True, hide_index=True,
            column_config={
                'Prix / L': st.column_config.NumberColumn(format="%d Ar"),
                'Index': st.column_config.NumberColumn(format="%d"),
                'Écart': st.column_config.NumberColumn(format="%d pts"),
            },
        )

    st.markdown("##### Export")
    csv = d[['Segment', 'Marque', 'Occ_Group', 'Format', 'Role_OBPPC',
             'Volume_L', 'PVF_Ajuste', 'P_Litre_Ajuste', 'Index', 'Statut']].to_csv(index=False)
    st.download_button(
        "Télécharger (CSV)", data=csv,
        file_name=f"obppc_{channel.split()[0].lower()}.csv",
        mime="text/csv",
    )
