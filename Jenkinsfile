pipeline {
    agent any
    environment {
        SCRIPT_PATH = "statuswithdelay.py"  // Relative path within your repository (no need for ITC_BD/ prefix)
        CSV_FILE = "tfl_realtime_data_underground.csv"  // Relative path within your repository (no need for ITC_BD/ prefix)
        REMOTE_HDFS_PATH = "/tmp/big_datajan2025/TFL/TFLUnderground"  // HDFS path
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
                // Upload the CSV file directly to HDFS
                sh """
                hdfs dfs -mkdir -p ${REMOTE_HDFS_PATH}
                hdfs dfs -put -f ${CSV_FILE} ${REMOTE_HDFS_PATH}/tfl_realtime_data_underground.csv
                """
            }
        }
    }
}
