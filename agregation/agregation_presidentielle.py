import pandas as pd
import os


def load_election_dataset(file_path, columns, dtypes, year, sep=","):
    """Charge un fichier d'élection, sélectionne les colonnes utiles et ajoute l'année."""
    df = pd.read_csv(file_path, sep=sep, dtype=dtypes, low_memory=False)

    # Vérifier les colonnes disponibles
    available_columns = set(df.columns)
    expected_columns = set(columns)
    missing_columns = expected_columns - available_columns

    if missing_columns:
        with open("diagnostic_manquants.txt", "a", encoding="utf-8") as diag_file:
            diag_file.write(
                f"⚠️ Manque dans {file_path} : {', '.join(missing_columns)}\n"
            )
        print(f"⚠️ Colonnes manquantes dans {file_path} -> {missing_columns}")

    # Filtrer les colonnes existantes uniquement
    cols_to_keep = [col for col in columns if col in available_columns]
    df = df[cols_to_keep]

    # Ajouter l'année
    df["année"] = int(year)

    return df


# 📍 Définition des fichiers enrichis
DATA_DIR = "D:/Projet_final_data/Piketty_data/enriched_data"

# 📍 Colonnes à garder pour **le 1er et 2nd tour**
COLUMNS = [
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

DTYPES = {
    "codecommune": str,
    "exprimes": float,
    "voteG": float,
    "voteCG": float,
    "voteC": float,
    "voteCD": float,
    "voteD": float,
    "voteTG": float,
    "voteTD": float,
    "voteGCG": float,
    "voteDCD": float,
    "pvoteG": float,
    "pvoteCG": float,
    "pvoteC": float,
    "pvoteCD": float,
    "pvoteD": float,
    "pvoteTGratio": float,
    "pvoteTDratio": float,
    "exprimesT2": float,
    "voteT2_ED": float,
    "voteT2_D": float,
    "voteT2_CD": float,
    "voteT2_C": float,
    "voteT2_G": float,
    "pvoteT2_ED": float,
    "pvoteT2_D": float,
    "pvoteT2_CD": float,
    "pvoteT2_C": float,
    "pvoteT2_G": float,
    "pvoteT2_EDratio": float,
    "pvoteT2_Dratio": float,
    "pvoteT2_CDratio": float,
    "pvoteT2_Cratio": float,
    "pvoteT2_Gratio": float,
}

# 📌 Fusion des fichiers enrichis en série temporelle
df_elections = []
for file_name in os.listdir(DATA_DIR):
    if file_name.endswith("_enriched.csv"):  # Vérifie que c'est bien un fichier enrichi
        year = file_name.replace("pres", "").replace("_enriched.csv", "")
        file_path = os.path.join(DATA_DIR, file_name)

        print(f"🔄 Chargement de la présidentielle {year} depuis {file_path}...")

        df = load_election_dataset(file_path, COLUMNS, DTYPES, year)
        df_elections.append(df)

# 📌 Concaténer les élections pour former un dataset temporel
df_elections = pd.concat(df_elections, ignore_index=True)

# 📌 Enregistrement du dataset final
output_path = "D:/Projet_final_data/Piketty_data/elections_fusionnees.csv"
df_elections.to_csv(output_path, index=False)

print(f"✅ Données des élections fusionnées enregistrées sous {output_path}")
print(f"🔍 Nombre de lignes : {df_elections.shape[0]}")
print(f"🔍 Nombre de colonnes : {df_elections.shape[1]}")
