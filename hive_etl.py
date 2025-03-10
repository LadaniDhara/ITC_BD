from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

# Create Spark Session with Hive support
spark = SparkSession.builder \
    .appName("TfL Underground ETL") \
    .enableHiveSupport() \
    .getOrCreate()

# Read data from Hive table
df = spark.sql("SELECT * FROM default.tfl_undergroundrecord")

# Example Transformation: Convert all status descriptions to uppercase
transformed_df = df.withColumn("status", upper(col("status")))

# Save transformed data to new Hive table
transformed_df.write.mode("overwrite").saveAsTable("default.tfl_undergroundresult")

print("✅ Transformation complete. Data saved to default.tfl_undergroundresult.")

# Stop Spark session
spark.stop()
