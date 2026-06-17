#!/bin/bash

# 1. create namespace for Airflow
echo "Ensuring Airflow namespace exists..."
kubectl create namespace data-platform --dry-run=client -o yaml | kubectl apply -f - 

# 2. add Helm repo for Airflow
echo "Adding Helm repository for Airflow..."
helm repo add apache-airflow https://airflow.apache.org --force-update
helm repo update

# 3. Deploy Airflow using Helm & customize values as needed
echo "Deploying Airflow. Might take a few minutes..."
helm upgrade --install airflow apache-airflow/airflow \
    --namespace data-platform \
    -f infrastructure/airflow/airflow-values.yaml \
    --create-namespace

# 4. Wait for Airflow pods to be ready
echo "Waiting for Airflow pods to be ready..."
kubectl rollout status deployment airflow-api-server \
  --namespace data-platform \
  --timeout=500s

echo "=================================="
echo "Airflow deployment complete!"
echo ""
echo "Access the Airflow webserver at:"
echo "webserver: http://localhost:8080" 
echo "Default user (Airflow UI) Login credentials:
    username: admin
    password: admin"
echo ""
echo "=================================="