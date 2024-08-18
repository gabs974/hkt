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

# Récupération des données de population
try:
    url_population = "https://data.regionreunion.com/api/explore/v2.1/catalog/datasets/population-francaise-communespublic/records?limit=100&refine=nom_de_la_region%3A%22La%20R%C3%A9union%22"
    population = fetch_all_data(url_population)
    print("Données de population récupérées avec succès.")
except Exception as e:
    print(f"Erreur lors de la récupération des données de population : {e}")

# Récupération des données de consommation d'énergie
try:
    url_conso_nrj = "https://opendata-reunion.edf.fr/api/explore/v2.1/catalog/datasets/consommation-annuelle-par-commune0/records?limit=100"
    conso_nrj = fetch_all_data(url_conso_nrj)
    print("Données de consommation d'énergie récupérées avec succès.")
except Exception as e:
    print(f"Erreur lors de la récupération des données de consommation d'énergie : {e}")

# À ce stade, vérifiez que les colonnes `annee_utilisation` et `population_totale` existent réellement
# dans le DataFrame `population`, sinon ajustez la structure des données en conséquence.

# Agrégation des données de population par année
if "annee_utilisation" in population.columns:
    df_population = (population.groupby("annee_utilisation", as_index=False)["population_totale"]
                     .sum()
                    )
    df_population = df_population.rename(columns={"annee_utilisation": "annee"})
else:
    print("La colonne 'annee_utilisation' n'existe pas dans le DataFrame 'population'.")

# Agrégation des données de consommation d'énergie par année
if "annee" in conso_nrj.columns:
    df_conso = (conso_nrj.groupby("annee", as_index=False)["consommation_mwh"]
                .sum()
               )
    df_conso["annee"] = df_conso["annee"].astype(str)
else:
    print("La colonne 'annee' n'existe pas dans le DataFrame 'conso_nrj'.")

# Fusion des DataFrames population et consommation d'énergie sur la colonne 'annee'
if "annee" in df_population.columns and "annee" in df_conso.columns:
    population_merged = pd.merge(df_population, df_conso, on="annee", how="inner")

    # Sauvegarde des résultats fusionnés dans un fichier CSV
    population_merged.to_csv('resultat_fusion.csv', index=False)
else:
    print("La fusion des DataFrames n'a pas été possible car la colonne 'annee' est manquante.")

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
