
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from silver.adjust_cyclical_time_features import add_cyclical_time_features
from bronze.data_injection import load_data
from silver.data_cleaning import data_cleaning
from silver.normalisation import normalize

def split_data(normalized_df):
  train, test= normalized_df.randomSplit([0.7, 0.3])
  return train, test

df= load_data()
df_clean = data_cleaning(df)
df_clean = add_cyclical_time_features(df_clean)
normalized_df=normalize(df_clean)
train, test = split_data(normalized_df)
train.show(2)