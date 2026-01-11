
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from silver.normalisation import normalize
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator

from bronze.data_injection import load_data
from silver.adjust_cyclical_time_features import add_cyclical_time_features
from silver.data_cleaning import data_cleaning
from silver.split_data import split_data
def training_rf(train, test):
  #set spark logs
  # spark.sparkContext.setLogLevel("INFO")
  rf= RandomForestRegressor(featuresCol= "features", labelCol="dure_trajet", predictionCol="prediction_dure",  numTrees=10,  maxDepth=6)
  model=rf.fit(train)
  predictions= model.transform(test)
  evaluator= RegressionEvaluator(labelCol="dure_trajet", predictionCol="prediction_dure", metricName="rmse")
  print(f"remse:  {evaluator.evaluate(predictions)}" )

  evaluator= RegressionEvaluator(labelCol="dure_trajet", predictionCol="prediction_dure", metricName="r2")
  print(f"re : {evaluator.evaluate(predictions)}")

  return model
df= load_data()
df_clean = data_cleaning(df)
df_clean = add_cyclical_time_features(df_clean)
normalized_df=normalize(df_clean)
train, test = split_data(normalized_df)
training_rf(train, test)