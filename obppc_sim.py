import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(
    page_title="Simulateur OBPPC",
    layout="wide"
)

# Données initiales
@st.cache_data
def load_initial_data():
    data = {
        'Segment': ['Energie', 'Energie', 'Energie', 'Energie', 'Energie', 'Energie',
                   'Boisson Gazeuse', 'Boisson Gazeuse', 'Boisson Gazeuse', 'Boisson Gazeuse', 'Boisson Gazeuse',
                   'Eaux', 'Eaux', 'Eaux', 'Eaux', 'Eaux', 'Eaux', 'Eaux',
                   'Bière', 'Bière', 'Bière', 'Bière', 'Bière'],
        'Marque': ['Red Bull', 'Monster', 'FOSA', 'XXL', 'DYNAMIC', 'BOOST VITALITY',
                  'COCA', 'WOCO', 'FANTA', 'CAPRICE', 'TONIC',
                  'Cristal', 'RANOVISY', 'VISY GASY', 'Eau vive', 'Cristalline', 'OLYMPIKO', 'NATUR EAU',
                  'Beaufort', 'Gold', 'THB', 'Queen', 'Fresh'],
        'Occasion': ['Energie', 'Energie', 'Energie', 'Energie', 'Energie', 'Energie',
                    'Rafraîchissement', 'Rafraîchissement', 'Rafraîchissement', 'Rafraîchissement', 'Rafraîchissement',
                    'Hydratation', 'Hydratation', 'Hydratation', 'Hydratation', 'Hydratation', 'Hydratation', 'Hydratation',
                    'Sociale', 'Sociale', 'Sociale', 'Sociale', 'Sociale'],
        'Role_OBPPC': ['Premium', 'Premium', 'Value', 'Value', 'Value', 'Premium',
                      'Frequency', 'Value', 'Frequency', 'Value', 'Premium',
                      'Entry', 'Entry', 'Value', 'Premium', 'Entry', 'Value', 'Entry',
                      'Frequency', 'Entry', 'Frequency', 'Entry', 'Frequency'],
        'Description': ['Red Bull 25cl CAN', 'Monster 50cl CAN', 'FOSA 33cl VER', 'XXL 33cl CAN', 'DYNAMIC 33cl CAN', 'BOOST VITALITY 25cl CAN',
                       'COCA 33cl VER', 'WOCO 33cl VER', 'FANTA 33cl VER', 'CAPRICE 33cl VER', 'TONIC 33cl VER',
                       'Cristal 50cl VER', 'RANOVISY 50cl VER', 'VISY GASY 50cl VER', 'Eau vive 50cl VER', 'Cristalline 50cl VER', 'OLYMPIKO 50cl VER', 'NATUR EAU 50cl VER',
                       'Beaufort 33cl VER', 'Gold 50cl VER', 'THB 65cl VER', 'Queen 65cl VER', 'Fresh 33cl VER'],
        'Volume_L': [0.25, 0.50, 0.33, 0.33, 0.33, 0.25,
                    0.33, 0.33, 0.33, 0.33, 0.33,
                    0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50,
                    0.33, 0.50, 0.65, 0.65, 0.33],
        'PVF_Ar': [8000, 10000, 3500, 4000, 3500, 9000,
                  3500, 2500, 3500, 2500, 4500,
                  2000, 1500, 1500, 2500, 1500, 1500, 1500,
                  4000, 4500, 4500, 4000, 2500]
    }
    df = pd.DataFrame(data)
    df['P_Litre_Ar'] = df['PVF_Ar'] / df['Volume_L']
    
    # Initialiser les colonnes d'index avec des floats
    df['Index_PVF'] = 0.0
    df['Index_P_Litre'] = 0.0
    df['Index_PVF_Freq'] = 0.0
    df['Index_P_Litre_Freq'] = 0.0
    
    # Calculer les index initiaux par segment
    for segment in df['Segment'].unique():
        segment_mask = df['Segment'] == segment
        segment_data = df[segment_mask]
        
        # Base = premier produit du segment
        base_pvf = segment_data.iloc[0]['PVF_Ar']
        base_p_litre = segment_data.iloc[0]['P_Litre_Ar']
        
        df.loc[segment_mask, 'Index_PVF'] = (df.loc[segment_mask, 'PVF_Ar'] / base_pvf * 100).round(1)
        df.loc[segment_mask, 'Index_P_Litre'] = (df.loc[segment_mask, 'P_Litre_Ar'] / base_p_litre * 100).round(1)
    
    # Calculer les index vs Frequency global
    frequency_data = df[df['Role_OBPPC'] == 'Frequency']
    if len(frequency_data) > 0:
        base_freq_pvf = frequency_data['PVF_Ar'].mean()
        base_freq_p_litre = frequency_data['P_Litre_Ar'].mean()
        
        df['Index_PVF_Freq'] = (df['PVF_Ar'] / base_freq_pvf * 100).round(1)
        df['Index_P_Litre_Freq'] = (df['P_Litre_Ar'] / base_freq_p_litre * 100).round(1)
    else:
        df['Index_PVF_Freq'] = 100.0
        df['Index_P_Litre_Freq'] = 100.0
    
    return df

