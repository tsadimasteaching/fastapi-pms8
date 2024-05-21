pipeline {
    agent any

    stages {
        stage('test') {
            sh '''
                docker compose up -d --build
                docker compose exec -T fastapi tavern-ci tests
            '''
        }

    }
}