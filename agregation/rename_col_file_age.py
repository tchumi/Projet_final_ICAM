import pandas as pd
import re

# Charger le fichier CSV
file_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/Age_csp/agesexcommunes.csv"
output_file = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/Age_csp/agesexcommunes_renamed.csv"

# 📌 Chargement du fichier CSV
df = pd.read_csv(file_path, low_memory=False)

# 📌 Renommage des colonnes concernées
df.columns = df.columns.str.replace(r'^prop014', 'propA', regex=True)
df.columns = df.columns.str.replace(r'^prop1539', 'propB', regex=True)
df.columns = df.columns.str.replace(r'^prop4059', 'propC', regex=True)

# 📌 Sauvegarde du fichier modifié
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"✅ Fichier modifié enregistré : {output_file}")