# Charger les données
df_initial = load_initial_data()

# Titre
st.title("🎯 Simulateur OBPPC")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("🔍 Filtres")
    
    # Sélection des segments
    segments = st.multiselect(
        "Segments",
        options=df_initial['Segment'].unique(),
        default=df_initial['Segment'].unique()
    )
    
    # Filtrer les marques selon les segments
    if segments:
        available_brands = df_initial[df_initial['Segment'].isin(segments)]['Marque'].unique()
    else:
        available_brands = df_initial['Marque'].unique()
    
    # Sélection des marques
    brands = st.multiselect(
        "Marques",
        options=available_brands,
        default=available_brands
    )
    
    st.markdown("---")
    st.header("⚙️ Paramètres")
    
    # Type d'index à ajuster
    index_type = st.radio(
        "Type d'index à ajuster",
        options=['Index PVF', 'Index Prix/Litre']
    )
    
    # Réinitialisation
    if st.button("🔄 Réinitialiser tous les index"):
        st.session_state.index_values = {}
        st.rerun()

# Filtrer les données
if segments and brands:
    df_filtered = df_initial[
        (df_initial['Segment'].isin(segments)) &
        (df_initial['Marque'].isin(brands))
    ].copy()
else:
    df_filtered = df_initial.copy()

# Créer deux colonnes : sliders à gauche, tableau à droite
col1, col2 = st.columns([1, 2])

# Sliders dans la colonne gauche
with col1:
    st.subheader("🎚️ Ajustement des Index")
    
    # Initialiser le dictionnaire des index
    if 'index_values' not in st.session_state:
        st.session_state.index_values = {}
    
    index_values = {}
    
    # Organiser par segment
    for segment in segments if segments else df_filtered['Segment'].unique():
        segment_data = df_filtered[df_filtered['Segment'] == segment]
        if len(segment_data) > 0:
            st.markdown(f"### {segment}")
            
            for idx, row in segment_data.iterrows():
                # Index initial selon le type choisi
                if index_type == 'Index PVF':
                    initial_index = row['Index_PVF']
                else:
                    initial_index = row['Index_P_Litre']
                
                # Récupérer la valeur stockée
                current_value = st.session_state.index_values.get(row['Description'], initial_index)
                
                # Slider
                st.markdown(f"**{row['Marque']}** - *{row['Role_OBPPC']}*")
                new_index = st.slider(
                    row['Description'],
                    min_value=float(max(10, initial_index - 50)),
                    max_value=float(initial_index + 100),
                    value=float(current_value),
                    step=1.0,
                    key=f"slider_{row['Description']}"
                )
                index_values[row['Description']] = new_index
                st.markdown("---")
    
    # Stocker les valeurs
    st.session_state.index_values = index_values

