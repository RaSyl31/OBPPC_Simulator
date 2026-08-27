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
        'Segment': [],
        'Marque': [],
        'Occasion': [],
        'Role_OBPPC': [],
        'Description': [],
        'Volume_L': [],
        'PVF_Ar': []
    }
    
    # Energie
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
    
    # Boisson Gazeuse
    boisson_data = [
        ('Boisson Gazeuse', 'COCA', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35 (N° 1 vente en col)', 0.35, 1500),
        ('Boisson Gazeuse', 'COCA', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'COCA', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'COCA', 'FC (PET)', 'Entry (Entrée de gamme)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'WOCO', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'WOCO', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'WOCO', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'WOCO', 'FC (PET)', 'Entry (Entrée de gamme)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'WOCO', 'FC (VER)', 'Entry (Entrée de gamme)', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'FANTA', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35 (N° 1 vente en col)', 0.35, 1500),
        ('Boisson Gazeuse', 'FANTA', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'FANTA', 'FC (PET)', 'Entry (Entrée de gamme)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'CAPRICE', 'IC (PET)', 'Entry (Entrée de gamme)', 'PET 35', 0.35, 1500),
        ('Boisson Gazeuse', 'CAPRICE', 'IC (PET)', 'Frequency (Cœur de gamme)', 'PET 50', 0.50, 2000),
        ('Boisson Gazeuse', 'CAPRICE', 'Upscale', 'Upscale (Premium)', 'CAN 33', 0.33, 2500),
        ('Boisson Gazeuse', 'CAPRICE', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'CAPRICE', 'FC (PET)', 'Entry (Entrée de gamme)', 'PET 150', 1.50, 5000),
        ('Boisson Gazeuse', 'CAPRICE', 'FC (VER)', 'Entry (Entrée de gamme)', 'VC 100', 1.00, 3000),
        ('Boisson Gazeuse', 'TONIC', 'IC (VER)', 'Entry (Entrée de gamme)', 'VC 30', 0.30, 1200),
        ('Boisson Gazeuse', 'TONIC', 'FC (VER)', 'Entry (Entrée de gamme)', 'VC 100', 1.00, 3000),
    ]
    
    # Eaux
    eaux_data = [
        ('Eaux', 'Cristal', 'IC (VER)', 'Entry (Entrée de gamme)', 'Cristal 30 cl VER', 0.30, 1500),
        ('Eaux', 'Cristal', 'IC (VER)', 'Frequency (Cœur de gamme)', 'Cristal 50 cl VER', 0.50, 2200),
        ('Eaux', 'Cristal', 'FC (VER)', 'Upscale (Premium)', 'Cristal 100 cl VER', 1.00, 3800),
        ('Eaux', 'Cristal', 'FC (PET)', 'Frequency (Cœur de gamme)', 'Cristal 150 cl PET', 1.50, 5500),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Entry (Entrée de gamme)', 'RANOVISY 33 PET', 0.33, 1000),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Frequency (Cœur de gamme)', 'RANOVISY 50 CL PET', 0.50, 2400),
        ('Eaux', 'RANOVISY', 'IC (PET)', 'Upsize (Grand format)', 'RANOVISY 75 PET', 0.75, 3000),
        ('Eaux', 'VISY GASY', 'IC (PET)', 'Entry (Entrée de gamme)', 'VISY GASY 60 PET', 0.60, 2500),
        ('Eaux', 'VISY GASY', 'FC (PET)', 'Entry (Entrée de gamme)', 'VISY GASY 100 PET', 1.00, 3000),
        ('Eaux', 'Eau vive', 'IC (PET)', 'Entry (Entrée de gamme)', 'Eau vive 50 cl PET', 0.50, 1600),
        ('Eaux', 'Eau vive', 'FC (PET)', 'Frequency (Cœur de gamme)', 'Eau vive 150 cl PET', 1.50, 3300),
        ('Eaux', 'Eau vive', 'IC (VER)', 'Frequency (Cœur de gamme)', 'Eau vive 50 cl VER', 0.50, 2200),
        ('Eaux', 'Cristalline', 'FC (PET)', 'Frequency (Cœur de gamme)', 'Cristalline 100 cl PET', 1.50, 2100),
        ('Eaux', 'Cristalline', 'FC (PET)', 'Upsize (Grand format)', 'Cristalline 200 cl PET', 2.00, 3600),
        ('Eaux', 'OLYMPIKO', 'IC (PET)', 'Entry (Entrée de gamme)', 'OLYMPIKO 50', 0.50, 1500),
        ('Eaux', 'OLYMPIKO', 'FC (PET)', 'Frequency (Cœur de gamme)', 'OLYMPIKO 100', 1.00, 2000),
        ('Eaux', 'OLYMPIKO', 'FC (PET)', 'Upsize (Grand format)', 'OLYMPIKO 150', 1.50, 2500),
        ('Eaux', 'NATUR EAU', 'IC (PET)', 'Entry (Entrée de gamme)', 'NATUR EAU 50', 0.50, 1500),
        ('Eaux', 'NATUR EAU', 'FC (PET)', 'Frequency (Cœur de gamme)', 'NATUR EAU 100', 1.00, 2000),
        ('Eaux', 'NATUR EAU', 'FC (PET)', 'Upsize (Grand format)', 'NATUR EAU 150', 1.50, 2500),
    ]
    
    # Bière
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
    
    # Combiner toutes les données
    all_data = energie_data + boisson_data + eaux_data + biere_data
    
    for item in all_data:
        data['Segment'].append(item[0])
        data['Marque'].append(item[1])
        data['Occasion'].append(item[2])
        data['Role_OBPPC'].append(item[3])
        data['Description'].append(item[4])
        data['Volume_L'].append(item[5])
        data['PVF_Ar'].append(item[6])
    
    df = pd.DataFrame(data)
    return df

# Charger les données
df_initial = load_initial_data()

# Références des index Prix/Litre
references = {
    'Entry (Entrée de gamme)': 110,
    'Frequency (Cœur de gamme)': 100,
    'Upsize (Grand format)': 90,
    'Upscale (Premium)': 140,
    'Upscale (Super-Premium Niche)': 140
}

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
    
    st.markdown("---")
    st.header("📊 Références Index Prix/Litre")
    st.markdown("""
    - **Entry** : ~110
    - **Frequency** : 100
    - **Upsize** : ~90
    - **Upscale** : ~140
    """)

# Filtrer les données
if segments and brands:
    df_filtered = df_initial[
        (df_initial['Segment'].isin(segments)) &
        (df_initial['Marque'].isin(brands))
    ].copy()
else:
    df_filtered = df_initial.copy()

# Utiliser un seul conteneur pour les deux tableaux
main_container = st.container()

with main_container:
    # Créer le DataFrame éditable
    st.subheader("📝 Tableau Éditable")

    edited_df = st.data_editor(
        df_filtered,
        column_config={
            "Segment": st.column_config.SelectboxColumn(
                "Segment",
                options=['Energie', 'Boisson Gazeuse', 'Eaux', 'Bière'],
                required=True
            ),
            "Marque": st.column_config.SelectboxColumn(
                "Marque",
                options=sorted(df_initial['Marque'].unique()),
                required=True
            ),
            "Occasion": st.column_config.SelectboxColumn(
                "Occasion",
                options=['IC (VER)', 'IC (PET)', 'FC (VER)', 'FC (PET)', 'Upscale', ''],
                required=False
            ),
            "Role_OBPPC": st.column_config.SelectboxColumn(
                "Rôle OBPPC",
                options=[
                    'Entry (Entrée de gamme)',
                    'Frequency (Cœur de gamme)',
                    'Upsize (Grand format)',
                    'Upscale (Premium)',
                    'Upscale (Super-Premium Niche)'
                ],
                required=True
            ),
            "Description": st.column_config.TextColumn(
                "Description / Format"
            ),
            "Volume_L": st.column_config.NumberColumn(
                "Volume (L)",
                min_value=0.1,
                step=0.01,
                format="%.2f",
                required=True
            ),
            "PVF_Ar": st.column_config.NumberColumn(
                "Prix de Vente Facial (PVF) en Ar",
                min_value=0,
                step=100,
                format="%d",
                required=True
            )
        },
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
        key="data_editor",
        height=500
    )

    # Bouton pour recalculer
    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

    with col_btn2:
        if st.button("🔄 Recalculer les index", type="primary", use_container_width=True):
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
                        edited_df.loc[segment_mask, 'Index_PVF'] = (edited_df.loc[segment_mask, 'PVF_Ar'] / base_pvf * 100).round(0).astype(int)
                    if base_p_litre > 0:
                        edited_df.loc[segment_mask, 'Index_P_Litre'] = (edited_df.loc[segment_mask, 'P_Litre_Ar'] / base_p_litre * 100).round(0).astype(int)
            
            # Calculer les index vs Frequency global
            frequency_data = edited_df[edited_df['Role_OBPPC'].str.contains('Frequency', na=False)]
            if len(frequency_data) > 0:
                base_freq_pvf = frequency_data['PVF_Ar'].mean()
                base_freq_p_litre = frequency_data['P_Litre_Ar'].mean()
                
                if base_freq_pvf > 0:
                    edited_df['Index_PVF_Freq'] = (edited_df['PVF_Ar'] / base_freq_pvf * 100).round(0).astype(int)
                if base_freq_p_litre > 0:
                    edited_df['Index_P_Litre_Freq'] = (edited_df['P_Litre_Ar'] / base_freq_p_litre * 100).round(0).astype(int)
            else:
                # Si pas de produit Frequency, utiliser la moyenne globale
                base_freq_pvf = edited_df['PVF_Ar'].mean()
                base_freq_p_litre = edited_df['P_Litre_Ar'].mean()
                
                if base_freq_pvf > 0:
                    edited_df['Index_PVF_Freq'] = (edited_df['PVF_Ar'] / base_freq_pvf * 100).round(0).astype(int)
                if base_freq_p_litre > 0:
                    edited_df['Index_P_Litre_Freq'] = (edited_df['P_Litre_Ar'] / base_freq_p_litre * 100).round(0).astype(int)
            
            # Créer le tableau final avec les 11 colonnes + colonne de comparaison
            display_df = pd.DataFrame({
                'Marque': edited_df['Marque'],
                'Occasion': edited_df['Occasion'],
                'Rôle OBPPC': edited_df['Role_OBPPC'],
                'Description / Format': edited_df['Description'],
                'Volume (L)': edited_df['Volume_L'],
                'Prix de Vente Facial (PVF) en Ar': edited_df['PVF_Ar'].round(0).astype(int),
                'Prix au Litre (P/L) en Ar': edited_df['P_Litre_Ar'].round(0).astype(int),
                'Index PVF': edited_df['Index_PVF'].round(0).astype(int),
                'Index Prix/Litre': edited_df['Index_P_Litre'].round(0).astype(int),
                'Index PVF (Vs Frequency global)': edited_df['Index_PVF_Freq'].round(0).astype(int),
                'Index Prix/Litre (Vs Frequency global)': edited_df['Index_P_Litre_Freq'].round(0).astype(int),
                'Référence Index P/L': edited_df['Role_OBPPC'].map(references).fillna(100).astype(int),
                'Écart vs Référence': (edited_df['Index_P_Litre'] - edited_df['Role_OBPPC'].map(references).fillna(100)).round(0).astype(int),
                'Statut': edited_df.apply(lambda row: '✅ OK' if abs(row['Index_P_Litre'] - references.get(row['Role_OBPPC'], 100)) <= 10 else ('⚠️ À vérifier' if abs(row['Index_P_Litre'] - references.get(row['Role_OBPPC'], 100)) <= 20 else '❌ Hors cible'), axis=1)
            })
            
            # Afficher le tableau final avec la même largeur
            st.subheader("📋 Tableau avec les Index Calculés")
            
            # Utiliser st.dataframe avec use_container_width=True pour la même largeur
            st.dataframe(
                display_df, 
                use_container_width=True, 
                height=800
            )
            
            # Export CSV
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger les résultats (CSV)",
                data=csv,
                file_name="simulation_obppc.csv",
                mime="text/csv"
            )
        else:
            st.info("👆 Modifiez les données dans le tableau, puis cliquez sur 'Recalculer les index' pour voir les résultats avec les 11 colonnes.")
