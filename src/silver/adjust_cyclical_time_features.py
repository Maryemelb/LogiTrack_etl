from pyspark.sql.functions import sin, cos, col, lit
import math
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bronze.data_injection import load_data
from silver.data_cleaning import data_cleaning


def add_cyclical_time_features(df):
    # Precompute constants
    angle_hour = 2 * math.pi / 24
    angle_day = 2 * math.pi / 7
    angle_month = 2 * math.pi / 12

    # Pickup time
    df = df.withColumn("pickup_hour_sin", sin(col("pickup_hour") * lit(angle_hour))) \
           .withColumn("pickup_hour_cos", cos(col("pickup_hour") * lit(angle_hour))) \
           .withColumn("pickup_dayofweek_sin", sin((col("pickup_dayofweek") - lit(1)) * lit(angle_day))) \
           .withColumn("pickup_dayofweek_cos", cos((col("pickup_dayofweek") - lit(1)) * lit(angle_day))) \
           .withColumn("pickup_month_sin", sin((col("pickup_month") - lit(1)) * lit(angle_month))) \
           .withColumn("pickup_month_cos", cos((col("pickup_month") - lit(1)) * lit(angle_month)))

    # Dropoff time
    df = df.withColumn("dropoff_hour_sin", sin(col("dropoff_hour") * lit(angle_hour))) \
           .withColumn("dropoff_hour_cos", cos(col("dropoff_hour") * lit(angle_hour))) \
           .withColumn("dropoff_dayofweek_sin", sin((col("dropoff_dayofweek") - lit(1)) * lit(angle_day))) \
           .withColumn("dropoff_dayofweek_cos", cos((col("dropoff_dayofweek") - lit(1)) * lit(angle_day))) \
           .withColumn("dropoff_month_sin", sin((col("dropoff_month") - lit(1)) * lit(angle_month))) \
           .withColumn("dropoff_month_cos", cos((col("dropoff_month") - lit(1)) * lit(angle_month)))

    # Drop original hour/day/month columns
    df = df.drop("pickup_hour", "pickup_dayofweek", "pickup_month",
                 "dropoff_hour", "dropoff_dayofweek", "dropoff_month")

    return df
df= load_data()
df_clean = data_cleaning(df)
df_clean = add_cyclical_time_features(df_clean)
df_clean.show(5)