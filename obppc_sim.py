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
    
    # Déterminer automatiquement l'Occasion selon le volume
    df['Occasion'] = df['Volume_L'].apply(lambda x: 'FC' if x > 0.99 else 'IC')
    
    # Initialiser le Role_OBPPC
    df['Role_OBPPC'] = ''
    
    # Attribution automatique du Role_OBPPC selon l'Occasion
    # Pour IC (volume < 1L) : Entry ou Frequency ou Upscale
    # Pour FC (volume > 0.99L) : Upsize (Grand format)
    # Pour Upscale : Upscale (Premium)
    
    # Attribution manuelle pour l'exemple (à ajuster selon vos besoins)
    role_mapping = {
        'Red Bull 25cl CAN': 'Upscale (Premium)',
        'Monster 50cl CAN': 'Upscale (Premium)',
        'FOSA 33cl VER': 'Entry (Entrée de gamme)',
        'XXL 33cl CAN': 'Entry (Entrée de gamme)',
        'DYNAMIC 33cl CAN': 'Entry (Entrée de gamme)',
        'BOOST VITALITY 25cl CAN': 'Upscale (Premium)',
        'COCA 33cl VER': 'Frequency (Cœur de gamme)',
        'WOCO 33cl VER': 'Entry (Entrée de gamme)',
        'FANTA 33cl VER': 'Frequency (Cœur de gamme)',
        'CAPRICE 33cl VER': 'Entry (Entrée de gamme)',
        'TONIC 33cl VER': 'Upscale (Premium)',
        'Cristal 50cl VER': 'Entry (Entrée de gamme)',
        'RANOVISY 50cl VER': 'Entry (Entrée de gamme)',
        'VISY GASY 50cl VER': 'Entry (Entrée de gamme)',
        'Eau vive 50cl VER': 'Upscale (Premium)',
        'Cristalline 50cl VER': 'Entry (Entrée de gamme)',
        'OLYMPIKO 50cl VER': 'Entry (Entrée de gamme)',
        'NATUR EAU 50cl VER': 'Entry (Entrée de gamme)',
        'Beaufort 33cl VER': 'Frequency (Cœur de gamme)',
        'Gold 50cl VER': 'Entry (Entrée de gamme)',
        'THB 65cl VER': 'Frequency (Cœur de gamme)',
        'Queen 65cl VER': 'Entry (Entrée de gamme)',
        'Fresh 33cl VER': 'Frequency (Cœur de gamme)'
    }
    df['Role_OBPPC'] = df['Description'].map(role_mapping)
    
    return df

# Charger les données
df_initial = load_initial_data()

# Titre
st.title("🎯 Simulateur OBPPC")
st.markdown("---")

# Sidebar pour les filtres
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

# Filtrer les données
if segments and brands:
    df_filtered = df_initial[
        (df_initial['Segment'].isin(segments)) &
        (df_initial['Marque'].isin(brands))
    ].copy()
else:
    df_filtered = df_initial.copy()

# Créer le DataFrame éditable
st.subheader("📝 Tableau Éditable - Modifiez les prix en Ariary (Ar)")
st.markdown("*Modifiez les prix dans la colonne PVF, puis cliquez sur 'Recalculer les index'*")

# Fonction pour mettre à jour l'occasion selon le volume
def update_occasion(volume):
    return 'FC' if volume > 0.99 else 'IC'

# Fonction pour mettre à jour le rôle OBPPC selon l'occasion
def update_role_obppc(occasion, current_role):
    if occasion == 'Upscale':
        return 'Upscale (Premium)'
    elif occasion == 'FC':
        return 'Upsize (Grand format)'
    else:  # IC
        # Garder le rôle actuel si c'est Entry, Frequency ou Upscale
        if current_role in ['Entry (Entrée de gamme)', 'Frequency (Cœur de gamme)', 'Upscale (Premium)']:
            return current_role
        else:
            return 'Entry (Entrée de gamme)'  # Par défaut

edited_df = st.data_editor(
    df_filtered,
    column_config={
        "PVF_Ar": st.column_config.NumberColumn(
            "Prix de Vente Facial (PVF) en Ar",
            min_value=0,
            step=100,
            format="%d",
            required=True
        ),
        "Volume_L": st.column_config.NumberColumn(
            "Volume (L)",
            min_value=0.1,
            step=0.01,
            format="%.2f",
            required=True
        ),
        "Segment": st.column_config.TextColumn(
            "Segment",
            disabled=True
        ),
        "Marque": st.column_config.TextColumn(
            "Marque",
            disabled=True
        ),
        "Occasion": st.column_config.SelectboxColumn(
            "Occasion",
            options=['IC', 'FC', 'Upscale'],
            required=True
        ),
        "Role_OBPPC": st.column_config.SelectboxColumn(
            "Rôle OBPPC",
            options=[
                'Entry (Entrée de gamme)',
                'Frequency (Cœur de gamme)',
                'Upsize (Grand format)',
                'Upscale (Premium)'
            ],
            required=True
        ),
        "Description": st.column_config.TextColumn(
            "Description / Format",
            disabled=True
        )
    },
    hide_index=True,
    use_container_width=True,
    num_rows="dynamic",
    key="data_editor"
)

