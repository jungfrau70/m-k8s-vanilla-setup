#!/bin/bash

source .env

kubectl apply --validate=false -f https://raw.githubusercontent.com/jetstack/cert-manager/v0.13.0/deploy/manifests/00-crds.yaml
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install $RELEASE \
  --namespace $NAMESPACE \
  --version v0.13.0 \
  jetstack/cert-manager
