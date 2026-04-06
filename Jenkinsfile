pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "f1-predictor"
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code already handled by Jenkins in standard builds
                echo "Code checked out successfully."
            }
        }

        stage('Build Environment') {
            steps {
                echo "Installing dependencies..."
                sh 'pip install --no-cache-dir -r requirements.txt'
            }
        }

        stage('Pre-train Model') {
            steps {
                echo "Running training script..."
                sh 'python src/train_no_mlflow.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image ${DOCKER_IMAGE_NAME}..."
                sh "docker build -t ${DOCKER_IMAGE_NAME}:latest ."
            }
        }

        stage('Self-Test & Health Check') {
            steps {
                echo "Launching temporary container for health check..."
                sh "docker run -d --name temp_f1_test -p 8001:8000 ${DOCKER_IMAGE_NAME}:latest"
                
                // Simple health check against the FastAPI root
                script {
                    echo "Checking if API is responding..."
                    sleep 5
                    sh "curl -f http://localhost:8001/ || (docker stop temp_f1_test && docker rm temp_f1_test && exit 1)"
                }

                echo "Cleaning up test container..."
                sh "docker stop temp_f1_test && docker rm temp_f1_test"
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo "Archiving developed models..."
                archiveArtifacts artifacts: 'models/*.pkl', fingerprint: true
            }
        }
    }

    post {
        always {
            echo "CI pipeline completed."
        }
        success {
            echo "Deployment ready: Run 'docker run -p 8000:8000 ${DOCKER_IMAGE_NAME}'"
        }
        failure {
            echo "CI pipeline failed. Please check build logs."
        }
    }
}
