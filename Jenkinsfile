pipeline {
    agent any

    environment {
        PYTHON_PATH = 'C:\\Users\\amith\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe'
        DOCKER_PATH = 'C:\\Program Files\\Docker\\Docker\\resources\\bin\\docker.exe'
        IMAGE_NAME = 'bhumisheru/ear-disease-app:latest'
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
                bat '"%PYTHON_PATH%" -m pip install -r requirements.txt'
            }
        }

        stage('Code Quality Check') {
            steps {
                bat '"%PYTHON_PATH%" -m py_compile app.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '"%DOCKER_PATH%" build -t ear-disease-app .'
            }
        }

        stage('Tag Docker Image') {
            steps {
                bat '"%DOCKER_PATH%" tag ear-disease-app %IMAGE_NAME%'
            }
        }

        stage('Docker Login') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_PASS'
                )]) {

                    bat '"%DOCKER_PATH%" login -u %DOCKER_USER% -p %DOCKER_PASS%'
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                bat '"%DOCKER_PATH%" push %IMAGE_NAME%'
            }
        }

        stage('Remove Old Container') {
            steps {
                bat '"%DOCKER_PATH%" rm -f ear-container || exit 0'
            }
        }

        stage('Run Docker Container') {
            steps {
                bat '"%DOCKER_PATH%" run -d --name ear-container -p 5001:5000 ear-disease-app'
            }
        }
    }

    post {
        success {
            echo 'Pipeline executed successfully!'
        }

        failure {
            echo 'Pipeline execution failed!'
        }
    }
}