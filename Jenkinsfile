pipeline {
    agent any
    environment {
        SCRIPT_PATH = "SendDatatoKafka.scala"
    }
    stages {
        stage('Build') {
            steps {
                echo "Building the project..."
                sh "scalac ${SCRIPT_PATH}"
            }
        }
        stage('Run Script') {
            steps {
                script {
                    echo "Executing Scala script: ${SCRIPT_PATH}"
                    sh "scala kafkaspark.SendDatatoKafka"
                }
            }
        }
    }
}
