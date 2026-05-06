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
                sh '''
                    docker run --rm \
                    -v "$PWD":/app \
                    -w /app \
                    python:3.11-slim \
                    sh -c "pip install flake8 && flake8 app.py"
                '''
            }
        }

        stage('Code Build') {
            steps {
                sh 'docker build -t flask-notes-app .'
            }
        }

        stage('Containerized Deployment') {
            steps {
                sh 'docker-compose down -v || true'
                sh 'docker-compose up -d --build'
                sh 'sleep 40'
                sh 'docker ps'
                sh 'docker network ls'
            }
        }

        stage('Containerized Selenium Testing') {
            steps {
                sh 'docker build -t flask-notes-selenium ./selenium-tests'
                sh '''
                    docker run --rm \
                    --network assignment-03_default \
                    -e APP_URL=http://web:5000 \
                    flask-notes-selenium
                '''
            }
        }
    }

    post {
        always {
            sh 'docker-compose down -v || true'
        }

        success {
            echo 'Pipeline completed successfully.'
        }

        failure {
            echo 'Pipeline failed.'
        }
    }
}
