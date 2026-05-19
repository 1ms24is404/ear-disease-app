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
                bat '"C:\\Users\\amith\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m pip install -r requirements.txt'
            }
        }

        stage('Code Quality Check') {
            steps {
                bat '"C:\\Users\\amith\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m py_compile app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" build -t ear-disease-app .'
            }
        }

        stage('Tag Docker Image') {
            steps {
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" tag ear-disease-app bhumisheru/ear-disease-app:latest'
            }
        }

        stage('Push Docker Image') {
            steps {
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" push bhumisheru/ear-disease-app:latest'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat '"C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe" run -d -p 5001:5000 ear-disease-app'
            }
        }
    }
}