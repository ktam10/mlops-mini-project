from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
from deep_translator import GoogleTranslator
from prometheus_fastapi_instrumentator import Instrumentator
import whisper
import tempfile
import os
import mlflow

# Global model variable
model = None

# Load model ONCE at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Set MLflow tracking URI
    mlflow.set_tracking_uri(os.environ.get("MLFLOW_TRACKING_URI", "http://18.223.143.16:5000"))

    # Pull the Production model from MLflow instead of loading directly
    model_uri = "models:/whisper-transcription/Production"
    loaded_model = mlflow.pyfunc.load_model(model_uri)
    app.state.model = loaded_model

    # Translator stays the same
    app.state.translator = GoogleTranslator(source="en", target="es")

    print("Whisper loaded from MLflow Production registry")

    yield # --- app runs here ---

    # Shutdown (optional cleanup)
    print("Shutting down...")
app = FastAPI(lifespan=lifespan)
Instrumentator().instrument(app).expose(app)


@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("audio/"):
        raise HTTPException(status_code=400, detail="File must be an audio type")
    
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=" .mp3") as temp:
            contents = await file.read()
            temp.write(contents)
            temp_path = temp.name

        # Use preloaded model
        result = app.state.model.predict({"audio_path": temp_path})
        english_text = result

        # Step 2: Translate (deep_translator)
        spanish_text = app.state.translator.translate(english_text)


        # Cleanup
        os.remove(temp_path)

        return {
            "filename": file.filename,
            "english_text": english_text,
            "spanish_text": spanish_text
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))