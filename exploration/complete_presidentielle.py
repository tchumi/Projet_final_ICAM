"""
Ce script enrichit les fichiers CSV des résultats des élections présidentielles françaises avec des informations supplémentaires sur les votes du second tour par famille politique.
Fonctionnalités principales :
1. Détection des fichiers CSV des élections dans un répertoire donné.
2. Enrichissement des fichiers CSV avec des colonnes supplémentaires pour les votes du second tour par famille politique.
3. Vérification de la cohérence des totaux des votes.
4. Sauvegarde des fichiers enrichis dans un répertoire de sortie.
Variables globales :
- base_dir : Chemin du répertoire contenant les données des élections.
- output_dir : Chemin du répertoire où les fichiers enrichis seront sauvegardés.
- familles_politique_t2 : Dictionnaire des regroupements politiques pour le second tour des élections.
Fonctions :
- detect_elections(base_dir) : Détecte les fichiers CSV des élections dans le répertoire de base.
- enrich_election_data(file_path, election_year) : Enrichit un fichier CSV avec les votes du second tour par famille politique.
Utilisation :
1. Définir le chemin du répertoire de base contenant les données des élections.
2. Exécuter le script pour détecter et enrichir les fichiers CSV des élections.
3. Les fichiers enrichis seront sauvegardés dans le répertoire de sortie spécifié.
Exemple d'exécution :

"""

import os
import pandas as pd

# Chemins des répertoires
base_dir = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
#base_dir = "D:/Projet_final_data/Piketty_data"

output_dir = os.path.join(base_dir, "enriched_data")
os.makedirs(output_dir, exist_ok=True)

# Dictionnaire des regroupements politiques pour le 2nd tour
familles_politique_t2 = {
    "2022": {"MACRON": "C", "MLEPEN": "ED"},
    "2017": {"MACRON": "C", "MLEPEN": "ED"},
    "2012": {"HOLLANDE": "G", "SARKOZY": "D"},
    "2007": {"SARKOZY": "D", "ROYAL": "G"},
    "2002": {"CHIRAC": "D", "LEPEN": "ED"},
    "1995": {"CHIRAC": "D", "JOSPIN": "G"},
    "1988": {"MITTERRAND": "G", "CHIRAC": "D"},
    "1981": {"MITTERRAND": "G", "GISCARDDESTAING": "CD"},
    "1974": {"GISCARDDESTAING": "CD", "MITTERRAND": "G"},
    "1969": {"POMPIDOU": "D", "POHER": "C"},
    "1965": {"DEGAULLE": "D", "MITTERRAND": "G"},
}


# Fonction pour détecter les fichiers CSV des élections
def detect_elections(base_dir):
    elections = {}
    for folder in os.listdir(base_dir):
        if folder.startswith("pres") and folder.endswith("_csv"):
            folder_path = os.path.join(base_dir, folder)
            for file in os.listdir(folder_path):
                if file.endswith(".csv"):
                    elections[folder] = os.path.join(folder_path, file)
    return elections


# Détecte les fichiers électoraux disponibles
election_files = detect_elections(base_dir)


# Fonction pour enrichir les fichiers CSV avec les votes du 2nd tour par famille politique
def enrich_election_data(file_path, election_year):
    try:
        df = pd.read_csv(file_path, sep=",", dtype=str)
        columns = df.columns.tolist()

        # Vérifier si les données du second tour existent
        if "exprimesT2" not in columns:
            print(f"⚠️ Aucun second tour détecté dans {file_path}. Ignoré.")
            return

        df["exprimesT2"] = (
            pd.to_numeric(df["exprimesT2"], errors="coerce").fillna(0).astype(int)
        )

        # Initialisation des nouvelles colonnes avec des valeurs par défaut
        for famille in ["ED", "D", "CD", "C", "G"]:
            df[f"voteT2_{famille}"] = 0
            df[f"pvoteT2_{famille}"] = 0.0  # Force en float
            df[f"pvoteT2_{famille}ratio"] = 0.0  # Force en float

        # Attribution des votes aux familles politiques, ligne par ligne
        for candidat, famille in familles_politique_t2.get(election_year, {}).items():
            voix_col = f"voixT2{candidat.upper()}"
            pvoix_col = f"pvoixT2{candidat.upper()}"
            pvoix_ratio_col = f"pvoixT2{candidat.upper()}ratio"

            vote_col = f"voteT2_{famille}"
            pvote_col = f"pvoteT2_{famille}"
            pvote_ratio_col = f"pvoteT2_{famille}ratio"

            if voix_col in df.columns:
                df[voix_col] = (
                    pd.to_numeric(df[voix_col], errors="coerce").fillna(0).astype(int)
                )
                df[vote_col] = df[voix_col]

            if pvoix_col in df.columns:
                df[pvoix_col] = (
                    pd.to_numeric(df[pvoix_col], errors="coerce")
                    .fillna(0)
                    .astype(float)
                )
                df[pvote_col] = df[pvoix_col]

            if pvoix_ratio_col in df.columns:
                df[pvoix_ratio_col] = (
                    pd.to_numeric(df[pvoix_ratio_col], errors="coerce")
                    .fillna(0)
                    .astype(float)
                )
                df[pvote_ratio_col] = df[pvoix_ratio_col]

        # Suppression des anciennes colonnes `voixT2_x` et `pvoixT2_x`
        old_columns = [
            col
            for col in df.columns
            if col.startswith("voixT2") or col.startswith("pvoixT2")
        ]
        df.drop(columns=old_columns, inplace=True, errors="ignore")

        # Vérification de la cohérence des totaux
        df["voteT2_total"] = (
            df["voteT2_ED"]
            + df["voteT2_D"]
            + df["voteT2_CD"]
            + df["voteT2_C"]
            + df["voteT2_G"]
        )
        ecart = abs(df["voteT2_total"].sum() - df["exprimesT2"].sum())

        if ecart > 1:
            print(f"⚠️ **Écart détecté pour {election_year}** : {ecart} voix")

        # Sauvegarde du fichier enrichi
        output_file = os.path.join(output_dir, f"pres{election_year}_enriched.csv")
        df.to_csv(output_file, index=False, sep=",", encoding="utf-8")
        print(f"✅ Fichier enrichi sauvegardé : {output_file}")

    except Exception as e:
        print(f"❌ Erreur lors de l'enrichissement du fichier {file_path}: {e}")


# Parcours et enrichissement des fichiers électoraux
for election, file_path in election_files.items():
    year = election.replace("pres", "").replace("_csv", "")
    enrich_election_data(file_path, year)

print(f"🎯 Tous les fichiers ont été enrichis et sont disponibles dans {output_dir}")
