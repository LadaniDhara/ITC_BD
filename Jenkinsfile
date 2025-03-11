pipeline {
    agent any
    environment {
        SPARK_HOME = "/path/to/spark"  // ✅ Set the correct path to your Spark installation
        PYSPARK_PYTHON = "python3"  // ✅ Ensure Python3 is used
        PATH = "$SPARK_HOME/bin:$PATH"
    }
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
                sh '''
                export SPARK_HOME=/opt/spark/
                export PYSPARK_PYTHON=python3
                export PATH=$SPARK_HOME/bin:$PATH
                python3 hive_etl.py  // ✅ Run the PySpark script
                '''
            }
        }
    }
}
