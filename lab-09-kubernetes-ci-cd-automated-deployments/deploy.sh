#!/bin/bash

# Set the Docker image name and tag
IMAGE_NAME=<your-dockerhub-username>/k8s-cicd-demo
IMAGE_TAG=1.1

# Update the Kubernetes deployment
kubectl set image deployment/k8s-cicd-demo k8s-cicd-demo=$IMAGE_NAME:$IMAGE_TAG

# Verify the deployment
kubectl rollout status deployment/k8s-cicd-demo
kubectl get pods -l app=k8s-cicd-demo