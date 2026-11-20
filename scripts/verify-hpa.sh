#!/usr/bin/env bash
set -euo pipefail
mkdir -p evidence
exec > >(tee evidence/hpa.txt) 2>&1

kubectl -n mlops rollout status deployment/iris --timeout=120s
for ((i=0; i<30; i++)); do
    target=$(kubectl -n mlops get hpa iris -o jsonpath='{.status.currentMetrics[0].resource.current.averageUtilization}')
    [[ -n "$target" ]] && break
    sleep 5
done
[[ -n "$target" ]] || { echo "HPA CPU metrics unavailable"; exit 1; }

echo "Before load"
kubectl -n mlops get hpa iris
baseline=$(kubectl -n mlops get deployment iris -o jsonpath='{.status.readyReplicas}')
[[ "$baseline" == 1 ]]
kubectl -n mlops apply -f k8s/load.yaml

scaled=false
for ((i=0; i<40; i++)); do
    date -u +"%H:%M:%S UTC"
    kubectl -n mlops get hpa iris
    replicas=$(kubectl -n mlops get deployment iris -o jsonpath='{.status.readyReplicas}')
    if (( ${replicas:-0} > baseline )); then
        scaled=true
        echo "Ready replicas: $baseline -> $replicas"
        kubectl -n mlops get pods -l app=iris
        break
    fi
    sleep 5
done
kubectl -n mlops wait --for=condition=complete job/iris-load --timeout=240s
kubectl -n mlops logs job/iris-load
[[ "$scaled" == true ]]
