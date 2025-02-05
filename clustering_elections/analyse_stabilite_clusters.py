import pandas as pd
import os

# 📍 Chemin du fichier des clusters
DATA_DIR = "C:/Users/Admin.local/Documents/Projet_final_data/Piketty_data"
CLUSTER_FILE = os.path.join(DATA_DIR, "clusters_elections.csv")
REPORT_FILE = os.path.join(DATA_DIR, "rapport_stabilite_clusters.txt")

# 📌 Chargement du fichier des clusters
df_clusters = pd.read_csv(CLUSTER_FILE, sep=",", dtype={"codecommune": str})

# 📌 Vérification des colonnes disponibles
print("Colonnes du dataset :", df_clusters.columns.tolist())

# 📌 Vérification des élections disponibles
elections_disponibles = df_clusters["année"].unique()
print(f"Élections disponibles : {sorted(elections_disponibles)}")

# 📌 Analyse des transitions entre le 1er et le 2nd tour
def analyse_stabilite_tours(df):
    """
    Vérifie si les communes restent dans le même cluster entre le 1er et le 2nd tour d'une même élection.
    """
    rapport = []
    for annee in sorted(df["année"].unique()):
        df_election = df[df["année"] == annee]
        transition = df_election.groupby("codecommune")[["cluster_1er_tour", "cluster_2nd_tour"]].nunique()
        changements = transition[transition["cluster_1er_tour"] != transition["cluster_2nd_tour"]]
        
        rapport.append(f"\n📌 Élection {annee} : {len(changements)} communes ont changé de cluster entre les tours")
    
    return "\n".join(rapport)

# 📌 Analyse de la stabilité entre deux élections successives
def analyse_stabilite_elections(df):
    """
    Vérifie la stabilité des clusters entre deux élections successives.
    """
    rapport = []
    for annee1, annee2 in zip(sorted(df["année"].unique())[:-1], sorted(df["année"].unique())[1:]):
        df_prev = df[df["année"] == annee1]
        df_next = df[df["année"] == annee2]
        
        df_merged = df_prev.merge(df_next, on="codecommune", suffixes=(f"_{annee1}", f"_{annee2}"))
        
        transition_1er_tour = df_merged[df_merged[f"cluster_1er_tour_{annee1}"] != df_merged[f"cluster_1er_tour_{annee2}"]]
        transition_2nd_tour = df_merged[df_merged[f"cluster_2nd_tour_{annee1}"] != df_merged[f"cluster_2nd_tour_{annee2}"]]
        
        rapport.append(f"\n📌 De {annee1} à {annee2} : {len(transition_1er_tour)} changements au 1er tour, {len(transition_2nd_tour)} au 2nd tour.")
    
    return "\n".join(rapport)

# 📌 Génération du rapport
rapport_final = "📊 Analyse de la stabilité des clusters\n"
rapport_final += "======================================\n\n"
rapport_final += analyse_stabilite_tours(df_clusters) + "\n\n"
rapport_final += analyse_stabilite_elections(df_clusters)

# 📌 Écriture du rapport
with open(REPORT_FILE, "w", encoding="utf-8") as file:
    file.write(rapport_final)

print(f"✅ Rapport généré : {REPORT_FILE}")
