"""
Ce script vérifie la présence des colonnes attendues dans les fichiers CSV enrichis situés dans un répertoire spécifié.
Modules:
    os: Fournit un moyen d'utiliser des fonctionnalités dépendantes du système d'exploitation.
    pandas: Bibliothèque pour la manipulation et l'analyse des données.
Constantes:
    DATA_DIR (str): Chemin vers le répertoire contenant les fichiers CSV enrichis.
    COLUMNS_ATTENDUES (list): Liste des noms de colonnes attendus dans les fichiers CSV enrichis.
Fonctionnalités:
    - Parcourt tous les fichiers dans le répertoire spécifié.
    - Vérifie si le nom du fichier se termine par "_enriched.csv".
    - Lit le fichier CSV dans un DataFrame pandas.
    - Compare les colonnes du DataFrame avec les colonnes attendues.
    - Affiche un message d'avertissement si des colonnes sont manquantes.
    - Affiche un message de succès si toutes les colonnes attendues sont présentes.
"""

import os
import pandas as pd

# 📍 Chemin des fichiers enrichis
#DATA_DIR = "D:/Projet_final_data/Piketty_data/enriched_data"
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/enriched_data"

# 📌 Colonnes attendues
COLUMNS_ATTENDUES = [
    "codecommune",
    "exprimes",
    "voteG",
    "voteCG",
    "voteC",
    "voteCD",
    "voteD",
    "voteTG",
    "voteTD",
    "voteGCG",
    "voteDCD",
    "pvoteG",
    "pvoteCG",
    "pvoteC",
    "pvoteCD",
    "pvoteD",
    "pvoteTG",
    "pvoteTD",
    "pvoteTGratio",
    "pvoteTDratio",
    "exprimesT2",
    "voteT2_ED",
    "voteT2_D",
    "voteT2_CD",
    "voteT2_C",
    "voteT2_G",
    "pvoteT2_ED",
    "pvoteT2_D",
    "pvoteT2_CD",
    "pvoteT2_C",
    "pvoteT2_G",
    "pvoteT2_EDratio",
    "pvoteT2_Dratio",
    "pvoteT2_CDratio",
    "pvoteT2_Cratio",
    "pvoteT2_Gratio",
]

# 📌 Vérification des colonnes par fichier enrichi
for file_name in os.listdir(DATA_DIR):
    if file_name.endswith("_enriched.csv"):
        file_path = os.path.join(DATA_DIR, file_name)
        df = pd.read_csv(file_path, sep=",", dtype=str, low_memory=False)

        missing_columns = set(COLUMNS_ATTENDUES) - set(df.columns)

        if missing_columns:
            print(f"⚠️ Colonnes manquantes dans {file_name} -> {missing_columns}")
        else:
            print(f"✅ {file_name} contient toutes les colonnes attendues")
