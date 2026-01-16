# Système de Prédiction de Durée de Trajets Urbains

Un pipeline complet de Machine Learning de bout en bout pour prédire la durée des trajets de taxi urbains, intégrant le traitement distribué de données, l'entraînement de modèles ML et le déploiement d'API sécurisée.


## 1. Aperçu du Projet

Ce projet construit un système complet de traitement de données et de machine learning pour une start-up de logistique urbaine afin d'améliorer les prédictions de Temps d'Arrivée Estimé (ETA). Le système gère l'ingestion de données, le nettoyage, l'ingénierie de features, l'entraînement de modèles et fournit des prédictions via une API sécurisée.

### Contexte Métier

Une start-up de logistique urbaine souhaite améliorer la visibilité sur les temps d'arrivée. Ce système fournit :

- Pipeline automatisé d'ingestion et de traitement des données
- Prédictions ETA en temps réel
- Analyses avancées des patterns de trajets
- Accès API sécurisé avec authentification JWT
- Monitoring et logging complets

## 2. Architecture

Le projet suit une architecture médaillon avec trois zones de données :

1. **Couche Bronze** : Données brutes, non traitées
2. **Couche Silver** : Données nettoyées, normaliser et enrichies stockées dans PostgreSQL
3. **Couche ML** : Modèles entraînés et prédictions

### Flux de Données

```
Données Brutes → DAG Airflow → Traitement PySpark → PostgreSQL → FastAPI → Client
```

## Dataset

**Source** : Enregistrements des trajets de taxis NYC

### Caractéristiques Principales

| Colonne | Description |
|---------|-------------|
| `VendorID` | Identifiant du fournisseur de taxi (1 ou 2) |
| `tpep_pickup_datetime` | Date et heure de début du trajet |
| `tpep_dropoff_datetime` | Date et heure de fin du trajet |
| `passenger_count` | Nombre de passagers |
| `trip_distance` | Distance du trajet en miles |
| `RatecodeID` | Code du type de tarif (1=Standard, 2=Spécial, 3=Newark, etc.) |
| `PULocationID` | Identifiant de la zone de départ (pickup) |
| `DOLocationID` | Identifiant de la zone d'arrivée (dropoff) |
| `payment_type` | Type de paiement (0=Espèces, 1=Carte, etc.) |
| `fare_amount` | Tarif de base |
| `total_amount` | Montant total payé |

### Variable Cible

**`duration_minutes`** : Calculée comme `tpep_dropoff_datetime - tpep_pickup_datetime`

## ✨ Fonctionnalités

### Traitement des Données

- **Détection des Valeurs Aberrantes** : Filtrage basé sur IQR pour les trajets aberrants
- **Validation des Données** : 
  - Distance : 0 < distance ≤ 200 miles
  - Durée : > 0 minutes
  - Passagers : > 0
- **Ingénierie de Features** :
  - `pickup_hour` : Heure de la journée (0-23)
  - `day_of_week` : Jour de la semaine (0-6)
  - `month` : Mois de l'année (1-12)

### Machine Learning

- **Algorithme** : Random Forest Regressor
- **Cible** : Durée du trajet en minutes
- **Métriques d'Évaluation** : RMSE, R²

### API & Analytics

- **Endpoint de Prédiction** : Prédictions ETA en temps réel
- **Analytics Avancées** : Analyses basées sur SQL utilisant des CTEs
- **Sécurité** : Authentification JWT
- **Monitoring** : Logging des prédictions pour suivi du modèle

## Stack Technique

- **Orchestration** : Apache Airflow
- **Traitement de Données** : PySpark
- **Base de Données** : PostgreSQL
- **Framework ML** : Random Forest Regressor
- **API** : FastAPI
- **Authentification** : JWT
- **Conteneurisation** : Docker & Docker Compose
- **Tests** : Pytest

## 🚀 Installation

### Prérequis

- Docker & Docker Compose
- Python 3.8+
- 8GB RAM minimum

