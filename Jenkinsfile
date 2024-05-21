pipeline {
    agent any
    environment {
        DOCKER_TOKEN=credentials('docker-push-secret')
        DOCKER_USER='tsadimas'
        DOCKER_SERVER='ghcr.io'
        DOCKER_PREFIX='ghcr.io/tsadimas/pms8-fastapi'
    }
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
        stage('docker build and push') {
            steps {
                sh '''
                   HEAD_COMMIT=$(git rev-parse --short HEAD)
                   TAG=$HEAD_COMMIT-$BUILD_ID
                   docker build --rm -t $DOCKER_PREFIX:$TAG -t $DOCKER_PREFIX:latest -f nonroot.Dockerfile .
                '''

                sh '''
                    echo $DOCKER_TOKEN | docker login $DOCKER_SERVER -u $DOCKER_USER --password-stdin
                    docker push $DOCKER_PREFIX --all-tags
                '''
            }
        }
    }
}