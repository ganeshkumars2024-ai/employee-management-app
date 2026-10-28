
pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        IMAGE_NAME = 'employee-management'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Application') {
            steps {
                 bat 'where python'
                  bat 'python --version'
                   bat 'python -m pip --version'
                   bat 'python -m pip install -r requirements.txt'
                    bat 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_PASSWORD'
                    )
                ]) {
                    bat 'docker build -t %DH_USER%/%IMAGE_NAME%:%BUILD_NUMBER% .'
                    bat 'docker tag %DH_USER%/%IMAGE_NAME%:%BUILD_NUMBER% %DH_USER%/%IMAGE_NAME%:latest'
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_PASSWORD'
                    )
                ]) {
                    bat 'docker login -u %DH_USER% --password-stdin < NUL'
                    powershell '''
                        $env:DH_PASSWORD | docker login -u $env:DH_USER --password-stdin
                        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
                    '''
                    bat 'docker push %DH_USER%/%IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'docker push %DH_USER%/%IMAGE_NAME%:latest'
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DH_USER',
                        passwordVariable: 'DH_PASSWORD'
                    )
                ]) {
                    bat 'kubectl apply -f k8s/deployment.yaml'
                    bat 'kubectl apply -f k8s/service.yaml'
                    bat 'kubectl set image deployment/employee-management employee-management=%DH_USER%/%IMAGE_NAME%:%BUILD_NUMBER%'
                    bat 'kubectl rollout status deployment/employee-management --timeout=180s'
                    bat 'kubectl get pods'
                    bat 'kubectl get services'
                }
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Tests, Docker publishing and Kubernetes deployment completed.'
        }
        failure {
            echo 'FAILED: Check the first failed stage in the Jenkins console output.'
        }
    }
}
