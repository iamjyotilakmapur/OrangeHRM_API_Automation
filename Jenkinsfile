
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
                sh '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 --version'
                sh '/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv .venv'
                sh '.venv/bin/python3.12 -m pip install -r requirements.txt'
            }
        }

        stage('Run Pytest') {
            steps {
                sh '.venv/bin/python3.12 -m pytest -v'
            }
        }
    }
}
