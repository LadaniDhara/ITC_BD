from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

# Create Spark Session with Hive support and explicit Hive Metastore configuration
spark = SparkSession.builder \
    .appName("TfL Underground ETL") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
    .config("spark.hadoop.hive.metastore.uris", "thrift://18.170.23.150:9083") \
    .enableHiveSupport() \
    .getOrCreate()

# Log available databases and tables to verify connection
databases = spark.sql("SHOW DATABASES")
print("Available databases:", databases.collect())

tables = spark.sql("SHOW TABLES IN default")
print("Tables in default:", tables.collect())

# Explicitly use the default database
spark.sql("USE default")

# Refresh the table metadata to avoid caching issues
spark.catalog.refreshTable("default.tfl_undergroundrecord")

# Read data from Hive table
try:
    df = spark.sql("SELECT * FROM default.tfl_undergroundrecord")
    print("Table 'tfl_undergroundrecord' loaded successfully with {} rows.".format(df.count()))
except Exception as e:
    print("Error reading table: {}".format(e))
    spark.stop()
    exit(1)

# Example Transformation: Convert all status descriptions to uppercase
transformed_df = df.withColumn("status", upper(col("status")))

# Save transformed data to new Hive table
transformed_df.write.mode("overwrite").saveAsTable("default.tfl_underground_result")

print("✅ Transformation complete. Data saved to default.tfl_underground_result.")

# Stop Spark session
spark.stop()
