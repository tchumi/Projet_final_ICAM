"""
Ce script effectue les opérations suivantes :
1. Chargement des fichiers de données :
    - Fichier des élections fusionnées nettoyé.
    - Fichier des communes avec noms enrichis.
2. Nettoyage des données :
    - Suppression des lignes avec des codes communes invalides (".", "").
3. Fusion des données :
    - Fusion des données des élections avec les noms des communes basées sur le code commune.
4. Vérification et rapport :
    - Vérification des communes sans nom après la fusion.
    - Génération d'un rapport listant les communes sans nom et le nombre de lignes supprimées.
5. Sauvegarde des résultats :
    - Enregistrement du fichier fusionné avec les noms des communes.

"""

import pandas as pd
import os

# 📍 Chemins des fichiers
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
ELECTIONS_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned.csv")
COMMUNE_FILE = os.path.join(DATA_DIR, "Taille_agglo_commune_csv/codescommunes2014_enrichi.csv")
OUTPUT_FILE = os.path.join(DATA_DIR, "elections_fusionnees_cleaned_with_names.csv")
REPORT_FILE = "rapport_elections_fusionnees_nom_communes.txt"

# 📌 Chargement du fichier des élections
df_elections = pd.read_csv(ELECTIONS_FILE, sep=",", dtype={"codecommune": str})

# 📌 Chargement du fichier des communes (avec noms)
df_communes = pd.read_csv(COMMUNE_FILE, sep=",", dtype={"codecommune": str})

# 📌 Sélection des colonnes utiles du fichier des communes
df_communes = df_communes[["codecommune", "nomcommune"]]

# 📌 Suppression des lignes avec code commune "."
invalid_codes = [".", ""]
df_elections_cleaned = df_elections[~df_elections["codecommune"].isin(invalid_codes)]

# 📌 Nombre de lignes supprimées
rows_removed = len(df_elections) - len(df_elections_cleaned)

# 📌 Fusion avec le fichier des communes
df_merged = df_elections_cleaned.merge(df_communes, on="codecommune", how="left")

# 📌 Vérification des communes manquantes après fusion
missing_names = df_merged[df_merged["nomcommune"].isnull()]

# 📌 Écriture du rapport des communes sans nom
with open(REPORT_FILE, "w", encoding="utf-8") as report:
    report.write("📌 Rapport de la fusion des communes\n")
    report.write("===================================\n\n")
    report.write(f"⚠️ Nombre total de communes sans nom après fusion : {len(missing_names)}\n\n")
    report.write(f"🗑️ Nombre de lignes supprimées (code commune '.' ou vide) : {rows_removed}\n\n")
    
    if not missing_names.empty:
        report.write("📌 Liste des codes communes et années concernées :\n")
        report.write(missing_names[["codecommune", "année"]].to_string(index=False))
    
print(f"⚠️ {len(missing_names)} communes sans nom après fusion.")
print(f"🗑️ {rows_removed} lignes supprimées (code commune invalide).")
print(f"📄 Rapport généré : {REPORT_FILE}")

# 📌 Sauvegarde du fichier complété
df_merged.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Fichier enrichi avec noms des communes enregistré sous : {OUTPUT_FILE}")
