import pandas as pd
import geopandas as gpd
import folium
import numpy as np
from shapely.geometry import Polygon
from streamlit_folium import st_folium
import streamlit as st

# 📍 Chemins des fichiers
data_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_fusionnees_tracking_1er_tour.csv"
geojson_path = "C:/Users/Admin.local/Documents/Projet_final_data/contours-simplifies.geojson"

# 📌 Chargement des données
df = pd.read_csv(data_path, sep=",", dtype={"codecommune": str})
gdf_communes = gpd.read_file(geojson_path)

# 📌 Assurer la compatibilité des codes communes
gdf_communes = gdf_communes.rename(columns={"codeCommune": "codecommune"})
gdf_communes["codecommune"] = gdf_communes["codecommune"].astype(str)
df["codecommune"] = df["codecommune"].astype(str)

# 📌 Reprojection des géométries en EPSG:3857
gdf_communes = gdf_communes.to_crs(epsg=3857)

# 📌 Barre latérale avec filtres
st.sidebar.title("🔍 Filtres et Debug")
selected_year = st.sidebar.selectbox("📅 Sélectionner une année :", sorted(df["année"].unique(), reverse=True))
available_clusters = sorted(df["cluster_corrige_1er_tour"].dropna().unique())
selected_clusters = st.sidebar.multiselect("📍 Sélectionner les clusters à afficher :", available_clusters, default=available_clusters)

# 📌 Filtrer les données selon les sélections (PAS DE RÉDUCTION ICI)
df_filtered = df[(df["année"] == selected_year) & (df["cluster_corrige_1er_tour"].isin(selected_clusters))]

# 📌 Fusionner les données électorales avec le GeoJSON
gdf_final = gdf_communes.merge(df_filtered, on="codecommune", how="left")

# 📌 Vérification des données fusionnées
st.sidebar.write("📌 Nombre de communes fusionnées :", gdf_final.shape[0])
st.sidebar.write("📌 Exemples de clusters affectés :", gdf_final[["codecommune", "cluster_corrige_1er_tour"]].dropna().head())

# 📌 Simplification du GeoJSON
gdf_final["geometry"] = gdf_final["geometry"].simplify(tolerance=100, preserve_topology=True)
st.sidebar.success("✅ Simplification des géométries appliquée.")

# 📌 Création de la grille Hexbin
xmin, ymin, xmax, ymax = gdf_final.total_bounds
hex_size = 10000  # Réduction à 10 km
cols = np.arange(xmin, xmax, hex_size * 1.5)
rows = np.arange(ymin, ymax, hex_size * np.sqrt(3))
hexagons = []

for x in cols:
    for y in rows:
        hexagon = Polygon([(x, y), (x + hex_size, y), (x + hex_size * 1.5, y + hex_size * np.sqrt(3)/2),
                            (x + hex_size, y + hex_size * np.sqrt(3)), (x, y + hex_size * np.sqrt(3)),
                            (x - hex_size * 0.5, y + hex_size * np.sqrt(3)/2)])
        hexagons.append(hexagon)

gdf_hex = gpd.GeoDataFrame(geometry=hexagons, crs=gdf_final.crs)

# 📌 Filtrer les hexagones pour ne garder que ceux qui intersectent les communes
gdf_bounds = gdf_final.geometry.buffer(0).union_all().envelope
valid_hexagons = [hexagon for hexagon in gdf_hex.geometry if hexagon.intersects(gdf_bounds)]
gdf_hex = gpd.GeoDataFrame(geometry=valid_hexagons, crs=gdf_final.crs)
st.sidebar.write("📌 Nombre d'hexagones après filtrage :", gdf_hex.shape[0])

# 📌 Attribution des clusters aux hexagones
gdf_final["centroid"] = gdf_final.geometry.centroid
gdf_final = gdf_final.set_geometry("centroid")
gdf_merged = gpd.sjoin(gdf_final, gdf_hex, how="left", predicate="intersects")

def safe_mode(series):
    if series.empty or series.dropna().empty:
        return np.nan  # Retourne NaN si aucun cluster n'est disponible
    return series.value_counts().idxmax()  # Retourne le cluster dominant sinon

gdf_hex["cluster"] = gdf_merged.groupby("index_right")["cluster_corrige_1er_tour"].apply(safe_mode)

# 📌 Vérification avant affichage
st.sidebar.write("📌 Nombre d'hexagones attribués après correction :", gdf_hex["cluster"].notna().sum())
st.sidebar.write("📌 Nombre d'hexagones sans cluster :", gdf_hex["cluster"].isna().sum())

# 📌 Réduction à 5000 hexagones pour l'affichage (PAS AVANT)
if len(gdf_hex) > 5000:
    gdf_hex = gdf_hex.sample(n=5000, random_state=42)
    st.sidebar.warning("⚠️ Affichage limité à 5000 hexagones pour optimiser le rendu.")

# 📌 Création de la carte Folium
m = folium.Map(location=[46.603354, 1.888334], zoom_start=6, tiles="cartodb positron")
folium.Choropleth(
    geo_data=gdf_hex,
    name="Clusters Hexbins",
    data=gdf_hex,
    columns=[gdf_hex.index, "cluster"],
    key_on="feature.id",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Cluster Dominant"
).add_to(m)

# 📌 Affichage de la carte avec Streamlit
st_folium(m, width=1000, height=600)

st.sidebar.success("✅ Carte Hexbin générée avec succès !")