# Tableau dans la colonne droite
with col2:
    st.subheader("📋 Tableau des Prix")
    
    # Créer le DataFrame de simulation
    df_sim = df_filtered.copy()
    
    # Calculer les nouveaux prix selon les index
    if index_type == 'Index PVF':
        df_sim['Index_PVF_Simule'] = df_sim['Description'].map(index_values).astype(float)
        
        # Trouver le prix de référence (produit avec index = 100 dans le segment)
        for segment in df_sim['Segment'].unique():
            segment_mask = df_sim['Segment'] == segment
            segment_indices = df_sim.loc[segment_mask, 'Index_PVF_Simule']
            base_index = segment_indices.min()  # On garde la même base que l'initial
            base_pvf = df_initial[df_initial['Segment'] == segment].iloc[0]['PVF_Ar']
            
            df_sim.loc[segment_mask, 'PVF_Simule'] = (df_sim.loc[segment_mask, 'Index_PVF_Simule'] / 100) * base_pvf
        
        df_sim['P_Litre_Simule'] = df_sim['PVF_Simule'] / df_sim['Volume_L']
        df_sim['Index_P_Litre_Simule'] = (df_sim['P_Litre_Simule'] / df_sim['P_Litre_Ar']) * df_sim['Index_P_Litre']
    else:
        df_sim['Index_P_Litre_Simule'] = df_sim['Description'].map(index_values).astype(float)
        
        # Trouver le prix de référence (produit avec index = 100 dans le segment)
        for segment in df_sim['Segment'].unique():
            segment_mask = df_sim['Segment'] == segment
            base_p_litre = df_initial[df_initial['Segment'] == segment].iloc[0]['P_Litre_Ar']
            
            df_sim.loc[segment_mask, 'P_Litre_Simule'] = (df_sim.loc[segment_mask, 'Index_P_Litre_Simule'] / 100) * base_p_litre
        
        df_sim['PVF_Simule'] = df_sim['P_Litre_Simule'] * df_sim['Volume_L']
        df_sim['Index_PVF_Simule'] = (df_sim['PVF_Simule'] / df_sim['PVF_Ar']) * df_sim['Index_PVF']
    
    # Recalculer les index vs Frequency global
    frequency_data = df_sim[df_sim['Role_OBPPC'] == 'Frequency']
    if len(frequency_data) > 0:
        base_freq_pvf = frequency_data['PVF_Simule'].mean()
        base_freq_p_litre = frequency_data['P_Litre_Simule'].mean()
        
        df_sim['Index_PVF_Freq_Simule'] = (df_sim['PVF_Simule'] / base_freq_pvf * 100).round(1)
        df_sim['Index_P_Litre_Freq_Simule'] = (df_sim['P_Litre_Simule'] / base_freq_p_litre * 100).round(1)
    else:
        df_sim['Index_PVF_Freq_Simule'] = df_sim['Index_PVF_Simule']
        df_sim['Index_P_Litre_Freq_Simule'] = df_sim['Index_P_Litre_Simule']
    
    # Créer le tableau avec les 11 colonnes
    display_df = pd.DataFrame({
        'Marque': df_sim['Marque'],
        'Occasion': df_sim['Occasion'],
        'Rôle OBPPC': df_sim['Role_OBPPC'],
        'Description / Format': df_sim['Description'],
        'Volume (L)': df_sim['Volume_L'],
        'Prix de Vente Facial (PVF)': df_sim['PVF_Simule'].round(0).astype(int),
        'Prix au Litre (P/L)': df_sim['P_Litre_Simule'].round(1),
        'Index PVF': df_sim['Index_PVF_Simule'].round(1),
        'Index Prix/Litre': df_sim['Index_P_Litre_Simule'].round(1),
        'Index PVF (Vs Frequency global)': df_sim['Index_PVF_Freq_Simule'].round(1),
        'Index Prix/Litre (Vs Frequency global)': df_sim['Index_P_Litre_Freq_Simule'].round(1)
    })
    
    # Afficher le tableau
    st.dataframe(display_df, use_container_width=True, height=600)
    
    # Export CSV
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger (CSV)",
        data=csv,
        file_name="simulation_obppc.csv",
        mime="text/csv"
    )
