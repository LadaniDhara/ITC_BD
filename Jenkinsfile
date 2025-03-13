pipeline {
    agent any
    environment {
        SCRIPT_NAME = "SendDataToKafka"
        SCRIPT_PATH = "SendDataToKafka.scala"
        JAR_NAME = "SendDataToKafka.jar"
        MAIN_CLASS = "kafkaspark.SendDataToKafka"
    }
    stages {
        stage('Setup') {
            steps {
                echo "Checking system dependencies..."
                sh "scala -version"
                sh "scalac -version"
                sh "spark-submit --version || echo 'Spark not found'"
            }
        }
        stage('Build') {
            steps {
                echo "Compiling Scala application..."
                sh """scalac -classpath \$(hadoop classpath) -d ${JAR_NAME} ${SCRIPT_PATH}"""
            }
        }
        stage('Run') {
            steps {
                script {
                    echo "Running the Spark job..."
                    sh """
                    spark-submit --class ${MAIN_CLASS} --master local[*] \
                    --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 \
                    ${JAR_NAME}
                    """
                }
            }
        }
    }
}
