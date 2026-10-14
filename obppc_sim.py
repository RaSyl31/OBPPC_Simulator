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

    /* ---------- INPUTS / SELECT ---------- */
    [data-baseweb="select"] > div,
    [data-baseweb="input"] > div,
    [data-testid="stMultiSelect"] [data-baseweb="select"] > div,
    [data-testid="stSelectbox"] [data-baseweb="select"] > div {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
    }
    /* Texte affiché dans le select (valeur choisie + placeholder) */
    [data-baseweb="select"] div,
    [data-baseweb="select"] span,
    [data-baseweb="select"] input,
    [data-baseweb="select"] [data-testid="stMarkdownContainer"],
    [data-baseweb="input"] input {
        color: #ffffff !important;
    }
    /* Placeholder */
    [data-baseweb="select"] input::placeholder,
    [data-baseweb="input"] input::placeholder {
        color: #a8c0dd !important;
        opacity: 1 !important;
    }
    /* Icônes chevron / croix */
    [data-baseweb="select"] svg,
    [data-testid="stMultiSelect"] svg {
        fill: #a8c0dd !important;
        color: #a8c0dd !important;
    }

    /* ---------- TAGS MULTISELECT ---------- */
    [data-baseweb="tag"] {
        background-color: #4a9eff !important;
        color: #ffffff !important;
        border: none !important;
    }
    [data-baseweb="tag"] *,
    [data-baseweb="tag"] span,
    [data-baseweb="tag"] div,
    [data-baseweb="tag"] svg {
        color: #ffffff !important;
        fill: #ffffff !important;
        background-color: transparent !important;
    }

    /* ---------- DROPDOWN / POPOVER (le vrai problème) ---------- */
    [data-baseweb="popover"],
    [data-baseweb="popover"] > div,
    [data-baseweb="popover"] [role="listbox"],
    [data-baseweb="popover"] [role="dialog"],
    [data-baseweb="menu"],
    [data-baseweb="menu"] > div,
    div[role="listbox"],
    ul[role="listbox"] {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
        box-shadow: 0 8px 24px rgba(0,0,0,0.5) !important;
    }
    /* Options individuelles */
    [data-baseweb="menu"] li,
    [data-baseweb="menu"] [role="option"],
    [data-baseweb="popover"] li,
    [data-baseweb="popover"] [role="option"],
    div[role="option"],
    li[role="option"] {
        background-color: #132f4c !important;
        color: #ffffff !important;
        font-size: 0.9rem !important;
    }
    /* Texte à l'intérieur des options (spans, divs) */
    [data-baseweb="menu"] li *,
    [data-baseweb="menu"] [role="option"] *,
    [data-baseweb="popover"] li *,
    [data-baseweb="popover"] [role="option"] *,
    [role="option"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    /* Hover et sélection */
    [data-baseweb="menu"] li:hover,
    [data-baseweb="menu"] [role="option"]:hover,
    [data-baseweb="popover"] li:hover,
    [data-baseweb="popover"] [role="option"]:hover,
    [role="option"]:hover {
        background-color: #1e4976 !important;
        color: #ffffff !important;
    }
    [data-baseweb="menu"] [aria-selected="true"],
    [data-baseweb="popover"] [aria-selected="true"],
    [role="option"][aria-selected="true"] {
        background-color: #4a9eff !important;
        color: #ffffff !important;
    }
    /* L'option sélectionnée garde son texte blanc */
    [role="option"][aria-selected="true"] * {
        color: #ffffff !important;
    }

    /* ---------- RADIO / CHECKBOX ---------- */
    .stRadio label, .stCheckbox label,
    .stRadio > div > label > div { color: #ffffff !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: #ffffff !important; }

    /* ---------- BOUTONS ---------- */
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
        color: #ffffff !important;
    }

    /* ---------- METRICS ---------- */
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"],
    [data-testid="stMetricDelta"] { color: #ffffff !important; }

    /* ---------- TABS ---------- */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #1e4976;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a8c0dd !important;
        background-color: transparent !important;
    }
    .stTabs [data-baseweb="tab"] * { color: inherit !important; }
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        border-bottom: 2px solid #4a9eff !important;
    }

    /* ---------- DATAFRAME / DATA EDITOR ---------- */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        border-radius: 8px;
    }
    /* Toolbar du data_editor */
    [data-testid="stDataEditor"] [data-testid="stElementToolbar"] button,
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"] button {
        background-color: transparent !important;
        color: #ffffff !important;
        border-color: #1e4976 !important;
    }
    [data-testid="stDataEditor"] [data-testid="stElementToolbar"] button:hover {
        background-color: #1e4976 !important;
    }
    /* Le canvas du data_editor est impossible à styler via CSS,
       mais on force le container pour éviter les bords blancs */
    [data-testid="stDataEditor"] canvas,
    [data-testid="stDataFrame"] canvas {
        background-color: #132f4c !important;
    }

    /* ---------- ALERTS ---------- */
    .stAlert {
        background-color: #132f4c !important;
        border: 1px solid #1e4976 !important;
        color: #ffffff !important;
    }
    .stAlert *,
    .stAlert p { color: #ffffff !important; }

    /* ---------- DIVERS ---------- */
    hr { border-color: #1e4976 !important; }
    strong, b { color: #ffffff !important; }
    a { color: #4a9eff !important; }

    /* Filet de sécurité : tout texte blanc par défaut dans les composants interactifs */
    [role="listbox"] *,
    [role="option"] *,
    [role="dialog"] * {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)
