from pyspark.sql import SparkSession

def load_data():
    # Use a clear app name
    #spark = SparkSession.builder.appName("taxi_bronze_layer").getOrCreate()
        spark = SparkSession.builder\
    .appName("session_spark")\
    .master("local[*]")\
    .config("spark.driver.memory", "1g")\
    .config("spark.executor.memory", "1g")\
    .config(
        "spark.jars","/opt/airflow/jars/postgresql-42.6.2.jar")\
    .getOrCreate()

        # Use ABSOLUTE paths inside the docker container
        input_path = "/opt/airflow/data/dataset.parquet"
        output_path = "/opt/airflow/data/bronze/taxi"
        
        df = spark.read.parquet(input_path)
        
        # Write the data
        df.write.mode("overwrite").parquet(output_path)
  
        
        # IMPORTANT: Return the STRING path, NOT the 'df' object
        return output_path
        
   