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
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'pytest --cov=src tests/'
            }
        }
        stage('Build Artifact') {
            steps {
                sh 'zip -r build-artifact.zip src/'
            }
        }
        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'build-artifact.zip', fingerprint: true
            }
        }
    }
}