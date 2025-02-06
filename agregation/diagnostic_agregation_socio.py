import pandas as pd
import os

# 📍 Chemin du fichier
DATA_PATH = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/df_final_transposed_socio.csv"
DIAGNOSTIC_PATH = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/diagnostic_transposed.txt"

# 📌 Chargement du fichier
df = pd.read_csv(DATA_PATH)

# 📌 Vérification des dimensions
num_rows, num_cols = df.shape

# 📌 Vérification des années
expected_years = list(range(1960, 2023))  # De 1960 à 2022
unique_years = sorted(df["année"].unique())

# 📌 Vérification des communes uniques
num_communes = df["codecommune"].nunique()

# 📌 Vérification des colonnes attendues
expected_columns = ["codecommune", "année", "revratio",
                    "pchom", "pouvr", "pcadr", "pbac", "psup", "ppropri", "petranger",
                    "pop", "propf", "propA", "propB", "propC", "prop60p", "age",
                    "pibratio"]
# expected_columns = ["codecommune", "année", "revmoy", "revmoyfoy", "revratio",
#                     "pchom", "pouvr", "pcadr", "pbac", "psup", "ppropri", "petranger",
#                     "pop", "propf", "propA", "propB", "propC", "prop60p", "age",
#                     "pibratio", "pibtot", "capitalratio", "capitalimmo", "pisf"]

missing_columns = [col for col in expected_columns if col not in df.columns]

# 📌 Vérification des valeurs manquantes
missing_values = df.isna().sum()
missing_values = missing_values[missing_values > 0]

# 📌 Vérification des doublons
duplicated_rows = df[df.duplicated(subset=["codecommune", "année"], keep=False)]

# 📌 Vérification de la cohérence des proportions (0-100)
proportion_columns = ["propf", "prop014", "propB", "propC", "prop60p", "pchom", "pouvr", "pcadr", "pbac", "psup", "petranger", "ppropri"]
issues = {}

for col in proportion_columns:
    if col in df.columns:
        invalid_values = df[(df[col] < 0) | (df[col] > 100)][col]
        if not invalid_values.empty:
            issues[col] = f"{len(invalid_values)} valeurs hors intervalle [0, 100]"

# 📌 Vérification des âges (0-120)
if "age" in df.columns:
    invalid_age = df[(df["age"] < 0) | (df["age"] > 120)]["age"]
    if not invalid_age.empty:
        issues["age"] = f"{len(invalid_age)} valeurs hors intervalle [0, 120]"

# 📌 Enregistrement du diagnostic
with open(DIAGNOSTIC_PATH, "w", encoding="utf-8") as diag_file:
    diag_file.write("📌 DIAGNOSTIC DU FICHIER TRANSPOSE\n")
    diag_file.write("="*50 + "\n")
    diag_file.write(f"🔍 Nombre de lignes : {num_rows}\n")
    diag_file.write(f"🔍 Nombre de colonnes : {num_cols}\n")
    diag_file.write(f"🏙️ Nombre total de communes : {num_communes}\n")
    diag_file.write(f"📆 Nombre total d'années : {len(unique_years)} (Attendu : {len(expected_years)})\n")
    diag_file.write(f"📅 Années détectées : {unique_years}\n")
    diag_file.write("="*50 + "\n")

    if missing_columns:
        diag_file.write("⚠️ Colonnes manquantes :\n")
        diag_file.write(", ".join(missing_columns) + "\n\n")

    if not missing_values.empty:
        diag_file.write("🔍 Valeurs manquantes par colonne :\n")
        diag_file.write(missing_values.to_string() + "\n\n")

    if not duplicated_rows.empty:
        diag_file.write(f"⚠️ {len(duplicated_rows)} doublons détectés sur 'codecommune' et 'année' \n")

    if issues:
        diag_file.write("⚠️ Anomalies détectées :\n")
        for col, msg in issues.items():
            diag_file.write(f"🔹 {col} : {msg}\n")

print(f"✅ Rapport de diagnostic généré : {DIAGNOSTIC_PATH}")
