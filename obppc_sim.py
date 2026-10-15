import streamlit as st
import pandas as pd
import io
import re
import base64
from pathlib import Path

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

    /* Nom de marque STAR en rouge */
    .brand-star { color: #f85149 !important; font-weight: 700; }
    .brand-comp { color: #e6edf3; font-weight: 700; }

    /* Logo officiel (image PNG) */
    .brand-logo {
        display: inline-block;
        width: 22px; height: 22px;
        border-radius: 4px;
        margin-right: 7px;
        vertical-align: middle;
        object-fit: contain;
        background: #ffffff;
        padding: 1px;
        box-shadow: 0 0 0 1px rgba(255,255,255,0.12);
    }

    /* Fallback : pastille colorée avec initiale si logo manquant */
    .brand-logo-fallback {
        display: inline-flex; align-items: center; justify-content: center;
        width: 22px; height: 22px; border-radius: 4px;
        font-size: 0.62rem; font-weight: 800; color: #fff;
        margin-right: 7px; vertical-align: middle;
        text-transform: uppercase;
    }

    /* Tags STAR / CONCUR */
    .tag {
        display: inline-block; padding: 1px 6px; border-radius: 3px;
        font-size: 0.62rem; font-weight: 700; letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    .tag-star { background: #f85149; color: #fff; }
    .tag-comp { background: #484f58; color: #e6edf3; }

    .role-dot { display: inline-block; width: 8px; height: 8px;
                border-radius: 50%; margin-right: 6px; vertical-align: middle; }

    .ok { color: #3fb950; font-weight: 700; }
    .ko { color: #f85149; font-weight: 700; }

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

    .pap-info {
        background: #0c1a24; border: 1px solid #0e7490;
        border-radius: 6px; padding: 10px 14px; margin: 8px 0 14px 0;
        font-size: 0.78rem; color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# MAPPING MARQUE → FICHIER LOGO
# =============================================================================
LOGO_FILES = {
    'Beaufort':       'beaufort.png',
    'Gold':           'gold.png',
    'THB':            'thb.png',
    'Queen':          'queen.png',
    'Fresh':          'fresh.png',
    'COCA':           'coca.png',
    'WOCO':           'woco.png',
    'FANTA':          'fanta.png',
    'CAPRICE':        'caprice.png',
    'TONIC':          'tonic.png',
    'Cristal':        'cristal.png',
    'RANOVISY':       'ranovisy.png',
    'VISY GASY':      'visy_gasy.png',
    'Eau vive':       'eau_vive.png',
    'Cristalline':    'cristalline.png',
    'OLYMPIKO':       'olympiko.png',
    'NATUR EAU':      'natur_eau.png',
    'Red Bull':       'red_bull.png',
    'Monster':        'monster.png',
    'FOSA':           'fosa.png',
    'XXL':            'xxl.png',
    'DYNAMIC':        'dynamic.png',
    'BOOST VITALITY': 'boost_vitality.png',
}

BRAND_LOGOS = {
    'Beaufort':       {'color': '#c9a227', 'init': 'B'},
    'Gold':           {'color': '#d4a017', 'init': 'G'},
    'THB':            {'color': '#0e7490', 'init': 'T'},
    'Queen':          {'color': '#9d174d', 'init': 'Q'},
    'Fresh':          {'color': '#16a34a', 'init': 'F'},
    'COCA':           {'color': '#dc2626', 'init': 'C'},
    'WOCO':           {'color': '#7c3aed', 'init': 'W'},
    'FANTA':          {'color': '#ea580c', 'init': 'F'},
    'CAPRICE':        {'color': '#db2777', 'init': 'C'},
    'TONIC':          {'color': '#0891b2', 'init': 'T'},
    'Cristal':        {'color': '#0284c7', 'init': 'C'},
    'RANOVISY':       {'color': '#2563eb', 'init': 'R'},
    'VISY GASY':      {'color': '#059669', 'init': 'V'},
    'Eau vive':       {'color': '#0ea5e9', 'init': 'E'},
    'Cristalline':    {'color': '#38bdf8', 'init': 'C'},
    'OLYMPIKO':       {'color': '#1d4ed8', 'init': 'O'},
    'NATUR EAU':      {'color': '#65a30d', 'init': 'N'},
    'Red Bull':       {'color': '#1e3a8a', 'init': 'RB'},
    'Monster':        {'color': '#166534', 'init': 'M'},
    'FOSA':           {'color': '#b91c1c', 'init': 'F'},
    'XXL':            {'color': '#7c2d12', 'init': 'X'},
    'DYNAMIC':        {'color': '#a21caf', 'init': 'D'},
    'BOOST VITALITY': {'color': '#ca8a04', 'init': 'B'},
}
DEFAULT_LOGO = {'color': '#64748b', 'init': '?'}


# =============================================================================
# CHARGEMENT DES LOGOS
# =============================================================================
LOGOS_DIR = Path(__file__).parent / "logos"


@st.cache_data(show_spinner=False)
def _load_logo_b64(filename: str):
    if not filename:
        return None
    path = LOGOS_DIR / filename
    if not path.exists():
        return None
    try:
        return base64.b64encode(path.read_bytes()).decode()
    except Exception:
        return None


def brand_logo_html(marque):
    filename = LOGO_FILES.get(marque)
    b64 = _load_logo_b64(filename) if filename else None
    if b64:
        return (
            f'<img class="brand-logo" '
            f'src="data:image/png;base64,{b64}" '
            f'alt="{marque}" />'
        )
    info = BRAND_LOGOS.get(marque, DEFAULT_LOGO)
    return (
        f'<span class="brand-logo-fallback" '
        f'style="background:{info["color"]};">{info["init"]}</span>'
    )


# =============================================================================
# DONNÉES — BI
# =============================================================================
DATA_BI = [
    {'marque': 'Beaufort', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Beaufort 33CL VER', 'vol': 0.33,
     'pvf': 4000, 'prop_pvf': 4500,
     'pva': 2900, 'pv_ds': 3500, 'pvc': 4000,
     'commentaire': 'PVC +500 / PVA +400'},
    {'marque': 'Beaufort', 'role': 'Upscale (Super-Premium Niche)',
     'format': 'Beaufort 33 CL CAN', 'vol': 0.33,
     'pvf': 5000, 'prop_pvf': 5500,
     'pva': 3800, 'pv_ds': 4600, 'pvc': 5000,
     'commentaire': 'PVC Vs P/L Upscale & FRE'},
    {'marque': 'Gold', 'role': 'Entry (Entrée de gamme)',
     'format': 'Gold Blanche 33cl VER', 'vol': 0.33,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 2580, 'pv_ds': 3100, 'pvc': 3500,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Entry (Entrée de gamme)',
     'format': 'Gold 8 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blanche 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'commentaire': 'PVC Vs PVF THB 65'},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blonde 50 cl VER', 'vol': 0.50,
     'pvf': 4500, 'prop_pvf': 4800,
     'pva': 3200, 'pv_ds': 3900, 'pvc': 4500,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Gold Blonde 65 cl VER', 'vol': 0.65,
     'pvf': 5000, 'prop_pvf': 5300,
     'pva': 3600, 'pv_ds': 4320, 'pvc': 5000,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold 8 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'commentaire': ''},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold Blanche 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'commentaire': 'PVC Vs P/L Upscale & FRE'},
    {'marque': 'Gold', 'role': 'Upscale (Premium)',
     'format': 'Gold Blonde 50 cl CAN', 'vol': 0.50,
     'pvf': 6000, 'prop_pvf': 6500,
     'pva': 4500, 'pv_ds': 5400, 'pvc': 6000,
     'commentaire': ''},
    {'marque': 'THB', 'role': 'Entry (Entrée de gamme)',
     'format': 'THB Pilsener 33 cl VER', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1900, 'pv_ds': 2280, 'pvc': 2500,
     'commentaire': ''},
    {'marque': 'THB', 'role': 'Frequency (Cœur de gamme)',
     'format': 'THB Pilsener 65 cl VER', 'vol': 0.65,
     'pvf': 4500, 'prop_pvf': 4700,
     'pva': 3250, 'pv_ds': 3900, 'pvc': 4500,
     'commentaire': 'PVA Vs Marge PDV'},
    {'marque': 'THB', 'role': 'Upscale (Premium)',
     'format': 'THB Pilsener 50 cl CAN', 'vol': 0.50,
     'pvf': 5000, 'prop_pvf': 5200,
     'pva': 3800, 'pv_ds': 4560, 'pvc': 5000,
     'commentaire': 'PVC +200 / PVA +300'},
    {'marque': 'Queen', 'role': 'Entry (Entrée de gamme)',
     'format': "Queen s 65 cl VER", 'vol': 0.65,
     'pvf': 4000, 'prop_pvf': 4200,
     'pva': 3000, 'pv_ds': 3600, 'pvc': 4000,
     'commentaire': ''},
    {'marque': 'Fresh', 'role': 'Entry (Entrée de gamme)',
     'format': 'THB Fresh 33 cl VER', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1900, 'pv_ds': 2280, 'pvc': 2500,
     'commentaire': ''},
    {'marque': 'Fresh', 'role': 'Frequency (Cœur de gamme)',
     'format': 'THB Fresh 65 cl VER', 'vol': 0.65,
     'pvf': 4000, 'prop_pvf': 4200,
     'pva': 3000, 'pv_ds': 3600, 'pvc': 4000,
     'commentaire': 'PVC Vs P/L Entry'},
    {'marque': 'Fresh', 'role': 'Upscale (Premium)',
     'format': 'FRESH 33 cl CAN', 'vol': 0.33,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 2650, 'pv_ds': 3200, 'pvc': 3500,
     'commentaire': 'Réduct° prix Vs Perf marque'},
]


# =============================================================================
# DONNÉES — BG
# =============================================================================
DATA_BG = [
    {'marque': 'COCA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35 (N°1 vente en col)', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1380, 'pv_ds': 1380, 'pvc': 1500,
     'commentaire': ''},
    {'marque': 'COCA', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 0, 'pv_ds': 0, 'pvc': 2000,
     'commentaire': ''},
    {'marque': 'COCA', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 0, 'pv_ds': 0, 'pvc': 2500,
     'commentaire': ''},
    {'marque': 'COCA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 4480, 'pv_ds': 4480, 'pvc': 5000,
     'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1080, 'pv_ds': 1300, 'pvc': 1500,
     'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 1465, 'pv_ds': 1758, 'pvc': 2000,
     'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1850, 'pv_ds': 2220, 'pvc': 2500,
     'commentaire': 'PVA +150 / PVC inchangé'},
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 30', 'vol': 0.30,
     'pvf': 1200, 'prop_pvf': 1200,
     'pva': 875, 'pv_ds': 1050, 'pvc': 1200,
     'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 3650, 'pv_ds': 4380, 'pvc': 5000,
     'commentaire': ''},
    {'marque': 'WOCO', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 100', 'vol': 1.00,
     'pvf': 3000, 'prop_pvf': 3000,
     'pva': 2180, 'pv_ds': 2616, 'pvc': 3000,
     'commentaire': ''},
    {'marque': 'FANTA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35 (N°1 vente en col)', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1370, 'pv_ds': 1370, 'pvc': 1500,
     'commentaire': ''},
    {'marque': 'FANTA', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 0, 'pv_ds': 0, 'pvc': 2000,
     'commentaire': ''},
    {'marque': 'FANTA', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 4410, 'pv_ds': 4410, 'pvc': 5000,
     'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 35', 'vol': 0.35,
     'pvf': 1500, 'prop_pvf': 1500,
     'pva': 1080, 'pv_ds': 1300, 'pvc': 1500,
     'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 50', 'vol': 0.50,
     'pvf': 2000, 'prop_pvf': 2000,
     'pva': 1465, 'pv_ds': 1758, 'pvc': 2000,
     'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1850, 'pv_ds': 2220, 'pvc': 2500,
     'commentaire': 'PVA +150 / PVC inchangé'},
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 30', 'vol': 0.30,
     'pvf': 1200, 'prop_pvf': 1200,
     'pva': 875, 'pv_ds': 1050, 'pvc': 1200,
     'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'PET 150', 'vol': 1.50,
     'pvf': 5000, 'prop_pvf': 5000,
     'pva': 3650, 'pv_ds': 4380, 'pvc': 5000,
     'commentaire': ''},
    {'marque': 'CAPRICE', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 100', 'vol': 1.00,
     'pvf': 3000, 'prop_pvf': 3000,
     'pva': 2180, 'pv_ds': 2616, 'pvc': 3000,
     'commentaire': ''},
    {'marque': 'TONIC', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 30', 'vol': 0.30,
     'pvf': 1200, 'prop_pvf': 1800,
     'pva': 875, 'pv_ds': 1050, 'pvc': 1200,
     'commentaire': ''},
    {'marque': 'TONIC', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 100', 'vol': 1.00,
     'pvf': 3000, 'prop_pvf': 3500,
     'pva': 2180, 'pv_ds': 2616, 'pvc': 3000,
     'commentaire': ''},
]


# =============================================================================
# DONNÉES — EAUX
# =============================================================================
DATA_EAUX = [
    {'marque': 'Cristal', 'role': 'Entry (Entrée de gamme)',
     'format': 'Cristal 30 cl VER', 'vol': 0.30,
     'pvf': 1500, 'prop_pvf': 2000,
     'pva': 1130, 'pv_ds': 1350, 'pvc': 1500,
     'commentaire': ''},
    {'marque': 'Cristal', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Cristal 50 cl VER', 'vol': 0.50,
     'pvf': 2200, 'prop_pvf': 3000,
     'pva': 1600, 'pv_ds': 1752, 'pvc': 2200,
     'commentaire': ''},
    {'marque': 'Cristal', 'role': 'Upscale (Premium)',
     'format': 'Cristal 100 cl VER', 'vol': 1.00,
     'pvf': 3800, 'prop_pvf': 5000,
     'pva': 2750, 'pv_ds': 3270, 'pvc': 3800,
     'commentaire': ''},
    {'marque': 'Cristal', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Cristal 150 cl PET', 'vol': 1.50,
     'pvf': 5500, 'prop_pvf': 6500,
     'pva': 4265, 'pv_ds': 5080, 'pvc': 5500,
     'commentaire': ''},
    {'marque': 'RANOVISY', 'role': 'Entry (Entrée de gamme)',
     'format': 'RANOVISY 33 PET', 'vol': 0.33,
     'pvf': 1000, 'prop_pvf': 1000,
     'pva': 570, 'pv_ds': 700, 'pvc': 1000,
     'commentaire': ''},
    {'marque': 'RANOVISY', 'role': 'Frequency (Cœur de gamme)',
     'format': 'RANOVISY 50 CL PET', 'vol': 0.50,
     'pvf': 2300, 'prop_pvf': 2300,
     'pva': 1800, 'pv_ds': 2000, 'pvc': 2300,
     'commentaire': ''},
    {'marque': 'RANOVISY', 'role': 'Upsize (Grand format)',
     'format': 'RANOVISY 75 PET', 'vol': 0.75,
     'pvf': 1800, 'prop_pvf': 1800,
     'pva': 1260, 'pv_ds': 1700, 'pvc': 1800,
     'commentaire': ''},
    {'marque': 'VISY GASY', 'role': 'Entry (Entrée de gamme)',
     'format': 'VISY GASY 60 PET', 'vol': 0.60,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1920, 'pv_ds': 2000, 'pvc': 2500,
     'commentaire': ''},
    {'marque': 'VISY GASY', 'role': 'Entry (Entrée de gamme)',
     'format': 'VISY GASY 100 PET', 'vol': 1.00,
     'pvf': 3000, 'prop_pvf': 3000,
     'pva': 2640, 'pv_ds': 2750, 'pvc': 3000,
     'commentaire': ''},
    {'marque': 'Eau vive', 'role': 'Entry (Entrée de gamme)',
     'format': 'Eau vive 50 cl PET', 'vol': 0.50,
     'pvf': 1600, 'prop_pvf': 1600,
     'pva': 1235, 'pv_ds': 1492, 'pvc': 1600,
     'commentaire': ''},
    {'marque': 'Eau vive', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Eau vive 150 cl PET', 'vol': 1.50,
     'pvf': 3300, 'prop_pvf': 3300,
     'pva': 2465, 'pv_ds': 2979, 'pvc': 3300,
     'commentaire': ''},
    {'marque': 'Eau vive', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Eau vive 50 cl VER', 'vol': 0.50,
     'pvf': 2200, 'prop_pvf': 3000,
     'pva': 1600, 'pv_ds': 1950, 'pvc': 2200,
     'commentaire': ''},
    {'marque': 'Cristalline', 'role': 'Frequency (Cœur de gamme)',
     'format': 'Cristalline 100 cl PET', 'vol': 1.00,
     'pvf': 2100, 'prop_pvf': 2200,
     'pva': 1550, 'pv_ds': 1876, 'pvc': 2100,
     'commentaire': '+ 100 PVC / + 150 PVQ'},
    {'marque': 'Cristalline', 'role': 'Upsize (Grand format)',
     'format': 'Cristalline 200 cl PET', 'vol': 2.00,
     'pvf': 3600, 'prop_pvf': 3800,
     'pva': 2680, 'pv_ds': 3240, 'pvc': 3600,
     'commentaire': ''},
    {'marque': 'OLYMPIKO', 'role': 'Entry (Entrée de gamme)',
     'format': 'OLYMPIKO 50', 'vol': 0.50,
     'pvf': 1200, 'prop_pvf': 1200,
     'pva': 0, 'pv_ds': 1090, 'pvc': 1200,
     'commentaire': ''},
    {'marque': 'OLYMPIKO', 'role': 'Frequency (Cœur de gamme)',
     'format': 'OLYMPIKO 100', 'vol': 1.00,
     'pvf': 1900, 'prop_pvf': 1900,
     'pva': 1050, 'pv_ds': 1300, 'pvc': 1900,
     'commentaire': ''},
    {'marque': 'OLYMPIKO', 'role': 'Upsize (Grand format)',
     'format': 'OLYMPIKO 150', 'vol': 1.50,
     'pvf': 2400, 'prop_pvf': 2400,
     'pva': 1800, 'pv_ds': 2000, 'pvc': 2400,
     'commentaire': ''},
    {'marque': 'NATUR EAU', 'role': 'Entry (Entrée de gamme)',
     'format': 'NATUR EAU 50', 'vol': 0.50,
     'pvf': 1300, 'prop_pvf': 1300,
     'pva': 1040, 'pv_ds': 1208, 'pvc': 1300,
     'commentaire': ''},
    {'marque': 'NATUR EAU', 'role': 'Frequency (Cœur de gamme)',
     'format': 'NATUR EAU 100', 'vol': 1.00,
     'pvf': 1800, 'prop_pvf': 1800,
     'pva': 1380, 'pv_ds': 1625, 'pvc': 1800,
     'commentaire': ''},
    {'marque': 'NATUR EAU', 'role': 'Upsize (Grand format)',
     'format': 'NATUR EAU 150', 'vol': 1.50,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1850, 'pv_ds': 2250, 'pvc': 2500,
     'commentaire': ''},
]


# =============================================================================
# DONNÉES — ENERGY
# =============================================================================
DATA_ENERGY = [
    {'marque': 'Red Bull', 'role': 'Upscale (Premium)',
     'format': 'CAN 25', 'vol': 0.25,
     'pvf': 9900, 'prop_pvf': 9900,
     'pva': 0, 'pv_ds': 0, 'pvc': 9900,
     'commentaire': 'Exclusivement moderne trade'},
    {'marque': 'Monster', 'role': 'Upscale (Premium)',
     'format': 'CAN 50', 'vol': 0.50,
     'pvf': 9900, 'prop_pvf': 9900,
     'pva': 0, 'pv_ds': 0, 'pvc': 9900,
     'commentaire': 'Exclusivement moderne trade'},
    {'marque': 'FOSA', 'role': 'Upscale (Premium)',
     'format': 'CAN 50', 'vol': 0.50,
     'pvf': 5000, 'prop_pvf': 5500,
     'pva': 3830, 'pv_ds': 4596, 'pvc': 5000,
     'commentaire': '414 PVA / 500 PVC'},
    {'marque': 'XXL', 'role': 'Entry (Entrée de gamme)',
     'format': 'VC 30', 'vol': 0.30,
     'pvf': 2500, 'prop_pvf': 2500,
     'pva': 1750, 'pv_ds': 2100, 'pvc': 2500,
     'commentaire': ''},
    {'marque': 'XXL', 'role': 'Frequency (Cœur de gamme)',
     'format': 'PET 35', 'vol': 0.35,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 2600, 'pv_ds': 3120, 'pvc': 3500,
     'commentaire': 'Réduction PET : -500Ar / Soit augmenter la FOSA à 7000Ar Vs Index P/L 140'},
    {'marque': 'XXL', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 4000, 'prop_pvf': 4000,
     'pva': 3000, 'pv_ds': 3600, 'pvc': 4000,
     'commentaire': 'Réduction PET : -500Ar / Soit augmenter la CAN Vs index P/L 140'},
    {'marque': 'DYNAMIC', 'role': 'Upscale (Premium)',
     'format': 'CAN 25', 'vol': 0.25,
     'pvf': 3500, 'prop_pvf': 3500,
     'pva': 3000, 'pv_ds': 3000, 'pvc': 3500,
     'commentaire': ''},
    {'marque': 'BOOST VITALITY', 'role': 'Upscale (Premium)',
     'format': 'CAN 33', 'vol': 0.33,
     'pvf': 4000, 'prop_pvf': 4000,
     'pva': 3335, 'pv_ds': 3335, 'pvc': 4000,
     'commentaire': ''},
]


# =============================================================================
# CONFIGURATION PAR CATÉGORIE
# =============================================================================
CATEGORIES = {
    'BI': {
        'label': 'BI — Bière',
        'data': DATA_BI,
        'ref_pvf': 4500,
        'ref_pl': 4500 / 0.65,
        'ref_label_pvf': 'THB Pilsener 65 cl VER',
        'ref_label_pl': 'THB Pilsener 65 cl VER',
        'star_brands': None,
        'has_competitors': False,
    },
    'BG': {
        'label': 'BG — Boissons Gazeuses',
        'data': DATA_BG,
        'ref_pvf': 2000,
        'ref_pl': 2000 / 0.50,
        'ref_label_pvf': 'CAPRICE PET 50 cl',
        'ref_label_pl': 'CAPRICE PET 50 cl',
        'star_brands': {'WOCO', 'CAPRICE', 'TONIC'},
        'has_competitors': True,
    },
    'EAUX': {
        'label': 'EAUX — Eaux',
        'data': DATA_EAUX,
        'ref_pvf': 2100,
        'ref_pl': 2100 / 1.00,
        'ref_label_pvf': 'Cristalline 100 cl PET',
        'ref_label_pl': 'Cristalline 100 cl PET',
        'star_brands': {'Cristal', 'Cristalline', 'Eau vive'},
        'has_competitors': True,
    },
    'ENERGY': {
        'label': 'ENERGY — Boissons Énergisantes',
        'data': DATA_ENERGY,
        'ref_pvf': 3500,
        'ref_pl': 3500 / 0.35,
        'ref_label_pvf': 'XXL PET 35 cl',
        'ref_label_pl': 'XXL PET 35 cl',
        'star_brands': {'XXL', 'FOSA', 'BOOST VITALITY'},
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


def brand_name_html(marque, star_brands):
    logo = brand_logo_html(marque)
    if star_brands is None or marque in star_brands:
        name = f'<span class="brand-star">{marque}</span>'
    else:
        name = f'<span class="brand-comp">{marque}</span>'
    return f'{logo}{name}'


def brand_tag(marque, star_brands):
    if star_brands is None or marque in star_brands:
        return '<span class="tag tag-star">STAR</span>'
    return '<span class="tag tag-comp">CONCUR</span>'


def _detect_emballage(format_str):
    f = str(format_str).upper()
    if 'PET' in f:  return 'PET'
    if 'CAN' in f:  return 'CAN'
    if 'VER' in f or 'VERRE' in f: return 'VERRE'
    if 'VC' in f:   return 'VERRE'
    return None


def _normalize(s):
    s = str(s).upper().strip()
    s = (s.replace(' ', '')
          .replace("'", '')
          .replace('’', '')
          .replace('-', '')
          .replace('_', ''))
    accents = {
        'É': 'E', 'È': 'E', 'Ê': 'E', 'Ë': 'E',
        'À': 'A', 'Â': 'A', 'Ä': 'A',
        'Î': 'I', 'Ï': 'I',
        'Ô': 'O', 'Ö': 'O',
        'Ù': 'U', 'Û': 'U', 'Ü': 'U',
        'Ç': 'C',
    }
    for k, v in accents.items():
        s = s.replace(k, v)
    return s


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

    d['marge_ds'] = d['pv_ds'] - d['pva']
    d['marge_ds_pct'] = d['marge_ds'] / d['pva'].replace(0, pd.NA)
    d['marge_pdv'] = d['pvc'] - d['pv_ds']
    d['marge_pdv_pct'] = d['marge_pdv'] / d['pv_ds'].replace(0, pd.NA)

    d['hausse'] = d['prop_pvf'] - d['pvf']
    d['hausse_pct'] = d['hausse'] / d['pvf']

    d['pva_2027'] = d['pva'] + d['hausse']
    d['pv_ds_2027'] = d['pv_ds'] + d['hausse']
    d['marge_ds_2027'] = d['pv_ds_2027'] - d['pva_2027']
    d['marge_ds_2027_pct'] = d['marge_ds_2027'] / d['pva_2027'].replace(0, pd.NA)
    d['pvc_2027'] = d['prop_pvf']
    d['marge_pdv_2027'] = d['pvc_2027'] - d['pv_ds_2027']
    d['marge_pdv_2027_pct'] = d['marge_pdv_2027'] / d['pv_ds_2027'].replace(0, pd.NA)

    d['role_simple'] = d['role'].apply(role_simple)
    d['statut'] = d.apply(
        lambda r: status_from_idx(r['idx_pl'], r['role_simple']), axis=1)

    if cfg['star_brands'] is None:
        d['type'] = 'STAR'
    else:
        d['type'] = d['marque'].apply(
            lambda m: 'STAR' if m in cfg['star_brands'] else 'Concurrent')
    return d


# =============================================================================
# SESSION STATE INIT
# =============================================================================
if 'pap_max_data' not in st.session_state:
    st.session_state.pap_max_data = {}

if 'commentaires' not in st.session_state:
    st.session_state.commentaires = {}


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
            if (k.startswith('prop_editor')
                or k.startswith('pap_editor')
                or k.startswith('comment_editor')
                or k == 'commentaires'):
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
# SECTION PAP — Import CR PANEL (Excel) / Saisie manuelle
# =============================================================================
st.markdown("### PAP — Prix d'Achat Produit")
st.markdown(
    '<div class="pap-info">'
    '<b style="color:#a5b4fc;">💡 Logique PAP</b><br>'
    '• <b>PAP min</b> = <b>PVC</b> (donnée OBPPC existante)<br>'
    '• <b>PAP max</b> = colonne <code>Prix de vente</code> du fichier '
    '<b>CR PANEL</b> (feuille <code>Saisie</code>), agrégée par SKU.'
    '</div>',
    unsafe_allow_html=True)


MAPPING_MARQUE = {
    'WOCO': 'WORLD COLA',
    'COCA': 'COCA COLA',
    'FANTA': 'FANTA',
    'CAPRICE': 'CAPRICE',
    'TONIC': 'TONIC',
    'CRISTAL': 'CRISTAL',
    'CRISTALLINE': 'CRISTALLINE',
    'EAU VIVE': 'EAU VIVE',
    'RANOVISY': 'RANO VISY',
    'VISY GASY': 'VISY GASY',
    'OLYMPIKO': 'OLYMPIKO',
    'NATUR EAU': "NATUR'EAU",
    'BEAUFORT': 'BEAUFORT',
    'GOLD': 'GOLD',
    'THB': 'THB',
    'QUEEN': 'QUEENS',
    'FRESH': 'FRESH',
    'XXL': 'XXL',
    'FOSA': 'FOSA',
    'BOOST VITALITY': 'BOOST',
    'DYNAMIC': 'DYNAMIC',
    'RED BULL': 'RED BULL',
    'MONSTER': 'MONSTER',
}


pap_tab1, pap_tab2 = st.tabs(["📥 Importer CR PANEL (Excel)", "✏️ Saisie manuelle"])

with pap_tab1:
    uploaded = st.file_uploader(
        "Charger le fichier CR PANEL (Excel)",
        type=['xlsx', 'xls'],
        help="Feuille 'Saisie' avec colonnes : Nom Produit, "
             "Format (en cl), Emballage, Prix de vente")

    if uploaded is not None:
        try:
            df_cr = pd.read_excel(uploaded, sheet_name='Saisie')

            required_cols = ['Nom Produit', 'Format (en cl)', 'Emballage', 'Prix de vente']
            missing = [c for c in required_cols if c not in df_cr.columns]
            if missing:
                st.error(f"Colonnes manquantes dans la feuille 'Saisie' : {missing}")
            else:
                df_cr = df_cr[required_cols].copy()
                df_cr.columns = ['nom_produit', 'format_cl', 'emballage', 'prix_vente']

                df_cr['nom_produit'] = (
                    df_cr['nom_produit'].astype(str).str.upper().str.strip()
                )
                df_cr['emballage'] = (
                    df_cr['emballage'].astype(str).str.upper().str.strip()
                )
                df_cr['format_cl'] = pd.to_numeric(df_cr['format_cl'], errors='coerce')
                df_cr['prix_vente'] = pd.to_numeric(df_cr['prix_vente'], errors='coerce')
                df_cr = df_cr.dropna(subset=['format_cl', 'prix_vente'])

                df_cr['nom_norm'] = df_cr['nom_produit'].apply(_normalize)

                pap_max_dict = {}
                non_trouves = []

                for _, row in df.iterrows():
                    marque_obppc = str(row['marque']).upper().strip()
                    format_obppc = row['format']
                    vol_obppc = float(row['vol'])
                    vol_cl = round(vol_obppc * 100)

                    emb_obppc = _detect_emballage(format_obppc)

                    nom_cr = MAPPING_MARQUE.get(marque_obppc, marque_obppc)
                    nom_cr_norm = _normalize(nom_cr)

                    mask = df_cr['nom_norm'].str.contains(
                        re.escape(nom_cr_norm), case=False, na=False
                    ) & (df_cr['format_cl'] == vol_cl)

                    if emb_obppc:
                        mask &= (df_cr['emballage'] == emb_obppc)

                    match = df_cr[mask]
                    if not match.empty:
                        pap_max = float(match['prix_vente'].max())
                        pap_max_dict[(row['marque'], format_obppc)] = pap_max
                    else:
                        non_trouves.append(f"{row['marque']} | {format_obppc}")

                st.session_state.pap_max_data = pap_max_dict

                if pap_max_dict:
                    st.success(f"✅ {len(pap_max_dict)} PAP max trouvés dans le CR PANEL.")
                else:
                    st.warning("Aucun PAP max trouvé. Vérifie les correspondances.")

                if non_trouves:
                    with st.expander(f"⚠️ {len(non_trouves)} SKU sans correspondance"):
                        for s in non_trouves:
                            st.text(s)

        except Exception as e:
            st.error(f"Erreur de lecture du fichier Excel : {e}")

with pap_tab2:
    st.caption("Saisissez les PAP max directement. Le PAP min est égal au PVC.")
    pap_edit_rows = []
    for _, row in df.iterrows():
        key = (row['marque'], row['format'])
        current_max = st.session_state.pap_max_data.get(key, 0)
        pap_edit_rows.append({
            'marque': row['marque'],
            'format': row['format'],
            'pvc': row['pvc'],
            'pap_min': row['pvc'],
            'pap_max': int(current_max) if pd.notna(current_max) else 0,
        })
    pap_edit_df = pd.DataFrame(pap_edit_rows)

    pap_edited = st.data_editor(
        pap_edit_df,
        column_config={
            'marque': st.column_config.TextColumn("Marque", disabled=True, width=100),
            'format': st.column_config.TextColumn("Format", disabled=True, width=220),
            'pvc': st.column_config.NumberColumn("PVC", disabled=True, format="%d", width=100),
            'pap_min': st.column_config.NumberColumn("PAP min (=PVC)", disabled=True,
                                                     format="%d", width=120),
            'pap_max': st.column_config.NumberColumn("PAP max (Ar)", min_value=0, step=50,
                                                     format="%d", width=130),
        },
        hide_index=True,
        use_container_width=True,
        num_rows="fixed",
        height=min(400, 80 + 36 * len(pap_edit_df)),
        key=f"pap_editor_{cat_key}",
    )

    for _, r in pap_edited.iterrows():
        key = (r['marque'], r['format'])
        st.session_state.pap_max_data[key] = float(r['pap_max'])


# =============================================================================
# ÉDITEUR PRIX
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
    for col in ['role', 'vol', 'commentaire']:
        edited[col] = df[col].reset_index(drop=True).values

d = compute(edited, cfg)

# Réinjection PAP
d['pap_min'] = d['pvc']
d['pap_max'] = d.apply(
    lambda r: st.session_state.pap_max_data.get(
        (r['marque'], r['format']), 0
    ), axis=1)

d['marge_pdv_pap_min'] = d['pap_min'] - d['pvc']
d['marge_pdv_pap_min_pct'] = d['marge_pdv_pap_min'] / d['pvc'].replace(0, pd.NA)
d['marge_pdv_pap_max'] = d['pap_max'] - d['pvc']
d['marge_pdv_pap_max_pct'] = d['marge_pdv_pap_max'] / d['pvc'].replace(0, pd.NA)

# Réinjection commentaires édités (session_state prioritaire)
d['commentaire'] = d.apply(
    lambda r: st.session_state.commentaires.get(
        (r['marque'], r['format']), r.get('commentaire', '')
    ), axis=1)


# =============================================================================
# KPI
# =============================================================================
n_ok = int((d['statut'] == 'OK').sum())
n_total = len(d)
taux = n_ok / n_total * 100 if n_total else 0
n_pap = int((d['pap_max'] > 0).sum())

if cfg['has_competitors']:
    n_star = int((d['type'] == 'STAR').sum())
    n_comp = int((d['type'] == 'Concurrent').sum())
    kpi_html = f"""
    <div class="kpi-band">
        <div class="kpi-tile"><div class="lab">SKU STAR</div><div class="val">{n_star}</div></div>
        <div class="kpi-tile"><div class="lab">SKU Concurrents</div><div class="val">{n_comp}</div></div>
        <div class="kpi-tile"><div class="lab">Conformes</div>
            <div class="val" style="color:{'#3fb950' if taux>=70 else '#d29922' if taux>=40 else '#f85149'};">
                {n_ok}/{n_total}</div></div>
        <div class="kpi-tile"><div class="lab">Hausse moyenne</div>
            <div class="val">{d['hausse_pct'].mean()*100:+.1f}%</div></div>
        <div class="kpi-tile"><div class="lab">PAP renseignés</div>
            <div class="val">{n_pap}/{n_total}</div></div>
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
        <div class="kpi-tile"><div class="lab">PAP renseignés</div>
            <div class="val">{n_pap}/{n_total}</div></div>
    </div>
    """
st.markdown(kpi_html, unsafe_allow_html=True)


# =============================================================================
# TABLEAU PRINCIPAL  (logo + nom STAR en rouge)
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
        '<th>PAP min</th>',
        '<th>PAP max</th>',
        '<th>Marge PDV/PAP max</th>',
        '</tr></thead><tbody>']

for _, row in d.iterrows():
    color = ROLE_COLORS.get(row['role'], '#64748b')
    statut_cls = 'ok' if row['statut'] == 'OK' else 'ko'
    hp = row['hausse_pct'] * 100
    hausse_color = '#3fb950' if hp > 0 else '#8b949e' if hp == 0 else '#f85149'

    pap_min_txt = fmt(row['pap_min'])
    if row['pap_max'] > 0:
        pap_max_txt = fmt(row['pap_max'])
        marge_pap = safe_pct(row['marge_pdv_pap_max_pct'])
    else:
        pap_max_txt = '<span class="muted">—</span>'
        marge_pap = '<span class="muted">—</span>'

    html.append(
        '<tr>'
        f'<td class="left bold">{brand_name_html(row["marque"], cfg["star_brands"])}</td>'
        f'<td class="left"><span class="role-dot" style="background:{color};"></span>'
        f'{row["role"]}</td>'
        f'<td class="left">{row["format"]}</td>'
        f'<td class="center">{row["vol"]:.2f}</td>'
        f'<td class="bold">{fmt(row["pvf"])}</td>'
        f'<td>{fmt(row["p_litre"])}</td>'
        f'<td class="{statut_cls}">{row["idx_pl"]} ●</td>'
        f'<td class="bold">{fmt(row["prop_pvf"])}</td>'
        f'<td style="color:{hausse_color};">{fmt(row["hausse"])} ({hp:+.1f}%)</td>'
        f'<td>{pap_min_txt}</td>'
        f'<td>{pap_max_txt}</td>'
        f'<td class="muted">{marge_pap}</td>'
        '</tr>'
    )
html.append('</tbody></table>')
st.markdown(''.join(html), unsafe_allow_html=True)


# =============================================================================
# ANALYSE CONCURRENTIELLE
# =============================================================================
if cfg['has_competitors']:
    st.markdown("---")
    st.markdown("### Analyse concurrentielle")
    st.caption("Comparaison STAR vs Concurrents sur le prix au litre moyen.")

    ref_pl = cfg['ref_pl']
    agg = d.groupby('type')['p_litre'].mean().round(0)

    c1, c2 = st.columns(2)
    with c1:
        star_val = agg.get('STAR', 0)
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
        comp_val = agg.get('Concurrent', 0)
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

    # =========================================================================
    # COMPARAISON PAR CONTENANCE — trié du PVF le plus bas au plus élevé
    # =========================================================================
    st.markdown("---")
    st.markdown("##### Comparaison par contenance — tous formats confondus")
    st.caption("Regroupement par volume (L), trié du PVF le plus bas au plus élevé.")

    volumes = sorted(d['vol'].unique())

    for vol_ in volumes:
        sub = d[d['vol'] == vol_]
        if sub.empty:
            continue

        star_rows = sub[sub['type'] == 'STAR']
        comp_rows = sub[sub['type'] == 'Concurrent']

        star_pl = star_rows['p_litre'].mean() if not star_rows.empty else None
        comp_pl = comp_rows['p_litre'].mean() if not comp_rows.empty else None

        if star_pl is not None and comp_pl is not None and comp_pl > 0:
            ecart = (star_pl - comp_pl) / comp_pl * 100
            if ecart > 15:
                ecart_color, ecart_label = '#f85149', f"STAR {ecart:+.0f}% plus cher"
            elif ecart > 5:
                ecart_color, ecart_label = '#d29922', f"STAR {ecart:+.0f}% plus cher"
            elif ecart < -5:
                ecart_color, ecart_label = '#3fb950', f"STAR {ecart:+.0f}% moins cher"
            else:
                ecart_color, ecart_label = '#8b949e', "Positionnement aligné"
        elif star_pl is not None and comp_pl is None:
            ecart_color, ecart_label = '#a5b4fc', "Pas de concurrent sur cette contenance"
        elif star_pl is None and comp_pl is not None:
            ecart_color, ecart_label = '#6e7681', "STAR absent sur cette contenance"
        else:
            ecart_color, ecart_label = '#8b949e', "—"

        vol_cl = int(round(vol_ * 100))
        n_sku = len(sub)

        st.markdown(
            f"<div style='background:#1a1f2b; border:1px solid #30363d; "
            f"border-radius:6px; padding:8px 12px; margin:14px 0 6px 0; "
            f"display:flex; justify-content:space-between; align-items:center;'>"
            f"<div style='font-weight:700; color:#e6edf3; font-size:0.95rem;'>"
            f"📦 {vol_cl} cl "
            f"<span style='color:#8b949e; font-weight:400; font-size:0.8rem;'>"
            f"· {n_sku} SKU</span></div>"
            f"<div style='font-size:0.75rem; color:{ecart_color}; font-weight:600;'>"
            f"{ecart_label}</div></div>",
            unsafe_allow_html=True)

        html = ['<table class="obppc"><thead><tr>',
                '<th class="left">Type</th>',
                '<th class="left">Marque</th>',
                '<th class="left">Format</th>',
                '<th class="left">Rôle</th>',
                '<th>PVF 2026</th>',
                '<th>P/L 2026</th>',
                '<th>Index P/L</th>',
                '<th>PAP min</th>',
                '<th>PAP max</th>',
                '<th>Marge PDV/PAP max</th>',
                '</tr></thead><tbody>']

        ordered = sub.sort_values('pvf', ascending=True)

        for _, row in ordered.iterrows():
            type_label = brand_tag(row['marque'], cfg['star_brands'])
            statut_cls = 'ok' if row['statut'] == 'OK' else 'ko'
            role_color = ROLE_COLORS.get(row['role'], '#64748b')

            pap_min_txt = fmt(row['pap_min'])
            if row['pap_max'] > 0:
                pap_max_txt = fmt(row['pap_max'])
                marge_pap = safe_pct(row['marge_pdv_pap_max_pct'])
            else:
                pap_max_txt = '<span class="muted">—</span>'
                marge_pap = '<span class="muted">—</span>'

            html.append(
                '<tr>'
                f'<td class="left">{type_label}</td>'
                f'<td class="left bold">{brand_name_html(row["marque"], cfg["star_brands"])}</td>'
                f'<td class="left">{row["format"]}</td>'
                f'<td class="left"><span class="role-dot" '
                f'style="background:{role_color};"></span>{row["role"]}</td>'
                f'<td class="bold">{fmt(row["pvf"])}</td>'
                f'<td>{fmt(row["p_litre"])}</td>'
                f'<td class="{statut_cls}">{row["idx_pl"]}</td>'
                f'<td>{pap_min_txt}</td>'
                f'<td>{pap_max_txt}</td>'
                f'<td class="muted">{marge_pap}</td>'
                '</tr>'
            )

        html.append('</tbody></table>')
        st.markdown(''.join(html), unsafe_allow_html=True)


# =============================================================================
# DÉTAILS EN ONGLETS
# =============================================================================
st.markdown("### Détails par SKU")
tab1, tab2, tab3 = st.tabs(["Prix & Index", "Marges 2026", "Marges 2027"])

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
            f'<td class="left bold">{brand_name_html(row["marque"], cfg["star_brands"])}</td>'
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

with tab2:
    html = ['<table class="obppc"><thead><tr>',
            '<th class="left">Marque</th>',
            '<th class="left">Format</th>',
            '<th>PVA</th><th>PV DS</th><th>Marge DS</th><th>Taux DS</th>',
            '<th>PVC</th><th>PAP min</th><th>PAP max</th><th>Marge PDV/PAP max</th>',
            '</tr></thead><tbody>']
    for _, row in d.iterrows():
        pap_min_txt = fmt(row['pap_min'])
        if row['pap_max'] > 0:
            pap_max_txt = fmt(row['pap_max'])
            marge_pap = safe_pct(row['marge_pdv_pap_max_pct'])
        else:
            pap_max_txt = '<span class="muted">—</span>'
            marge_pap = '<span class="muted">—</span>'
        html.append(
            '<tr>'
            f'<td class="left bold">{brand_name_html(row["marque"], cfg["star_brands"])}</td>'
            f'<td class="left">{row["format"]}</td>'
            f'<td>{fmt(row["pva"])}</td>'
            f'<td>{fmt(row["pv_ds"])}</td>'
            f'<td>{fmt(row["marge_ds"])}</td>'
            f'<td class="muted">{safe_pct(row["marge_ds_pct"])}</td>'
            f'<td>{fmt(row["pvc"])}</td>'
            f'<td>{pap_min_txt}</td>'
            f'<td>{pap_max_txt}</td>'
            f'<td class="muted">{marge_pap}</td>'
            '</tr>'
        )
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)

with tab3:
    html = ['<table class="obppc"><thead><tr>',
            '<th class="left">Marque</th>',
            '<th class="left">Format</th>',
            '<th>PVA 27</th><th>DS 27</th><th>Marge 27</th><th>Taux DS</th>',
            '<th>PVC 27</th>',
            '</tr></thead><tbody>']
    for _, row in d.iterrows():
        html.append(
            '<tr>'
            f'<td class="left bold">{brand_name_html(row["marque"], cfg["star_brands"])}</td>'
            f'<td class="left">{row["format"]}</td>'
            f'<td>{fmt(row["pva_2027"])}</td>'
            f'<td>{fmt(row["pv_ds_2027"])}</td>'
            f'<td>{fmt(row["marge_ds_2027"])}</td>'
            f'<td class="muted">{safe_pct(row["marge_ds_2027_pct"])}</td>'
            f'<td>{fmt(row["pvc_2027"])}</td>'
            '</tr>'
        )
    html.append('</tbody></table>')
    st.markdown(''.join(html), unsafe_allow_html=True)


# =============================================================================
# ✅ COLONNE COMMENTAIRE ÉDITABLE (indépendante, sous les onglets)
# =============================================================================
st.markdown("---")
st.markdown("### ✏️ Commentaires (modifiables)")
st.caption("Cliquez dans une cellule pour saisir ou modifier un commentaire.")

comment_rows = []
for _, row in d.iterrows():
    key = (row['marque'], row['format'])
    current = st.session_state.commentaires.get(
        key, row.get('commentaire', '')
    )
    comment_rows.append({
        'marque': row['marque'],
        'format': row['format'],
        'commentaire': current,
    })

comment_df = pd.DataFrame(comment_rows)

edited_comments = st.data_editor(
    comment_df,
    column_config={
        'marque': st.column_config.TextColumn(
            "Marque", disabled=True, width=120),
        'format': st.column_config.TextColumn(
            "Format", disabled=True, width=280),
        'commentaire': st.column_config.TextColumn(
            "Commentaire", width=650,
            help="Saisir une note libre (ex : PVC +500 / PVA +400)"),
    },
    hide_index=True,
    use_container_width=True,
    num_rows="fixed",
    height=min(500, 80 + 36 * len(comment_df)),
    key=f"comment_editor_{cat_key}",
)

for _, r in edited_comments.iterrows():
    key = (r['marque'], r['format'])
    st.session_state.commentaires[key] = r['commentaire']

# Réinjection (utile pour l'export CSV)
d['commentaire'] = d.apply(
    lambda r: st.session_state.commentaires.get(
        (r['marque'], r['format']), r.get('commentaire', '')
    ), axis=1)


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
    'pvc',
    'pap_min', 'pap_max',
    'marge_pdv_pap_min', 'marge_pdv_pap_min_pct',
    'marge_pdv_pap_max', 'marge_pdv_pap_max_pct',
    'pva_2027', 'pv_ds_2027', 'marge_ds_2027', 'marge_ds_2027_pct',
    'pvc_2027', 'statut', 'commentaire',
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
    'pvc': 'PVC 2026',
    'pap_min': 'PAP min',
    'pap_max': 'PAP max',
    'marge_pdv_pap_min': 'Marge PDV/PAP min',
    'marge_pdv_pap_min_pct': 'Taux PDV/PAP min',
    'marge_pdv_pap_max': 'Marge PDV/PAP max',
    'marge_pdv_pap_max_pct': 'Taux PDV/PAP max',
    'pva_2027': 'PVA 2027', 'pv_ds_2027': 'PV DS 2027',
    'marge_ds_2027': 'Marge DS 2027', 'marge_ds_2027_pct': 'Taux DS 2027',
    'pvc_2027': 'PVC 2027',
    'statut': 'Statut', 'commentaire': 'Commentaire',
})

st.download_button(
    f"📥 Télécharger {cat_key} (CSV)",
    data=export.to_csv(index=False).encode('utf-8'),
    file_name=f"simulateur_obppc_{cat_key.lower()}.csv",
    mime="text/csv",
)
