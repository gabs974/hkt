import requests
import pandas as pd
#import streamlit as st
#from regressionLinear import df_predictions


# @st.cache_data
def fetch_data_from_api(url: str, offset: int, limit: int) -> dict:
    params = {'limit': limit, 'offset': offset}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        raise Exception(f"Failed API request: Status {response.status_code}")
    

# @st.cache_data
def fetch_all_data(url: str) -> pd.DataFrame:
    all_data = []
    limit = 100
    offset = 0
    total_records = None

    while total_records is None or offset < total_records:
        data = fetch_data_from_api(url, offset, limit)
        all_data.extend(data['results'])

        if total_records is None:
            total_records = data['total_count']
        offset += limit

    return pd.json_normalize(all_data)

# Utilisez la fonction fetch_all_data et gérez les exceptions ou les notifications en dehors de la fonction
try:
    url_api = "https://data.regionreunion.com/api/explore/v2.1/catalog/datasets/population-francaise-communespublic/records"
    population = fetch_all_data(url_api)
except Exception as e:
    print(f"Erreur lors de la récupération des données : {e}")


try:
    url_api = "https://opendata-reunion.edf.fr/api/explore/v2.1/catalog/datasets/consommation-annuelle-par-commune0/records"
    conso_nrj = fetch_all_data(url_api)
except Exception as e:
    print(f"Erreur lors de la récupération des données : {e}")


df_population = (population.groupby("annee_utilisation", as_index=False)["population_totale"]
      .sum()
     )
#renomme annee_utilisation en année pour la fusion
df_population = df_population.rename(columns={"annee_utilisation": 'annee'})
codes1 = sorted(df_population["annee"].unique())
df_conso = (conso_nrj.groupby("annee", as_index=False)["consommation_mwh"]
      .sum()
     )
codes2 = sorted(df_conso["annee"].unique())
df_conso["annee"] = df_conso["annee"].astype(str)

# Fusionner les DataFrames sur la colonne 'annee'
#population_df_conso = pd.merge(df_population, df_conso, on='annee', how='inner')
population = pd.merge(df_population, df_conso, on='annee', how='inner')

# dataset
#df_predictions = (pd.read_csv("./predictions_2012_2030.csv",
#                 sep=",", na_values="-")
#           .fillna(0)
#          )
#from regressionLinear import df_predictions

#df_predictions["annee"] = df_predictions["annee"].astype(str)

#population =  pd.concat([population_df_conso, df_predictions], ignore_index=True)

population.to_csv('resultat_fusion.csv', index=False)


#creation dataframe populations avec clé_unique code_commune
df_population_codcom = (population.groupby("code_insee_commune", as_index=False)["population_totale"]
      .sum()
     )
codes4 = sorted(df_population_codcom["code_insee_commune"].unique())

#creation dataframe conso_nrj avec clé_unique code_insee
df_conso_edf_codcom = (conso_nrj.groupby("code_insee", as_index=False)["consommation_mwh"]
      .sum()
     )
#codes5 = sorted(conso_nrj["code_insee_commune"].unique())

from regressionLinear import df_predictions

df_predictions["annee"] = df_predictions["annee"].astype(str)

population =  pd.concat([population, df_predictions], ignore_index=True)

