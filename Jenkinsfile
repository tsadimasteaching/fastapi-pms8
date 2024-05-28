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
        stage('deploy to k8s') {
            steps {
                sh '''
                    HEAD_COMMIT=$(git rev-parse --short HEAD)
                    TAG=$HEAD_COMMIT-$BUILD_ID
                    kubectl config use-context microk8s
                    if kubectl get deploy | grep 'fastapi-deployment'; then
                        kubectl set image -f k8s/fastapi/fastapi-deployment.yaml fastapi=$DOCKER_PREFIX:$TAG
                    else
                        kubectl patch -f k8s/fastapi/fastapi-deployment.yaml --type=json -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"$DOCKER_PREFIX:$TAG"}]'
                        kubectl apply -f k8s/fastapi/fastapi-deployment.yaml

                    fi
                  
                    RUNNING_TAG=$(kubectl get pods  -o=jsonpath="{.items[*].spec.containers[*].image}" -l component=fastapi | grep $TAG)
                    FOUND=$(echo $RUNNING_TAG | wc -l)
                    timeout --preserve-status 3m bash -c  -- "while [ $FOUND -eq  0 ] ; do echo \"waiting\"; sleep 1; done"
                '''

            }
        }
    }
}