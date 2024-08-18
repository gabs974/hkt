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
    filepath_population = "population-francaise-communespublic.xlsx"
    population = fetch_excel_data(filepath_population)
except Exception as e:
    print(f"Erreur lors du traitement des données de population : {e}")
    
# Renommer les colonnes pour qu'elles correspondent à celles de l'API
population.rename(columns={
    'Code région': 'code_region',
    'Nom de la région': 'nom_de_la_region',
    'Code département': 'code_departement',
    'Code arrondissement départemental': 'code_arrondissement',
    'Code canton': 'code_canton',
    'Code commune': 'code_commune',
    'Nom de la commune': 'nom_de_la_commune',
    'Population municipale': 'population_municipale',
    'Population comptée à part': 'population_comptee_a_part',
    'Population totale': 'population_totale',
    'Année recensement': 'annee_recensement',
    'Année utilisation': 'annee_utilisation',
    'Code INSEE (commune ou arrondissement)': 'code_insee',
    'Superficie de la commune': 'superficie_commune',
    'Statut': 'statut',
    'Code INSEE de la commune': 'code_insee_commune',
    'Nom de la commune IGN': 'nom_commune_ign',
    'Nom du département IGN': 'nom_departement_ign',
    'Nom de la région': 'nom_region',
    'Code EPCI': 'code_epci',
    'EPCI': 'epci'
}, inplace=True)


# Récupération des données de consommation d'énergie à partir du fichier Excel
try:
    filepath_conso_nrj = "consommation-annuelle-par-commune0.xlsx"
    conso_nrj = fetch_excel_data(filepath_conso_nrj)
    
    # Renommer les colonnes pour qu'elles correspondent à celles de l'API
    conso_nrj.rename(columns={
        'nb ligne': 'nb_ligne',
        'Commune': 'commune',
        'annee': 'annee',
        'Code INSEE': 'code_insee',
        'Secteur': 'secteur',
        'Consommation (MWh)': 'consommation_mwh',
        'Nombre de PDS': 'nombre_pds'
    }, inplace=True)
except Exception as e:
    print(f"Erreur lors du traitement des données de consommation d'énergie : {e}")