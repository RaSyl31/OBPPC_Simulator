import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulateur OBPPC", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main .block-container { padding-top: 1.25rem; max-width: 100%; }

    .obppc { width: 100%; border-collapse: collapse; font-size: 0.85rem; }
    .obppc th {
        background: #1a1f2b; color: #8b949e; padding: 10px 10px;
        font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.05em;
        border: 1px solid #30363d; font-weight: 600; text-align: center;
    }
    .obppc th.left { text-align: left; }
    .obppc td {
        border: 1px solid #30363d; padding: 9px 10px;
        text-align: right; color: #e6edf3; background: #0e1117;
        font-variant-numeric: tabular-nums;
    }
    .obppc td.left { text-align: left; }
    .obppc td.center { text-align: center; }
    .obppc td.bold { font-weight: 600; }
    .obppc td.muted { color: #8b949e; }
    .obppc tr:hover td { background: #161b22; }

    .role-dot { display: inline-block; width: 8px; height: 8px;
                border-radius: 50%; margin-right: 6px; vertical-align: middle; }

    .ok { color: #3fb950; font-weight: 700; }
    .ko { color: #f85149; font-weight: 700; }

    .tag {
        display: inline-block; padding: 1px 6px; border-radius: 3px;
        font-size: 0.62rem; font-weight: 700; letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .tag-star { background: #7c3aed; color: #fff; }
    .tag-comp { background: #484f58; color: #e6edf3; }

    .kpi-band {
        display: grid; grid-template-columns: repeat(5, 1fr);
        gap: 0.6rem; margin: 0.5rem 0 1rem 0;
    }
    .kpi-tile {
        background: #161b22; border: 1px solid #30363d;
        border-radius: 6px; padding: 0.7rem 0.9rem;
    }
    .kpi-tile .lab {
        font-size: 0.62rem; color: #8b949e; text-transform: uppercase;
        letter-spacing: 0.07em; font-weight: 600;
    }
    .kpi-tile .val {
        font-size: 1.25rem; color: #e6edf3; font-weight: 700;
        font-variant-numeric: tabular-nums; margin-top: 3px;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# DONNÉES — BI
# =============================================================================
DATA_BI = [
    {'marque': 'Beaufort', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Beaufort 33CL VER', 'vol': 0.33,
     'pvf': 4000, 'prop_pvf': 4500,
     'pva': 2900, 'pv_ds': 3500, 'pvc': 4000,
     'pap_min': 4000, 'pap_max': 5000, 'commentaire': 'PVC +500 / PVA +400'},
    {'marque': 'Beaufort', 'role': 'Upscale (Super-Premium Niche)',
     'format': 'Beaufort 33 CL CAN', 'vol': 0.33,
     'pvf': 5000, 'prop_pvf': 5500,
     'pva': 3800, 'pv_ds': 4600, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 6500, 'commentaire': 'PVC Vs P/L Upscale & FRE'},
    {'marque': 'Gold', 'role': 'Entry (Entrée de gamme)',
     'format': 'Gold Blanche 33cl VER', 'vol': 0.33,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 2580, 'pv_ds': 3100, 'pvc': 3500,
     'pap_min': 3500, 'pap_max': 4000, 'commentaire': ''},
    {'marque': 'Gold', 'role': 'Entry (Entrée de gamme)',
     'format': 'Gold 8 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000, 'commentaire': ''},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blanche 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000, 'commentaire': 'PVC Vs PVF THB 65'},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blonde 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000, 'commentaire': ''},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blonde 65 cl VER', 'vol': 0.65,
     'pvf': 5000, 'prop_pvf': 5300,
     'pva': 3600, 'pv_ds': 4320, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 5500, 'commentaire': ''},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold 8 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'pap_min': 6000, 'pap_max': 6500, 'commentaire': ''},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold Blanche 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'pap_min': 6000, 'pap_max': 6500, 'commentaire': 'PVC Vs P/L Upscale & FRE'},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold Blonde 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'pap_min': 6000, 'pap_max': 6500, 'commentaire': ''},
    {'marque': 'THB', 'role': 'Entry (Entrée de gamme)',
     'format': 'THB Pilsener 33 cl VER', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1900, 'pv_ds': 2280, 'pvc': 2500,
     'pap_min': 2500, 'pap_max': 3000, 'commentaire': ''},
    {'marque': 'THB', 'role': 'Frequency (Cœur de gamme)',
     'format': 'THB Pilsener 65 cl VER', 'vol': 0.65,
     'pvf': 4500, 'prop_pvf': 4700,
     'pva': 3250, 'pv_ds': 3900, 'pvc': 4500,
     'pap_min': 4500, 'pap_max': 5000, 'commentaire': 'PVA Vs Marge PDV'},
    {'marque': 'THB', 'role': 'Upscale (Premium)',
     'format': 'THB Pilsener 50 cl CAN', 'vol': 0.50,
     'pvf': 5000, 'prop_pvf': 5200,
     'pva': 3800, 'pv_ds': 4560, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 6000, 'commentaire': 'PVC +200 / PVA +300'},
    {'marque': 'Queen', 'role': 'Entry (Entrée de gamme)',
     'format': "Queen s 65 cl VER", 'vol': 0.65,
     'pvf': 4000, 'prop_pvf': 4200,
     'pva': 3000, 'pv_ds': 3600, 'pvc': 4000,
     'pap_min': 4000, 'pap_max': 4000, 'commentaire': ''},
    {'marque': 'Fresh', 'role': 'Entry (Entrée de gamme)',
     'format': 'THB Fresh 33 cl VER', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1900, 'pv_ds': 2280, 'pvc': 2500,
     'pap_min': 2500, 'pap_max': 3000, 'commentaire': ''},
    {'marque': 'Fresh', 'role': 'Frequency (Cœur de gamme)',
     'format': 'THB Fresh 65 cl VER', 'vol': 0.65,
     'pvf': 4000, 'prop_pvf': 4200,
     'pva': 3000, 'pv_ds': 3600, 'pvc': 4000,
     'pap_min': 4000, 'pap_max': 5000, 'commentaire': 'PVC Vs P/L Entry'},
    {'marque': 'Fresh', 'role': 'Upscale (Premium)',
     'format': 'FRESH 33 cl CAN', 'vol': 0.33,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 2650, 'pv_ds': 3200, 'pvc': 3500,
     'pap_min': 3500, 'pap_max': 4000, 'commentaire': 'Réduct° prix Vs Perf marque'},
]


# =============================================================================
# DONNÉES — BG
# =============================================================================
DATA_BG = [
    # --- COCA (Concurrent) ---
    {'marque': 'COCA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35 (N°1 vente en col)', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1380, 'pv_ds': 1380, 'pvc': 1500,
     'pap_min': 1500, 'pap_max': 2000, 'commentaire': ''},
    {'marque': 'COCA', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 0, 'pv_ds': 0, 'pvc': 2000,
     'pap_min': 2000, 'pap_max': 2500, 'commentaire': ''},
    {'marque': 'COCA', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 0, 'pv_ds': 0, 'pvc': 2500,
     'pap_min': 2500, 'pap_max': 4000, 'commentaire': ''},
    {'marque': 'COCA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 4480, 'pv_ds': 4480, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 5500, 'commentaire': ''},

    # --- WOCO (STAR) ---
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1080, 'pv_ds': 1300, 'pvc': 1500,
     'pap_min': 1500, 'pap_max': 2000, 'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 1465, 'pv_ds': 1758, 'pvc': 2000,
     'pap_min': 2000, 'pap_max': 2500, 'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1850, 'pv_ds': 2220, 'pvc': 2500,
     'pap_min': 2500, 'pap_max': 3500, 'commentaire': 'PVA +150 / PVC inchangé'},
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 30', 'vol': 0.30,
     'pvf': 1200, 'prop_pvf': 1200,
     'pva': 875, 'pv_ds': 1050, 'pvc': 1200,
     'pap_min': 1200, 'pap_max': 1500, 'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 3650, 'pv_ds': 4380, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 5500, 'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 100', 'vol': 1.00,
     'pvf': 3000, 'prop_pvf': 3000,
     'pva': 2180, 'pv_ds': 2616, 'pvc': 3000,
     'pap_min': 3000, 'pap_max': 3500, 'commentaire': ''},

    # --- FANTA (Concurrent) ---
    {'marque': 'FANTA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35 (N°1 vente en col)', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1370, 'pv_ds': 1370, 'pvc': 1500,
     'pap_min': 1500, 'pap_max': 2000, 'commentaire': ''},
    {'marque': 'FANTA', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 0, 'pv_ds': 0, 'pvc': 2000,
     'pap_min': 2000, 'pap_max': 2500, 'commentaire': ''},
    {'marque': 'FANTA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 4410, 'pv_ds': 4410, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 5500, 'commentaire': ''},

    # --- CAPRICE (STAR) ---
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1080, 'pv_ds': 1300, 'pvc': 1500,
     'pap_min': 1500, 'pap_max': 2000, 'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 1465, 'pv_ds': 1758, 'pvc': 2000,
     'pap_min': 2000, 'pap_max': 2500, 'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1850, 'pv_ds': 2220, 'pvc': 2500,
     'pap_min': 2500, 'pap_max': 3500, 'commentaire': 'PVA +150 / PVC inchangé'},
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 30', 'vol': 0.30,
     'pvf': 1200, 'prop_pvf': 1200,
     'pva': 875, 'pv_ds': 1050, 'pvc': 1200,
     'pap_min': 1200, 'pap_max': 1500, 'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 3650, 'pv_ds': 4380, 'pvc': 5000,
     'pap_min': 5000, 'pap_max': 5500, 'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 100', 'vol': 1.00,
     'pvf': 3000, 'prop_pvf': 3000,
     'pva': 2180, 'pv_ds': 2616, 'pvc': 3000,
     'pap_min': 3000, 'pap_max': 3500, 'commentaire': ''},

    # --- TONIC (STAR) ---
    {'marque': 'TONIC', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 30', 'vol': 0.30,
     'pvf': 1200, 'prop_pvf': 1800,
     'pva': 875, 'pv_ds': 1050, 'pvc': 1200,
     'pap_min': 1200, 'pap_max': 1200, 'commentaire': ''},
    {'marque': 'TONIC', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 100', 'vol': 1.00,
     'pvf': 3000, 'prop_pvf': 3500,
     'pva': 2180, 'pv_ds': 2616, 'pvc': 3000,
     'pap_min': 3000, 'pap_max': 4000, 'commentaire': ''},
]


# =============================================================================
# CONFIGURATION PAR CATÉGORIE
# =============================================================================
CATEGORIES = {
    'BI': {
        'label': 'BI — Bière',
        'data': DATA_BI,
        'ref_pvf': 4000,
        'ref_pl': 4500 / 0.65,
        'ref_label_pvf': 'Beaufort 33CL VER (Frequency)',
        'ref_label_pl': 'THB Pilsener 65 cl VER (Frequency)',
        'star_brands': None,   # toutes STAR (pas de concurrent)
        'has_competitors': False,
    },
    'BG': {
        'label': 'BG — Boissons Gazeuses',
        'data': DATA_BG,
        'ref_pvf': 2000,
        'ref_pl': 2000 / 0.50,
        'ref_label_pvf': 'PET 50 (Frequency)',
        'ref_label_pl': 'PET 50 (Frequency)',
        'star_brands': {'WOCO', 'CAPRICE', 'TONIC'},
        'has_competitors': True,
    },
}


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
ROLE_TARGET = {'Entry': '101–110', 'Frequency': '100',
               'Upsize': '90–99', 'Upscale': '≥ 111'}

def role_simple(r):
    if r.startswith('Upscale'):   return 'Upscale'
    if r.startswith('Entry'):     return 'Entry'
    if r.startswith('Frequency'): return 'Frequency'
    if r.startswith('Upsize'):    return 'Upsize'
    return 'Autre'

def status_from_idx(idx, role):
    if role == 'Entry':     return 'OK' if 101 <= idx <= 110 else 'KO'
    if role == 'Frequency': return 'OK' if idx == 100 else 'KO'
    if role == 'Upsize':    return 'OK' if 90 <= idx <= 99 else 'KO'
    if role == 'Upscale':   return 'OK' if idx >= 111 else 'KO'
    return '—'

def fmt(v):
    if pd.isna(v): return '—'
    try: v = float(v)
    except (TypeError, ValueError): return str(v)
    if v.is_integer(): v = int(v)
    return f"{v:,.0f}".replace(',', ' ')

def safe_pct(v, d=0):
    try:
        f = float(v)
        if pd.isna(f): return '—'
        return f"{f*100:.{d}f}%"
    except (TypeError, ValueError):
        return '—'

def brand_tag(marque, star_brands):
    """Retourne HTML du badge STAR / Concurrent / rien."""
    if star_brands is None:
        return f'<span class="tag tag-star">{marque}</span>'
    if marque in star_brands:
        return f'<span class="tag tag-star">{marque}</span>'
    return f'<span class="tag tag-comp">{marque}</span>'


# =============================================================================
# CALCUL
# =============================================================================
def compute(df, cfg):
    d = df.copy()
    d['p_litre'] = d['pvf'] / d['vol']
    d['prop_p_litre'] = d['prop_pvf'] / d['vol']

    ref_pvf = cfg['ref_pvf']
    ref_pl = cfg['ref_pl']

    d['idx_pvf'] = (d['pvf'] / ref_pvf * 100).round(0).astype(int)
    d['idx_pl']  = (d['p_litre'] / ref_pl * 100).round(0).astype(int)
    d['idx_pl_prop'] = (d['prop_p_litre'] / ref_pl * 100).round(0).astype(int)

    # Marges 2026
    d['marge_ds'] = d['pv_ds'] - d['pva']
    d['marge_ds_pct'] = d['marge_ds'] / d['pva'].replace(0, pd.NA)
    d['marge_pdv'] = d['pvc'] - d['pv_ds']
    d['marge_pdv_pct'] = d['marge_pdv'] / d['pv_ds'].replace(0, pd.NA)

    # Hausse
    d['hausse'] = d['prop_pvf'] - d['pvf']
    d['hausse_pct'] = d['hausse'] / d['pvf']

    # PAP 2027
    d['pva_2027'] = d['pva'] + d['hausse']
    d['pv_ds_2027'] = d['pv_ds'] + d['hausse']
    d['marge_ds_2027'] = d['pv_ds_2027'] - d['pva_2027']
    d['marge_ds_2027_pct'] = d['marge_ds_2027'] / d['pva_2027'].replace(0, pd.NA)
    d['pvc_2027'] = d['prop_pvf']
    d['marge_pdv_2027'] = d['pvc_2027'] - d['pv_ds_2027']
    d['marge_pdv_2027_pct'] = d['marge_pdv_2027'] / d['pv_ds_2027'].replace(0, pd.NA)

    # Statut
    d['role_simple'] = d['role'].apply(role_simple)
    d['statut'] = d.apply(
        lambda r: status_from_idx(r['idx_pl'], r['role_simple']), axis=1)

    # STAR/Concurrent
    if cfg['star_brands'] is None:
        d['type'] = 'STAR'
    else:
        d['type'] = d['marque'].apply(
            lambda m: 'STAR' if m in cfg['star_brands'] else 'Concurrent')
    return d


# =============================================================================
# SIDEBAR
# =============================================================================
with st.sidebar:
    st.markdown("### Simulateur OBPPC")
    st.caption("Occasion · Brand · Package · Price · Channel")
    st.markdown("---")

    cat_key = st.selectbox(
        "Catégorie",
        options=list(CATEGORIES.keys()),
        format_func=lambda k: CATEGORIES[k]['label'],
    )
    cfg = CATEGORIES[cat_key]
    df_raw = pd.DataFrame(cfg['data'])

    marques = st.multiselect(
        "Marques",
        options=sorted(df_raw['marque'].unique()),
        default=sorted(df_raw['marque'].unique()))
    roles = st.multiselect(
        "Rôles OBPPC",
        options=list(df_raw['role'].unique()),
        default=list(df_raw['role'].unique()))

    st.markdown("---")
    if st.button("Réinitialiser", use_container_width=True):
        for k in list(st.session_state.keys()):
            if k.startswith('prop_editor'):
                del st.session_state[k]
        st.rerun()

    st.markdown("---")
    st.markdown("##### Cibles index P/L")
    for r, target in ROLE_TARGET.items():
        ck = [k for k in ROLE_COLORS if k.startswith(r)]
        color = ROLE_COLORS[ck[0]] if ck else '#64748b'
        st.markdown(
            f"<div style='font-size:0.72rem; color:#cbd5e1; margin-bottom:3px;'>"
            f"<span class='role-dot' style='background:{color};'></span>"
            f"<b>{r}</b> — {target}</div>",
            unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        f"<div style='font-size:0.68rem; color:#6e7681; line-height:1.6;'>"
        f"<b style='color:#a5b4fc;'>Références d'index</b><br>"
        f"• Index <b>PVF</b> : {cfg['ref_label_pvf']}<br>"
        f"• Index <b>P/L</b> : {cfg['ref_label_pl']}"
        f"</div>",
        unsafe_allow_html=True)


# =============================================================================
# HEADER
# =============================================================================
st.markdown(f"## Simulateur OBPPC — {cfg['label']}")
st.caption(
    f"Index PVF → {cfg['ref_label_pvf']} &nbsp;·&nbsp; "
    f"Index P/L → {cfg['ref_label_pl']}"
)


# =============================================================================
# FILTRAGE
# =============================================================================
df = df_raw[
    df_raw['marque'].isin(marques) & df_raw['role'].isin(roles)
].reset_index(drop=True)

if df.empty:
    st.warning("Aucune référence à afficher avec ces filtres.")
    st.stop()


# =============================================================================
# ÉDITEUR
# =============================================================================
with st.expander("✏️ Éditer les prix", expanded=False):
    editable = df[['marque', 'format', 'pvf', 'prop_pvf', 'pva', 'pv_ds', 'pvc']].copy()
    edited = st.data_editor(
        editable,
        column_config={
            'marque': st.column_config.TextColumn("Marque", disabled=True, width=100),
            'format': st.column_config.TextColumn("Format", disabled=True, width=220),
            'pvf': st.column_config.NumberColumn("PVF 2026", disabled=True,
                                                 format="%d", width=100),
            'prop_pvf': st.column_config.NumberColumn("PVF 2027", min_value=0, step=100,
                                                      format="%d", width=110),
            'pva': st.column_config.NumberColumn("PVA HT", min_value=0, step=10,
                                                 format="%d", width=90),
            'pv_ds': st.column_config.NumberColumn("PV DS HT", min_value=0, step=10,
                                                   format="%d", width=90),
            'pvc': st.column_config.NumberColumn("PVC", min_value=0, step=10,
                                                 format="%d", width=90),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        height=min(500, 80 + 36 * len(editable)),
        key=f"prop_editor_{cat_key}",
    )
    for col in ['role', 'vol', 'pap_min', 'pap_max', 'commentaire']:
        edited[col] = df[col].reset_index(drop=True).values

d = compute(edited, cfg)


# =============================================================================
# KPI
# =============================================================================
n_ok = int((d['statut'] == 'OK').sum())
n_total = len(d)
taux = n_ok / n_total * 100 if n_total else 0

# KPI supplémentaire : nb concurrents (uniquement BG)
n_star = int((d['type'] == 'STAR').sum())
n_comp = int((d['type'] == 'Concurrent').sum())

if cfg['has_competitors']:
    kpi_html = f"""
    <div class="kpi-band">
        <div class="kpi-tile"><div class="lab">SKU STAR</div><div class="val">{n_star}</div></div>
        <div class="kpi-tile"><div class="lab">SKU Concurrents</div><div class="val">{n_comp}</div></div>
        <div class="kpi-tile"><div class="lab">Conformes</div>
            <div class="val" style="color:{'#3fb950' if taux>=70 else '#d29922' if taux>=40 else '#f85149'};">
                {n_ok}/{n_total}</div></div>
        <div class="kpi-tile"><div class="lab">Hausse moyenne</div>
            <div class="val">{d['hausse_pct'].mean()*100:+.1f}%</div></div>
        <div class="kpi-tile"><div class="lab">Marge DS moy.</div>
            <div class="val">{d['marge_ds_pct'].mean()*100:.1f}%</div></div>
    </div>
    """
else:
    kpi_html = f"""
    <div class="kpi-band">
        <div class="kpi-tile"><div class="lab">Références</div><div class="val">{n_total}</div></div>
        <div class="kpi-tile"><div class="lab">Conformes</div>
            <div class="val" style="color:{'#3fb950' if taux>=70 else '#d29922' if taux>=40 else '#f85149'};">
                {n_ok}/{n_total}</div></div>
        <div class="kpi-tile"><div class="lab">Hausse moyenne</div>
            <div class="val">{d['hausse_pct'].mean()*100:+.1f}%</div></div>
        <div class="kpi-tile"><div class="lab">Marge DS moy.</div>
            <div class="val">{d['marge_ds_pct'].mean()*100:.1f}%</div></div>
        <div class="kpi-tile"><div class="lab">Marge PDV moy.</div>
            <div class="val">{d['marge_pdv_pct'].mean()*100:.1f}%</div></div>
    </div>
    """
st.markdown(kpi_html, unsafe_allow_html=True)


# =============================================================================
# TABLEAU PRINCIPAL
# =============================================================================
st.markdown("### Vue d'ensemble")

html = ['<table class="obppc"><thead><tr>',
        '<th class="left">Marque</th>',
        '<th class="left">Rôle</th>',
        '<th class="left">Format</th>',
        '<th>Vol (L)</th>',
        '<th>PVF 2026</th>',
        '<th>P/L 2026</th>',
        '<th>Index P/L</th>',
        '<th>PVF 2027</th>',
        '<th>Hausse</th>',
        '<th>Marge DS</th>',
        '<th>Marge PDV</th>',
        '</tr></thead><tbody>']

for _, row in d.iterrows():
    color = ROLE_COLORS.get(row['role'], '#64748b')
    statut_cls = 'ok' if row['statut'] == 'OK' else 'ko'
    statut_dot = '●'
    hp = row['hausse_pct'] * 100
    hausse_color = '#3fb950' if hp > 0 else '#8b949e' if hp == 0 else '#f85149'

    html.append(
        '<tr>'
        f'<td class="left bold">{brand_tag(row["marque"], cfg["star_brands"])}</td>'
        f'<td class="left"><span class="role-dot" style="background:{color};"></span>'
        f'{row["role"]}</td>'
        f'<td class="left">{row["format"]}</td>'
        f'<td class="center">{row["vol"]:.2f}</td>'
        f'<td class="bold">{fmt(row["pvf"])}</td>'
        f'<td>{fmt(row["p_litre"])}</td>'
        f'<td class="{statut_cls}">{row["idx_pl"]} {statut_dot}</td>'
        f'<td class="bold">{fmt(row["prop_pvf"])}</td>'
        f'<td style="color:{hausse_color};">{fmt(row["hausse"])} ({hp:+.1f}%)</td>'
        f'<td class="muted">{safe_pct(row["marge_ds_pct"])}</td>'
        f'<td class="muted">{safe_pct(row["marge_pdv_pct"])}</td>'
        '</tr>'
    )
html.append('</tbody></table>')
st.markdown(''.join(html), unsafe_allow_html=True)


# =============================================================================
# ANALYSE CONCURRENTIELLE (uniquement BG)
# =============================================================================
if cfg['has_competitors']:
    st.markdown("### Analyse concurrentielle")
    st.caption("Comparaison STAR vs Concurrents sur le prix au litre moyen.")

    ref_pl = cfg['ref_pl']
    agg = d.groupby('type')['p_litre'].mean().round(0)

    c1, c2 = st.columns(2)
    with c1:
        star_val = agg.get('STAR', 0)
        comp_val = agg.get('Concurrent', 0)
        st.markdown(f"""
        <div class="kpi-tile" style="padding:1rem 1.2rem;">
            <div class="lab">Prix / L moyen STAR</div>
            <div class="val" style="font-size:1.6rem; color:#a5b4fc;">
                {star_val:,.0f} Ar
            </div>
            <div style="font-size:0.75rem; color:#8b949e; margin-top:6px;">
                Index vs référence : {(star_val/ref_pl*100):.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="kpi-tile" style="padding:1rem 1.2rem;">
            <div class="lab">Prix / L moyen Concurrents</div>
            <div class="val" style="font-size:1.6rem; color:#cbd5e1;">
                {comp_val:,.0f} Ar
            </div>
            <div style="font-size:0.75rem; color:#8b949e; margin-top:6px;">
                Index vs référence : {(comp_val/ref_pl*100):.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Écart par rôle
    st.markdown("##### Écart de positionnement par rôle")
    roles_present = [r for r in ['Entry', 'Frequency', 'Upsize', 'Upscale']
                     if r in d['role_simple'].unique()]
    for role in roles_present:
        sub = d[d['role_simple'] == role]
        s = sub[sub['type'] == 'STAR']['p_litre'].mean()
        c = sub[sub['type'] == 'Concurrent']['p_litre'].mean()
        if pd.isna(s) or pd.isna(c) or c == 0:
            continue
        ecart = (s - c) / c * 100
        color = '#f85149' if ecart > 15 else '#d29922' if ecart > 5 else '#3fb950'
        sign = 'plus cher' if ecart > 0 else 'moins cher'
        st.markdown(
            f"<div style='padding:8px 12px; background:#161b22; "
            f"border-left:3px solid {color}; border-radius:6px; margin-bottom:6px;'>"
            f"<b style='color:#e6edf3;'>{role}</b> — STAR est "
            f"<span style='color:{color}; font-weight:600;'>"
            f"{abs(ecart):.0f}% {sign}</span> que la concurrence "
            f"<span style='color:#8b949e; font-size:0.8rem;'>"
            f"(STAR {s:,.0f} vs Concur. {c:,.0f} Ar/L)</span></div>",
            unsafe_allow_html=True)


# =============================================================================
# DÉTAILS EN ONGLETS
# =============================================================================
st.markdown("### Détails par SKU")
tab1, tab2, tab3 = st.tabs(["Prix & Index", "Marges 2026", "Marges 2027"])

# --- TAB 1 : Prix & Index
with tab1:
    html = ['<table class="obppc"><thead><tr>',
            '<th class="left">Marque</th>',
            '<th class="left">Format</th>',
            '<th colspan="4">2026</th>',
            '<th colspan="4">2027</th>',
            '<th class="left">Commentaire</th>',
            '</tr><tr>',
            '<th></th><th></th>',
            '<th>PVF</th><th>P/L</th><th>Idx PVF</th><th>Idx P/L</th>',
            '<th>PVF</th><th>P/L</th><th>Idx P/L</th><th>Hausse</th>',
            '<th></th>',
            '</tr></thead><tbody>']
    for _, row in d.iterrows():
        statut_cls = 'ok' if row['statut'] == 'OK' else 'ko'
        html.append(
            '<tr>'
            f'<td class="left bold">{brand_tag(row["marque"], cfg["star_brands"])}</td>'
            f'<td class="left">{row["format"]}</td>'
            f'<td>{fmt(row["pvf"])}</td>'
            f'<td>{fmt(row["p_litre"])}</td>'
            f'<td class="muted">{row["idx_pvf"]}</td>'
            f'<td class="{statut_cls}">{row["idx_pl"]}</td>'
            f'<td>{fmt(row["prop_pvf"])}</td>'
            f'<td>{fmt(row["prop_p_litre"])}</td>'
            f'<td class="muted">{row["idx_pl_prop"]}</td>'
            f'<td>{row["hausse_pct"]*100:+.1f}%</td>'
            f'<td class="left muted">{row["commentaire"]}</td>'
            '</tr>'
        )
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)
    st.caption(f"**Idx PVF** réf. {cfg['ref_label_pvf']} · "
               f"**Idx P/L** réf. {cfg['ref_label_pl']}")

# --- TAB 2 : Marges 2026
with tab2:
    html = ['<table class="obppc"><thead><tr>',
            '<th class="left">Marque</th>',
            '<th class="left">Format</th>',
            '<th>PVA</th><th>PV DS</th><th>Marge DS</th><th>Taux DS</th>',
            '<th>PVC</th><th>Marge PDV</th><th>Taux PDV</th>',
            '</tr></thead><tbody>']
    for _, row in d.iterrows():
        html.append(
            '<tr>'
            f'<td class="left bold">{brand_tag(row["marque"], cfg["star_brands"])}</td>'
            f'<td class="left">{row["format"]}</td>'
            f'<td>{fmt(row["pva"])}</td>'
            f'<td>{fmt(row["pv_ds"])}</td>'
            f'<td>{fmt(row["marge_ds"])}</td>'
            f'<td class="muted">{safe_pct(row["marge_ds_pct"])}</td>'
            f'<td>{fmt(row["pvc"])}</td>'
            f'<td>{fmt(row["marge_pdv"])}</td>'
            f'<td class="muted">{safe_pct(row["marge_pdv_pct"])}</td>'
            '</tr>'
        )
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)

# --- TAB 3 : Marges 2027
with tab3:
    html = ['<table class="obppc"><thead><tr>',
            '<th class="left">Marque</th>',
            '<th class="left">Format</th>',
            '<th>PVA 27</th><th>DS 27</th><th>Marge 27</th><th>Taux DS</th>',
            '<th>PVC 27</th><th>Taux PDV</th>',
            '</tr></thead><tbody>']
    for _, row in d.iterrows():
        html.append(
            '<tr>'
            f'<td class="left bold">{brand_tag(row["marque"], cfg["star_brands"])}</td>'
            f'<td class="left">{row["format"]}</td>'
            f'<td>{fmt(row["pva_2027"])}</td>'
            f'<td>{fmt(row["pv_ds_2027"])}</td>'
            f'<td>{fmt(row["marge_ds_2027"])}</td>'
            f'<td class="muted">{safe_pct(row["marge_ds_2027_pct"])}</td>'
            f'<td>{fmt(row["pvc_2027"])}</td>'
            f'<td class="muted">{safe_pct(row["marge_pdv_2027_pct"])}</td>'
            '</tr>'
        )
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)


# =============================================================================
# EXPORT CSV
# =============================================================================
st.markdown("---")

export = d[[
    'marque', 'type', 'role', 'format', 'vol',
    'pvf', 'p_litre', 'idx_pvf', 'idx_pl',
    'prop_pvf', 'prop_p_litre', 'idx_pl_prop',
    'hausse', 'hausse_pct',
    'pva', 'pv_ds', 'marge_ds', 'marge_ds_pct',
    'pvc', 'marge_pdv', 'marge_pdv_pct',
    'pva_2027', 'pv_ds_2027', 'marge_ds_2027', 'marge_ds_2027_pct',
    'pvc_2027', 'marge_pdv_2027', 'marge_pdv_2027_pct',
    'statut', 'commentaire',
]].copy()

export = export.rename(columns={
    'marque': 'Marque', 'type': 'Type', 'role': 'Rôle OBPPC',
    'format': 'Format', 'vol': 'Volume (L)',
    'pvf': 'PVF 2026', 'p_litre': 'P/L 2026',
    'idx_pvf': 'Idx PVF', 'idx_pl': 'Idx P/L',
    'prop_pvf': 'PVF 2027', 'prop_p_litre': 'P/L 2027',
    'idx_pl_prop': 'Idx P/L 2027',
    'hausse': 'Hausse (Ar)', 'hausse_pct': 'Hausse %',
    'pva': 'PVA 2026', 'pv_ds': 'PV DS 2026',
    'marge_ds': 'Marge DS', 'marge_ds_pct': 'Taux DS',
    'pvc': 'PVC 2026', 'marge_pdv': 'Marge PDV', 'marge_pdv_pct': 'Taux PDV',
    'pva_2027': 'PVA 2027', 'pv_ds_2027': 'PV DS 2027',
    'marge_ds_2027': 'Marge DS 2027', 'marge_ds_2027_pct': 'Taux DS 2027',
    'pvc_2027': 'PVC 2027',
    'marge_pdv_2027': 'Marge PDV 2027', 'marge_pdv_2027_pct': 'Taux PDV 2027',
    'statut': 'Statut', 'commentaire': 'Commentaire',
})

st.download_button(
    f"📥 Télécharger {cat_key} (CSV)",
    data=export.to_csv(index=False).encode('utf-8'),
    file_name=f"simulateur_obppc_{cat_key.lower()}.csv",
    mime="text/csv",
)
