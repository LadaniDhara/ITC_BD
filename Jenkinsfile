pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'muazrana', url: 'https://github.com/LadaniDhara/ITC_BD.git'
            }
        }
        stage('Run PySpark Transformation') {
            steps {
                sh 'python3 hive_etl.py'  // ✅ Ensure the script is run with Python
            }
        }
    }
}
