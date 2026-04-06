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
                echo "Building Docker image %DOCKER_IMAGE_NAME%... (This includes training)"
                bat "docker build -t %DOCKER_IMAGE_NAME%:latest ."
            }
        }

        stage('Extract Artifacts') {
            steps {
                echo "Extracting model files from the image for archiving..."
                // Create a temporary container to copy files out
                bat "docker create --name temp_extract %DOCKER_IMAGE_NAME%:latest"
                bat "if not exist models mkdir models"
                bat "docker cp temp_extract:/app/models/. ./models/"
                bat "docker rm temp_extract"
            }
        }

        stage('Self-Test & Health Check') {
            steps {
                echo "Launching temporary container for health check..."
                bat "docker stop temp_f1_test >nul 2>&1 || rem"
                bat "docker rm temp_f1_test >nul 2>&1 || rem"
                
                bat "docker run -d --name temp_f1_test -p 8001:8000 %DOCKER_IMAGE_NAME%:latest"
                
                script {
                    echo "Checking if API is responding..."
                    sleep 10 // Give it a bit more time to start
                    bat 'powershell -Command "try { $response = Invoke-WebRequest -Uri http://localhost:8001/ -UseBasicParsing; if ($response.StatusCode -ne 200) { exit 1 } } catch { exit 1 }"'
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
        success {
            echo "Deployment ready: Run 'docker run -p 8000:8000 %DOCKER_IMAGE_NAME%'"
        }
        failure {
            echo "CI pipeline failed. Please check build logs."
        }
    }
}
