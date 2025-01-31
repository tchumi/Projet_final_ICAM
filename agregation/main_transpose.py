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
        print(f"⚠️ Colonnes manquantes dans {file_path} -> {missing_columns}")
    
    # Filtrer les colonnes existantes uniquement
    cols_to_keep = [col for col in columns if col in available_columns]
    df = df[cols_to_keep]
    
    return df

# 📍 Définition des fichiers et variables
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"

DATASETS = {
    "revenus": {
        "file": "Revenus_csv/revcommunes.csv",
        "columns": ["codecommune"] + [f"revmoy{year}" for year in range(2000, 2023)],
        "dtypes": {f"revmoy{year}": float for year in range(2000, 2023)}
    },
    "csp": {
        "file": "CSP_csv/cspcommunes.csv",
        "columns": ["codecommune"] + [f"pchom{year}" for year in range(2000, 2023)],
        "dtypes": {f"pchom{year}": float for year in range(2000, 2023)}
    },
    "diplomes": {
        "file": "Diplomes_csv/diplomescommunes.csv",
        "columns": ["codecommune"] + [f"pbac{year}" for year in range(2000, 2023)],
        "dtypes": {f"pbac{year}": float for year in range(2000, 2023)}
    },
    "proprietaires": {
        "file": "Proprietaires_csv/proprietairescommunes.csv",
        "columns": ["codecommune"] + [f"ppropri{year}" for year in range(2000, 2023)],
        "dtypes": {f"ppropri{year}": float for year in range(2000, 2023)}
    },
    "etrangers": {
        "file": "Nationalites_csv/etrangerscommunes.csv",
        "columns": ["codecommune"] + [f"petranger{year}" for year in range(2000, 2023)],
        "dtypes": {f"petranger{year}": float for year in range(2000, 2023)}
    },
    "ages": {
        "file": "Age_csp/agesexcommunes.csv",
        "columns": ["codecommune"] + [f"pop{year}" for year in range(2000, 2023)],
        "dtypes": {f"pop{year}": int for year in range(2000, 2023)}
    }
}

# 📌 Transformation en format long (melt)
df_long = None

for key, params in DATASETS.items():
    file_path = os.path.join(DATA_DIR, params["file"])
    print(f"🔄 Chargement de {key} depuis {file_path}...")
    
    df = load_dataset(file_path, params["columns"], params["dtypes"])
    
    # Transformation en format long
    df_melted = df.melt(id_vars=["codecommune"], var_name="année", value_name=key)
    df_melted["année"] = df_melted["année"].str.extract(r'(\d{4})').astype(int)
    
    # Fusion avec la table principale
    if df_long is None:
        df_long = df_melted
    else:
        df_long = df_long.merge(df_melted, on=["codecommune", "année"], how="left")

# 📌 Enregistrement du dataset transformé
output_path = "C:/Users/Admin.local/Documents/Projet_final_ICAM/df_final_transposed_socio.csv"
df_long.to_csv(output_path, index=False)

print(f"✅ Données socio-démographiques transposées enregistrées sous {output_path}")

# 📌 Vérification après transformation
print(f"🔍 Nombre de lignes après transformation : {df_long.shape[0]}")
print(f"🔍 Nombre de colonnes après transformation : {df_long.shape[1]}")
