pipeline {
    agent any
    
    environment {
    DOCKER_IMAGE = 'my-ml-app'
    DOCKER_TAG = "${BUILD_NUMBER}"
    PYTHON_PATH = '/usr/local/bin/python3'
    DOCKER_PATH = '/usr/local/bin/docker'
    PATH = "/usr/local/bin:$PATH"
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

        stage('Docker Check') {
    steps {
        sh '''
            docker version
        '''
    }
}
        
        stage('Build Docker Image') {
    steps {
        sh '''
            # Setup Docker config without credsStore
            mkdir -p ~/.docker
            echo '{ "credsStore": "" }' > ~/.docker/config.json

            # Check Docker installation
            if [ ! -x "${DOCKER_PATH}" ]; then
                echo "Docker is not installed or not executable at ${DOCKER_PATH}"
                exit 1
            fi
            
            # Check Docker daemon (no custom DOCKER_HOST anymore)
            if ! ${DOCKER_PATH} info &> /dev/null; then
                echo "❌ Docker is not running or Docker socket not available to Jenkins."
                exit 1
            fi
            
            # Check Dockerfile existence
            if [ ! -f "Dockerfile" ]; then
                echo "Dockerfile not found in the workspace"
                exit 1
            fi
            
            echo "✅ Building Docker image..."
            ${DOCKER_PATH} build --progress=plain -t ${DOCKER_IMAGE}:${DOCKER_TAG} .
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