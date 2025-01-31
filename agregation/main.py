import pandas as pd
import os

def load_dataset(file_path, columns, dtypes, sep=','):
    """Charge un dataset en filtrant les colonnes utiles et en appliquant les types de données spécifiés."""
    df = pd.read_csv(file_path, sep=sep, dtype=dtypes, low_memory=False)
    
    # Vérifier quelles colonnes sont disponibles
    available_columns = set(df.columns)
    expected_columns = set(columns)
    missing_columns = expected_columns - available_columns
    
    if missing_columns:
        with open("diagnostic_manquants.txt", "a", encoding="utf-8") as diag_file:
            diag_file.write(f"⚠️ Manque dans {file_path} : {', '.join(missing_columns)}\n")
        print(f"⚠️ Attention : Colonnes manquantes dans {file_path} -> {missing_columns}")
    
    # Filtrer les colonnes existantes uniquement
    cols_to_keep = [col for col in columns if col in available_columns]
    df = df[cols_to_keep]
    
    # Vérifier unicité de 'codecommune'
    if df["codecommune"].duplicated().sum() > 0:
        print(f"⚠️ Attention : {file_path} contient des doublons sur 'codecommune'. On va les agréger.")
        df = df.groupby("codecommune").mean().reset_index()  # On agrège pour éviter les doublons
    
    return df

# 📍 Définition des fichiers et variables
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"

DATASETS = {
    "revenus": {
        "file": "Revenus_csv/revcommunes.csv",
        "columns": ["codecommune", "revmoy2022", "revmoyfoy2022", "revratio2022"],
        "dtypes": {"codecommune": str, "revmoy2022": float, "revmoyfoy2022": float, "revratio2022": float}
    },
    "csp": {
        "file": "CSP_csv/cspcommunes.csv",
        "columns": ["codecommune", "pchom2022", "pouvr2022", "pcadr2022"],
        "dtypes": {"codecommune": str, "pchom2022": float, "pouvr2022": float, "pcadr2022": float}
    },
    "diplomes": {
        "file": "Diplomes_csv/diplomescommunes.csv",
        "columns": ["codecommune", "pbac2022", "psup2022"],
        "dtypes": {"codecommune": str, "pbac2022": float, "psup2022": float}
    },
    "etrangers": {
        "file": "Nationalites_csv/etrangerscommunes.csv",
        "columns": ["codecommune", "petranger2022"],
        "dtypes": {"codecommune": str, "petranger2022": float}
    },
    "proprietaires": {
        "file": "Proprietaires_csv/proprietairescommunes.csv",
        "columns": ["codecommune", "ppropri2022"],
        "dtypes": {"codecommune": str, "ppropri2022": float}
    },
    "ages": {
        "file": "Age_csp/agesexcommunes.csv",
        "columns": ["codecommune", "pop2022", "propf2022", "prop0142022", "prop15392022", "prop40592022", "prop60p2022", "age2022"],
        "dtypes": {"codecommune": str, "pop2022": int, "propf2022": float, "prop0142022": float, "prop15392022": float, 
                   "prop40592022": float, "prop60p2022": float, "age2022": float}
    },
    "pib": {
        "file": "Revenus_csv/pibcommunes.csv",
        "columns": ["codecommune", "pibratio2022", "pibtot2022"],
        "dtypes": {"codecommune": str, "pibratio2022": float, "pibtot2022": float}
    },
    "capital_immo": {
        "file": "Capital_immobilier_csv/capitalimmobiliercommunes.csv",
        "columns": ["codecommune", "capitalratio2022", "capitalimmo2022", "prixm2_2022"],
        "dtypes": {"codecommune": str, "capitalratio2022": float, "capitalimmo2022": float, "prixm2_2022": float}
    },
    "isf": {
        "file": "Capital_immobilier_csv/isfcommunes.csv",
        "columns": ["codecommune", "pisf2022"],
        "dtypes": {"codecommune": str, "pisf2022": float}
    },
    "presidentielle_2022": {
        "file": "pres2022_csv/pres2022comm.csv",
        "columns": ["codecommune", "exprimes", "voteG", "voteCG", "voteC", "voteCD", "voteD", "voteTG", "voteTD",
                    "voteGCG", "voteDCD", "pvoixT2MACRON", "pvoixT2MLEPEN", "pabs", "pblancsnuls", "pabsT2", "pblancsnulsT2"],
        "dtypes": {"codecommune": str, "exprimes": float, "voteG": float, "voteCG": float, "voteC": float,
                   "voteCD": float, "voteD": float, "voteTG": float, "voteTD": float, "voteGCG": float,
                   "voteDCD": float, "pvoixT2MACRON": float, "pvoixT2MLEPEN": float, "pabs": float, 
                   "pblancsnuls": float, "pabsT2": float, "pblancsnulsT2": float}
    }
}

# 📌 Nettoyage du fichier diagnostic
diagnostic_path = "diagnostic_manquants.txt"
if os.path.exists(diagnostic_path):
    os.remove(diagnostic_path)

# 📌 Chargement et fusion des datasets
df_final = None
for key, params in DATASETS.items():
    file_path = os.path.join(DATA_DIR, params["file"])
    
    print(f"🔄 Chargement de {key} depuis {file_path}...")
    
    df = load_dataset(file_path, params["columns"], params["dtypes"])
    
    # Vérification du nombre de communes avant fusion
    print(f"📊 {key}: {df.shape[0]} lignes, {df.shape[1]} colonnes après nettoyage")
    
    if df_final is None:
        df_final = df
    else:
        df_final = df_final.merge(df, on="codecommune", how="left")

# 📌 Vérification après fusion
print(f"✅ Fusion complète. Nombre final de lignes : {df_final.shape[0]}")
print(f"🔍 Nombre de communes uniques : {df_final['codecommune'].nunique()}")

# 📌 Enregistrement du dataset final
output_path = "C:/Users/Admin.local/Documents/Projet_final_ICAM/df_final_cleaned.csv"
df_final.to_csv(output_path, index=False)

print(f"✅ Données enregistrées sous {output_path}")

# 📌 Résumé final dans le fichier diagnostic
with open(diagnostic_path, "a", encoding="utf-8") as diag_file:
    diag_file.write(f"\n🔍 Résumé final :\n")
    diag_file.write(f"✅ Fusion complète. Nombre final de lignes : {df_final.shape[0]}\n")
    diag_file.write(f"🔍 Nombre de communes uniques : {df_final['codecommune'].nunique()}\n")

print(f"📄 Rapport enregistré dans {diagnostic_path}")
