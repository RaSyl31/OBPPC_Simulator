import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Simulateur OBPPC", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main .block-container { padding-top: 1.25rem; max-width: 100%; }
    .obppc-table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
    .obppc-table th {
        background: #161b22; color: #8b949e; padding: 8px 10px;
        font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.05em;
        border: 1px solid #30363d; font-weight: 600; text-align: center;
    }
    .obppc-table td {
        border: 1px solid #30363d; padding: 8px 10px;
        text-align: center; color: #e6edf3; background: #0e1117;
        font-variant-numeric: tabular-nums;
    }
    .obppc-table td.left { text-align: left; }
    .obppc-table td.bold { font-weight: 600; }
    .role-dot { display: inline-block; width: 8px; height: 8px;
                border-radius: 50%; margin-right: 6px; }
    .ok { color: #3fb950; font-weight: 600; }
    .ko { color: #f85149; font-weight: 600; }
    .star-badge {
        display: inline-block; padding: 1px 6px; border-radius: 3px;
        font-size: 0.62rem; font-weight: 600; color: #fff;
    }
    .badge-star { background: #8b5cf6; }
    .badge-comp { background: #484f58; color: #cbd5e1; }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DONNÉES — Uniquement des feuilles visibles
#   Simulateur OBPPC_EAUX / _BG / _ENERGIE / _BI
#   + Feuil1 (STAR - portefeuille et parts de marché)
# =============================================================================

# Marquage STAR vs Concurrents
STAR_BRANDS = {
    # BI (bières STAR)
    'THB', 'Gold', 'Beaufort', 'Fresh', 'Queen',
    # BG (boissons gazeuses STAR)
    'CAPRICE', 'WOCO', 'TONIC',
    # EAUX (eaux STAR)
    'Cristal', 'Eau vive', 'Cristalline', 'RANOVISY', 'VISY GASY',
    'OLYMPIKO', 'NATUR EAU',
    # ENERGIE (STAR)
    'XXL', 'FOSA', 'DYNAMIC', 'BOOST VITALITY',
}
COMPETITOR_BRANDS = {
    'Red Bull', 'Monster',           # ENERGIE import
    'COCA', 'FANTA',                 # Coca-Cola Company
    'Heineken', 'Carlsberg', 'Vody', 'Cody\'s', 'Ivanstoff',
    'Sambo', 'Ambilobe', 'XHUM', 'Shandy', 'Smirnoff Ice',
    'Sprite', 'Pepsi',
}

def brand_type(brand):
    if brand in STAR_BRANDS:    return 'STAR'
    if brand in COMPETITOR_BRANDS: return 'Concurrent'
    return '—'

def brand_badge(brand):
    t = brand_type(brand)
    if t == 'STAR':
        return f'<span class="star-badge badge-star">{brand}</span>'
    if t == 'Concurrent':
        return f'<span class="star-badge badge-comp">{brand}</span>'
    return brand


# -----------------------------------------------------------------------------
# Données OBPPC (feuilles principales)
# -----------------------------------------------------------------------------
DATA = {
    'EAUX': [
        # marque, occasion, rôle, format, vol, PVF_PVC, PVF_PAP
        ('Cristal',     'IC (VER)', 'Entry (Entrée de gamme)', 'Cristal 30 cl VER',       0.30, 1500, 1500),
        ('Eau vive',    'IC (PET)', 'Entry (Entrée de gamme)', 'Eau vive 50 cl PET',      0.50, 1600, 1600),
        ('Cristal',     'IC (VER)', 'Frequency (Cœur de gamme)','Cristal 50 cl VER',      0.50, 2200, 3000),
        ('Cristalline', 'FC (PET)', 'Frequency (Cœur de gamme)','Cristalline 100 cl PET', 1.50, 2100, 2500),
        ('Eau vive',    'FC (PET)', 'Frequency (Cœur de gamme)','Eau vive 150 cl PET',    1.50, 3300, 3300),
        ('Cristalline', 'FC (PET)', 'Upsize (Grand format)',   'Cristalline 200 cl PET', 2.00, 3600, 3800),
        ('Cristal',     'FC (VER)', 'Upscale (Premium)',       'Cristal 100 cl VER',     1.00, 3800, 5000),
        ('Cristal',     'FC (PET)', 'Upscale (Premium)',       'Cristal 150 cl PET',     1.50, 5500, 6500),
    ],
    'BG': [
        ('CAPRICE', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35',  0.35, 1500, 1500),
        ('WOCO',    'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30',   0.30, 1200, 1500),
        ('CAPRICE', 'IC (PET)', 'Frequency (Cœur de gamme)','PET 50', 0.50, 2000, 2000),
        ('WOCO',    'FC (PET)', 'Upsize (Grand format)',   'PET 150', 1.50, 5000, 5000),
        ('CAPRICE', 'FC (VER)', 'Upsize (Grand format)',   'VC 100',  1.00, 3000, 3500),
        ('TONIC',   'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30',   0.30, 1200, 1500),
        ('CAPRICE', 'Upscale',  'Upscale (Premium)',       'CAN 33',  0.33, 2500, 3500),
        ('COCA',    'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35',  0.35, 1500, 1500),
        ('COCA',    'IC (PET)', 'Frequency (Cœur de gamme)','PET 50', 0.50, 2000, 2000),
        ('COCA',    'FC (PET)', 'Upsize (Grand format)',   'PET 150', 1.50, 5000, 5000),
        ('COCA',    'Upscale',  'Upscale (Premium)',       'CAN 33',  0.33, 2500, 3500),
        ('FANTA',   'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35',  0.35, 1500, 1500),
        ('FANTA',   'IC (PET)', 'Frequency (Cœur de gamme)','PET 50', 0.50, 2000, 2000),
        ('FANTA',   'FC (PET)', 'Upsize (Grand format)',   'PET 150', 1.50, 5000, 5000),
    ],
    'ENERGIE': [
        ('XXL', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30',       0.30, 2500, 2500),
        ('XXL', 'IC (PET)', 'Frequency (Cœur de gamme)','PET 35',     0.35, 3500, 3500),
        ('FOSA','Upscale',  'Upscale (Premium)',       'CAN 50',     0.50, 5000, 5000),
        ('XXL', 'Upscale',  'Upscale (Premium)',       'CAN 33',     0.33, 4000, 4000),
        ('DYNAMIC','Upscale','Upscale (Premium)',      'CAN 25',     0.25, 3500, 3500),
        ('BOOST VITALITY','Upscale','Upscale (Premium)','CAN 33',    0.33, 4000, 4000),
        ('Red Bull','Upscale','Upscale (Premium)',     'CAN 25',     0.25, 9900, 9900),
        ('Monster', 'Upscale','Upscale (Premium)',     'CAN 50',     0.50, 9900, 9900),
    ],
    'BI': [
        ('THB',      'IC (VER)', 'Entry (Entrée de gamme)', 'THB Pilsener 33 cl VER', 0.33, 2500, 3000),
        ('Fresh',    'IC (VER)', 'Entry (Entrée de gamme)', 'THB Fresh 33 cl VER',    0.33, 2500, 3000),
        ('Fresh',    'FC (VER)', 'Entry (Entrée de gamme)', 'THB Fresh 65 cl VER',    0.65, 4000, 4000),
        ('Queen',    'FC (VER)', 'Entry (Entrée de gamme)', 'Queen s 65 cl VER',      0.65, 4000, 4000),
        ('THB',      'FC (VER)', 'Frequency (Cœur de gamme)','THB Pilsener 65 cl VER',0.65, 4500, 4500),
        ('Gold',     'FC (VER)', 'Frequency (Cœur de gamme)','Gold Blanche 50 cl VER',0.50, 4500, 4500),
        ('Gold',     'FC (VER)', 'Upsize (Grand format)',   'Gold Blonde 65 cl VER',  0.65, 5000, 5500),
        ('Fresh',    'IC (CAN)', 'Upscale (Premium)',       'FRESH 33 cl CAN',        0.33, 3500, 3500),
        ('Gold',     'IC (VER)', 'Upscale (Premium)',       'Gold Blanche 33cl VER',  0.33, 3500, 3500),
        ('Gold',     'Upscale',  'Upscale (Premium)',       'Gold 8 50 cl VER',       0.50, 4500, 4800),
        ('Gold',     'Upscale',  'Upscale (Premium)',       'Gold Blonde 50 cl VER',  0.50, 4500, 4800),
        ('THB',      'IC (CAN)', 'Upscale (Premium)',       'THB Pilsener 50 cl CAN', 0.50, 5000, 5200),
        ('Beaufort', 'IC (VER)', 'Upscale (Super-Premium Niche)','Beaufort 33CL VER', 0.33, 4000, 4500),
        ('Beaufort', 'IC (CAN)', 'Upscale (Super-Premium Niche)','Beaufort 33 CL CAN',0.33, 5000, 5500),
        ('Gold',     'IC (CAN)', 'Upscale (Premium)',       'Gold 8 50 cl CAN',       0.50, 6000, 6500),
        ('Gold',     'IC (CAN)', 'Upscale (Premium)',       'Gold Blanche 50 cl CAN', 0.50, 6000, 6500),
        ('Gold',     'IC (CAN)', 'Upscale (Premium)',       'Gold Blonde 50 cl CAN',  0.50, 6000, 6500),
    ],
}


# -----------------------------------------------------------------------------
# STAR — portefeuille et parts de marché (extrait de Feuil1, feuille visible)
# -----------------------------------------------------------------------------
STAR_PORTFOLIO = [
    # segment, marque, format, pva, pvc, prix_app, a_minus_1, a, croissance, part
    ('BI', 'THB',   'THB Pilsener 65 cl VER', 3250, 4500, 4500, 213_466_746, 219_943_730, 0.030, 0.642),
    ('BI', 'THB',   'THB Pilsener 50 cl CAN', 3800, 5000, 6000,  10_786_501,  11_382_976, 0.055, 0.033),
    ('BI', 'THB',   'THB Pilsener 33 cl VER', 1900, 2500, 3000,  29_191_830,  28_394_908,-0.027, 0.083),
    ('BI', 'Gold',  'Gold Blanche 50 cl VER', 3200, 4500, 4500,  11_016_701,  15_245_244, 0.384, 0.044),
    ('BI', 'Gold',  'Gold Blonde 50 cl VER',  3200, 4500, 4500,   2_771_831,   2_920_944, 0.054, 0.009),
    ('BI', 'Gold',  'Gold 8 50 cl VER',       3200, 4500, 4500,   1_813_520,   1_682_704,-0.072, 0.005),
    ('BI', 'Gold',  'Gold Blonde 65 cl VER',  3600, 5000, 5500,   6_020_685,   7_740_173, 0.286, 0.023),
    ('BI', 'Gold',  'Gold Blanche 33cl VER',  2580, 3500, 3500,   8_865_161,   7_551_006,-0.148, 0.022),
    ('BI', 'Gold',  'Gold 8 50 cl CAN',       4500, 6000, 6000,     253_726,     245_375,-0.033, 0.001),
    ('BI', 'Gold',  'Gold Blanche 50 cl CAN', 4500, 6000, 6000,   6_651_989,   7_601_335, 0.143, 0.022),
    ('BI', 'Gold',  'Gold Blonde 50 cl CAN',  4500, 6000, 6000,   1_550_510,   1_586_837, 0.023, 0.005),
    ('BI', 'Fresh', 'THB Fresh 65 cl VER',    3000, 4000, 4000,   6_422_752,   5_393_010,-0.160, 0.016),
    ('BI', 'Fresh', 'THB Fresh 33 cl VER',    1900, 2500, 3000,   1_232_031,     653_514,-0.470, 0.002),
    ('BI', 'Fresh', 'FRESH 33 cl CAN',        2650, 3500, 3500,           0,     382_056, None,  0.001),
    ('BI', 'Queen', 'Queen s 65 cl VER',      3000, 4000, 4000,  19_159_787,  20_770_151, 0.084, 0.061),
    ('BI', 'Beaufort','Beaufort 33CL VER',    2900, 4000, 4000,   8_847_629,   9_752_382, 0.102, 0.028),
    ('BI', 'Beaufort','Beaufort 33 CL CAN',   3800, 5000, 6000,           0,   1_324_817, None,  0.004),
]


# =============================================================================
# Helpers
# =============================================================================
ROLE_COLORS = {'Entry': '#58a6ff', 'Frequency': '#3fb950',
               'Upsize': '#d29922', 'Upscale': '#bc8cff'}
ROLE_ORDER  = ['Entry', 'Frequency', 'Upsize', 'Upscale']
ROLE_TARGET = {'Entry': '101–110', 'Frequency': '100',
               'Upsize': '90–99', 'Upscale': '≥ 111'}
OBJECTIFS = {
    'Entry':     'Recrutement, accessibilité prix, achat d\'impulsion',
    'Frequency': 'RÉFÉRENCE (Index 100) — Rotation quotidienne',
    'Upsize':    'Volume, consommation à domicile, meilleur P/L',
    'Upscale':   'Valorisation, image de marque, forte marge',
}

def simple_role(r):
    if r.startswith('Upscale'):   return 'Upscale'
    if r.startswith('Entry'):     return 'Entry'
    if r.startswith('Frequency'): return 'Frequency'
    if r.startswith('Upsize'):    return 'Upsize'
    return 'Autre'

def check_status(idx, role):
    if role == 'Entry':     return 'OK' if 101 <= idx <= 110 else 'KO'
    if role == 'Frequency': return 'OK' if idx == 100 else 'KO'
    if role == 'Upsize':    return 'OK' if 90 <= idx <= 99 else 'KO'
    if role == 'Upscale':   return 'OK' if idx >= 111 else 'KO'
    return '—'

def build_df(category, view='PVC'):
    rows = []
    for brand, occ, role, fmt, vol, pvf_pvc, pvf_pap in DATA[category]:
        pvf = pvf_pvc if view == 'PVC' else pvf_pap
        rows.append({
            'marque': brand, 'type': brand_type(brand),
            'occasion': occ, 'role': role, 'format': fmt,
            'vol': vol, 'pvf': pvf,
        })
    df = pd.DataFrame(rows)
    df['role_simple'] = df['role'].apply(simple_role)
    df['p_litre'] = df['pvf'] / df['vol']
    return df


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### Simulateur OBPPC")
    st.caption("Occasion · Brand · Package · Price · Channel")
    st.markdown("---")

    category = st.selectbox("Catégorie", ['EAUX', 'BG', 'ENERGIE', 'BI'])
    view_label = st.radio("Vue",
                          ['PVC — Prix Consommateur', 'PAP — Prix Achat Produit'],
                          key='view')
    view = 'PVC' if view_label.startswith('PVC') else 'PAP'

    st.markdown("---")
    st.markdown("##### Cibles d'index P/L")
    for r in ROLE_ORDER:
        st.markdown(
            f"<div style='font-size:0.75rem; color:#cbd5e1; margin-bottom:4px;'>"
            f"<span class='role-dot' style='background:{ROLE_COLORS[r]};'></span>"
            f"<b>{r}</b> — {ROLE_TARGET[r]}</div>",
            unsafe_allow_html=True)


# =============================================================================
# HEADER
# =============================================================================
st.markdown(f"## Simulateur OBPPC — {category} · {view}")
st.caption("Édition directe des prix. Référence = produit **Frequency** (Index 100). "
           "Portefeuille **STAR** vs **Concurrents** identifié par badge.")


# =============================================================================
# ONGLETS
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Simulateur", "Portefeuille STAR", "STAR vs Concurrents", "Diagnostic",
])


# -----------------------------------------------------------------------------
# TAB 1 — SIMULATEUR
# -----------------------------------------------------------------------------
with tab1:
    base = build_df(category, view)

    st.markdown("### Éditeur de prix")
    st.caption("Modifiez les PVF ou volumes — tous les calculs se recalculent.")

    editor_in = base[['marque', 'type', 'role', 'format', 'vol', 'pvf']].copy()

    edited = st.data_editor(
        editor_in,
        column_config={
            "marque": st.column_config.TextColumn("Marque", disabled=True, width="small"),
            "type": st.column_config.TextColumn("Type", disabled=True, width="small"),
            "role": st.column_config.SelectboxColumn(
                "Rôle OBPPC",
                options=['Entry (Entrée de gamme)', 'Frequency (Cœur de gamme)',
                         'Upsize (Grand format)', 'Upscale (Premium)',
                         'Upscale (Super-Premium Niche)'],
                required=True, width="medium"),
            "format": st.column_config.TextColumn("Format", disabled=True, width="medium"),
            "vol": st.column_config.NumberColumn(
                "Volume (L)", min_value=0.05, step=0.05, format="%.2f", width="small"),
            "pvf": st.column_config.NumberColumn(
                "PVF (Ar)", min_value=0, step=100, format="%d", width="medium"),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        height=min(600, 80 + 36 * len(editor_in)),
        key=f"editor_{category}_{view}",
    )

    # Recalcul
    d = edited.copy()
    d['role_simple'] = d['role'].apply(simple_role)
    d['p_litre'] = d['pvf'] / d['vol']

    freq = d[(d['role_simple'] == 'Frequency') & (d['type'] == 'STAR')]
    if freq.empty:
        freq = d[d['role_simple'] == 'Frequency']

    base_pl = freq['p_litre'].mean() if not freq.empty else d['p_litre'].mean()
    base_pvf = freq['pvf'].mean() if not freq.empty else d['pvf'].mean()

    d['idx_pvf'] = (d['pvf'] / base_pvf * 100).round(0).astype(int)
    d['idx_pl']  = (d['p_litre'] / base_pl * 100).round(0).astype(int)
    d['statut']  = d.apply(lambda r: check_status(r['idx_pl'], r['role_simple']), axis=1)

    st.markdown(f"### Tableau OBPPC complet")
    st.caption(f"Référence Frequency : **{base_pvf:,.0f} Ar** · **{base_pl:,.0f} Ar/L**")

    html = ['<table class="obppc-table"><thead><tr>',
            '<th>Marque</th><th>Type</th><th>Rôle OBPPC</th><th>Format</th>',
            '<th>Vol (L)</th><th>PVF (Ar)</th><th>Prix / L</th>',
            '<th>Idx PVF</th><th>Idx P/L</th><th>Cible</th><th>Statut</th></tr></thead><tbody>']

    for _, row in d.iterrows():
        color = ROLE_COLORS[row['role_simple']]
        statut_cls = 'ok' if row['statut'] == 'OK' else 'ko' if row['statut'] == 'KO' else ''
        statut_txt = '● OK' if row['statut'] == 'OK' else '● KO' if row['statut'] == 'KO' else '—'
        html.append(
            f'<tr>'
            f'<td class="left">{brand_badge(row["marque"])}</td>'
            f'<td>{row["type"]}</td>'
            f'<td class="left"><span class="role-dot" style="background:{color};"></span>{row["role"]}</td>'
            f'<td class="left">{row["format"]}</td>'
            f'<td>{row["vol"]:.2f}</td>'
            f'<td class="bold">{int(row["pvf"]):,}</td>'
            f'<td>{int(row["p_litre"]):,}</td>'
            f'<td>{row["idx_pvf"]}</td>'
            f'<td>{row["idx_pl"]}</td>'
            f'<td>{ROLE_TARGET[row["role_simple"]]}</td>'
            f'<td class="{statut_cls}">{statut_txt}</td>'
            f'</tr>'
        )
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)

    export = d[['marque', 'type', 'role', 'format', 'vol', 'pvf', 'p_litre',
                'idx_pvf', 'idx_pl', 'statut']].copy()
    export.columns = ['Marque', 'Type', 'Rôle OBPPC', 'Format', 'Volume (L)',
                      'PVF (Ar)', 'Prix / L', 'Idx PVF', 'Idx P/L', 'Statut']
    st.download_button(
        "Télécharger (CSV)",
        data=export.to_csv(index=False).encode('utf-8'),
        file_name=f"obppc_{category.lower()}_{view.lower()}.csv",
        mime="text/csv",
    )


# -----------------------------------------------------------------------------
# TAB 2 — PORTEFEUILLE STAR
# -----------------------------------------------------------------------------
with tab2:
    st.markdown("### Portefeuille STAR")
    st.caption("Performance du portefeuille STAR (feuille de référence).")

    star_df = pd.DataFrame(STAR_PORTFOLIO,
        columns=['Segment', 'Marque', 'Format', 'PVA', 'PVC', 'Prix_App',
                 'A_minus_1', 'A', 'Croissance', 'Part'])

    # KPI globaux
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SKU STAR", len(star_df))
    c2.metric("CA Année A", f"{star_df['A'].sum()/1e6:,.1f} M")
    c3.metric("Croissance moy.", f"{star_df['Croissance'].dropna().mean()*100:.1f}%")
    c4.metric("Part de marché cumulée", f"{star_df['Part'].sum()*100:.1f}%")

    st.markdown("##### Détail par SKU")
    view_df = star_df.copy()
    view_df['A_minus_1'] = (view_df['A_minus_1']/1e6).round(1)
    view_df['A'] = (view_df['A']/1e6).round(1)
    view_df['Croissance'] = view_df['Croissance'].apply(
        lambda x: f"{x*100:+.1f}%" if pd.notna(x) else '—')
    view_df['Part'] = view_df['Part'].apply(lambda x: f"{x*100:.2f}%")
    view_df.columns = ['Segment', 'Marque', 'Format', 'PVA', 'PVC', 'Prix App',
                       'A-1 (M)', 'A (M)', 'Croissance', 'Part marché']

    st.dataframe(view_df, use_container_width=True, hide_index=True,
                 column_config={
                     'PVA': st.column_config.NumberColumn(format="%d Ar"),
                     'PVC': st.column_config.NumberColumn(format="%d Ar"),
                     'Prix App': st.column_config.NumberColumn(format="%d Ar"),
                 })

    # Croissance par marque
    st.markdown("##### Croissance par marque")
    brand_agg = star_df.groupby('Marque').agg(
        ca_a=('A', 'sum'),
        ca_a1=('A_minus_1', 'sum'),
    )
    brand_agg['croissance'] = (brand_agg['ca_a'] / brand_agg['ca_a1'] - 1) * 100
    brand_agg = brand_agg.sort_values('ca_a', ascending=True)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=brand_agg.index,
        x=brand_agg['croissance'],
        orientation='h',
        text=[f"{v:+.1f}%" for v in brand_agg['croissance']],
        textposition='outside',
        textfont=dict(color='#e6edf3', size=11),
        marker_color=['#3fb950' if v >= 0 else '#f85149' for v in brand_agg['croissance']],
        marker_line=dict(color='#0e1117', width=1),
    ))
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=40, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1', family='Inter'),
        xaxis=dict(title='Croissance (%)', gridcolor='#21262d', zeroline=True,
                   zerolinecolor='#484f58'),
        yaxis=dict(title='', gridcolor='#21262d'),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


# -----------------------------------------------------------------------------
# TAB 3 — STAR vs CONCURRENTS
# -----------------------------------------------------------------------------
with tab3:
    st.markdown("### STAR vs Concurrents")
    st.caption("Comparaison par segment et par rôle OBPPC.")

    base = build_df(category, view)
    base['role_simple'] = base['role'].apply(simple_role)
    base['p_litre'] = base['pvf'] / base['vol']

    # Référence : Frequency STAR
    star_freq = base[(base['type'] == 'STAR') & (base['role_simple'] == 'Frequency')]
    if star_freq.empty:
        star_freq = base[base['role_simple'] == 'Frequency']
    ref_pl = star_freq['p_litre'].mean() if not star_freq.empty else base['p_litre'].mean()

    base['idx_pl'] = (base['p_litre'] / ref_pl * 100).round(0).astype(int)

    # KPIs
    star_count = (base['type'] == 'STAR').sum()
    comp_count = (base['type'] == 'Concurrent').sum()
    star_pl = base[base['type'] == 'STAR']['p_litre'].mean()
    comp_pl = base[base['type'] == 'Concurrent']['p_litre'].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SKU STAR", star_count)
    c2.metric("SKU Concurrents", comp_count)
    c3.metric("Prix/L STAR moyen", f"{star_pl:,.0f} Ar" if pd.notna(star_pl) else "—")
    c4.metric("Prix/L Concur. moyen", f"{comp_pl:,.0f} Ar" if pd.notna(comp_pl) else "—")

    # Graphique comparatif par rôle
    st.markdown("##### Prix au litre moyen par rôle — STAR vs Concurrents")

    comp_agg = base.groupby(['role_simple', 'type'])['p_litre'].mean().reset_index()
    roles_present = [r for r in ROLE_ORDER if r in comp_agg['role_simple'].unique()]

    fig = go.Figure()
    for typ, color in [('STAR', '#8b5cf6'), ('Concurrent', '#484f58')]:
        sub = comp_agg[comp_agg['type'] == typ]
        if sub.empty:
            continue
        fig.add_trace(go.Bar(
            name=typ,
            x=sub['role_simple'],
            y=sub['p_litre'],
            text=[f"{v:,.0f}" for v in sub['p_litre']],
            textposition='outside',
            textfont=dict(color='#e6edf3', size=11),
            marker_color=color,
            marker_line=dict(color='#0e1117', width=1),
        ))
    fig.update_layout(
        barmode='group',
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#cbd5e1', family='Inter'),
        yaxis=dict(title='Prix / L (Ar)', gridcolor='#21262d'),
        xaxis=dict(title='', gridcolor='#21262d'),
        legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Tableau détaillé par marque
    st.markdown("##### Récapitulatif par marque")

    brand_agg = base.groupby(['type', 'marque']).agg(
        sku=('format', 'count'),
        pl_moyen=('p_litre', 'mean'),
        pl_min=('p_litre', 'min'),
        pl_max=('p_litre', 'max'),
        roles=('role_simple', lambda x: ', '.join(sorted(set(x)))),
    ).reset_index().sort_values(['type', 'marque'])

    brand_agg['pl_moyen'] = brand_agg['pl_moyen'].round(0).astype(int)
    brand_agg['pl_min'] = brand_agg['pl_min'].round(0).astype(int)
    brand_agg['pl_max'] = brand_agg['pl_max'].round(0).astype(int)

    disp = brand_agg.copy()
    disp.columns = ['Type', 'Marque', 'SKU', 'P/L moyen', 'P/L min', 'P/L max', 'Rôles couverts']

    st.dataframe(
        disp,
        use_container_width=True,
        hide_index=True,
        column_config={
            'P/L moyen': st.column_config.NumberColumn(format="%d Ar"),
            'P/L min':   st.column_config.NumberColumn(format="%d Ar"),
            'P/L max':   st.column_config.NumberColumn(format="%d Ar"),
        })

    # Alertes d'écart
    st.markdown("##### Écarts concurrentiels")
    st.caption("Comparaison de positionnement tarifaire entre STAR et Concurrents.")

    for role in roles_present:
        sub = base[base['role_simple'] == role]
        s = sub[sub['type'] == 'STAR']['p_litre'].mean()
        c = sub[sub['type'] == 'Concurrent']['p_litre'].mean()
        if pd.isna(s) or pd.isna(c):
            continue
        ecart = (s - c) / c * 100
        color = '#f85149' if ecart > 15 else '#d29922' if ecart > 5 else '#3fb950'
        sign = 'plus cher' if ecart > 0 else 'moins cher'
        st.markdown(
            f"<div style='padding:8px 12px; background:#161b22; "
            f"border-left:3px solid {color}; border-radius:6px; margin-bottom:6px;'>"
            f"<b style='color:#e6edf3;'>{role}</b> — "
            f"STAR est <span style='color:{color}; font-weight:600;'>"
            f"{abs(ecart):.0f}% {sign}</span> que la concurrence "
            f"<span style='color:#8b949e; font-size:0.8rem;'>"
            f"(STAR {s:,.0f} vs Concur. {c:,.0f} Ar/L)</span>"
            f"</div>",
            unsafe_allow_html=True)


# -----------------------------------------------------------------------------
# TAB 4 — DIAGNOSTIC
# -----------------------------------------------------------------------------
with tab4:
    st.markdown("### Diagnostic de conformité OBPPC")

    base = build_df(category, view)
    base['role_simple'] = base['role'].apply(simple_role)
    base['p_litre'] = base['pvf'] / base['vol']

    freq = base[(base['type'] == 'STAR') & (base['role_simple'] == 'Frequency')]
    if freq.empty:
        freq = base[base['role_simple'] == 'Frequency']
    ref_pl = freq['p_litre'].mean() if not freq.empty else base['p_litre'].mean()

    base['idx_pl'] = (base['p_litre'] / ref_pl * 100).round(0).astype(int)
    base['statut'] = base.apply(lambda r: check_status(r['idx_pl'], r['role_simple']), axis=1)

    # Filtre STAR uniquement pour le diagnostic
    star_only = st.checkbox("Diagnostic STAR uniquement", value=True)
    d = base[base['type'] == 'STAR'] if star_only else base

    n_total = len(d)
    n_ok = (d['statut'] == 'OK').sum()
    n_ko = n_total - n_ok
    taux = n_ok / n_total * 100 if n_total else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SKU analysés", n_total)
    c2.metric("Conformes", n_ok)
    c3.metric("Non conformes", n_ko)
    c4.metric("Taux conformité", f"{taux:.0f}%")

    st.markdown("##### Conformité par rôle")
    for role in [r for r in ROLE_ORDER if r in d['role_simple'].unique()]:
        sub = d[d['role_simple'] == role]
        ok = (sub['statut'] == 'OK').sum()
        pct = ok / len(sub) * 100 if len(sub) else 0
        color = '#3fb950' if pct >= 70 else '#d29922' if pct >= 40 else '#f85149'
        st.markdown(
            f"<div style='display:flex; align-items:center; gap:1rem; margin-bottom:6px;'>"
            f"<div style='width:120px; font-size:0.82rem; color:#e6edf3; font-weight:500;'>"
            f"<span class='role-dot' style='background:{ROLE_COLORS[role]};'></span>{role}</div>"
            f"<div style='flex:1; height:16px; background:#161b22; border-radius:4px; overflow:hidden;'>"
            f"<div style='height:100%; width:{pct:.0f}%; background:{color}; opacity:0.85;'></div></div>"
            f"<div style='width:150px; text-align:right; font-size:0.75rem; color:#8b949e; "
            f"font-variant-numeric:tabular-nums;'>"
            f"<span style='color:{color}; font-weight:600;'>{pct:.0f}%</span> · {ok}/{len(sub)}</div>"
            f"</div>",
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("##### Positions à réviser")
    ko = d[d['statut'] == 'KO'].copy()

    if ko.empty:
        st.success("Toutes les positions respectent la cible OBPPC.")
    else:
        def ecart(row):
            i, r = row['idx_pl'], row['role_simple']
            if r == 'Entry':     return max(101 - i, i - 110, 0)
            if r == 'Frequency': return abs(i - 100)
            if r == 'Upsize':    return max(90 - i, i - 99, 0)
            if r == 'Upscale':   return max(111 - i, 0)
            return 0
        ko['ecart'] = ko.apply(ecart, axis=1)
        ko = ko.sort_values('ecart', ascending=False)

        view_ko = ko[['marque', 'type', 'role', 'format', 'vol', 'pvf',
                      'p_litre', 'idx_pl', 'ecart']].copy()
        view_ko.columns = ['Marque', 'Type', 'Rôle', 'Format', 'Vol (L)',
                           'PVF (Ar)', 'P/L (Ar)', 'Idx P/L', 'Écart']
        view_ko['Vol (L)'] = view_ko['Vol (L)'].round(2)
        view_ko['PVF (Ar)'] = view_ko['PVF (Ar)'].astype(int)
        view_ko['P/L (Ar)'] = view_ko['P/L (Ar)'].round(0).astype(int)
        st.dataframe(view_ko, use_container_width=True, hide_index=True,
                     column_config={
                         'Vol (L)': st.column_config.NumberColumn(format="%.2f"),
                         'PVF (Ar)': st.column_config.NumberColumn(format="%d"),
                         'P/L (Ar)': st.column_config.NumberColumn(format="%d"),
                         'Idx P/L': st.column_config.NumberColumn(format="%d"),
                         'Écart': st.column_config.NumberColumn(format="%d"),
                     })

    st.markdown("---")
    if taux >= 80:
        st.success(f"**Cohérence élevée** — {n_ok}/{n_total} SKU conformes ({taux:.0f}%).")
    elif taux >= 50:
        st.warning(f"**Cohérence partielle** — {n_ok}/{n_total} SKU conformes ({taux:.0f}%).")
    else:
        st.error(f"**Cohérence faible** — {n_ok}/{n_total} SKU conformes ({taux:.0f}%).")
