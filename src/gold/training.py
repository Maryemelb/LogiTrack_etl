
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import VectorAssembler

from bronze.data_injection import load_data
from silver.data_cleaning import data_cleaning
from silver.split_data import split_data
from pyspark.sql import SparkSession
def training_rf():
  #set spark logs
  # spark.sparkContext.setLogLevel("INFO")
  train_input_path= "/opt/airflow/data/bronze/train_parquet"
  test_input_path= "/opt/airflow/data/bronze/test_parquet"
 # spark= SparkSession.builder.appName('train_silver').master("local[*]").getOrCreate()
  POSTGRES_JAR = "/opt/airflow/jars/postgresql-42.6.2.jar"
  spark = SparkSession.builder\
    .appName("session_spark")\
    .master("local[*]")\
    .config("spark.driver.memory", "1g")\
    .config("spark.executor.memory", "1g")\
    .config("spark.jars", POSTGRES_JAR)\
    .config("spark.driver.extraClassPath", POSTGRES_JAR)\
    .config("spark.executor.extraClassPath", POSTGRES_JAR)\
    .getOrCreate()

  rf= RandomForestRegressor(featuresCol= "features", labelCol="dure_trajet", predictionCol="prediction_dure",  numTrees=10,  maxDepth=6)
  train= spark.read.parquet(train_input_path)
  test= spark.read.parquet(test_input_path)
  cols = ["VendorID","passenger_count","trip_distance","RatecodeID","DOLocationID","payment_type","tip_amount","tolls_amount","congestion_surcharge","Airport_fee","dure_trajet","dropoff_hour","dropoff_dayofweek","dropoff_month","pickup_hour","pickup_dayofweek","pickup_month"]
  assembler = VectorAssembler(
    inputCols=cols,
    outputCol="features"
  )

  train_vec = assembler.transform(train)
  test_vec  = assembler.transform(test)
  rf= RandomForestRegressor(featuresCol= "features", labelCol="dure_trajet", predictionCol="prediction_dure",  numTrees=10,  maxDepth=6)
  model=rf.fit(train_vec)
  
  predictions= model.transform(test_vec)
  evaluator= RegressionEvaluator(labelCol="dure_trajet", predictionCol="prediction_dure", metricName="rmse")
  remse= evaluator.evaluate(predictions)

  evaluator= RegressionEvaluator(labelCol="dure_trajet", predictionCol="prediction_dure", metricName="r2")
  r2 = evaluator.evaluate(predictions)
  model.write().overwrite().save("/opt/airflow/data/gold/saved_model")
  return {
    "rmse": remse,
    "r2": r2
  }

#df= load_data()
#df_clean = data_cleaning(df)
#df_clean = add_cyclical_time_features(df_clean)
#normalized_df=normalize(df_clean)
#train, test = split_data(normalized_df)
#training_rf(train, test)