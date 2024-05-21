pipeline {
    agent any

    stages {
        stage('test') {
            steps {
                sh '''
                docker compose down --volumes
                docker compose up -d --build
                while ! wget -S --spider http://localhost:8000/docs; do sleep 1; done
                docker compose exec -T fastapi tavern-ci tests
                docker compose down --volumes
            '''
            }
        }
    }
}