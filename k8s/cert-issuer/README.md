## install cert-manager

```bash
helm repo add jetstack https://charts.jetstack.io --force-update
helm install \\n  cert-manager jetstack/cert-manager \\n  --namespace cert-manager \\n  --create-namespace \\n  --version v1.14.5 \\n  --set installCRDs=true
```

## create cert-issuer

replace email in k8s/cert-issuer/cert-issuer.yaml file and apply
```bash
kubectl apply -f k8s/cert-issuer/cert-issuer.yaml
```

## create ingress

edit file k8s/fastapi/fastapi-ingress-ssl.yaml, replace host
```bash
kubectl apply -f k8s/fastapi/fastapi-ingress-ssl.yaml
```