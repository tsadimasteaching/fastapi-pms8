# Create namespace

```bash
kubectl create namespace keycloak
```

# create database
```bash
kubectl apply -f db-pvc.yaml
kubectl apply -f postgres-deployment.yaml
kubectl apply -f db-svc.yaml
```

# create keycloak
```bash
kubectl apply -f keycloak-deployment.yaml
kubectl apply -f keycloak-svc.yaml
kubectl apply -f keycloak-ingress.yaml
```

Note: in case you need https, you need to add A DNS record for your IP and Domain.
Also fix hostname in deployment.yaml and ingress.yaml
