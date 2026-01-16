
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bronze.data_injection import load_data
from silver.data_cleaning import data_cleaning
from pyspark.sql import SparkSession
def split_data():
 # spark= SparkSession.builder.appName('split_silver').master("local[*]").getOrCreate()
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

   input_path= "/opt/airflow/data/silver/cleaned_data"
   normalized_df = spark.read.parquet(input_path)

   train, test= normalized_df.randomSplit([0.7, 0.3])
   train.write.mode("overwrite").parquet("/opt/airflow/data/bronze/train_parquet")
   test.write.mode("overwrite").parquet("/opt/airflow/data/bronze/test_parquet")

# df= load_data()
# df_clean = data_cleaning(df)
#df_clean = add_cyclical_time_features(df_clean)
#normalized_df=normalize(df_clean)
#train, test = split_data(normalized_df)
#rain.show(2)