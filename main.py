import pandas as pd
# Lecture du fichier
from fastapi import FastAPI

df = pd.read_parquet('data/dataset.parquet')

# Vérification
print(df.head())
print(df.info())
app= FastAPI()