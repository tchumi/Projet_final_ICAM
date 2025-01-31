import geopandas as gpd

# 📍 Chemin du fichier d'origine
geojson_path = "C:/Users/Admin.local/Documents/Projet_final_data/contours-france-entiere-latest-v2.geojson"

# 📥 Charger le fichier GEOJSON
print("🔄 Chargement du fichier GEOJSON...")
gdf_communes = gpd.read_file(geojson_path)

# 🧐 Afficher les premières lignes
print(gdf_communes.head())

# 📌 Vérifier la colonne qui contient le code commune
# (On suppose ici qu'elle s'appelle "codeCommune" ou "id_bv")
if "codeCommune" in gdf_communes.columns:
    gdf_communes = gdf_communes.rename(columns={"codeCommune": "codecommune"})
elif "id_bv" in gdf_communes.columns:  # Si les données sont par bureau de vote
    gdf_communes["codecommune"] = gdf_communes["id_bv"].str[:5]

# ✅ Vérifier la structure après renommage
print("✅ Colonnes disponibles :", gdf_communes.columns)

# 🚀 Réduction de la complexité des polygones
# 🔥 Facteur de simplification : Plus la valeur est grande, plus la précision baisse
simplification_factor = 0.01  # 1% des points conservés
print(f"🔧 Simplification des polygones avec un facteur de {simplification_factor}...")

gdf_communes["geometry"] = gdf_communes["geometry"].simplify(simplification_factor, preserve_topology=True)

# 📉 Afficher la réduction de taille des polygones
original_size = gdf_communes.memory_usage(deep=True).sum() / (1024 * 1024)  # Mo
print(f"📏 Taille du fichier avant simplification : {original_size:.2f} Mo")

# 🔽 Sauvegarde du fichier simplifié
output_path = "C:/Users/Admin.local/Documents/Projet_final_data/contours-simplifies.geojson"
gdf_communes.to_file(output_path, driver="GeoJSON")

# 📉 Vérifier la taille après simplification
new_size = gdf_communes.memory_usage(deep=True).sum() / (1024 * 1024)  # Mo
print(f"✅ Taille du fichier après simplification : {new_size:.2f} Mo")

print(f"🎉 Fichier GEOJSON simplifié sauvegardé : {output_path}")
