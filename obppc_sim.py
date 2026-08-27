import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Simulateur OBPPC - Multi-Segments",
    layout="wide",
    initial_sidebar_state="expanded"
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
        'PVF': [8000, 10000, 3500, 4000, 3500, 9000,
               3500, 2500, 3500, 2500, 4500,
               2000, 1500, 1500, 2500, 1500, 1500, 1500,
               4000, 4500, 4500, 4000, 2500]
    }
    df = pd.DataFrame(data)
    df['P_Litre'] = df['PVF'] / df['Volume_L']
    
    # Calculer les index initiaux
    # Index PVF et Prix/Litre par segment (base = premier produit du segment)
    df['Index_PVF'] = 0
    df['Index_P_Litre'] = 0
    
    for segment in df['Segment'].unique():
        segment_mask = df['Segment'] == segment
        segment_data = df[segment_mask]
        
        # Base = premier produit du segment
        base_pvf = segment_data.iloc[0]['PVF']
        base_p_litre = segment_data.iloc[0]['P_Litre']
        
        df.loc[segment_mask, 'Index_PVF'] = (df.loc[segment_mask, 'PVF'] / base_pvf * 100).round(1)
        df.loc[segment_mask, 'Index_P_Litre'] = (df.loc[segment_mask, 'P_Litre'] / base_p_litre * 100).round(1)
    
    # Calculer les index vs Frequency global
    frequency_data = df[df['Role_OBPPC'] == 'Frequency']
    if len(frequency_data) > 0:
        base_freq_pvf = frequency_data['PVF'].mean()
        base_freq_p_litre = frequency_data['P_Litre'].mean()
        
        df['Index_PVF_Freq'] = (df['PVF'] / base_freq_pvf * 100).round(1)
        df['Index_P_Litre_Freq'] = (df['P_Litre'] / base_freq_p_litre * 100).round(1)
    else:
        df['Index_PVF_Freq'] = 100
        df['Index_P_Litre_Freq'] = 100
    
    return df

df_initial = load_initial_data()

# Titre principal
st.title("🎯 Simulateur OBPPC - Multi-Segments")
st.markdown("""
    **Ajustez les index pour simuler différents scénarios de positionnement prix.**
    Les prix se recalculent automatiquement en fonction des index que vous définissez.
""")

# Sidebar - Filtres et paramètres
with st.sidebar:
    st.header("🔍 Filtres")
    
    # Sélection des segments
    segments = st.multiselect(
        "Segments",
        options=df_initial['Segment'].unique(),
        default=df_initial['Segment'].unique(),
        help="Sélectionnez les segments à afficher"
    )
    
    # Filtrer les marques en fonction des segments sélectionnés
    if segments:
        available_brands = df_initial[df_initial['Segment'].isin(segments)]['Marque'].unique()
    else:
        available_brands = df_initial['Marque'].unique()
    
    # Sélection des marques
    brands = st.multiselect(
        "Marques",
        options=available_brands,
        default=available_brands,
        help="Sélectionnez les marques à afficher"
    )
    
    st.markdown("---")
    st.header("⚙️ Paramètres de Simulation")
    
    # Type d'index à ajuster
    index_type = st.radio(
        "Type d'index à ajuster",
        options=['Index PVF', 'Index Prix/Litre'],
        help="Choisissez quel type d'index vous voulez modifier"
    )
    
    # Prix de référence
    st.subheader("💰 Prix de Référence")
    
    # Produit de référence (peut changer selon le type d'index)
    if index_type == 'Index PVF':
        reference_product = st.selectbox(
            "Produit de référence",
            options=df_initial['Description'].tolist(),
            index=df_initial[df_initial['Description'] == 'THB 65cl VER'].index[0] if 'THB 65cl VER' in df_initial['Description'].tolist() else 0,
            help="Le produit dont l'index sera fixé à 100"
        )
        ref_data = df_initial[df_initial['Description'] == reference_product].iloc[0]
        reference_price = st.number_input(
            "Prix de référence (PVF)",
            value=float(ref_data['PVF']),
            step=100.0,
            format="%.0f"
        )
    else:
        reference_product = st.selectbox(
            "Produit de référence",
            options=df_initial['Description'].tolist(),
            index=df_initial[df_initial['Description'] == 'THB 65cl VER'].index[0] if 'THB 65cl VER' in df_initial['Description'].tolist() else 0,
            help="Le produit dont l'index sera fixé à 100"
        )
        ref_data = df_initial[df_initial['Description'] == reference_product].iloc[0]
        reference_price = st.number_input(
            "Prix de référence (P/Litre)",
            value=float(ref_data['P_Litre']),
            step=100.0,
            format="%.0f"
        )
    
    st.markdown("---")
    st.subheader("📊 Options d'affichage")
    
    show_initial = st.checkbox("Afficher les valeurs initiales", value=True)
    show_alerts = st.checkbox("Afficher les alertes de cohérence", value=True)
    
    # Bouton de réinitialisation
    if st.button("🔄 Réinitialiser tous les index"):
        st.session_state.index_values = {}
        st.rerun()

