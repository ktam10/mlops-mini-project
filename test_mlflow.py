import mlflow

mlflow.set_tracking_uri("http://13.59.120.105:5000")

mlflow.set_experiment("whisper-test")

with mlflow.start_run():

    mlflow.log_param("model", "whisper-base")

    mlflow.log_metric("accuracy", 0.95)

    print("MLflow logging successful")