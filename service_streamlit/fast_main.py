import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

# 📍 Chemins des fichiers
geojson_path = "C:/Users/Admin.local/Documents/Projet_final_data/contours-simplifies.geojson"
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_fusionnees_cleaned_with_names_clusters.csv"

# 🎯 Configurer Streamlit
st.set_page_config(layout="wide")
st.title("📊 Dynamique des Clusters des Communes - Élections Présidentielles")

# 📥 Mise en cache des données électorales et géographiques
@st.cache_data
def load_data():
    df = pd.read_csv(data_path, sep=",", dtype=str, low_memory=False)
    gdf = gpd.read_file(geojson_path)
    
    # ⚡ Simplifier la géométrie du GeoJSON pour accélérer l'affichage
    gdf["geometry"] = gdf["geometry"].simplify(tolerance=0.001, preserve_topology=True)
    
    return df, gdf

df_votes, gdf_communes = load_data()

# 📌 Vérifier et uniformiser les colonnes
if "codeCommune" in gdf_communes.columns:
    gdf_communes = gdf_communes.rename(columns={"codeCommune": "codecommune"})

# 📌 Assurer que `codecommune` est bien une chaîne de caractères
df_votes["codecommune"] = df_votes["codecommune"].astype(str)
gdf_communes["codecommune"] = gdf_communes["codecommune"].astype(str)

# 🔥 Convertir les colonnes numériques et ajuster les pourcentages
for col in ["pvoteG", "pvoteCG", "pvoteC", "pvoteCD", "pvoteD", "pvoteT2_G", "pvoteT2_C", "pvoteT2_CD", "pvoteT2_D", "pvoteT2_ED"]:
    df_votes[col] = pd.to_numeric(df_votes[col], errors="coerce") * 100
    df_votes[col] = df_votes[col].round(2)

# 📌 Sidebar pour les filtres
with st.sidebar:
    st.header("🔍 Filtres")
    
    # Sélection de l'année électorale
    selected_year = st.selectbox("📅 Sélectionner une année :", sorted(df_votes["année"].unique(), reverse=True))
    
    # Sélection du tour de l'élection
    tour_options = {"1er tour": "cluster_1er_tour", "2nd tour": "cluster_2nd_tour"}
    selected_tour = st.radio("📌 Sélectionner le tour :", list(tour_options.keys()))
    
    # Filtrer les données selon l’année et le tour
    df_filtered = df_votes[df_votes["année"] == selected_year].copy()
    cluster_column = tour_options[selected_tour]

    # Sélection des clusters disponibles
    available_clusters = sorted(df_filtered[cluster_column].dropna().unique())
    selected_clusters = st.multiselect("📍 Sélectionner les clusters pour la carte :", available_clusters, default=available_clusters[:3])

# 📌 Fonction pour générer la carte Folium avec **les clusters sélectionnés uniquement**
def generate_map(filtered_df, cluster_column):
    # Filtrer les données pour la carte
    filtered_df = filtered_df[filtered_df[cluster_column].isin(selected_clusters)].copy()

    # 🔗 Fusion entre résultats électoraux et contours des communes
    gdf_final = gdf_communes.merge(filtered_df, on="codecommune", how="left")

    # 🔥 Convertir les clusters en numérique et éviter les NaN
    gdf_final[cluster_column] = pd.to_numeric(gdf_final[cluster_column], errors='coerce').fillna(-1)

    # 📌 Réduction des données affichées (ex: limiter à 5000 communes)
    if len(gdf_final) > 5000:
        gdf_final = gdf_final.sample(5000, random_state=42)

    # 📌 Définition des couleurs par cluster
    color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
    color_dict = {cid: color_palette[i % len(color_palette)] for i, cid in enumerate(selected_clusters)}

    # 🗺️ Création de la carte avec Folium
    m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodb positron")

    # 🔥 Ajouter la carte choroplèthe pour afficher les clusters sélectionnés
    folium.Choropleth(
        geo_data=gdf_final,
        name="Clusters Présidentielle",
        data=gdf_final,
        columns=["codecommune", cluster_column],
        key_on="feature.properties.codecommune",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"Clusters ({selected_tour})"
    ).add_to(m)

    return m

# 📌 Générer et afficher la carte
col1, col2 = st.columns([2, 1])

with col1:
    if selected_clusters:
        st.write("📌 Carte interactive des clusters")
        folium_map = generate_map(df_filtered, cluster_column)
        st_folium(folium_map, width=1000, height=600)
        st.success("✅ Carte affichée avec succès !")
    else:
        st.warning("⚠️ Veuillez sélectionner au moins un cluster pour afficher la carte.")

# 📌 Générer et afficher les camemberts pour **tous les clusters** du tour
with col2:
    st.write("📊 Répartition des votes par cluster")

    all_clusters = sorted(df_filtered[cluster_column].dropna().unique())  # Tous les clusters du tour

    for cluster in all_clusters:
        cluster_data = df_filtered[df_filtered[cluster_column] == cluster]

        # Somme pondérée des votes pour le cluster sélectionné
        if selected_tour == "1er tour":
            vote_columns = ["pvoteG", "pvoteCG", "pvoteC", "pvoteCD", "pvoteD"]
            labels = ["Gauche", "Centre-Gauche", "Centre", "Centre-Droite", "Droite"]
        else:
            vote_columns = ["pvoteT2_G", "pvoteT2_C", "pvoteT2_CD", "pvoteT2_D", "pvoteT2_ED"]
            labels = ["Gauche", "Centre", "Centre-Droite", "Droite", "Extrême Droite"]

        votes = cluster_data[vote_columns].sum().values

        # Ne garder que les labels et valeurs non nulles
        valid_indices = votes > 0
        filtered_votes = votes[valid_indices]
        filtered_labels = [labels[i] for i in range(len(labels)) if valid_indices[i]]

        # Générer le camembert
        fig, ax = plt.subplots(figsize=(3.5, 3.5))  # Réduction de 20% de la taille
        ax.pie(filtered_votes, labels=filtered_labels, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', startangle=90, colors=["blue", "lightblue", "yellow", "orange", "red"])
        ax.axis('equal')  # Camembert en cercle parfait

        st.write(f"Cluster {cluster}")
        st.pyplot(fig)
