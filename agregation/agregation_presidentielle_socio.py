import pandas as pd

# 📂 Chemins des fichiers
path_socio = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/df_final_transposed_socio.csv"
path_elections = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_fusionnees_tracking_1er_tour.csv"
output_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"

# 📌 Chargement des fichiers CSV avec gestion des types mixtes
df_socio = pd.read_csv(path_socio, dtype={"codecommune": str}, low_memory=False)
df_elections = pd.read_csv(path_elections, dtype={"codecommune": str, "année": int}, low_memory=False)

# 📌 Sélection des années électorales
years_electoral = [1965, 1969, 1974, 1981, 1988, 1995, 2002, 2007, 2012, 2017, 2022]
df_socio = df_socio[df_socio["année"].isin(years_electoral)]

# 📌 Gestion des valeurs manquantes
# Convertir les colonnes en types appropriés pour éviter l'erreur d'interpolation
df_socio = df_socio.infer_objects(copy=False)

# Séparer les colonnes numériques pour l'interpolation
numeric_cols = df_socio.select_dtypes(include=["number"]).columns

# Appliquer l'interpolation uniquement sur les colonnes numériques, en conservant l'alignement des index
df_socio[numeric_cols] = df_socio.groupby("codecommune")[numeric_cols].transform(lambda x: x.interpolate(method='linear'))

# Remplissage des valeurs manquantes avec la dernière valeur connue
df_socio.fillna(method="ffill", inplace=True)

# 📌 Fusion des fichiers sur "année" et "codecommune"
df_fusion = pd.merge(df_elections, df_socio, on=["année", "codecommune"], how="left")

# 📌 Vérification des données fusionnées
print(df_fusion.head())
print(df_fusion.isnull().sum())

# 📌 Sauvegarde du fichier final
df_fusion.to_csv(output_path, index=False)
print(f"✅ Fichier fusionné sauvegardé : {output_path}")
