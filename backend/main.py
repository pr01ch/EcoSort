from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from PIL import Image
import numpy as np
import tensorflow as tf
from dotenv import load_dotenv
import google.generativeai as genai
import os
import traceback

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY not found in .env file!")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")

app = FastAPI(title="EcoSort Backend", version="2.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    model = tf.keras.models.load_model("ai-model/e_waste_model.keras")
    print("TensorFlow model loaded successfully.")
except Exception as e:
    print("Failed to load TensorFlow model:", str(e))
    model = None

CLASS_NAMES = [
    "Battery", "Keyboard", "Microwave", "Mobile", "Mouse",
    "PCB", "Player", "Printer", "Television", "Washing Machine",
]

def preprocess_image(image: Image.Image):
    """Resize and normalize the image for model input."""
    image = image.resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# Prediction Endpoint (using your ML model)
# Replace the predict and chat endpoints in main.py with the following

from fastapi import HTTPException

@app.post("/predict/")
async def predict(
    file: UploadFile = File(...),           
    weight: float = Form(0.0),             
    location: str = Form("")               
):
    if model is None:
        return JSONResponse(content={"error": "Model not loaded."}, status_code=500)

    try:
        # Ensure numeric file read and convert to RGB
        image = Image.open(file.file).convert("RGB")
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        predicted_class_index = int(np.argmax(prediction[0]))
        confidence = float(np.max(prediction[0])) * 100.0
        waste_type = CLASS_NAMES[predicted_class_index]

        return JSONResponse(
            content={
                "waste_type": waste_type,
                "confidence": round(confidence, 2),
                "weight": weight,
                "location": location,
            }
        )
    except Exception as e:
        # Always return JSON on errors
        traceback.print_exc()
        return JSONResponse(
            content={"error": f"Prediction failed: {str(e)}"},
            status_code=500
        )

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = """
You are EcoSort — an expert in recycling, e-waste management, and sustainability 🌱
Keep answers:
- Friendly, concise, and easy to understand.
- Encourage safe disposal of electronics.
- Use emojis occasionally.
If the user asks unrelated questions, gently bring the topic back to e-waste or eco-living.
"""

@app.post("/chat/")
async def chat(req: ChatRequest):
    try:
        user_input = req.message.strip()
        if not user_input:
            return JSONResponse(content={"error": "Empty message."}, status_code=400)

        prompt = f"{SYSTEM_PROMPT}\nUser: {user_input}\nAssistant:"

        # Try to call Gemini and handle model-not-found gracefully
        try:
            response = gemini_model.generate_content(prompt)
            # Some SDKs return an object with .text; adapt defensively:
            reply = ""
            if response is None:
                reply = "Sorry, I couldn't generate a reply."
            else:
                # try multiple access patterns
                if hasattr(response, "text"):
                    reply = response.text
                elif isinstance(response, dict):
                    reply = response.get("text") or response.get("content") or str(response)
                else:
                    reply = str(response)

                reply = reply.strip() if reply else "Sorry, I couldn't generate a reply 😅"

            return JSONResponse(content={"reply": reply})
        except Exception as gerr:
            # If Gemini model name/method is unsupported you'll often get a 404 or SDK error.
            tb = str(gerr)
            traceback.print_exc()
            if "404" in tb or "not found" in tb.lower():
                return JSONResponse(
                    content={"error": "Gemini model not found or not supported by your SDK. Please check your model name or update the google.generativeai package."},
                    status_code=502
                )
            return JSONResponse(content={"error": f"Gemini API error: {str(gerr)}"}, status_code=502)

    except Exception as e:
        traceback.print_exc()
        return JSONResponse(content={"error": f"Server error: {str(e)}"}, status_code=500)

# Health Check 
@app.get("/")
def root():
    return {"message": "EcoSort Gemini backend running successfully!"}
