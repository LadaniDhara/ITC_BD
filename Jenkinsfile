pipeline {
    agent any
    environment {
        SCRIPT_PATH = "TFL_Underground.py"
    }
    stages {
        stage('Fetch & Store Data in HDFS') {
            steps {
                script {
                    sh "python3 ${SCRIPT_PATH}"
                }
            }
        }
    }
    triggers {
        cron('H/30 * * * *')  // Runs every 30 minutes
    }
}