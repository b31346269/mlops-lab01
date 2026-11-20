# MLOps Lab 1

使用 scikit-learn 訓練 Iris 分類模型，透過 MLflow 追蹤參數、測試集指標與模型檔。將同一份訓練產物打包成容器，以 Kubernetes Deployment、Service 和 HPA 提供推論與 CPU 自動擴展。

## 重現實驗

GitHub Actions 的 Lab 1 execution 工作流程使用 Ubuntu runner 建立臨時 kind 叢集。其產物包含 MLflow UI 截圖、由真實 kubectl 執行輸出產生的 HPA 截圖，以及原始執行結果。

本機需準備 Python 3.12、Docker、kind、kubectl。依照 [工作流程](.github/workflows/lab01.yml) 的順序執行。第一階段先啟動 MLflow Tracking Server，再於另一個終端執行訓練。

```bash
python -m pip install -r requirements.txt
mlflow server --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

```bash
python train.py
```

瀏覽 http://127.0.0.1:5000 並選取 lab01-iris 實驗。模型檔同時保存在本地 model.joblib 和對應的 MLflow run。部署階段將模型包入容器。kind 的 Metrics Server kubelet 憑證設定僅供這個本機測試叢集使用。

## 驗收方式

- MLflow run 應顯示完成、模型參數、accuracy 和 macro-F1。
- Kubernetes Job 送出批次推論請求，並檢查回傳筆數。
- 驗證腳本先確認 HPA 有 CPU 指標與一個就緒 Pod，再記錄負載期間的 HPA 狀態。擴展後至少要有兩個就緒副本，且負載測試 Job 必須成功。
