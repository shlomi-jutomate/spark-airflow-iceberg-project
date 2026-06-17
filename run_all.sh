#!/bin/bash

# Coloring
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE} Initiate deployment...${NC}\n"

echo -e "${YELLOW} 1. Create Infrastructure with Minikube...${NC}\n"
./infrastructure/setup_cluster.sh
echo -e "${GREEN} Infrastructure is ready!${NC}\n"

echo -e "${YELLOW} 2. Deploy MinIO as object storage...${NC}\n"
./infrastructure/minio/deploy_minio.sh
echo -e "${GREEN} MinIO installed successfully!${NC}\n"

echo -e "${YELLOW} 3. Deploy Airflow...${NC}\n"
./infrastructure/airflow/deploy_airflow.sh
echo -e "${GREEN} Airflow installed successfully!${NC}\n"

echo -e "${BLUE}======================================================${NC}"
echo -e "${GREEN}Everything is ready!${NC}"
echo -e "${BLUE}======================================================${NC}"
echo -e "Now open *two new terminal windows* and run the following commands:\n"

echo -e "${YELLOW}1. MinIO:${NC}"
echo -e "   run: ${GREEN}kubectl port-forward svc/my-minio 9000:9000 --namespace data-platform${NC}"
echo -e "   run: ${GREEN}kubectl port-forward svc/my-minio-console 9001:9001 --namespace data-platform${NC}"
echo -e "   Username: admin | Password: admin123\n"

echo -e "${YELLOW}2. Aiflow:${NC}"
echo -e "   run: ${GREEN}kubectl port-forward svc/airflow-api-server 8080:8080 --namespace data-platform${NC}"
echo -e "   Access from your browser: http://localhost:8080"
echo -e "   Username: admin | Password: admin"
echo -e "${BLUE}======================================================${NC}"