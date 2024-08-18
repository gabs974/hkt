import requests
import pandas as pd
from regressionLinear import df_predictions

# Fonction pour récupérer les données de l'API et les convertir en DataFrame
def fetch_all_data(url: str) -> pd.DataFrame:
    response = requests.get(url)
    
    if response.status_code != 200:
        raise Exception(f"Erreur lors de la requête à l'API : {response.status_code}. URL: {url}")
    
    data = response.json()
    
    # Normaliser les données JSON en DataFrame
    df = pd.json_normalize(data['results'])  # Supposant que les résultats sont dans 'results'
    
    # Débogage : Afficher les colonnes disponibles et un échantillon des données
    print("Colonnes disponibles : ", df.columns)
    print("Échantillon des données :\n", df.head())
    
    return df

# Fonction pour lire les fichiers Excel et les convertir en DataFrame
def fetch_excel_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(filepath)
        return df
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Excel : {e}")
        return pd.DataFrame()

# Récupération des données de population à partir du fichier Excel
try:
    filepath_population = "./app/population-francaise-communespublic.xlsx"
    population = fetch_excel_data(filepath_population)
    
    # Nettoyage des noms de colonnes
    population.columns = population.columns.astype(str).str.strip().str.replace(' ', '_')
    
except Exception as e:
    print(f"Erreur lors du traitement des données de population : {e}")
    
# Renommer les colonnes pour qu'elles correspondent à celles de l'API
population.rename(columns={
    'Code_région': 'code_region',
    'Nom_de_la_région': 'nom_de_la_region',
    'Code_département': 'code_departement',
    'Code_arrondissement_départemental': 'code_arrondissement',
    'Code_canton': 'code_canton',
    'Code_commune': 'code_commune',
    'Nom_de_la_commune': 'nom_de_la_commune',
    'Population_municipale': 'population_municipale',
    'Population_comptée_à_part': 'population_comptee_a_part',
    'Population_totale': 'population_totale',
    'Année_recensement': 'annee_recensement',
    'Année_utilisation': 'annee_utilisation',
    'Code_INSEE_(commune_ou_arrondissement)': 'code_insee_commune_ou_arrondissement',
    'Superficie_de_la_commune': 'superficie_commune',
    'Statut': 'statut',
    'Code_INSEE_de_la_commune': 'code_insee_commune',
    'Nom_de_la_commune_IGN': 'nom_commune_ign',
    'Nom_du_département_IGN': 'nom_departement_ign',
    'Nom_de_la_région': 'nom_region',
    'Code_EPCI': 'code_epci',
    'EPCI': 'epci'
}, inplace=True)

# Récupération des données de consommation d'énergie à partir du fichier Excel
try:
    filepath_conso_nrj = "./app/consommation-annuelle-par-commune0.xlsx"
    conso_nrj = fetch_excel_data(filepath_conso_nrj)
    
    # Nettoyage des noms de colonnes
    conso_nrj.columns = conso_nrj.columns.astype(str).str.strip().str.replace(' ', '_')
    
    # Renommer les colonnes pour qu'elles correspondent à celles de l'API
    conso_nrj.rename(columns={
        'nb_ligne': 'nb_ligne',
        'Commune': 'commune',
        'annee': 'annee',
        'Code_INSEE': 'code_insee',
        'Secteur': 'secteur',
        'Consommation_(MWh)': 'consommation_mwh',
        'Nombre_de_PDS': 'nombre_pds'
    }, inplace=True)
except Exception as e:
    print(f"Erreur lors du traitement des données de consommation d'énergie : {e}")

# Agrégation des données de population par année
if "annee_utilisation" in population.columns:
    df_population = (population.groupby("annee_utilisation", as_index=False)["population_totale"]
                     .sum()
                    )
    df_population = df_population.rename(columns={"annee_utilisation": "annee"})
    df_population["annee"] = df_population["annee"].astype(str)  # Conversion en chaîne de caractères
else:
    print("La colonne 'annee_utilisation' n'existe pas dans le DataFrame 'population'.")
    df_population = pd.DataFrame()  # Créer un DataFrame vide pour éviter les erreurs plus tard

# Agrégation des données de consommation d'énergie par année
if "annee" in conso_nrj.columns:
    df_conso = (conso_nrj.groupby("annee", as_index=False)["consommation_mwh"]
                .sum()
               )
    df_conso["annee"] = df_conso["annee"].astype(str)  # Conversion en chaîne de caractères
else:
    print("La colonne 'annee' n'existe pas dans le DataFrame 'conso_nrj'.")
    df_conso = pd.DataFrame()  # Créer un DataFrame vide pour éviter les erreurs plus tard

# Fusion des DataFrames population et consommation d'énergie sur la colonne 'annee'
if not df_population.empty and not df_conso.empty:
    population_merged = pd.merge(df_population, df_conso, on="annee", how="inner")
    # Sauvegarde des résultats fusionnés dans un fichier CSV
    population_merged.to_csv('resultat_fusion.csv', index=False)
else:
    print("La fusion des DataFrames n'a pas été possible car un des DataFrames est vide.")

# Création du DataFrame populations avec clé unique code_commune
if "code_insee_commune" in population.columns:
    df_population_codcom = (population.groupby("code_insee_commune", as_index=False)["population_totale"]
                            .sum()
                           )
else:
    print("La colonne 'code_insee_commune' n'existe pas dans le DataFrame 'population'.")

# Création du DataFrame consommation d'énergie avec clé unique code_insee
if "code_insee" in conso_nrj.columns:
    df_conso_edf_codcom = (conso_nrj.groupby("code_insee", as_index=False)["consommation_mwh"]
                           .sum()
                          )
else:
    print("La colonne 'code_insee' n'existe pas dans le DataFrame 'conso_nrj'.")

# Préparation des prédictions et concaténation avec les données fusionnées
df_predictions["annee"] = df_predictions["annee"].astype(str)
population = pd.concat([population_merged, df_predictions], ignore_index=True)

# Optionnel: Vous pouvez enregistrer le DataFrame final si nécessaire
population.to_csv('population_final.csv', index=False)
