pipeline {
    agent any
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
        stage('Run Tests') {
            steps {
                sh '''
                . venv/bin/activate
                pytest --cov=src tests/
                '''
            }
        }
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