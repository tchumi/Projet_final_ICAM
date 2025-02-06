import pandas as pd

# 📂 Chemin du fichier fusionné
output_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/elections_socio_fusionnes.csv"

# 📌 Chargement du fichier
df_fusion = pd.read_csv(output_path, dtype={"codecommune": str, "année": int}, low_memory=False)

# 📌 Nombre total de communes uniques
num_communes = df_fusion["codecommune"].nunique()

# 📌 Liste des années présentes
years_present = sorted(df_fusion["année"].unique())

# 📌 Nombre de valeurs manquantes par variable
missing_values = df_fusion.isnull().sum()

# 📌 Génération du rapport
report = f"""
📊 **Rapport de Contrôle du Fichier Final**
----------------------------------------
✅ Nombre total de communes : {num_communes}
✅ Années présentes : {years_present}

🔍 **Nombre de valeurs manquantes par variable :**
{missing_values.to_string()}
"""

# 📌 Sauvegarde du rapport dans un fichier texte
report_path = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data/diagnostic_elections_socio_fusionnes.txt"
with open(report_path, "w", encoding="utf-8") as f:
    f.write(report)

# 📌 Affichage du rapport dans la console
print(report)
print(f"✅ Rapport sauvegardé : {report_path}")
