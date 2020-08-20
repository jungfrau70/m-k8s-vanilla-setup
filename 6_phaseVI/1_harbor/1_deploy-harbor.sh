#!/bin/bash
# Suggested values: advanced users of Kubernetes and Helm should feel
# free to use different values.
source ./.env

helm repo add harbor https://helm.goharbor.io
helm repo update

kubectl create ns $NAMESPACE
kubectl apply -f istio-harbor.yaml

cd harbor-helm
helm install . \
  --name $RELEASE \
  --namespace $NAMESPACE \
  --set harborAdminPassword="admin" \
  --values values.yaml