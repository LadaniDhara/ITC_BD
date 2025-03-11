import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, upper

# Redirect stdout and stderr to ensure logs are captured in Jenkins console
sys.stdout = sys.stderr

# Create Spark Session with Hive support
spark = SparkSession.builder \
    .appName("TfL Underground ETL") \
    .enableHiveSupport() \
    .getOrCreate()
    # .config("spark.sql.warehouse.dir", "/user/hive/warehouse")  # Uncomment only if necessary
    # .config("spark.hadoop.hive.metastore.uris", "thrift://18.170.23.150:9083")  # Uncomment only if necessary

print("Starting the Spark job...")

# Log available databases and tables to verify connection
try:
    databases = spark.sql("SHOW DATABASES")
    print("Available databases:", databases.collect())
    
    tables = spark.sql("SHOW TABLES IN default")
    print("Tables in default:", tables.collect())

    # Explicitly use the default database
    spark.sql("USE default")

    # Refresh the table metadata to avoid caching issues
    spark.catalog.refreshTable("default.tfl_undergroundrecord")

    # Read data from Hive table
    df = spark.sql("SELECT * FROM default.tfl_undergroundrecord")
    print(f"Table 'tfl_undergroundrecord' loaded successfully with {df.count()} rows.")
except Exception as e:
    print(f"Error occurred during Hive operations: {e}")
    spark.stop()
    sys.exit(1)

# Example Transformation: Convert all status descriptions to uppercase
transformed_df = df.withColumn("status", upper(col("status")))

# Save transformed data to new Hive table
try:
    transformed_df.write.mode("overwrite").saveAsTable("default.tfl_undergroundresult")
    print("✅ Transformation complete. Data saved to default.tfl_undergroundresult.")
except Exception as e:
    print(f"Error occurred during table creation: {e}")
    spark.stop()
    sys.exit(1)

# Show tables after the operation to verify
tables_after = spark.sql("SHOW TABLES IN default")
print("Tables in default after operation:", tables_after.collect())

# Stop Spark session
print("Stopping the Spark session...")
spark.stop()

print("Spark job completed successfully.")
