from pyspark.sql import SparkSession

def load_data():
    # Use a clear app name
    spark = SparkSession.builder.appName("taxi_bronze_layer").getOrCreate()
    
    try:
        # Use ABSOLUTE paths inside the docker container
        input_path = "/opt/airflow/data/dataset.parquet"
        output_path = "/opt/airflow/data/bronze/taxi"
        
        df = spark.read.parquet(input_path)
        
        # Write the data
        df.write.mode("overwrite").parquet(output_path)
        
        # IMPORTANT: Return the STRING path, NOT the 'df' object
        return output_path
        
    finally:
        # Stop the session to free up memory
        spark.stop()