# Filtrer les données
df_filtered = df_initial[
    (df_initial['Segment'].isin(segments)) &
    (df_initial['Marque'].isin(brands))
].copy() if segments and brands else df_initial.copy()

# Créer les colonnes pour l'affichage
col1, col2 = st.columns([1, 2])

# Zone des sliders (colonne gauche)
with col1:
    st.subheader("🎚️ Ajustement des Index")
    st.markdown(f"*Base : {reference_product} = 100*")
    
    # Initialiser le dictionnaire des index dans la session si nécessaire
    if 'index_values' not in st.session_state:
        st.session_state.index_values = {}
    
    # Créer un slider pour chaque produit filtré
    index_values = {}
    
    # Grouper par segment pour une meilleure organisation
    for segment in segments:
        segment_data = df_filtered[df_filtered['Segment'] == segment]
        if len(segment_data) > 0:
            st.markdown(f"### {segment}")
            
            for idx, row in segment_data.iterrows():
                # Déterminer l'index initial en fonction du type choisi
                if index_type == 'Index PVF':
                    initial_index = row['Index_PVF']
                else:
                    initial_index = row['Index_P_Litre']
                
                # Récupérer la valeur stockée ou utiliser l'initiale
                current_value = st.session_state.index_values.get(row['Description'], initial_index)
                
                # Créer le slider
                st.markdown(f"**{row['Marque']}** - *{row['Role_OBPPC']}*")
                new_index = st.slider(
                    row['Description'],
                    min_value=float(initial_index - 50),
                    max_value=float(initial_index + 100),
                    value=float(current_value),
                    step=1.0,
                    key=f"slider_{row['Description']}",
                    help=f"Index initial : {initial_index:.1f}"
                )
                index_values[row['Description']] = new_index
                st.markdown("---")
    
    # Stocker les valeurs dans la session
    st.session_state.index_values = index_values

