from fastapi import FastAPI, UploadFile, File, HTTPException
from contextlib import asynccontextmanager
from deep_translator import GoogleTranslator
import whisper
import tempfile
import os


# Global model variable
model = None

# Load model ONCE at startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    app.state.model = whisper.load_model("base")

    # Optional: store translator config
    app.state.translator = GoogleTranslator(source="en", target="es")

    print("Whisper + Deep Translator loaded")

    yield # --- app runs here ---

    # Shutdown (optional cleanup)
    print("Shutting down...")
app = FastAPI(lifespan=lifespan)


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
        result = app.state.model.transcribe(temp_path)
        english_text = result["text"]

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