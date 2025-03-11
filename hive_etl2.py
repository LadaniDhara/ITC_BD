from pyspark.sql import *
from pyspark.sql.functions import *
import pyspark.sql.functions as F
from pyspark.sql.functions import col, upper
from pyspark.sql import SparkSession

spark = SparkSession.builder.master("local").appName("TfL Underground ETL").enableHiveSupport().getOrCreate()
try:
    df = spark.sql("SELECT * FROM default.tfl_undergroundrecord")
    print("data successfully read")
except Exception as e:
    print("Error occurred during Hive operations")

# Example Transformation: Convert all status descriptions to uppercase
df_transformed = df.withColumn("status", upper(col("status")))

try:
    df_transformed.write.mode("overwrite").saveAsTable("default.tfl_undergroundresul")
    print("Successfully Load to Hive")
except Exception as e:
    print("Error occurred during Hive operations")