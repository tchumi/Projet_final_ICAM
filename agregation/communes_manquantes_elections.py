import pandas as pd
import os

# 📍 Chemin des fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
FILE_PATH = os.path.join(DATA_DIR, "elections_fusionnees.csv")
COMMUNE_FILE = os.path.join(DATA_DIR, "Taille_agglo_commune_csv/codescommunes2014.csv")
OUTPUT_PATH = os.path.join(DATA_DIR, "communes_manquantes.csv")

# 📌 Chargement du fichier des élections
df = pd.read_csv(FILE_PATH, sep=",", dtype={"codecommune": str})

# 📌 Chargement du fichier des communes (avec noms et départements)
df_communes = pd.read_csv(COMMUNE_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des colonnes utiles du fichier des communes
df_communes = df_communes[["codecommune", "nomcommune", "dep", "nomdep"]]

# 📌 Sélection des communes avec des valeurs manquantes
df_missing = df[df.isnull().any(axis=1)]

# 📌 Fusion avec le fichier des noms de communes
df_missing = df_missing.merge(df_communes, on="codecommune", how="left")

# 📌 Sélection des colonnes finales
columns_to_keep = ["codecommune", "nomcommune", "dep", "nomdep", "année", "exprimes", "voteG", "voteCG", "voteC", "voteCD",
                   "voteD", "voteTG", "voteTD", "voteGCG", "voteDCD", "pvoteG", "pvoteCG", "pvoteC", "pvoteCD",
                   "pvoteD", "pvoteTG", "pvoteTD", "pvoteTGratio", "pvoteTDratio"]

df_missing = df_missing[columns_to_keep]

# 📌 Enregistrement du fichier des communes concernées avec noms
df_missing.to_csv(OUTPUT_PATH, index=False)

print(f"📄 Liste des communes avec valeurs manquantes enregistrée sous : {OUTPUT_PATH}")
