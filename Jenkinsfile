pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                git branch: 'muazrana', url: 'https://github.com/LadaniDhara/ITC_BD.git'
            }
        }
        stage('Setup Python & Install Dependencies') {
            steps {
                sh 'python3 -m ensurepip --default-pip'  // Ensure pip is available
                sh 'pip3 install --upgrade pip'  // Upgrade pip
                sh 'pip3 install pyspark'  // ✅ Install PySpark before running script
            }
        }
        stage('Run PySpark Transformation') {
            steps {
                sh 'python3 hive_etl.py'  // ✅ Run the PySpark script
            }
        }
    }
}
