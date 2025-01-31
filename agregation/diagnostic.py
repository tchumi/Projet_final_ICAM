import pandas as pd
import os

# 📍 Charger le fichier CSV
file_path = r"C:\Users\Admin.local\Documents\Projet_final_ICAM\df_final_cleaned.csv"
df = pd.read_csv(file_path, low_memory=False)

# 📌 1. Vérifier les valeurs manquantes
missing_values = df.isnull().sum()
missing_values = missing_values[missing_values > 0]
missing_values_report = missing_values.sort_values(ascending=False)

# 📌 2. Vérifier les valeurs aberrantes sur les colonnes clés
columns_to_check = ["pop2022"]
stats_report = {}

for col in columns_to_check:
    if col in df.columns:
        stats_report[col] = df[col].describe()

# 📌 3. Vérifier le nombre de communes disponibles
communes_disponibles = set(df["codecommune"].dropna().astype(str)) if "codecommune" in df.columns else set()
nb_communes = len(communes_disponibles)

# 📌 4. Sauvegarder le diagnostic dans un fichier texte
diagnostic_path = "diagnostic.txt"

with open(diagnostic_path, "w", encoding="utf-8") as f:
    f.write("📌 DIAGNOSTIC DES DONNÉES\n")
    f.write("=" * 50 + "\n\n")

    # 🔹 Colonnes avec valeurs manquantes
    f.write("🔍 Colonnes avec valeurs manquantes :\n")
    if not missing_values.empty:
        f.write(missing_values_report.to_string() + "\n")
    else:
        f.write("✅ Aucune valeur manquante détectée.\n")
    
    f.write("\n" + "=" * 50 + "\n\n")

    # 🔹 Statistiques des valeurs aberrantes
    f.write("📊 STATISTIQUES DES COLONNES CLÉS (Valeurs aberrantes)\n")
    for col, stats in stats_report.items():
        f.write(f"\n📊 {col} :\n")
        f.write(stats.to_string() + "\n")

    f.write("\n" + "=" * 50 + "\n\n")

    # 🔹 Nombre de communes disponibles
    f.write(f"🏙️ Nombre total de communes présentes : {nb_communes}\n")

print(f"✅ Rapport de diagnostic généré : {diagnostic_path}")
