import org.apache.spark.sql.{SparkSession, DataFrame}
import java.util.Properties

object ReadFromPostgres {
      def main(args: Array[String]): Unit = {
        // Step 1: Initialize SparkSession
        val spark = SparkSession.builder()
          .appName("Read from PostgreSQL")
          .master("local[*]")  // You can adjust this based on your cluster setup
          .getOrCreate()

        // Step 2: Define PostgreSQL connection properties
        val jdbcUrl = "jdbc:postgresql://18.170.23.150:5432/testdb"  // Your PostgreSQL URL
        val dbTable = "TFL_Underground_Scala"  // The table from which you want to read
        val dbUser = "consultants"  // PostgreSQL username
        val dbPassword = "WelcomeItc@2022"  // PostgreSQL password

        // JDBC connection properties
        val dbProperties = new Properties()
        dbProperties.setProperty("user", dbUser)
        dbProperties.setProperty("password", dbPassword)
        dbProperties.setProperty("driver", "org.postgresql.Driver")

        // Step 3: Read data from PostgreSQL into a DataFrame
        try {
          val df: DataFrame = spark.read
            .jdbc(jdbcUrl, dbTable, dbProperties)

          // Step 4: Show the data
          df.show()  // You can replace this with any other operation like df.printSchema()

          println("Data successfully loaded from PostgreSQL.")

        } catch {
          case e: Exception =>
            println(s"Error occurred while reading from PostgreSQL: ${e.getMessage}")
        }

        // Step 5: Stop Spark session
        spark.stop()
      }
    }
