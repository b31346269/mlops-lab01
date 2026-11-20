import json
import os
from pathlib import Path

import joblib
import mlflow
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split


def main():
    data = load_iris()
    x_train, x_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=0.25, random_state=42, stratify=data.target
    )
    params = {"n_estimators": 50, "max_depth": 4, "random_state": 42}
    model = RandomForestClassifier(**params)
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000"))
    experiment = mlflow.set_experiment("lab01-iris")
    with mlflow.start_run(run_name="iris-random-forest") as run:
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        metrics = {
            "accuracy": accuracy_score(y_test, predictions),
            "f1_macro": f1_score(y_test, predictions, average="macro"),
        }
        mlflow.log_params({**params, "dataset": "iris", "test_size": 0.25})
        mlflow.log_metrics(metrics)
        joblib.dump(model, "model.joblib")
        mlflow.log_artifact("model.joblib", artifact_path="model")
        result = {"experiment_id": experiment.experiment_id, "run_id": run.info.run_id, **metrics}
    Path("evidence").mkdir(exist_ok=True)
    Path("evidence/run.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
