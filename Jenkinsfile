pipeline {
    agent any

    tools {
        nodejs 'nodejs'
    }

    stages {

        stage('Clone Repository') {
            steps {
                git branch: 'main',
                url: 'https://github.com/1ms24is404/ear-disease-app.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Code Quality Check') {
            steps {
                bat 'python -m py_compile app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t ear-disease-app .'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat 'docker run -d -p 5000:5000 ear-disease-app'
            }
        }
    }
}