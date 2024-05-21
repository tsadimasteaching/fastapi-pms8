pipeline {
    agent any

    stages {
        stage('test') {
            steps {
                sh '''
                docker compose up -d --build
                docker compose exec -T fastapi tavern-ci tests
            '''
            }
        }
    }
}