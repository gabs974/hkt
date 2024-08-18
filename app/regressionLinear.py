import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
#import matplotlib.pyplot as plt
#from api import population
df_calc_population = pd.read_csv('./app/resultat_fusion.csv', sep=",", na_values="-")

# Sélectionnez les colonnes pertinentes
data = df_calc_population[['annee', 'population_totale', 'consommation_mwh']]

# Supprimez les lignes avec des valeurs manquantes
data = data.dropna()

# Définissez l'année comme index
data.set_index('annee', inplace=True)

# Séparez les données en variables explicatives (X) et la variable cible (y)
X = data[['population_totale']]
y = data['consommation_mwh']

# Divisez les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialisez le modèle de régression linéaire
model = LinearRegression()

# Entraînez le modèle sur l'ensemble d'entraînement
model.fit(X_train, y_train)

# Faites des prédictions sur l'ensemble de test
y_pred = model.predict(X_test)

# Évaluez les performances du modèle
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Tracez les prédictions par rapport aux valeurs réelles
#plt.scatter(X_test, y_test, color='black')
#plt.plot(X_test, y_pred, color='blue', linewidth=3)
#plt.xlabel('Population Totale')
#plt.ylabel('Consommation MWh')
#plt.title('Régression Linéaire : Population Totale vs. Consommation MWh')

last_year = df_calc_population['annee'].iloc[-1]
next_year = last_year + 1
next_year
years = list(range(next_year, 2031))
df_predictions = pd.DataFrame({'annee': years})
df_predictions.to_csv('predictions_2012_2030.csv', index=False)


# Supposons que vous avez déjà chargé vos données dans df_calc_population

# Sélectionnez les colonnes pertinentes
data = df_calc_population[['annee', 'population_totale', 'consommation_mwh']]
data = data.dropna()

# Divisez les données en ensemble d'entraînement et ensemble de test
X = data[['population_totale']]
y = data['consommation_mwh']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Supprimez les valeurs manquantes dans l'ensemble d'entraînement
X_train = X_train.dropna()
y_train = y_train.dropna()

# Créez et entraînez le modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# Faites des prédictions sur l'ensemble de test
y_pred = model.predict(X_test)

# Évaluez les performances du modèle
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

#print(f'Mean Squared Error: {mse}')
#print(f'R-squared: {r2}')

# Utilisez le modèle pour faire des prédictions pour l'année 2030
df_2030 = pd.DataFrame({'population_totale': df_calc_population['population_totale']})
predictions_2030 = model.predict(df_2030)
#print(f'Prédiction de consommation pour 2030: {predictions_2030[0]}')

# Supposons que vous avez déjà chargé vos données dans df_calc_population

# Sélectionnez les colonnes pertinentes
data = df_calc_population[['annee', 'population_totale', 'consommation_mwh']]
data = data.dropna()

# Divisez les données en ensemble d'entraînement et ensemble de test
X = data[['population_totale']]
y = data['consommation_mwh']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Créez et entraînez le modèle de régression linéaire
model = LinearRegression()
model.fit(X_train, y_train)

# Estimez la population pour chaque année de 2012 à 2030
#years = list(range(next_year, 2031))
#df_predictions = pd.DataFrame({'annee': years})

# Utilisez une fonction pour estimer la population pour chaque année
def estimate_population(year):
    # Remplacez cette fonction par votre propre logique d'estimation
    # Pour cet exemple, on suppose une croissance linéaire de la population
    initial_population = X['population_totale'].iloc[0]
    population_growth_rate = 0.027  # exemple de taux de croissance de 2% par an
    estimated_population = initial_population * (1 + population_growth_rate) ** (year - 2012)
    return estimated_population

# Appliquez la fonction d'estimation pour chaque année
df_predictions['population_totale'] = df_predictions['annee'].apply(estimate_population)

# Faites des prédictions en utilisant le modèle
#df_predictions['consommation_mwh'] = model.predict(df_predictions[['population_totale']])
# Faites des prédictions en utilisant le modèle
if not df_predictions.empty:
    df_predictions['consommation_mwh'] = model.predict(df_predictions[['population_totale']])
else:
    print("DataFrame df_predictions is empty. Unable to make predictions.")

# Enregistrez le DataFrame des prédictions dans un fichier CSV
df_predictions.to_csv('predictions_2012_2030.csv', index=False)

# Affichez le DataFrame des prédictions#
#print(df_predictions)





