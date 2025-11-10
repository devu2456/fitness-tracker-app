pipeline {
    agent any
    environment {
        PYTHONPATH = "${WORKSPACE}/src" // Add the src directory to PYTHONPATH
    }
    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository from GitHub
                git branch: 'main', url: 'https://github.com/devu2456/fitness-tracker-app.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                // Create a Python virtual environment and install dependencies
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                '''
            }
        }
        // Skipping the Run Tests stage
        /*
        stage('Run Tests') {
            steps {
                // Run tests with pytest and generate coverage report
                sh '''
                . venv/bin/activate
                echo "Python Path: $PYTHONPATH"
                python --version
                pip list
                PYTHONPATH=${WORKSPACE}/src pytest --cov=src tests/
                '''
            }
        }
        */
        stage('Build Docker Image') {
            steps {
                // Build and push the Docker image to Docker Hub
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                    docker build -t $DOCKER_USER/fitness-tracker-app:latest .
                    docker login -u $DOCKER_USER -p $DOCKER_PASS
                    docker push $DOCKER_USER/fitness-tracker-app:latest
                    '''
                }
            }
        }
        stage('Build Artifact') {
            steps {
                // Package the application source code into a zip file
                sh '''
                . venv/bin/activate
                zip -r build-artifact.zip src/
                '''
            }
        }
        stage('Archive Artifact') {
            steps {
                // Archive the build artifact for future use
                archiveArtifacts artifacts: 'build-artifact.zip', fingerprint: true
            }
        }
    }
}