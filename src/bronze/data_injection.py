from pyspark.sql import SparkSession

def load_data():
    spark = SparkSession.builder.appName("first_paquet").getOrCreate()
    df = spark.read.parquet("./data/dataset.parquet")
    return df
  #  df.show(5)
# load_data()