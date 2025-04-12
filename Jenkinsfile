pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'containerized-ml'
        DOCKER_TAG = "${BUILD_NUMBER}"
        PYTHON_PATH = '/usr/local/bin/python3'
    }
    
    stages {
        stage('Setup') {
            steps {
                sh '''
                    which python3 || echo "Python3 not found"
                    python3 -m venv venv
                    . venv/bin/activate && pip install -r requirements.txt
                '''
            }
        }
        
        stage('Test') {
            steps {
                sh '. venv/bin/activate && python3 -m pytest'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_IMAGE}:${DOCKER_TAG}")
                }
            }
        }
        
        stage('Deploy') {
            when {
                branch 'main'
            }
            steps {
                script {
                    echo "Deploying version ${DOCKER_TAG}"
                }
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline succeeded!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
} 