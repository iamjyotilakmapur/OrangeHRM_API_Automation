
pipeline {
    agent any

    environment {
        BASE_URL = 'https://opensource-demo.orangehrmlive.com/web/index.php'
        TOKEN = credentials('orangehrm-token')
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out project from GitHub'
            }
        }

        stage('Setup Python') {
            steps {
                sh 'python3 --version'
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
                sh '.venv/bin/python -m pytest -v'
            }
        }
    }
}
