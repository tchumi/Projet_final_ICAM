import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium

# 📍 Chemins des fichiers
geojson_path = "C:/Users/Admin.local/Documents/Projet_final_data/contours-simplifies.geojson"
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/pres2022_csv/pres2022comm.csv"

# 🎯 Configurer Streamlit
st.set_page_config(layout="wide")
st.title("Carte des Résultats Présidentielle 2022 - Second Tour")

# 📥 Charger les données électorales
st.write("🔄 Chargement des résultats électoraux...")
df_votes = pd.read_csv(data_path, sep=",", dtype=str, low_memory=False)

# 📥 Charger le fichier GEOJSON simplifié
st.write("🔄 Chargement du fichier des communes...")
gdf_communes = gpd.read_file(geojson_path)

# 📌 Vérification des colonnes pour `codecommune`
if "codeCommune" in gdf_communes.columns:
    gdf_communes = gdf_communes.rename(columns={"codeCommune": "codecommune"})
elif "id_bv" in gdf_communes.columns:  
    gdf_communes["codecommune"] = gdf_communes["id_bv"].str[:5]

# 📌 Assurer que `codecommune` est bien une chaîne de caractères
gdf_communes["codecommune"] = gdf_communes["codecommune"].astype(str)

# 📌 Sélection des colonnes utiles des votes
columns_votes = ["codecommune", "pvoixT2MACRON", "pvoixT2MLEPEN"]
df_votes = df_votes[columns_votes]

# 🔥 Convertir les colonnes en float
df_votes["pvoixT2MACRON"] = pd.to_numeric(df_votes["pvoixT2MACRON"], errors="coerce")
df_votes["pvoixT2MLEPEN"] = pd.to_numeric(df_votes["pvoixT2MLEPEN"], errors="coerce")

# 🔗 Fusion entre résultats électoraux et contours des communes
gdf_final = gdf_communes.merge(df_votes, on="codecommune", how="left")

# 🔥 Remplacer les NaN par 0 pour éviter les erreurs
gdf_final["pvoixT2MACRON"] = gdf_final["pvoixT2MACRON"].fillna(0)
gdf_final["pvoixT2MLEPEN"] = gdf_final["pvoixT2MLEPEN"].fillna(0)

# 🗺️ Création de la carte avec Folium
st.write("📌 Génération de la carte...")

# 📌 Définir la carte centrée sur la France
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodb positron")

# 🔥 Ajouter les résultats sous forme de carte choroplèthe (coloration des communes)
choropleth = folium.Choropleth(
    geo_data=gdf_final,
    name="Présidentielle 2022",
    data=gdf_final,
    columns=["codecommune", "pvoixT2MACRON"],
    key_on="feature.properties.codecommune",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="% Voix Macron (Second Tour)"
).add_to(m)

# 🗺️ Afficher la carte dans Streamlit avec `st_folium`
st_folium(m, width=1000, height=600)

st.success("✅ Carte affichée avec succès !")
