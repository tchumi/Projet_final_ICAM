import os
import pandas as pd

# Chemin du dossier contenant les données électorales
base_dir = "D:/Projet_final_data/Piketty_data"

# Liste pour stocker la synthèse
synthese = []

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


# Fonction pour extraire les résultats du 2nd tour
def extract_second_tour_results(file_path, election_year):
    try:
        df = pd.read_csv(file_path, sep=",", dtype=str)
        columns = df.columns.tolist()

        # Vérifier si les votes du 2nd tour existent
        exprimesT2_col = "exprimesT2"
        if exprimesT2_col not in columns:
            print(f"⚠️ Aucun second tour détecté dans {file_path}. Ignoré.")
            return

        df[exprimesT2_col] = pd.to_numeric(df[exprimesT2_col], errors="coerce").fillna(
            0
        )

        # Initialisation des totaux par famille
        total_voix = {}
        for famille in ["ED", "D", "CD", "C", "G"]:
            total_voix[famille] = 0

        # Attribution des votes aux familles politiques
        total_exprimesT2 = df[exprimesT2_col].sum()

        for candidat, famille in familles_politique_t2.get(election_year, {}).items():
            voix_col = f"voixT2{candidat.upper()}"
            if voix_col in df.columns:
                df[voix_col] = pd.to_numeric(df[voix_col], errors="coerce").fillna(0)
                total_voix[famille] += df[voix_col].sum()

        # Vérification de la cohérence des totaux
        total_votes_familles = sum(total_voix.values())
        ecart = abs(total_exprimesT2 - total_votes_familles)

        # Stockage de la synthèse pour cette élection
        synthese.append(f"🗳️ **Élection {election_year}**")
        synthese.append(f"📂 Fichier : {file_path}")
        synthese.append(
            f"🔹 Total des votes exprimés au 2nd tour : {total_exprimesT2:,.0f} voix"
        )
        synthese.append(f"🔹 Répartition des votes par famille politique :")
        for famille, total in total_voix.items():
            synthese.append(f"    - {famille} : {total:,.0f} voix")
        if ecart > 1:
            synthese.append(
                f"⚠️ **Écart détecté** : {ecart:,.0f} voix entre total des votes et total attendu."
            )
        else:
            synthese.append(
                f"✅ Vérification : La somme des votes par famille correspond bien au total des exprimés."
            )
        synthese.append("\n" + "-" * 80 + "\n")

    except Exception as e:
        print(
            f"❌ Erreur lors de l'extraction du second tour pour {election_year}: {e}"
        )


# Parcours et analyse des fichiers électoraux
for election, file_path in election_files.items():
    year = election.replace("pres", "").replace("_csv", "")
    extract_second_tour_results(file_path, year)

# Sauvegarde du fichier de synthèse dans le répertoire courant du script
output_file = os.path.join(os.getcwd(), "second_tour.txt")
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(synthese))

print(f"✅ Extraction terminée ! Résultats enregistrés dans {output_file}")
