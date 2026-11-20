# Lab 1 實測結果

2026-11-20 在 GitHub Actions 的 kind Kubernetes 叢集執行，原始程式版本為 `5a4e7b5`。[成功的執行紀錄](https://github.com/b31346269/mlops-lab01/actions/runs/44740703476)

- [MLflow Run 截圖](mlflow-run.png)顯示 Iris Random Forest 訓練已完成，測試集 Accuracy 92.11%，Macro F1 0.9230。[原始訓練輸出](run.json)
- [HPA Scaling 截圖](hpa-scaling.png)為瀏覽器呈現的真實 Kubernetes 命令輸出。就緒副本從 1 增加到 4，負載測試完成 56,810 次成功推論請求。[原始 kubectl 輸出](hpa.txt)