# Zone des résultats (colonne droite)
with col2:
    # Créer le DataFrame de simulation
    df_sim = df_filtered.copy()
    
    # Calculer les nouveaux prix en fonction des index
    if index_type == 'Index PVF':
        df_sim['Index_PVF_Simule'] = df_sim['Description'].map(index_values)
        df_sim['PVF_Simule'] = (df_sim['Index_PVF_Simule'] / 100) * reference_price
        df_sim['P_Litre_Simule'] = df_sim['PVF_Simule'] / df_sim['Volume_L']
        df_sim['Index_P_Litre_Simule'] = (df_sim['P_Litre_Simule'] / df_sim['P_Litre']) * df_sim['Index_P_Litre']
    else:
        df_sim['Index_P_Litre_Simule'] = df_sim['Description'].map(index_values)
        df_sim['P_Litre_Simule'] = (df_sim['Index_P_Litre_Simule'] / 100) * reference_price
        df_sim['PVF_Simule'] = df_sim['P_Litre_Simule'] * df_sim['Volume_L']
        df_sim['Index_PVF_Simule'] = (df_sim['PVF_Simule'] / df_sim['PVF']) * df_sim['Index_PVF']
    
    # Recalculer les index vs Frequency global
    frequency_data = df_sim[df_sim['Role_OBPPC'] == 'Frequency']
    if len(frequency_data) > 0:
        base_freq_pvf = frequency_data['PVF_Simule'].mean()
        base_freq_p_litre = frequency_data['P_Litre_Simule'].mean()
        
        df_sim['Index_PVF_Freq_Simule'] = (df_sim['PVF_Simule'] / base_freq_pvf * 100).round(1)
        df_sim['Index_P_Litre_Freq_Simule'] = (df_sim['P_Litre_Simule'] / base_freq_p_litre * 100).round(1)
    
    # Onglets pour différentes vues
    tab1, tab2, tab3, tab4 = st.tabs([
        "📋 Tableau Détaillé",
        "📈 Graphiques",
        "🔍 Analyse Cohérence",
        "📊 Synthèse"
    ])
    
    with tab1:
        st.subheader("Tableau des Résultats avec les 11 colonnes")
        
        # Créer le tableau final avec les 11 colonnes demandées
        if index_type == 'Index PVF':
            display_df = pd.DataFrame({
                'Marque': df_sim['Marque'],
                'Occasion': df_sim['Occasion'],
                'Rôle OBPPC': df_sim['Role_OBPPC'],
                'Description / Format': df_sim['Description'],
                'Volume (L)': df_sim['Volume_L'],
                'Prix de Vente Facial (PVF)': df_sim['PVF_Simule'].round(0),
                'Prix au Litre (P/L)': df_sim['P_Litre_Simule'].round(1),
                'Index PVF': df_sim['Index_PVF_Simule'].round(1),
                'Index Prix/Litre': df_sim['Index_P_Litre_Simule'].round(1),
                'Index PVF (Vs Frequency global)': df_sim['Index_PVF_Freq_Simule'].round(1),
                'Index Prix/Litre (Vs Frequency global)': df_sim['Index_P_Litre_Freq_Simule'].round(1)
            })
        else:
            display_df = pd.DataFrame({
                'Marque': df_sim['Marque'],
                'Occasion': df_sim['Occasion'],
                'Rôle OBPPC': df_sim['Role_OBPPC'],
                'Description / Format': df_sim['Description'],
                'Volume (L)': df_sim['Volume_L'],
                'Prix de Vente Facial (PVF)': df_sim['PVF_Simule'].round(0),
                'Prix au Litre (P/L)': df_sim['P_Litre_Simule'].round(1),
                'Index PVF': df_sim['Index_PVF_Simule'].round(1),
                'Index Prix/Litre': df_sim['Index_P_Litre_Simule'].round(1),
                'Index PVF (Vs Frequency global)': df_sim['Index_PVF_Freq_Simule'].round(1),
                'Index Prix/Litre (Vs Frequency global)': df_sim['Index_P_Litre_Freq_Simule'].round(1)
            })
        
        # Afficher le tableau
        st.dataframe(display_df, use_container_width=True, height=500)
        
        # Export
        csv = display_df.to_csv(index=False)
        st.download_button(
            label="📥 Télécharger les résultats (CSV)",
            data=csv,
            file_name="simulation_obppc_multisegments.csv",
            mime="text/csv"
        )
    
    with tab2:
        st.subheader("Visualisation des Résultats")
        
        # Graphique des index par segment
        fig1 = px.bar(
            df_sim,
            x='Description',
            y='Index_PVF_Simule' if index_type == 'Index PVF' else 'Index_P_Litre_Simule',
            color='Segment',
            facet_col='Segment',
            title=f"Index {index_type} par Produit et Segment",
            labels={'Index_PVF_Simule': f'Index {index_type}', 'Description': ''},
            height=400
        )
        fig1.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Base 100")
        fig1.update_xaxes(tickangle=45)
        st.plotly_chart(fig1, use_container_width=True)
        
        # Graphique de positionnement
        col_a, col_b = st.columns(2)
        
        with col_a:
            fig2 = px.scatter(
                df_sim,
                x='Volume_L',
                y='PVF_Simule',
                color='Segment',
                size='Index_PVF_Simule' if index_type == 'Index PVF' else 'Index_P_Litre_Simule',
                hover_data=['Description', 'Marque', 'Role_OBPPC'],
                title="Positionnement Prix vs Volume",
                labels={'PVF_Simule': 'PVF (FCFA)', 'Volume_L': 'Volume (L)'}
            )
            st.plotly_chart(fig2, use_container_width=True)
        
        with col_b:
            # Comparaison par segment
            fig3 = px.box(
                df_sim,
                x='Segment',
                y='P_Litre_Simule',
                color='Segment',
                title="Distribution des Prix au Litre par Segment",
                labels={'P_Litre_Simule': 'Prix au Litre (FCFA/L)'}
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        st.subheader("Analyse de Cohérence des Prix")
        
        # Vérifier la cohérence par rôle OBPPC
        alerts = []
        
        # Vérifier la hiérarchie des rôles
        for segment in df_sim['Segment'].unique():
            segment_data = df_sim[df_sim['Segment'] == segment]
            
            for role_pair in [('Entry', 'Frequency'), ('Frequency', 'Premium'), ('Entry', 'Premium'), ('Value', 'Premium')]:
                role_low = role_pair[0]
                role_high = role_pair[1]
                
                if role_low in segment_data['Role_OBPPC'].values and role_high in segment_data['Role_OBPPC'].values:
                    price_low = segment_data[segment_data['Role_OBPPC'] == role_low]['P_Litre_Simule'].min()
                    price_high = segment_data[segment_data['Role_OBPPC'] == role_high]['P_Litre_Simule'].min()
                    
                    if price_low >= price_high:
                        alerts.append({
                            'Type': '⚠️ Hiérarchie',
                            'Segment': segment,
                            'Message': f'{role_low} ({price_low:.0f} FCFA/L) devrait être inférieur à {role_high} ({price_high:.0f} FCFA/L)'
                        })
        
        # Vérifier les écarts trop importants
        for segment in df_sim['Segment'].unique():
            segment_data = df_sim[df_sim['Segment'] == segment]
            
            for role in segment_data['Role_OBPPC'].unique():
                role_data = segment_data[segment_data['Role_OBPPC'] == role]
                if len(role_data) > 1:
                    mean_price = role_data['P_Litre_Simule'].mean()
                    std_price = role_data['P_Litre_Simule'].std()
                    
                    for _, row in role_data.iterrows():
                        if abs(row['P_Litre_Simule'] - mean_price) > 1.5 * std_price:
                            alerts.append({
                                'Type': '📊 Écart',
                                'Segment': segment,
                                'Message': f'{row["Description"]} : {row["P_Litre_Simule"]:.0f} FCFA/L est éloigné de la moyenne {role} ({mean_price:.0f} FCFA/L)'
                            })
        
        if show_alerts and alerts:
            st.warning(f"**{len(alerts)} alertes de cohérence détectées**")
            
            for alert in alerts:
                if alert['Type'] == '⚠️ Hiérarchie':
                    st.error(f"{alert['Type']} - {alert['Segment']} : {alert['Message']}")
                else:
                    st.warning(f"{alert['Type']} - {alert['Segment']} : {alert['Message']}")
        else:
            st.success("✅ Aucune alerte de cohérence majeure détectée")
        
        # Matrice de cohérence
        st.subheader("Matrice de Positionnement par Segment")
        
        for segment in df_sim['Segment'].unique():
            segment_data = df_sim[df_sim['Segment'] == segment]
            pivot_data = segment_data.pivot_table(
                values='Index_PVF_Simule' if index_type == 'Index PVF' else 'Index_P_Litre_Simule',
                index='Marque',
                columns='Role_OBPPC',
                aggfunc='mean'
            ).round(1)
            
            st.markdown(f"**{segment}**")
            fig_heatmap = px.imshow(
                pivot_data,
                title=f"Heatmap des Index - {segment}",
                labels=dict(color=f"Index {index_type}"),
                aspect="auto",
                text_auto=True,
                height=300
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
    
    with tab4:
        st.subheader("Synthèse de la Simulation")
        
        # KPIs
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        
        with kpi1:
            avg_index = df_sim['Index_PVF_Simule' if index_type == 'Index PVF' else 'Index_P_Litre_Simule'].mean()
            st.metric("Index Moyen", f"{avg_index:.1f}")
        
        with kpi2:
            avg_price = df_sim['PVF_Simule'].mean()
            st.metric("PVF Moyen", f"{avg_price:,.0f} FCFA")
        
        with kpi3:
            avg_p_litre = df_sim['P_Litre_Simule'].mean()
            st.metric("Prix/Litre Moyen", f"{avg_p_litre:,.0f} FCFA/L")
        
        with kpi4:
            nb_products = len(df_sim)
            st.metric("Nombre de produits", nb_products)
        
        # Résumé par segment
        st.subheader("Résumé par Segment")
        segment_summary = df_sim.groupby('Segment').agg({
            'PVF_Simule': ['mean', 'min', 'max'],
            'P_Litre_Simule': ['mean', 'min', 'max'],
            'Index_PVF_Simule' if index_type == 'Index PVF' else 'Index_P_Litre_Simule': ['mean', 'min', 'max']
        }).round(1)
        
        st.dataframe(segment_summary, use_container_width=True)
        
        # Résumé par rôle OBPPC
        st.subheader("Résumé par Rôle OBPPC")
        role_summary = df_sim.groupby(['Segment', 'Role_OBPPC']).agg({
            'Index_PVF_Simule' if index_type == 'Index PVF' else 'Index_P_Litre_Simule': 'mean',
            'PVF_Simule': 'mean',
            'P_Litre_Simule': 'mean'
        }).round(1)
        
        st.dataframe(role_summary, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
    **💡 Guide d'utilisation :**
    - Filtrez par segment et marque dans la sidebar
    - Choisissez le type d'index à ajuster
    - Modifiez les index avec les sliders
    - Observez l'impact en temps réel dans le tableau et les graphiques
    - Vérifiez la cohérence dans l'onglet Analyse
""")
