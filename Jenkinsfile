pipeline {
    agent any

    options {
        timestamps()
    }

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Code Linting') {
            steps {
                sh 'python3 -m pip install --user flake8'
                sh 'python3 -m flake8 app.py'
            }
        }

        stage('E2E Build and Test') {
            steps {
                sh 'docker compose down -v || true'
                sh 'docker compose up --build --abort-on-container-exit --exit-code-from tests tests'
            }
        }
    }

    post {
        always {
            sh 'docker compose down -v || true'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
