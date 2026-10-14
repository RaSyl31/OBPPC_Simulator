import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="OBPPC", layout="wide", initial_sidebar_state="expanded")

# -----------------------------------------------------------------------------
# CSS — thème dark soft, polices lisibles
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        font-size: 14px;
        color: #e3e8ef;
    }
    .main .block-container { padding-top: 1.25rem; max-width: 100%; }
    h1, h2, h3, h4 { color: #f1f5f9; font-weight: 600; letter-spacing: -0.01em; }

    /* ---------- Tableau générique ---------- */
    .obppc-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        font-size: 0.82rem;
        border: 1px solid #2c3340;
        border-radius: 8px;
        overflow: hidden;
    }
    .obppc-table th {
        background: #232934;
        color: #94a3b8;
        padding: 10px 12px;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 600;
        text-align: center;
        border-bottom: 1px solid #2c3340;
    }
    .obppc-table th.row-head {
        text-align: left;
        min-width: 130px;
    }
    .obppc-table td {
        padding: 10px 12px;
        text-align: center;
        color: #e3e8ef;
        background: #1c212b;
        border-bottom: 1px solid #262c37;
        vertical-align: top;
    }
    .obppc-table td.row-head {
        text-align: left;
        font-weight: 600;
        color: #f1f5f9;
        background: #21262f;
        border-right: 1px solid #2c3340;
    }
    .obppc-table tr:last-child td { border-bottom: none; }
    .obppc-table td.empty { color: #48505f; font-style: italic; }

    /* ---------- Liste d'articles dans une cellule ---------- */
    .art-list {
        display: flex;
        flex-direction: column;
        gap: 3px;
        align-items: flex-start;
        text-align: left;
    }
    .art-item {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 4px;
        font-size: 0.72rem;
        font-weight: 500;
        background: rgba(255,255,255,0.04);
        border-left: 2px solid var(--c, #64748b);
        color: #e3e8ef;
        white-space: nowrap;
    }
    .art-item .idx {
        color: #94a3b8;
        font-size: 0.65rem;
        margin-left: 4px;
        font-weight: 400;
    }

    /* ---------- Matrice (cellules compactes) ---------- */
    .matrix-cell {
        font-weight: 600;
        font-size: 0.85rem;
        color: #f1f5f9;
    }
    .matrix-idx {
        font-size: 0.68rem;
        color: #94a3b8;
        margin-left: 4px;
        font-weight: 400;
    }
    .warn-mark { color: #f0883e; margin-left: 3px; font-weight: 700; }
    .ok-mark   { color: #4ade80; margin-left: 3px; font-weight: 700; }

    /* ---------- Légende ---------- */
    .legend { display: flex; gap: 1rem; margin: 0.75rem 0 1rem 0; flex-wrap: wrap; }
    .legend-item {
        display: flex; align-items: center; gap: 0.4rem;
        font-size: 0.75rem; color: #cbd5e1;
    }
    .legend-swatch { width: 10px; height: 10px; border-radius: 2px; }

    /* ---------- Couverture ---------- */
    .cov-pill {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 600;
    }

    /* ---------- Badge count ---------- */
    .count-badge {
        display: inline-block;
        min-width: 18px;
        padding: 1px 6px;
        border-radius: 8px;
        font-size: 0.68rem;
        font-weight: 600;
        background: rgba(255,255,255,0.06);
        color: #cbd5e1;
        margin-bottom: 4px;
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

    def occ_group(o):
        if o.startswith('IC'): return 'IC (Immédiate)'
        if o.startswith('FC'): return 'FC (Future)'
        return 'Hors occasion'
    df['Occ_Group'] = df['Occasion'].apply(occ_group)
    df['_id'] = range(len(df))
    return df


BASE = load_data()
ALL_SEGMENTS = sorted(BASE['Segment'].unique())

ROLE_SIMPLE = {
    'Entry (Entrée de gamme)': 'Entry',
    'Frequency (Cœur de gamme)': 'Frequency',
    'Upsize (Grand format)': 'Upsize',
    'Upscale (Premium)': 'Upscale',
    'Upscale (Super-Premium Niche)': 'Upscale',
}
ROLE_COLORS = {
    'Entry':     '#58a6ff',
    'Frequency': '#3fb950',
    'Upsize':    '#d29922',
    'Upscale':   '#bc8cff',
}
ROLE_TARGET = {'Entry': '101–110', 'Frequency': '100', 'Upsize': '90–99', 'Upscale': '≥111'}
ROLE_OPTIONS = ['Entry (Entrée de gamme)', 'Frequency (Cœur de gamme)',
                'Upsize (Grand format)', 'Upscale (Premium)',
                'Upscale (Super-Premium Niche)']


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
        sorted(BASE[BASE['Segment'].isin(segments)]['Marque'].unique())
        if segments else []
    )
    brands = st.multiselect("Marques", available_brands, default=available_brands)

    st.markdown("---")
    channel = st.radio("Canal", ["GMS", "Horeca (+35%)", "Traditionnel (+15%)"])
    coef = {"GMS": 1.00, "Horeca (+35%)": 1.35, "Traditionnel (+15%)": 1.15}[channel]

    st.markdown("---")
    if st.button("Réinitialiser les prix", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith("price_editor") or k == "editor_reset":
                del st.session_state[k]
        st.rerun()

    st.markdown("---")
    st.caption(
        "**Cibles index prix/litre**  \n"
        f"<span style='color:{ROLE_COLORS['Entry']}'>■</span> Entry — 101–110  \n"
        f"<span style='color:{ROLE_COLORS['Frequency']}'>■</span> Frequency — 100  \n"
        f"<span style='color:{ROLE_COLORS['Upsize']}'>■</span> Upsize — 90–99  \n"
        f"<span style='color:{ROLE_COLORS['Upscale']}'>■</span> Upscale — ≥111",
        unsafe_allow_html=True,
    )


# -----------------------------------------------------------------------------
# Filtrage
# -----------------------------------------------------------------------------
d_base = BASE[(BASE['Segment'].isin(segments)) & (BASE['Marque'].isin(brands))].copy()

if d_base.empty:
    st.warning("Sélectionnez au moins un segment et une marque.")
    st.stop()


# =============================================================================
# ÉDITEUR DE PRIX
# =============================================================================
st.markdown("## Éditeur de prix")
st.caption("Modifiez les PVF ou volumes — index, matrice et diagnostic se recalculent automatiquement.")

editor_df = d_base[['_id', 'Segment', 'Marque', 'Occasion', 'Role_OBPPC',
                    'Format', 'Volume_L', 'PVF_Ar']].copy()

edited = st.data_editor(
    editor_df,
    column_config={
        "_id": None,
        "Segment": st.column_config.TextColumn("Segment", disabled=True, width="small"),
        "Marque": st.column_config.TextColumn("Marque", disabled=True, width="small"),
        "Occasion": st.column_config.TextColumn("Occasion", disabled=True, width="small"),
        "Role_OBPPC": st.column_config.SelectboxColumn(
            "Rôle OBPPC", options=ROLE_OPTIONS, required=True, width="medium"),
        "Format": st.column_config.TextColumn("Format", disabled=True, width="medium"),
        "Volume_L": st.column_config.NumberColumn(
            "Volume (L)", min_value=0.05, step=0.05, format="%.2f", width="small"),
        "PVF_Ar": st.column_config.NumberColumn(
            "PVF (Ar)", min_value=0, step=100, format="%d", width="medium"),
    },
    hide_index=True,
    use_container_width=True,
    num_rows="fixed",
    height=min(500, 80 + 35 * len(editor_df)),
    key="price_editor",
)

# --- Recalcul complet
d = edited.copy()
d['P_Litre'] = d['PVF_Ar'] / d['Volume_L']
d['PVF_Ajuste'] = d['PVF_Ar'] * coef
d['P_Litre_Ajuste'] = d['P_Litre'] * coef
d['Role'] = d['Role_OBPPC'].map(ROLE_SIMPLE)

def occ_group(o):
    if str(o).startswith('IC'): return 'IC (Immédiate)'
    if str(o).startswith('FC'): return 'FC (Future)'
    return 'Hors occasion'
d['Occ_Group'] = d['Occasion'].apply(occ_group)

ref = d[d['Role'] == 'Frequency'].groupby(['Segment', 'Occ_Group'])['P_Litre_Ajuste'].mean()
d['Ref_Litre'] = d.set_index(['Segment', 'Occ_Group']).index.map(ref)
d['Ref_Litre'] = d['Ref_Litre'].fillna(
    d.groupby(['Segment', 'Occ_Group'])['P_Litre_Ajuste'].transform('mean')
)
d['Index'] = (d['P_Litre_Ajuste'] / d['Ref_Litre'] * 100).round(0).astype(int)
d['Statut'] = d.apply(lambda r: status(r['Index'], r['Role']), axis=1)

n_ok = int((d['Statut'] == 'OK').sum())
n_total = len(d)
taux = n_ok / n_total * 100 if n_total else 0
color = '#4ade80' if taux >= 80 else '#fbbf24' if taux >= 50 else '#f87171'
st.markdown(
    f"<div style='padding:8px 14px; background:#222732; border:1px solid #2c3340; "
    f"border-left:3px solid {color}; border-radius:6px; margin-top:0.5rem; "
    f"font-size:0.82rem;'>"
    f"<span style='color:#94a3b8; font-size:0.7rem; text-transform:uppercase; "
    f"letter-spacing:0.08em; font-weight:600;'>Conformité OBPPC</span>"
    f"<span style='color:{color}; font-weight:700; margin-left:10px;'>"
    f"{n_ok} / {n_total} &nbsp;·&nbsp; {taux:.0f}%</span>"
    f"</div>",
    unsafe_allow_html=True,
)


# =============================================================================
# Onglets
# =============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Matrice OBPPC", "Couverture des rôles", "Échelle de prix", "Diagnostic",
])


# =============================================================================
# TAB 1 — MATRICE
# =============================================================================
with tab1:
    seg_choice = st.selectbox("Segment", sorted(d['Segment'].unique()), key="t1_seg")
    sub = d[d['Segment'] == seg_choice].copy()
    sub['Occ_Order'] = sub['Occ_Group'].map(
        {'IC (Immédiate)': 0, 'FC (Future)': 1, 'Hors occasion': 2}
    )
    sub = sub.sort_values(['Occ_Order', 'Volume_L'])
    cols = sorted(sub['Format'].unique(),
                  key=lambda f: (sub[sub['Format'] == f]['Occ_Order'].iloc[0],
                                 sub[sub['Format'] == f]['Volume_L'].iloc[0]))
    brands_in = sorted(sub['Marque'].unique())

    html = ['<table class="obppc-table"><thead><tr><th class="row-head">Marque</th>']
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
                warn = '' if row['Statut'] == 'OK' else '<span class="warn-mark">⚠</span>'
                html.append(
                    f'<td style="border-left:3px solid {color};">'
                    f'<span class="matrix-cell">{int(row["PVF_Ajuste"]):,}</span>'
                    f'<span class="matrix-idx">·{row["Index"]}</span>{warn}'
                    f'</td>'
                )
        html.append('</tr>')
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)

    st.markdown(
        '<div class="legend">'
        + ''.join([
            f'<div class="legend-item">'
            f'<span class="legend-swatch" style="background:{c};"></span>'
            f'{r} (cible {ROLE_TARGET[r]})</div>'
            for r, c in ROLE_COLORS.items()
        ])
        + '</div>',
        unsafe_allow_html=True,
    )


# =============================================================================
# TAB 2 — COUVERTURE (LISTE DES ARTICLES)
# =============================================================================
with tab2:
    st.markdown("#### Couverture des rôles par marque")
    st.caption("Chaque cellule liste les articles (formats) qui occupent ce rôle sur l'occasion sélectionnée.")

    occ_choice = st.radio(
        "Occasion", ['IC (Immédiate)', 'FC (Future)', 'Hors occasion'],
        horizontal=True, key="t2_occ",
    )
    sub2 = d[d['Occ_Group'] == occ_choice]

    if sub2.empty:
        st.info("Aucun SKU sur cette occasion.")
    else:
        brands_in = sorted(sub2['Marque'].unique())
        roles_cols = ['Entry', 'Frequency', 'Upsize', 'Upscale']

        html = ['<table class="obppc-table"><thead><tr>'
                '<th class="row-head">Marque</th>'
                '<th>Entry</th><th>Frequency</th><th>Upsize</th><th>Upscale</th>'
                '<th style="min-width:80px;">Couverture</th></tr></thead><tbody>']

        for brand in brands_in:
            bsub = sub2[sub2['Marque'] == brand]
            html.append(f'<tr><td class="row-head">{brand}</td>')

            covered_roles = 0
            for role in roles_cols:
                rsub = bsub[bsub['Role'] == role]
                if rsub.empty:
                    html.append('<td class="empty">—</td>')
                else:
                    covered_roles += 1
                    color = ROLE_COLORS[role]
                    # Construire la liste des articles
                    items = []
                    for _, art in rsub.iterrows():
                        items.append(
                            f'<span class="art-item" style="--c:{color};">'
                            f'{art["Format"]}'
                            f'<span class="idx">{int(art["P_Litre_Ajuste"]):,} Ar/L</span>'
                            f'</span>'
                        )
                    html.append(
                        f'<td><div class="art-list">'
                        f'<span class="count-badge">{len(rsub)}</span>'
                        + ''.join(items) +
                        '</div></td>'
                    )

            # Couverture
            cov_color = '#4ade80' if covered_roles >= 3 else '#fbbf24' if covered_roles == 2 else '#f87171'
            html.append(
                f'<td><span class="cov-pill" style="background:{cov_color}22; '
                f'color:{cov_color};">{covered_roles}/4</span></td>'
            )
            html.append('</tr>')

        html.append('</tbody></table>')
        st.markdown(''.join(html), unsafe_allow_html=True)

        # Lacunes
        st.markdown("##### Lacunes détectées")
        any_gap = False
        for brand in brands_in:
            bsub = sub2[sub2['Marque'] == brand]
            gaps = [r for r in ['Entry', 'Frequency'] if bsub[bsub['Role'] == r].empty]
            if gaps:
                any_gap = True
                st.warning(f"**{brand}** — rôle(s) manquant(s) : {', '.join(gaps)}")
        if not any_gap:
            st.success("Toutes les marques couvrent Entry et Frequency sur cette occasion.")


# =============================================================================
# TAB 3 — ÉCHELLE DE PRIX
# =============================================================================
with tab3:
    st.markdown("#### Échelle de prix par marque")

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
                x=occ_df['Role'], y=occ_df['P_Litre_Ajuste'], name=occ,
                text=[f'{int(v):,}' for v in occ_df['P_Litre_Ajuste']],
                textposition='outside', textfont=dict(color='#e3e8ef', size=11),
                marker_color=[ROLE_COLORS[r] for r in occ_df['Role']],
                marker_line=dict(color='#181c24', width=1),
            ))
        fig.update_layout(
            barmode='group', height=420,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cbd5e1', family='Inter'),
            yaxis=dict(title='Prix / L (Ar)', gridcolor='#2c3340', zeroline=False),
            xaxis=dict(title='', gridcolor='#2c3340'),
            legend=dict(orientation='h', y=1.1, bgcolor='rgba(0,0,0,0)'),
        )
        st.plotly_chart(fig, use_container_width=True)

        view = bsub[['Occ_Group', 'Role', 'Format', 'Volume_L',
                     'PVF_Ajuste', 'P_Litre_Ajuste', 'Index', 'Statut']].copy()
        view.columns = ['Occasion', 'Rôle', 'Format', 'Volume (L)',
                        'PVF ajusté', 'Prix / L', 'Index', 'Statut']
        view['PVF ajusté'] = view['PVF ajusté'].round(0).astype(int)
        view['Prix / L'] = view['Prix / L'].round(0).astype(int)
        st.dataframe(view, use_container_width=True, hide_index=True,
                     column_config={
                         'Volume (L)': st.column_config.NumberColumn(format="%.2f"),
                         'PVF ajusté': st.column_config.NumberColumn(format="%d Ar"),
                         'Prix / L': st.column_config.NumberColumn(format="%d Ar"),
                         'Index': st.column_config.NumberColumn(format="%d"),
                     })


# =============================================================================
# TAB 4 — DIAGNOSTIC
# =============================================================================
with tab4:
    st.markdown("#### Diagnostic OBPPC")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("SKU analysés", n_total)
    c2.metric("Conformes", n_ok)
    c3.metric("Non conformes", n_total - n_ok)
    c4.metric("Taux conformité", f"{taux:.0f}%")

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
        st.dataframe(out, use_container_width=True, hide_index=True,
                     column_config={
                         'Prix / L': st.column_config.NumberColumn(format="%d Ar"),
                         'Index': st.column_config.NumberColumn(format="%d"),
                         'Écart': st.column_config.NumberColumn(format="%d pts"),
                     })

    st.markdown("##### Export")
    csv = d[['Segment', 'Marque', 'Occ_Group', 'Format', 'Role_OBPPC',
             'Volume_L', 'PVF_Ajuste', 'P_Litre_Ajuste', 'Index', 'Statut']].to_csv(index=False)
    st.download_button(
        "Télécharger (CSV)", data=csv,
        file_name=f"obppc_{channel.split()[0].lower()}.csv", mime="text/csv",
    )
