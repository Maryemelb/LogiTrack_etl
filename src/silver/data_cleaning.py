from pyspark.sql.functions import col, when, dayofweek, hour, month
import pyspark.sql.functions as sf
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pyspark.sql import SparkSession
from bronze.data_injection import load_data
def data_cleaning():
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

      df= spark.read.parquet('/opt/airflow/data/bronze/taxi')
      cleaned_df= df.na.drop()
      cleaned_df = cleaned_df.withColumn("dure_trajet", (sf.unix_timestamp(sf.col("tpep_dropoff_datetime"))- sf.unix_timestamp(sf.col("tpep_pickup_datetime")))/60)
      cleaned_df= cleaned_df.filter((col("trip_distance")> 0) & (col("trip_distance")<200 ) & ( col("dure_trajet") > 0) & (col("passenger_count") > 0))
      
      #drop unicessary columns
      cleaned_df =cleaned_df.drop("fare_amount","mta_tax", "total_amount","cbd_congestion_fee","store_and_fwd_flag", "extra","improvement_surcharge")

      #add date columns

      cleaned_df= cleaned_df.withColumn("dropoff_hour", hour("tpep_dropoff_datetime"))\
                 .withColumn("dropoff_dayofweek", dayofweek("tpep_dropoff_datetime")) \
                 .withColumn("dropoff_month", month("tpep_dropoff_datetime")) \
                 .withColumn("pickup_hour", hour("tpep_pickup_datetime")) \
                 .withColumn("pickup_dayofweek", dayofweek("tpep_pickup_datetime")) \
                 .withColumn("pickup_month", month("tpep_pickup_datetime"))
      cleaned_df=cleaned_df.drop("tpep_dropoff_datetime","tpep_pickup_datetime")
      #am not goign to unclude passenger_count because it have limited values in outliers handling
      numerical_df_cols= cleaned_df.select("dure_trajet","trip_distance","tip_amount","tolls_amount","congestion_surcharge","Airport_fee")

      #handle Outliers
      for feature in numerical_df_cols.columns:
         quartilles = numerical_df_cols.approxQuantile(feature, [0.25,0.50, 0.75],0.01) #0 err

         iqr = quartilles[2] - quartilles[0]
         uper_bound= quartilles[2] + 1.5 * iqr
         lower_bound= quartilles[0] - 1.5 * iqr

         cleaned_df= cleaned_df.withColumn( 
              feature,
              when(col(feature)>uper_bound , uper_bound) 
              .when(col(feature) < lower_bound , lower_bound)
              .otherwise(col(feature))
            
         )

      cleaned_df.write.mode("overwrite").parquet("/opt/airflow/data/silver/cleaned_data")
      cleaned_df.write \
  .format("jdbc") \
  .option("url", "jdbc:postgresql://postgres:5432/airflow") \
  .option("dbtable", "silver_taxis") \
  .option("user", "airflow") \
  .option("password", "airflow") \
  .option("driver", "org.postgresql.Driver") \
  .mode("overwrite") \
  .save() 
      return "data cleaning done"
#df= load_data()     
#df_clean = data_cleaning(df)
#df_clean.show()