pipeline {
    agent any
    environment {
        SCRIPT_PATH = "SendDatatoKafka.scala"
    }
    stages {
        stage('Build') {
            steps {
                echo "Building the project..."
            }
        }
        stage('Run Script') {
            steps {
                script {
                    echo "Executing Scala script: ${SCRIPT_PATH}"
                    sh "scala ${SCRIPT_PATH}"
                }
            }
        }
    }
}
