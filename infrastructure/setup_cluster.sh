#!/bin/bash
# This script sets up a Kubernetes cluster using kind (Kubernetes in Docker).

minikube delete # Clean up any existing minikube cluster

# Create a new kind cluster, specify resources for the cluster
# [CHECK] what each argument does and adjust as necessary for your system
minikube start \
    --cpus=4 \
    --memory=8192 \
    --disk-size=50g \
    --driver=docker \
    --container-runtime=containerd \
    --kubernetes-version=stable

# enable minikube addons if needed (e.g., ingress, metrics-server)
# [CHECK] which addons you need for your cluster and enable them
minikube addons enable ingress
minikube addons enable default-storageclass
# minikube addons enable metrics-server
minikube addons enable dashboard

echo "Kubernetes cluster setup complete! You can now use 'kubectl' to interact with your cluster."
kubectl cluster-info
kubectl get nodes

