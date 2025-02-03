import os
import pandas as pd

# 📍 Chemin des fichiers enrichis
DATA_DIR = "D:/Projet_final_data/Piketty_data/enriched_data"

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
