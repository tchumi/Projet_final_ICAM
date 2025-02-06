import pandas as pd
import os

def load_dataset(file_path, available_years, prefix, dtype=float, sep=','):
    """
    Charge un dataset en ne gardant que les années disponibles et en convertissant les types.
    """
    # Générer dynamiquement les colonnes disponibles
    columns = ["codecommune"] + [f"{prefix}{year}" for year in available_years]
    
    try:
        df = pd.read_csv(file_path, sep=sep, dtype=str, usecols=columns, low_memory=True)
        
        # Conversion en numérique (ignore les erreurs pour éviter les plantages)
        for col in columns[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        return df
    except Exception as e:
        print(f"❌ Erreur lors du chargement de {file_path}: {e}")
        return None

# 📍 Définition des fichiers et variables
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"

DATASETS = {
    "revenus": {
        "file": "Revenus_csv/revcommunes.csv",
        "prefixes": {"revratio": list(range(1960, 2023))},
        # "prefixes": {"revmoy": list(range(1960, 2023)), "revmoyfoy": list(range(1960, 2023)), "revratio": list(range(1960, 2023))}
    },
    "csp": {
        "file": "CSP_csv/cspcommunes.csv",
        "prefixes": {"pchom": list(range(1960, 2023)), "pouvr": list(range(1960, 2023)), "pcadr": list(range(1960, 2023))}
    },
    "pib": {
        "file": "Revenus_csv/pibcommunes.csv",
        "prefixes": {"pibratio": list(range(1960, 2023))},
        # "prefixes": {"pibratio": list(range(1960, 2023)), "pibtot": list(range(1960, 2023))}
    },
    # "ages": {
    #     "file": "Age_csp/agesexcommunes_renamed.csv",
    #     "prefixes": {"pop": list(range(1960, 2023)), "propf": list(range(1960, 2023)), "propA": list(range(1960, 2023)), 
    #                  "propB": list(range(1960, 2023)), "propC": list(range(1960, 2023)), "prop60p": list(range(1960, 2023)), 
    #                  "age": list(range(1960, 2023))}
    # },

    # "proprietaires": {
    #     "file": "Proprietaires_csv/proprietairescommunes.csv",
    #     "prefixes": {"ppropri": list(range(1960, 2023))}
    # },
    # "etrangers": {
    #     "file": "Nationalites_csv/etrangerscommunes.csv",
    #     "prefixes": {"petranger": list(range(1960, 2023))}
    # },
    # "diplomes": {
    #     "file": "Diplomes_csv/diplomescommunes.csv",
    #     "prefixes": {"pbac": list(range(1960, 2023)), "psup": list(range(1960, 2023))}
    # },
 
    # # "capital_immo": {
    # #     "file": "Capital_immobilier_csv/capitalimmobiliercommunes.csv",
    # #     "prefixes": {"capitalratio": list(range(1960, 2023)), "capitalimmo": list(range(1960, 2023))}
    # # },
    # # "isf": {
    # #     "file": "Capital_immobilier_csv/isfcommunes.csv",
    # #     "prefixes": {"pisf": [2017]}
    # # }
}

# 📌 Transformation en format long (melt)
df_long = None

for key, params in DATASETS.items():
    file_path = os.path.join(DATA_DIR, params["file"])
    print(f"🔄 Chargement de {key} depuis {file_path}...")

    df_aggregated = None

    for prefix, available_years in params["prefixes"].items():
        df = load_dataset(file_path, available_years, prefix)

        if df is not None:
            df_melted = df.melt(id_vars=["codecommune"], var_name="année", value_name=prefix)
            df_melted["année"] = df_melted["année"].str.extract(r'(\d{4})').astype(int)

            if df_aggregated is None:
                df_aggregated = df_melted
            else:
                df_aggregated = df_aggregated.merge(df_melted, on=["codecommune", "année"], how="left")

    # Fusion avec la table principale
    if df_long is None:
        df_long = df_aggregated
    else:
        df_long = df_long.merge(df_aggregated, on=["codecommune", "année"], how="left")

# 📌 Enregistrement du dataset transformé
output_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/df_final_transposed_socio.csv"
df_long.to_csv(output_path, index=False)

print(f"✅ Données socio-démographiques transposées enregistrées sous {output_path}")

# 📌 Vérification après transformation
print(f"🔍 Nombre de lignes après transformation : {df_long.shape[0]}")
print(f"🔍 Nombre de colonnes après transformation : {df_long.shape[1]}")
