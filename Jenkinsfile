pipeline {
    agent any
    environment {
        PYTHONPATH = "${WORKSPACE}/src" // Add the src directory to PYTHONPATH
    }
    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/devu2456/fitness-tracker-app.git'
            }
        }
        stage('Install Dependencies') {
            steps {
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
        stage('Build Artifact') {
            steps {
                sh '''
                . venv/bin/activate
                zip -r build-artifact.zip src/
                '''
            }
        }
        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'build-artifact.zip', fingerprint: true
            }
        }
    }
}