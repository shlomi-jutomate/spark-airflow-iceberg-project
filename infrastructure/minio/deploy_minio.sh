#!/bin/bash

echo "Deploying MinIO environment (Object Storage)..."

# if not exists add Helm repo, then force update to get the latest charts
helm repo add minio https://charts.min.io/ --force-update
helm repo update

# deploy MinIO into our namespace
echo "Installing MinIo..."
helm upgrade --install my-minio minio/minio \
 -f infrastructure/minio/minio-values.yaml \
 --namespace data-platform \
 --create-namespace \
 --set mode=standalone \
 --set rootUser=admin \
 --set rootPassword=admin123 

echo "================================"
echo "MinIO installation is complete!"
echo ""
echo "Login credentials:"
echo "  User: admin"
echo "  Password: admin123"
echo ""
echo "Run: kubectl port-forward svc/my-minio 9000:9000 9001:9001 --namespace data-platform"
echo "Then open http://localhost:9001 in your browser."
echo "================================"