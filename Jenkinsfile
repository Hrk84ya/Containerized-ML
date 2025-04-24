pipeline {
    agent any
    
    environment {
    DOCKER_IMAGE = 'my-ml-app'
    DOCKER_TAG = "${BUILD_NUMBER}"
    PYTHON_PATH = '/usr/local/bin/python3'
    DOCKER_PATH = '/usr/local/bin/docker'
    DOCKER_CONFIG = ''
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
                    export DOCKER_HOST=unix:///Users/hrk84ya/Library/Containers/com.docker.docker/Data/docker-cli.sock

                    if ! docker info &> /dev/null; then
                        echo "❌ Docker is not running or Docker socket not available to Jenkins."
                        exit 1
                    fi

                    echo "✅ Docker is running. Proceeding to build the image..."
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