pipeline {
    agent any
    environment {
        SCRIPT_PATH = "statuswithdelay.py"
        REMOTE_HDFS_FILE = "/tmp/big_datajan2025/TFL/TFLUnderground/tfl_realtime_data_underground.csv"  // Full path with filename
        LOCAL_TEMP_FILE = "merged_tfl_data.csv"
    }
    stages {
        stage('Collect Data & Upload to HDFS') {
            steps {
                script {
                    def fileExists = sh(script: "hdfs dfs -test -e ${REMOTE_HDFS_FILE} && echo 'EXIST' || echo 'MISSING'", returnStdout: true).trim()

                    if (fileExists == "EXIST") {
                        // Merge new data with existing HDFS file
                        sh """
                        hdfs dfs -cat ${REMOTE_HDFS_FILE} > ${LOCAL_TEMP_FILE}  // Download existing data
                        python3 ${SCRIPT_PATH} >> ${LOCAL_TEMP_FILE}  // Append new data from Python script
                        hdfs dfs -put -f ${LOCAL_TEMP_FILE} ${REMOTE_HDFS_FILE}  // Upload merged file
                        """
                    } else {
                        // First-time upload
                        sh "python3 ${SCRIPT_PATH} | hdfs dfs -put - ${REMOTE_HDFS_FILE}"
                    }
                }
            }
        }
    }
    triggers {
        cron('H/30 * * * *')  // Runs every 30 minutes
    }
}
