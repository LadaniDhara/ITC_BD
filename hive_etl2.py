from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.functions import col, upper, monotonically_increasing_id
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").appName("TfL Underground ETL").enableHiveSupport().getOrCreate()
try:
    df = spark.sql("SELECT * FROM default.tfl_undergroundrecord")
    print("data successfully read")
except Exception as e:
    print("Error occurred during Hive operations")

# Example Transformation: Convert all status descriptions to uppercase
df_transformed = df.withColumn("status", upper(col("status")))

df_transformed = df_transformed.withColumn("status", upper(col("status"))) \
    .withColumn("record_id", monotonically_increasing_id() + 1)

try:
    df_transformed.write.mode("overwrite").saveAsTable("default.tfl_undergroundresult")
    print("Successfully Load to Hive")
except Exception as e:
    print("Error occurred during Hive operations")