#pyspark Standar scaler
from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from silver.adjust_cyclical_time_features import add_cyclical_time_features

from bronze.data_injection import load_data
from silver.data_cleaning import data_cleaning
from pyspark.sql import SparkSession
def normalize():
 spark= SparkSession.builder.appName('normalize_silver').master("local[*]").getOrCreate()
 try:
    cols_to_scale=[
        "passenger_count", "trip_distance", "tip_amount", "tolls_amount","congestion_surcharge", "Airport_fee"
    ]
    input_path= "/opt/airflow/data/silver/cyclical_features"
    df= spark.read.parquet(input_path)
    assembler= VectorAssembler(inputCols= cols_to_scale, outputCol="vectors")
    assembled_df =assembler.transform(df)
    assembled_df.show(5)
    scaler= StandardScaler(inputCol="vectors", outputCol="scaled_features")
    scaler_df= scaler.fit(assembled_df).transform(assembled_df)
    cols_to_add_to_features= [
          "DOLocationID","PULocationID",
          "RatecodeID", "VendorID",
          "payment_type",
          "scaled_features",
          "pickup_hour_sin",
         "pickup_hour_cos",
        "pickup_dayofweek_sin",
        "pickup_dayofweek_cos",
        "pickup_month_sin",
        "pickup_month_cos",
        "dropoff_hour_sin",
        "dropoff_hour_cos",
        "dropoff_dayofweek_sin",
        "dropoff_dayofweek_cos",
        "dropoff_month_sin",
         "dropoff_month_cos"
         ]
    assembler_vector= VectorAssembler(inputCols=cols_to_add_to_features, outputCol="features")
    assembled_df_vecotr =assembler_vector.transform(scaler_df)
    assembled_df_vecotr =assembled_df_vecotr.select("features", "dure_trajet")
    output_path = "/opt/airflow/data/bronze/normalized_data"
    assembled_df_vecotr.write.mode("overwrite").parquet(output_path)
 finally:
    spark.stop()
#df= load_data()
#df_clean = data_cleaning(df)
#df_clean = add_cyclical_time_features(df_clean)
#normalized_df=normalize(df_clean)
#normalized_df.show(5)
    