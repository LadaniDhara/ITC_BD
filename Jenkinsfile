pipeline {
    agent any
    stages {
        stage('Run PySpark Transformation') {
            steps {
                sh 'hive_etl.py'
            }
        }
    }
}
