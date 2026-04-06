pipeline {
    agent any

    environment {
        DOCKER_IMAGE_NAME = "f1-predictor"
    }

    stages {
        stage('Checkout') {
            steps {
                echo "Code checked out successfully."
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image %DOCKER_IMAGE_NAME%..."
                bat "docker build -t %DOCKER_IMAGE_NAME%:latest ."
            }
        }

        stage('Extract Artifacts') {
            steps {
                echo "Extracting model files from the image..."
                bat "docker create --name temp_extract %DOCKER_IMAGE_NAME%:latest"
                bat "if not exist models mkdir models"
                bat "docker cp temp_extract:/app/models/. ./models/"
                bat "docker rm temp_extract"
            }
        }

        stage('Self-Test & Health Check') {
            steps {
                echo "Cleaning up any old test containers..."
                // Using '@' to suppress command output and ensuring the line always completes with success (exit 0)
                bat """
                    @echo off
                    docker stop temp_f1_test >nul 2>&1
                    docker rm temp_f1_test >nul 2>&1
                    exit /b 0
                """
                
                echo "Launching new container for health check..."
                bat "docker run -d --name temp_f1_test -p 8001:8000 %DOCKER_IMAGE_NAME%:latest"
                
                script {
                    echo "Checking if API is responding..."
                    sleep 10
                    bat 'powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:8001/health -UseBasicParsing; if ($response.StatusCode -ne 200) { exit 1 } } catch { exit 1 }"'
                }

                echo "Cleaning up test container..."
                bat "docker stop temp_f1_test"
                bat "docker rm temp_f1_test"
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
    }
}
