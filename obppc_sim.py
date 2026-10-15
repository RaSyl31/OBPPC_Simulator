import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulateur OBPPC — BI", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main .block-container { padding-top: 1.25rem; max-width: 100%; }

    /* --- Tableau principal --- */
    .obppc { width: 100%; border-collapse: collapse; font-size: 0.78rem; }
    .obppc th {
        background: #1a1f2b; color: #8b949e; padding: 7px 8px;
        font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.05em;
        border: 1px solid #30363d; font-weight: 600; text-align: center;
        vertical-align: middle; line-height: 1.2;
    }
    .obppc th.rot {
        writing-mode: vertical-rl; transform: rotate(180deg);
        height: 130px; width: 26px; padding: 4px 2px;
        font-size: 0.58rem;
    }
    .obppc td {
        border: 1px solid #30363d; padding: 6px 8px;
        text-align: right; color: #e6edf3; background: #0e1117;
        font-variant-numeric: tabular-nums; font-size: 0.78rem;
    }
    .obppc td.left { text-align: left; }
    .obppc td.center { text-align: center; }
    .obppc td.bold { font-weight: 600; }
    .obppc td.muted { color: #8b949e; }
    .obppc td.marge { color: #8b949e; font-size: 0.72rem; }

    .role-dot { display: inline-block; width: 8px; height: 8px;
                border-radius: 50%; margin-right: 6px; vertical-align: middle; }

    .ok { color: #3fb950; font-weight: 700; }
    .ko { color: #f85149; font-weight: 700; }
    .warn { color: #d29922; font-weight: 700; }

    /* Section marker */
    .group-header {
        background: #161b22 !important;
        color: #a5b4fc !important; font-weight: 700 !important;
        font-size: 0.7rem !important; text-align: left !important;
        letter-spacing: 0.08em; text-transform: uppercase;
    }

    /* KPI bandeau */
    .kpi-band {
        display: grid; grid-template-columns: repeat(5, 1fr);
        gap: 0.6rem; margin: 0.5rem 0 1rem 0;
    }
    .kpi-tile {
        background: #161b22; border: 1px solid #30363d;
        border-radius: 6px; padding: 0.6rem 0.8rem;
    }
    .kpi-tile .lab {
        font-size: 0.62rem; color: #8b949e; text-transform: uppercase;
        letter-spacing: 0.07em; font-weight: 600;
    }
    .kpi-tile .val {
        font-size: 1.15rem; color: #e6edf3; font-weight: 700;
        font-variant-numeric: tabular-nums; margin-top: 2px;
    }

    /* Alerte écart */
    .alert {
        padding: 8px 12px; background: #161b22; border-radius: 6px;
        border-left: 3px solid var(--c); margin-bottom: 6px;
        font-size: 0.82rem; color: #e6edf3;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DONNÉES — Feuille PVC BI (données exactes du fichier)
# =============================================================================
# Colonnes : marque, role, format, vol, pvf, prop_pvf, pva, pv_ds, pvc,
#            pap_min, pap_max, commentaire
DATA_BI = [
    # --- BEAUFORT ---
    {'marque': 'Beaufort', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Beaufort 33CL VER', 'vol': 0.33,
     'pvf': 4000, 'prop_pvf': 4500,
     'pva': 2900, 'pv_ds': 3500, 'pvc': 4000,
     'pap_min': 4000, 'pap_max': 5000,
     'commentaire': 'PVC +500 / PVA +400'},
    {'marque': 'Beaufort', 'role': 'Upscale (Super-Premium Niche)',
     'format': 'Beaufort 33 CL CAN', 'vol': 0.33,
     'pvf': 5000, 'prop_pvf': 5500,
     'pva': 3800, 'pv_ds': 4600, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 6500,
     'commentaire': 'PVC Vs P/L Upscale & FRE'},

    # --- GOLD ---
    {'marque': 'Gold', 'role': 'Entry (Entrée de gamme)',
     'format': 'Gold Blanche 33cl VER', 'vol': 0.33,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 2580, 'pv_ds': 3100, 'pvc': 3500,
     'pap_min': 3500, 'pap_max': 4000,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Entry (Entrée de gamme)',
     'format': 'Gold 8 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blanche 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000,
     'commentaire': 'PVC Vs PVF THB 65'},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blonde 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blonde 65 cl VER', 'vol': 0.65,
     'pvf': 5000, 'prop_pvf': 5300,
     'pva': 3600, 'pv_ds': 4320, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 5500,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold 8 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'pap_min': 6000, 'pap_max': 6500,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold Blanche 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'pap_min': 6000, 'pap_max': 6500,
     'commentaire': 'PVC Vs P/L Upscale & FRE'},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold Blonde 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'pap_min': 6000, 'pap_max': 6500,
     'commentaire': ''},

    # --- THB ---
    {'marque': 'THB', 'role': 'Entry (Entrée de gamme)',
     'format': 'THB Pilsener 33 cl VER', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1900, 'pv_ds': 2280, 'pvc': 2500,
     'pap_min': 2500, 'pap_max': 3000,
     'commentaire': ''},
    {'marque': 'THB', 'role': 'Frequency (Cœur de gamme)',
     'format': 'THB Pilsener 65 cl VER', 'vol': 0.65,
     'pvf': 4500, 'prop_pvf': 4700,
     'pva': 3250, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000,
     'commentaire': 'PVA Vs Marge PDV'},
    {'marque': 'THB', 'role': 'Upscale (Premium)',
     'format': 'THB Pilsener 50 cl CAN', 'vol': 0.50,
     'pvf': 5000, 'prop_pvf': 5200,
     'pva': 3800, 'pv_ds': 4560, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 6000,
     'commentaire': 'PVC +200 / PVA +300'},

    # --- QUEEN ---
    {'marque': 'Queen', 'role': 'Entry (Entrée de gamme)',
     'format': "Queen s 65 cl VER", 'vol': 0.65,
     'pvf': 4000, 'prop_pvf': 4200,
     'pva': 3000, 'pv_ds': 3600, 'pvc': 4000,
     'pap_min': 4000, 'pap_max': 4000,
     'commentaire': ''},

    # --- FRESH ---
    {'marque': 'Fresh', 'role': 'Entry (Entrée de gamme)',
     'format': 'THB Fresh 33 cl VER', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1900, 'pv_ds': 2280, 'pvc': 2500,
     'pap_min': 2500, 'pap_max': 3000,
     'commentaire': ''},
    {'marque': 'Fresh', 'role': 'Frequency (Cœur de gamme)',
     'format': 'THB Fresh 65 cl VER', 'vol': 0.65,
     'pvf': 4000, 'prop_pvf': 4200,
     'pva': 3000, 'pv_ds': 3600, 'pvc': 4000,
     'pap_min': 4000, 'pap_max': 5000,
     'commentaire': 'PVC Vs P/L Entry'},
    {'marque': 'Fresh', 'role': 'Upscale (Premium)',
     'format': 'FRESH 33 cl CAN', 'vol': 0.33,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 2650, 'pv_ds': 3200, 'pvc': 3500,
     'pap_min': 3500, 'pap_max': 4000,
     'commentaire': 'Réduct° prix Vs Perf marque'},
]

df_raw = pd.DataFrame(DATA_BI)

# Référence = Beaufort 33CL VER (Frequency ligne 1 dans le fichier)
REF_PVF_INDEX = 4000      # Beaufort Frequency = Index 100
REF_PL_INDEX = 4000 / 0.33
# Référence THB 65 (pour Index PVF/Prix (THB 65))
REF_THB65_PVF = 4500
REF_THB65_PL = 4500 / 0.65


# =============================================================================
# HELPERS
# =============================================================================
ROLE_COLORS = {
    'Entry (Entrée de gamme)': '#58a6ff',
    'Frequency (Cœur de gamme)': '#3fb950',
    'Upsize (Grand format)': '#d29922',
    'Upscale (Premium)': '#bc8cff',
    'Upscale (Super-Premium Niche)': '#a855f7',
}

def role_simple(r):
    if r.startswith('Upscale'):   return 'Upscale'
    if r.startswith('Entry'):     return 'Entry'
    if r.startswith('Frequency'): return 'Frequency'
    if r.startswith('Upsize'):    return 'Upsize'
    return 'Autre'

ROLE_TARGET = {'Entry': '101–110', 'Frequency': '100',
               'Upsize': '90–99', 'Upscale': '≥ 111'}

def status_from_idx(idx, role):
    if role == 'Entry':     return 'OK' if 101 <= idx <= 110 else 'KO'
    if role == 'Frequency': return 'OK' if idx == 100 else 'KO'
    if role == 'Upsize':    return 'OK' if 90 <= idx <= 99 else 'KO'
    if role == 'Upscale':   return 'OK' if idx >= 111 else 'KO'
    return '—'

def fmt(v, unit=''):
    if pd.isna(v): return '—'
    if isinstance(v, float) and v.is_integer(): v = int(v)
    return f"{v:,.0f}".replace(',', ' ') + (f" {unit}" if unit else '')

def fmt_pct(v):
    if pd.isna(v): return '—'
    return f"{v*100:.0f}%"


# =============================================================================
# CALCUL
# =============================================================================
def compute(df):
    d = df.copy()
    d['p_litre'] = d['pvf'] / d['vol']
    d['prop_p_litre'] = d['prop_pvf'] / d['vol']

    # Index vs Beaufort Frequency (ligne 1)
    d['idx_pvf']  = (d['pvf'] / REF_PVF_INDEX * 100).round(0).astype(int)
    d['idx_pl']   = (d['p_litre'] / REF_PL_INDEX * 100).round(0).astype(int)
    d['idx_pvf_thb65'] = (d['pvf'] / REF_THB65_PVF * 100).round(0).astype(int)
    d['idx_pl_thb65']  = (d['p_litre'] / REF_THB65_PL * 100).round(0).astype(int)

    # Proposition
    d['idx_pvf_prop']  = (d['prop_pvf'] / REF_PVF_INDEX * 100).round(0).astype(int)
    d['idx_pl_prop']   = (d['prop_p_litre'] / REF_PL_INDEX * 100).round(0).astype(int)
    d['idx_pvf_thb65_prop'] = (d['prop_pvf'] / REF_THB65_PVF * 100).round(0).astype(int)
    d['idx_pl_thb65_prop']  = (d['prop_p_litre'] / REF_THB65_PL * 100).round(0).astype(int)

    # Marges
    d['marge_ds'] = d['pv_ds'] - d['pva']
    d['marge_ds_pct'] = d['marge_ds'] / d['pva']
    d['marge_pdv'] = d['pvc'] - d['pv_ds']
    d['marge_pdv_pct'] = d['marge_pdv'] / d['pv_ds']
    d['marge_min'] = d['pap_min'] - d['pv_ds']
    d['marge_max'] = d['pap_max'] - d['pv_ds']
    d['marge_pdv_min_pct'] = d['marge_min'] / d['pv_ds']
    d['marge_pdv_max_pct'] = d['marge_max'] / d['pv_ds']
    d['hausse'] = d['prop_pvf'] - d['pvf']
    d['hausse_pct'] = d['hausse'] / d['pvf']

    # PAP 2027
    d['pva_2027'] = d['pva'] + d['hausse']
    d['pv_ds_2027'] = d['pv_ds'] + d['hausse']
    d['marge_ds_2027'] = d['pv_ds_2027'] - d['pva_2027']
    d['marge_ds_2027_pct'] = d['marge_ds_2027'] / d['pva_2027']
    d['pvc_2027'] = d['prop_pvf']
    d['marge_pdv_2027'] = d['pvc_2027'] - d['pv_ds_2027']
    d['marge_pdv_2027_pct'] = d['marge_pdv_2027'] / d['pv_ds_2027']

    # Statut vs cible du rôle (basé sur l'index P/L vs Beaufort Frequency)
    d['role_simple'] = d['role'].apply(role_simple)
    d['statut'] = d.apply(
        lambda r: status_from_idx(r['idx_pl'], r['role_simple']), axis=1)
    return d


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### Simulateur OBPPC — BI")
    st.caption("Beer · PVC / PAP 2026 → 2027")
    st.markdown("---")

    marques = st.multiselect(
        "Marques",
        options=sorted(df_raw['marque'].unique()),
        default=sorted(df_raw['marque'].unique()))

    roles = st.multiselect(
        "Rôles OBPPC",
        options=list(df_raw['role'].unique()),
        default=list(df_raw['role'].unique()))

    st.markdown("---")
    if st.button("Réinitialiser les propositions", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith('prop_') or k.startswith('editor_'):
                del st.session_state[k]
        st.rerun()

    st.markdown("---")
    st.markdown("##### Cibles index P/L")
    for r, target in ROLE_TARGET.items():
        color = ROLE_COLORS[[k for k in ROLE_COLORS if k.startswith(r)][0]]
        st.markdown(
            f"<div style='font-size:0.72rem; color:#cbd5e1; margin-bottom:3px;'>"
            f"<span class='role-dot' style='background:{color};'></span>"
            f"<b>{r}</b> — {target}</div>",
            unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.68rem; color:#6e7681; margin-top:10px;'>"
        "Référence index : <b>Beaufort 33CL VER Frequency</b> (Index 100)</div>",
        unsafe_allow_html=True)


# =============================================================================
# HEADER
# =============================================================================
st.markdown("## Simulateur OBPPC — BI")
st.caption("Feuille **PVC BI** · Référence index : Beaufort 33CL VER Frequency · "
           "Comparaison 2026 (actuel) vs 2027 (proposition)")


# =============================================================================
# FILTRAGE
# =============================================================================
df = df_raw[
    df_raw['marque'].isin(marques) & df_raw['role'].isin(roles)
].reset_index(drop=True)

if df.empty:
    st.warning("Aucune référence à afficher avec ces filtres.")
    st.stop()

# Édition des propositions
st.markdown("### Éditeur de propositions 2027")
st.caption("Modifiez le **PVF proposé** ou les prix **PVA / PV DS / PVC / PAP** — "
           "tous les index, marges et statuts se recalculent.")

editable = df[['marque', 'role', 'format', 'vol', 'pvf', 'prop_pvf',
               'pva', 'pv_ds', 'pvc', 'pap_min', 'pap_max']].copy()

edited = st.data_editor(
    editable,
    column_config={
        'marque': st.column_config.TextColumn("Marque", disabled=True, width=90),
        'role': st.column_config.TextColumn("Rôle", disabled=True, width=200),
        'format': st.column_config.TextColumn("Format", disabled=True, width=200),
        'vol': st.column_config.NumberColumn("Vol (L)", disabled=True, format="%.2f", width=70),
        'pvf': st.column_config.NumberColumn("PVF 2026", disabled=True, format="%d", width=90),
        'prop_pvf': st.column_config.NumberColumn("PVF 2027 (prop.)", min_value=0,
                                                  step=100, format="%d", width=120),
        'pva': st.column_config.NumberColumn("PVA HT", min_value=0, step=10,
                                             format="%d", width=90),
        'pv_ds': st.column_config.NumberColumn("PV DS HT", min_value=0, step=10,
                                               format="%d", width=90),
        'pvc': st.column_config.NumberColumn("PVC", min_value=0, step=10,
                                             format="%d", width=90),
        'pap_min': st.column_config.NumberColumn("PAP MIN", min_value=0, step=10,
                                                 format="%d", width=90),
        'pap_max': st.column_config.NumberColumn("PAP MAX", min_value=0, step=10,
                                                 format="%d", width=90),
    },
    hide_index=True,
    use_container_width=True,
    num_rows="fixed",
    height=min(600, 80 + 36 * len(editable)),
    key="prop_editor",
)

d = compute(edited)


# =============================================================================
# KPI BANDEAU
# =============================================================================
n_ok = (d['statut'] == 'OK').sum()
n_total = len(d)
taux = n_ok / n_total * 100 if n_total else 0
hausse_moy = d['hausse_pct'].mean() * 100
marge_ds_moy = d['marge_ds_pct'].mean() * 100
marge_pdv_moy = d['marge_pdv_pct'].mean() * 100

st.markdown(f"""
<div class="kpi-band">
    <div class="kpi-tile">
        <div class="lab">Références</div>
        <div class="val">{n_total}</div>
    </div>
    <div class="kpi-tile">
        <div class="lab">Conformes</div>
        <div class="val" style="color:{'#3fb950' if taux>=70 else '#d29922' if taux>=40 else '#f85149'};">
            {n_ok}/{n_total} · {taux:.0f}%
        </div>
    </div>
    <div class="kpi-tile">
        <div class="lab">Hausse moyenne</div>
        <div class="val">{hausse_moy:+.1f}%</div>
    </div>
    <div class="kpi-tile">
        <div class="lab">Marge DS moy.</div>
        <div class="val">{marge_ds_moy:.1f}%</div>
    </div>
    <div class="kpi-tile">
        <div class="lab">Marge PDV moy.</div>
        <div class="val">{marge_pdv_moy:.1f}%</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =============================================================================
# TABLEAU PRINCIPAL — reproduit la structure de la feuille PVC BI
# =============================================================================
st.markdown("### Tableau OBPPC — PVC BI")

# Construction HTML reproduisant la structure du fichier
def build_main_table(d):
    html = ['<table class="obppc">']

    # En-tête groupé
    html.append('<thead>')
    html.append('<tr>'
                '<th rowspan="2" class="left">Marque</th>'
                '<th rowspan="2" class="left">Rôle OBPPC</th>'
                '<th rowspan="2" class="left">Description / Format</th>'
                '<th rowspan="2">Volume<br>(L)</th>'
                '<th colspan="8">2026 · PRIX DE VENTE ACTUEL</th>'
                '<th colspan="8">2027 · PROPOSITION</th>'
                '<th colspan="7">2026 · MARGES (PAP)</th>'
                '<th colspan="6">2027 · MARGES (PAP)</th>'
                '<th rowspan="2" class="left">Commentaire</th>'
                '</tr>')
    html.append('<tr>'
                # 2026 pricing
                '<th>PVF</th><th>P/L</th>'
                '<th>Idx<br>PVF</th><th>Idx<br>P/L</th>'
                '<th>Idx<br>THB65<br>PVF</th><th>Idx<br>THB65<br>P/L</th>'
                '<th>Cible<br>PVF</th><th>Cible<br>P/L</th>'
                # 2027 proposition
                '<th>PVF</th><th>P/L</th>'
                '<th>Idx<br>PVF</th><th>Idx<br>P/L</th>'
                '<th>Idx<br>THB65<br>PVF</th><th>Idx<br>THB65<br>P/L</th>'
                '<th>Hausse</th><th>Hausse<br>%</th>'
                # 2026 margins
                '<th>PVA HT</th><th>PV DS HT</th>'
                '<th>Marge<br>DS</th><th>Taux<br>DS</th>'
                '<th>PVC</th><th>Marge<br>PDV</th><th>Taux<br>PDV</th>'
                # 2027 margins
                '<th>PVA 27</th><th>DS 27</th>'
                '<th>Marge 27</th><th>Taux<br>DS 27</th>'
                '<th>PVC 27</th><th>Taux<br>PDV 27</th>'
                '</tr>')
    html.append('</thead><tbody>')

    for _, row in d.iterrows():
        color = ROLE_COLORS[row['role']]
        statut_cls = 'ok' if row['statut'] == 'OK' else 'ko' if row['statut'] == 'KO' else 'muted'

        html.append(
            '<tr>'
            f'<td class="left bold">{row["marque"]}</td>'
            f'<td class="left"><span class="role-dot" style="background:{color};"></span>'
            f'{row["role"]}</td>'
            f'<td class="left">{row["format"]}</td>'
            f'<td class="center">{row["vol"]:.2f}</td>'

            # 2026 pricing
            f'<td class="bold">{fmt(row["pvf"])}</td>'
            f'<td>{fmt(row["p_litre"])}</td>'
            f'<td>{row["idx_pvf"]}</td>'
            f'<td class="{statut_cls}">{row["idx_pl"]}</td>'
            f'<td class="muted">{row["idx_pvf_thb65"]}</td>'
            f'<td class="muted">{row["idx_pl_thb65"]}</td>'
            f'<td class="muted">{ROLE_TARGET[row["role_simple"]]}</td>'
            f'<td class="muted">{ROLE_TARGET[row["role_simple"]]}</td>'

            # 2027 proposition
            f'<td class="bold">{fmt(row["prop_pvf"])}</td>'
            f'<td>{fmt(row["prop_p_litre"])}</td>'
            f'<td>{row["idx_pvf_prop"]}</td>'
            f'<td>{row["idx_pl_prop"]}</td>'
            f'<td class="muted">{row["idx_pvf_thb65_prop"]}</td>'
            f'<td class="muted">{row["idx_pl_thb65_prop"]}</td>'
            f'<td class="muted">{fmt(row["hausse"])}</td>'
            f'<td class="muted">{row["hausse_pct"]*100:+.1f}%</td>'

            # 2026 margins
            f'<td>{fmt(row["pva"])}</td>'
            f'<td>{fmt(row["pv_ds"])}</td>'
            f'<td>{fmt(row["marge_ds"])}</td>'
            f'<td class="marge">{row["marge_ds_pct"]*100:.0f}%</td>'
            f'<td>{fmt(row["pvc"])}</td>'
            f'<td>{fmt(row["marge_pdv"])}</td>'
            f'<td class="marge">{row["marge_pdv_pct"]*100:.0f}%</td>'

            # 2027 margins
            f'<td>{fmt(row["pva_2027"])}</td>'
            f'<td>{fmt(row["pv_ds_2027"])}</td>'
            f'<td>{fmt(row["marge_ds_2027"])}</td>'
            f'<td class="marge">{row["marge_ds_2027_pct"]*100:.0f}%</td>'
            f'<td>{fmt(row["pvc_2027"])}</td>'
            f'<td class="marge">{row["marge_pdv_2027_pct"]*100:.0f}%</td>'

            f'<td class="left muted">{row["commentaire"]}</td>'
            '</tr>'
        )
    html.append('</tbody></table>')
    return ''.join(html)

st.markdown(build_main_table(d), unsafe_allow_html=True)


# =============================================================================
# EXPORT
# =============================================================================
st.markdown("---")
export = d[['marque', 'role', 'format', 'vol', 'pvf', 'p_litre',
            'idx_pvf', 'idx_pl', 'idx_pvf_thb65', 'idx_pl_thb65',
            'prop_pvf', 'prop_p_litre', 'idx_pvf_prop', 'idx_pl_prop',
            'hausse', 'hausse_pct',
            'pva', 'pv_ds', 'marge_ds', 'marge_ds_pct',
            'pvc', 'marge_pdv', 'marge_pdv_pct',
            'pva_2027', 'pv_ds_2027', 'marge_ds_2027', 'marge_ds_2027_pct',
            'pvc_2027', 'marge_pdv_2027', 'marge_pdv_2027_pct',
            'statut', 'commentaire']].copy()

export.columns = ['Marque', 'Rôle OBPPC', 'Format', 'Volume (L)',
                  'PVF 2026', 'P/L 2026', 'Idx PVF', 'Idx P/L',
                  'Idx PVF THB65', 'Idx P/L THB65',
                  'PVF 2027', 'P/L 2027', 'Idx PVF 2027', 'Idx P/L 2027',
                  'Hausse', 'Hausse %',
                  'PVA 2026', 'PV DS 2026', 'Marge DS', 'Taux DS',
                  'PVC 2026', 'Marge PDV', 'Taux PDV',
                  'PVA 2027', 'DS 2027', 'Marge DS 2027', 'Taux DS 2027',
                  'PVC 2027', 'Taux PDV 2027',
                  'Statut', 'Commentaire']

st.download_button(
    "📥 Télécharger le tableau complet (CSV)",
    data=export.to_csv(index=False).encode('utf-8'),
    file_name="simulateur_obppc_bi.csv",
    mime="text/csv",
)
