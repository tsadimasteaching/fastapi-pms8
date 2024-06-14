

## Clone repo
```bash
git clone https://github.com/tsadimasteaching/fastapi-pms8.git
```
### Create virtual Environment, activate and install requirements
```bash
python3 -m venv favenv
source favenv/bin/activate
pip install -r requirements.txt
```
### Copy .env.example to .env
```bash
cp .env.example .env
```

### Start postgres as container
```bash
docker run --rm  --name pms8db \
-e POSTGRES_PASSWORD=pass123 \
-e POSTGRES_USER=dbuser \
-e POSTGRES_DB=pms8 \
-v pms8db:/var/lib/postgresql/data \
-p 5432:5432 -d postgres

```
### Run the app
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## docker compose

```bash
docker-compose up -d
```

# Container Registry (github packages)

## Github Packages
* create personal access token (settings --> Developer settings -- > Personal Access Tokens), select classic
* select write:packages
* save the token to a file
* to see packages, go to your github profile and select tab Packages
* tag an image
```bash
docker build -t ghcr.io/<GITHUB-USERNAME>/pms8-fastapi:latest -f fastapi.Dockerfile .
```
* login to docker registry
```bash
cat ~/github-image-repo.txt | docker login ghcr.io -u <GITHUB-USERNAME> --password-stdin
```
* push image
```bash
docker push ghcr.io/<GITHUB-USERNAME>/pms8-fastapi:latest
```

## create dockercongig secret
```bash
kubectl create secret docker-registry registry-credentials --from-file=.dockerconfigjson=k8s/.dockerconfig.json
```
