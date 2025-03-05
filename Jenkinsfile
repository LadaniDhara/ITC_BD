pipeline {
    agent any
    environment {
        SCRIPT_PATH = "fetch_tfl_data.py"
        REMOTE_HDFS_FILE = "/tmp/big_datajan2025/TFL/TFLUnderground/tfl_realtime_data_underground.csv"
    }
    stages {
        stage('Fetch & Append Data to HDFS') {
            steps {
                script {
                    sh """
                    python3 ${SCRIPT_PATH}
                    """
                }
            }
        }
    }
}
