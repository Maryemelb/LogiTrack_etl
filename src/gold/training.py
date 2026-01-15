
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
from pyspark.sql import SparkSession
def training_rf():
  #set spark logs
  # spark.sparkContext.setLogLevel("INFO")
 train_input_path= "/opt/airflow/data/bronze/train_parquet"
 test_input_path= "/opt/airflow/data/bronze/test_parquet"
 spark= SparkSession.builder.appName('train_silver').master("local[*]").getOrCreate()
 rf= RandomForestRegressor(featuresCol= "features", labelCol="dure_trajet", predictionCol="prediction_dure",  numTrees=10,  maxDepth=6)
 train= spark.read.parquet(train_input_path)
 test= spark.read.parquet(test_input_path)
 try:
  model=rf.fit(train)
  predictions= model.transform(test)
  evaluator= RegressionEvaluator(labelCol="dure_trajet", predictionCol="prediction_dure", metricName="rmse")
  remse= evaluator.evaluate(predictions)

  evaluator= RegressionEvaluator(labelCol="dure_trajet", predictionCol="prediction_dure", metricName="r2")
  r2 = evaluator.evaluate(predictions)
  model.write().overwrite().save("/opt/airflow/data/gold/saved_model")
  return {
    "rmse": remse,
    "r2": r2
  }
 finally:
   spark.stop()
#df= load_data()
#df_clean = data_cleaning(df)
#df_clean = add_cyclical_time_features(df_clean)
#normalized_df=normalize(df_clean)
#train, test = split_data(normalized_df)
#training_rf(train, test)