# Appliquer les règles automatiques après édition
# Si le volume change, mettre à jour l'occasion automatiquement
for idx in edited_df.index:
    # Règle : Volume > 0.99 => FC, sinon IC
    if edited_df.at[idx, 'Volume_L'] > 0.99:
        if edited_df.at[idx, 'Occasion'] != 'Upscale':
            edited_df.at[idx, 'Occasion'] = 'FC'
    else:
        if edited_df.at[idx, 'Occasion'] != 'Upscale':
            edited_df.at[idx, 'Occasion'] = 'IC'
    
    # Règle : Si Occasion == Upscale, alors Role_OBPPC == Upscale (Premium)
    if edited_df.at[idx, 'Occasion'] == 'Upscale':
        edited_df.at[idx, 'Role_OBPPC'] = 'Upscale (Premium)'
    # Règle : Si Occasion == FC, alors Role_OBPPC == Upsize (Grand format)
    elif edited_df.at[idx, 'Occasion'] == 'FC':
        edited_df.at[idx, 'Role_OBPPC'] = 'Upsize (Grand format)'

# Bouton pour recalculer
st.markdown("---")
if st.button("🔄 Recalculer les index", type="primary"):
    # Calculer les prix au litre
    edited_df['P_Litre_Ar'] = edited_df['PVF_Ar'] / edited_df['Volume_L']
    
    # Initialiser les colonnes d'index
    edited_df['Index_PVF'] = 0.0
    edited_df['Index_P_Litre'] = 0.0
    edited_df['Index_PVF_Freq'] = 0.0
    edited_df['Index_P_Litre_Freq'] = 0.0
    
    # Calculer les index par segment
    for segment in edited_df['Segment'].unique():
        segment_mask = edited_df['Segment'] == segment
        segment_data = edited_df[segment_mask]
        
        if len(segment_data) > 0:
            # Base = premier produit du segment
            base_pvf = segment_data.iloc[0]['PVF_Ar']
            base_p_litre = segment_data.iloc[0]['P_Litre_Ar']
            
            if base_pvf > 0:
                edited_df.loc[segment_mask, 'Index_PVF'] = (edited_df.loc[segment_mask, 'PVF_Ar'] / base_pvf * 100).round(1)
            if base_p_litre > 0:
                edited_df.loc[segment_mask, 'Index_P_Litre'] = (edited_df.loc[segment_mask, 'P_Litre_Ar'] / base_p_litre * 100).round(1)
    
    # Calculer les index vs Frequency global
    frequency_data = edited_df[edited_df['Role_OBPPC'] == 'Frequency (Cœur de gamme)']
    if len(frequency_data) > 0:
        base_freq_pvf = frequency_data['PVF_Ar'].mean()
        base_freq_p_litre = frequency_data['P_Litre_Ar'].mean()
        
        if base_freq_pvf > 0:
            edited_df['Index_PVF_Freq'] = (edited_df['PVF_Ar'] / base_freq_pvf * 100).round(1)
        if base_freq_p_litre > 0:
            edited_df['Index_P_Litre_Freq'] = (edited_df['P_Litre_Ar'] / base_freq_p_litre * 100).round(1)
    else:
        # Si pas de produit Frequency, utiliser la moyenne globale
        base_freq_pvf = edited_df['PVF_Ar'].mean()
        base_freq_p_litre = edited_df['P_Litre_Ar'].mean()
        
        if base_freq_pvf > 0:
            edited_df['Index_PVF_Freq'] = (edited_df['PVF_Ar'] / base_freq_pvf * 100).round(1)
        if base_freq_p_litre > 0:
            edited_df['Index_P_Litre_Freq'] = (edited_df['P_Litre_Ar'] / base_freq_p_litre * 100).round(1)
    
    # Créer le tableau final avec les 11 colonnes
    display_df = pd.DataFrame({
        'Marque': edited_df['Marque'],
        'Occasion': edited_df['Occasion'],
        'Rôle OBPPC': edited_df['Role_OBPPC'],
        'Description / Format': edited_df['Description'],
        'Volume (L)': edited_df['Volume_L'],
        'Prix de Vente Facial (PVF) en Ar': edited_df['PVF_Ar'],
        'Prix au Litre (P/L) en Ar': edited_df['P_Litre_Ar'].round(1),
        'Index PVF': edited_df['Index_PVF'].round(1),
        'Index Prix/Litre': edited_df['Index_P_Litre'].round(1),
        'Index PVF (Vs Frequency global)': edited_df['Index_PVF_Freq'].round(1),
        'Index Prix/Litre (Vs Frequency global)': edited_df['Index_P_Litre_Freq'].round(1)
    })
    
    # Afficher le tableau final
    st.subheader("📋 Tableau avec les Index Calculés")
    st.dataframe(display_df, use_container_width=True, height=600)
    
    # Export CSV
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Télécharger les résultats (CSV)",
        data=csv,
        file_name="simulation_obppc.csv",
        mime="text/csv"
    )
else:
    st.info("👆 Modifiez les prix dans le tableau ci-dessus, puis cliquez sur 'Recalculer les index' pour voir les résultats avec les 11 colonnes.")
    st.info("📏 Règles automatiques : Volume > 0.99L = FC → Upsize (Grand format) | Volume < 1L = IC | Occasion Upscale = Upscale (Premium)")
