

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
