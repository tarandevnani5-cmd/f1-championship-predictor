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

        stage('Build Environment') {
            steps {
                echo "Installing dependencies..."
                // Using 'bat' for Windows Jenkins
                bat "python -m pip install --upgrade pip"
                bat "pip install --no-cache-dir -r requirements.txt"
            }
        }

        stage('Pre-train Model') {
            steps {
                echo "Running training script..."
                bat "if not exist models mkdir models"
                bat "python src/train_no_mlflow.py"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image %DOCKER_IMAGE_NAME%..."
                bat "docker build -t %DOCKER_IMAGE_NAME%:latest ."
            }
        }

        stage('Self-Test & Health Check') {
            steps {
                echo "Launching temporary container for health check..."
                // Try to stop/remove if already exists from a previous failed run
                bat "docker stop temp_f1_test >nul 2>&1 || rem"
                bat "docker rm temp_f1_test >nul 2>&1 || rem"
                
                bat "docker run -d --name temp_f1_test -p 8001:8000 %DOCKER_IMAGE_NAME%:latest"
                
                script {
                    echo "Checking if API is responding..."
                    sleep 5
                    // Using PowerShell for a simple web request check on Windows
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
