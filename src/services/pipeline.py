

from pyspark.ml.feature import StandardScaler
from pyspark.ml.feature import VectorAssembler

def data_pipline(df):
    cols_to_scale=[
        "passenger_count", "trip_distance", "tip_amount", "tolls_amount","congestion_surcharge", "Airport_fee"
    ]
    assembler= VectorAssembler(inputCols= cols_to_scale, outputCol="vectors")
    assembled_df =assembler.transform(df)
    # assembled_df.show(5)
    scaler= StandardScaler(inputCol="vectors", outputCol="scaled_features")
    scaler_df= scaler.fit(assembled_df).transform(assembled_df)
    cols_to_add_to_features= [
          "DOLocationID",
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
    assembled_df_vecotr =assembled_df_vecotr.select("features")
    return assembled_df_vecotr