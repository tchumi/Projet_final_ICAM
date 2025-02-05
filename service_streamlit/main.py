import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

# 📍 Chemins des fichiers
geojson_path = "C:/Users/Admin.local/Documents/Projet_final_data/contours-simplifies.geojson"
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_fusionnees_cleaned_with_names_clusters.csv"

# 🎯 Configurer Streamlit
st.set_page_config(layout="wide")
st.title("Dynamique des Clusters des Communes - Élections Présidentielles")

# 📥 Charger les données électorales et les contours des communes
@st.cache_data
def load_data():
    df = pd.read_csv(data_path, sep=",", dtype=str, low_memory=False)
    gdf = gpd.read_file(geojson_path)
    return df, gdf

df_votes, gdf_communes = load_data()

# 📌 Vérifier et uniformiser les colonnes
if "codeCommune" in gdf_communes.columns:
    gdf_communes = gdf_communes.rename(columns={"codeCommune": "codecommune"})

# 📌 Assurer que `codecommune` est bien une chaîne de caractères
df_votes["codecommune"] = df_votes["codecommune"].astype(str)
gdf_communes["codecommune"] = gdf_communes["codecommune"].astype(str)

# 🔥 Convertir les colonnes numériques
for col in ["pvoteT2_G", "pvoteT2_D", "pvoteT2_C", "pvoteT2_CD", "pvoteT2_ED"]:
    df_votes[col] = pd.to_numeric(df_votes[col], errors="coerce")

# 📌 Sélection de l'année électorale
selected_year = st.selectbox("Sélectionner une élection (année) :", sorted(df_votes["année"].unique(), reverse=True))

# 📌 Sélection du tour de l'élection
tour_options = {"1er tour": "cluster_1er_tour", "2nd tour": "cluster_2nd_tour"}
selected_tour = st.radio("Sélectionner le tour :", list(tour_options.keys()))

# 📌 Filtrer les données selon l’année et le tour
df_filtered = df_votes[df_votes["année"] == selected_year]
cluster_column = tour_options[selected_tour]

# 📌 Sélection des clusters disponibles
available_clusters = sorted(df_filtered[cluster_column].dropna().unique())
selected_clusters = st.multiselect("Sélectionner un ou plusieurs clusters :", available_clusters, default=available_clusters[:3])

# 📌 Filtrer les données par clusters sélectionnés
df_filtered = df_filtered[df_filtered[cluster_column].isin(selected_clusters)]

# 🔗 Fusion entre résultats électoraux et contours des communes
gdf_final = gdf_communes.merge(df_filtered, on="codecommune", how="left")

# 🔥 Convertir les clusters en numérique
gdf_final[cluster_column] = pd.to_numeric(gdf_final[cluster_column], errors='coerce')

# 🔥 Remplacer les valeurs NaN par -1 pour éviter les erreurs dans Folium
gdf_final[cluster_column].fillna(-1, inplace=True)

# 📌 Définition des couleurs par cluster
color_palette = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
color_dict = {cid: color_palette[i % len(color_palette)] for i, cid in enumerate(available_clusters)}

# 🗺️ Création de la carte avec Folium
st.write("📌 Génération de la carte...")

m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodb positron")

# 🔥 Vérification des valeurs avant de créer Choropleth
st.write("Valeurs des clusters après conversion :")
st.write(gdf_final[cluster_column].unique())  # Débugging

# 🔥 Ajouter la carte choroplèthe pour afficher les clusters sélectionnés
choropleth = folium.Choropleth(
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

# 📌 Ajouter des popups avec détails des votes
for _, row in gdf_final.iterrows():
    folium.Marker(
        location=[row.geometry.centroid.y, row.geometry.centroid.x],
        popup=folium.Popup(
            f"Commune: {row['nomcommune']}<br>"
            f"Cluster: {row[cluster_column]}<br>"
            f"Gauche: {row['pvoteT2_G']}%<br>"
            f"Centre: {row['pvoteT2_C']}%<br>"
            f"Droite: {row['pvoteT2_D']}%<br>"
            f"Extrême Droite: {row['pvoteT2_ED']}%",
            max_width=300
        ),
        icon=folium.Icon(color=color_dict.get(row[cluster_column], "gray"))
    ).add_to(m)

# 🗺️ Afficher la carte dans Streamlit
st_folium(m, width=1000, height=600)

st.success("✅ Carte affichée avec succès !")
