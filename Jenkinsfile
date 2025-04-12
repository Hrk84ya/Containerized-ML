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
                sh '''
                    # Check Docker installation
                    if ! command -v docker &> /dev/null; then
                        echo "Docker is not installed or not in PATH"
                        exit 1
                    fi
                    
                    # Check Docker daemon
                    if ! docker info &> /dev/null; then
                        echo "Docker daemon is not running or not accessible"
                        exit 1
                    fi
                    
                    # Build the image
                    echo "Building Docker image..."
                    docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
                '''
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