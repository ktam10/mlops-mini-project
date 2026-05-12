import mlflow
import mlflow.pyfunc
import whisper
import os

# ---------------------------------------------------
# AWS Configuration
# ---------------------------------------------------

os.environ["AWS_DEFAULT_REGION"] = "us-east-2"

# ---------------------------------------------------
# MLflow Configuration
# ---------------------------------------------------

MLFLOW_TRACKING_URI = os.environ.get(
    "MLFLOW_TRACKING_URI",
    "http://18.223.143.16:5000"
)

EXPERIMENT_NAME = "whisper-test-prod"
MODEL_SIZE = "base"
RUN_NAME = "whisper-base-registration2"
REGISTERED_NAME = "whisper-transcription"

# ---------------------------------------------------
# MLflow Setup
# ---------------------------------------------------

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)

# End any dangling active runs
mlflow.end_run()

print("Tracking URI:", mlflow.get_tracking_uri())

# ---------------------------------------------------
# Whisper Wrapper
# ---------------------------------------------------

# MLflow doesn't natively understand Whisper.
# We wrap it in a pyfunc class so MLflow knows
# how to save and load it.

class WhisperWrapper(mlflow.pyfunc.PythonModel):

    def load_context(self, context):
        """
        Called once when the model is loaded.
        Loads the Whisper model into memory.
        """
        self.model = whisper.load_model(MODEL_SIZE)

    def predict(self, context, model_input):
        """
        Called on every inference request.

        Expects:
            model_input = {
                "audio_path": "path/to/audio.mp3"
            }

        Returns:
            Transcribed text
        """

        audio_path = model_input["audio_path"]

        result = self.model.transcribe(audio_path)

        return result["text"]


# ---------------------------------------------------
# Register Model
# ---------------------------------------------------

with mlflow.start_run(run_name=RUN_NAME) as run:

    print("Artifact URI:", mlflow.get_artifact_uri())

    # Log metadata
    mlflow.log_param("model_size", MODEL_SIZE)
    mlflow.log_param("task", "transcription")

    # Log Whisper model
    mlflow.pyfunc.log_model(
        artifact_path="whisper-model",
        python_model=WhisperWrapper(),
        registered_model_name=REGISTERED_NAME,
    )

    run_id = run.info.run_id

    print(f"Run ID      : {run_id}")
    print(f"Experiment  : {EXPERIMENT_NAME}")
    print(f"Run name    : {RUN_NAME}")

    print("Model logged successfully.")
    print("Open MLflow UI to view artifacts.")
    
    
#python -m mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root s3://mlflow-artifacts-ktam10 --host 0.0.0.0 --port 5000