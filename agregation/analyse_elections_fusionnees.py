"""
Ce script analyse les valeurs manquantes dans un fichier CSV contenant des données d'élections fusionnées, et génère un rapport détaillé sur ces valeurs manquantes. Il propose également trois méthodes de correction des valeurs manquantes et sauvegarde les datasets corrigés.
Fonctionnalités :
1. Chargement du fichier CSV contenant les données d'élections fusionnées.
2. Vérification et comptage des valeurs manquantes par colonne.
3. Analyse de l'impact des valeurs manquantes par année et par commune.
4. Génération d'un rapport détaillé sur les valeurs manquantes.
5. Correction des valeurs manquantes par trois méthodes différentes :
    - Suppression des lignes avec des valeurs manquantes.
    - Interpolation temporelle des valeurs manquantes par commune.
    - Remplissage des valeurs manquantes par la moyenne annuelle.
6. Sauvegarde des datasets corrigés dans des fichiers CSV distincts.
Variables :
- DATA_DIR : Chemin du répertoire contenant les données.
- FILE_PATH : Chemin complet du fichier CSV à analyser.
- REPORT_PATH : Chemin complet du fichier de rapport à générer.
- df : DataFrame contenant les données chargées depuis le fichier CSV.
- missing_values : Série contenant le nombre de valeurs manquantes par colonne.
- missing_by_year : Série contenant le nombre de lignes affectées par année.
- missing_by_commune : Nombre de communes affectées par des valeurs manquantes.
- df_cleaned : DataFrame après suppression des lignes avec des valeurs manquantes.
- df_interpolated : DataFrame après interpolation des valeurs manquantes par commune.
- df_filled : DataFrame après remplissage des valeurs manquantes par la moyenne annuelle.

"""

import pandas as pd
import os

# 📍 Chemin du fichier fusionné
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
FILE_PATH = os.path.join(DATA_DIR, "elections_fusionnees.csv")
REPORT_PATH = "analyse_manquants_elections_presidentielles.txt"

# 📌 Chargement du fichier
df = pd.read_csv(FILE_PATH, sep=",", dtype={"codecommune": str})

# 📌 Vérification des valeurs manquantes
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]

# 📌 Vérification de l'impact des valeurs manquantes par année
missing_by_year = df[df.isnull().any(axis=1)].groupby("année").size()

# 📌 Vérification de l'impact des valeurs manquantes par commune
missing_by_commune = df[df.isnull().any(axis=1)]["codecommune"].nunique()

# 📌 Écriture du rapport dans un fichier
with open(REPORT_PATH, "w", encoding="utf-8") as report:

    report.write(f"✅ Nombre total de lignes : {df.shape[0]}\n")
    report.write(f"✅ Nombre total de colonnes : {df.shape[1]}\n\n")

    report.write("📌 Colonnes avec des valeurs manquantes :\n")
    if missing_values.empty:
        report.write("✅ Aucune valeur manquante détectée.\n\n")
    else:
        report.write(missing_values.to_string() + "\n\n")

    report.write("📌 Nombre de lignes affectées par année :\n")
    report.write(missing_by_year.to_string() + "\n\n")

    report.write("📌 Nombre de communes concernées :\n")
    report.write(f"✅ {missing_by_commune} communes affectées sur {df['codecommune'].nunique()}\n\n")

    # 📌 Correction des valeurs manquantes (3 méthodes)

    # 1️⃣ Suppression des lignes avec valeurs manquantes
    df_cleaned = df.dropna()

    # 2️⃣ Interpolation temporelle avec correction du problème d'index
    df_interpolated = df.copy()
    
    # Séparer les colonnes numériques et non-numériques
    numeric_cols = df_interpolated.select_dtypes(include=['number']).columns

    # Interpolation sans modifier l'index
    df_interpolated[numeric_cols] = df_interpolated.groupby("codecommune")[numeric_cols].transform(lambda group: group.interpolate())

    # 3️⃣ Remplissage avec la moyenne par année
    df_filled = df.copy()
    df_filled[numeric_cols] = df_filled.groupby("année")[numeric_cols].transform("mean")

    # 📌 Sauvegarde des fichiers corrigés dans le même répertoire que le fichier source
    df_cleaned.to_csv(os.path.join(DATA_DIR, "elections_fusionnees_cleaned.csv"), index=False)
    df_interpolated.to_csv(os.path.join(DATA_DIR, "elections_fusionnees_interpolated.csv"), index=False)
    df_filled.to_csv(os.path.join(DATA_DIR, "elections_fusionnees_filled.csv"), index=False)

    report.write("✅ Trois versions du dataset corrigé ont été enregistrées :\n")
    report.write(f"- `{os.path.join(DATA_DIR, 'elections_fusionnees_cleaned.csv')}` (lignes supprimées)\n")
    report.write(f"- `{os.path.join(DATA_DIR, 'elections_fusionnees_interpolated.csv')}` (valeurs interpolées par commune)\n")
    report.write(f"- `{os.path.join(DATA_DIR, 'elections_fusionnees_filled.csv')}` (remplissage par moyenne annuelle)\n\n")

print(f"📄 Rapport généré et enregistré sous : {REPORT_PATH}")