### Configuration

1. Cloner le dépôt :
```bash
git clone <repository-url>
cd taxi-eta-prediction
```

2. Démarrer l'infrastructure :
```bash
docker-compose up -d
```

3. Accéder aux services :
- **Interface Airflow** : http://localhost:8080
- **Documentation FastAPI** : http://localhost:8000/docs
- **PostgreSQL** : localhost:5432

4. Déclencher le DAG Airflow pour démarrer le pipeline :
- Ouvrir l'interface Airflow
- Activer et déclencher le DAG `taxi_eta_pipeline`

## 📖 Utilisation

### Pipeline Airflow

Le DAG se compose de 5 tâches :

1. **Téléchargement du Dataset** : Récupération des données de trajets de taxi
2. **Stockage Bronze** : Stockage des données brutes
3. **Traitement Silver** : Nettoyage et enrichissement des données, stockage dans PostgreSQL
4. **Entraînement du Modèle** : Entraînement du modèle Random Forest
5. **Logging des Prédictions** : (Bonus) Enregistrement des prédictions pour monitoring

### Effectuer des Prédictions

```python
import requests

# Obtenir un token JWT
response = requests.post("http://localhost:8000/token", 
    data={"username": "user", "password": "password"})
token = response.json()["access_token"]

# Faire une prédiction
headers = {"Authorization": f"Bearer {token}"}
trip_data = {
    "trip_distance": 5.2,
    "pickup_hour": 14,
    "day_of_week": 3,
    "passenger_count": 2,
    "PULocationID": 161,
    "DOLocationID": 237
}

response = requests.post("http://localhost:8000/predict", 
    json=trip_data, 
    headers=headers)
print(response.json())
# Sortie : {"estimated_duration": 12.5}
```

## 🔌 Points de Terminaison API

### Authentification

- `POST /token` - Obtenir un token d'accès JWT

### Prédictions

- `POST /predict` - Obtenir une prédiction ETA
  - **Entrée** : Caractéristiques du trajet (JSON)
  - **Sortie** : `{"estimated_duration": <minutes>}`

### Analytics

#### 1. Durée Moyenne par Heure
- `GET /analytics/avg-duration-by-hour`
- Analyse les heures de pointe en utilisant une CTE SQL
- **Réponse** :
```json
[
  {"pickup_hour": 8, "avg_duration": 18.4},
  {"pickup_hour": 9, "avg_duration": 22.1}
]
```

#### 2. Analyse par Type de Paiement
- `GET /analytics/payment-analysis`
- Compare la durée moyenne par type de paiement
- **Réponse** :
```json
[
  {
    "payment_type": 1,
    "total_trips": 125430,
    "avg_duration": 21.6
  }
]
```

## 📈 Performance du Modèle

- **RMSE** : 3.93 minutes
- **Score R²** : 0.803
- **Algorithme** : Random Forest Regressor
- **Gestion des Valeurs Aberrantes** : Méthode IQR

```

## 🧪 Tests

Exécuter les tests unitaires :

```bash
pytest tests/ -v
```

Les tests couvrent :
- Fonctions de prétraitement des données
- Endpoints API
- Authentification
- Prédictions du modèle

## 🔒 Sécurité

- Authentification basée sur JWT pour tous les endpoints API
- Gestion sécurisée des credentials via variables d'environnement
- Validation et sanitisation des entrées

## 📊 Monitoring

Toutes les prédictions sont enregistrées dans la table PostgreSQL `eta_predictions` avec :
- Timestamp de la prédiction
- Features d'entrée
- Durée prédite
- Version du modèle

## 🤝 Contribution

1. Forker le dépôt
2. Créer une branche de fonctionnalité (`git checkout -b feature/fonctionnalite-incroyable`)
3. Commiter vos changements (`git commit -m 'Ajout d'une fonctionnalité incroyable'`)
4. Pousser vers la branche (`git push origin feature/fonctionnalite-incroyable`)
5. Ouvrir une Pull Request
