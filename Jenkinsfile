pipeline {
    agent any
    environment {
        SCRIPT_PATH = "statuswithdelay.py"  // Relative path within your repository (no need for ITC_BD/ prefix)
        CSV_FILE = "tfl_realtime_data_underground.csv"  // Relative path within your repository (no need for ITC_BD/ prefix)
        REMOTE_HDFS_PATH = "/tmp/big_datajan2025/TFL/TFLUnderground/tfl_realtime_data_underground.csv"  // HDFS path to the target CSV file
    }
    stages {
        stage('Collect Data') {
            steps {
                // Run the Python script to collect data
                sh "python3 ${SCRIPT_PATH}"
            }
        }
        stage('Upload to HDFS') {
            steps {
                // Upload the CSV file directly to HDFS and append the new data
                sh """
                hdfs dfs -mkdir -p ${REMOTE_HDFS_PATH}
                hdfs dfs -appendToFile ${CSV_FILE} ${REMOTE_HDFS_PATH}
                """
            }
        }
    }
    triggers {
        cron('H/30 * * * *')  // Runs every 30 minutes
    }
}
