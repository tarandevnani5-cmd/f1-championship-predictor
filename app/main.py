from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import joblib
import numpy as np
import os

app = FastAPI(
    title="🏎️ F1 Championship Predictor API",
    description="Predict whether an F1 driver will win the World Championship based on their season stats.",
    version="1.0.0"
)

# Absolute paths — works no matter where uvicorn is run from
BASE_DIR      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH    = os.path.join(BASE_DIR, "models", "f1_champion_model.pkl")
SCALER_PATH   = os.path.join(BASE_DIR, "models", "scaler.pkl")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# ── Load model & scaler at startup ────────────────────────────────────────────
try:
    model  = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    print("✅ Model loaded successfully")
except FileNotFoundError:
    model  = None
    scaler = None
    print("⚠️  Model not found. Run src/train.py first.")


class DriverStats(BaseModel):
    points:        float
    wins:          float
    podiums:       float
    dnfs:          float
    races_entered: float

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "points":        454.0,
                "wins":          19.0,
                "podiums":       21.0,
                "dnfs":          1.0,
                "races_entered": 22.0
            }]
        }
    }


class PredictionResult(BaseModel):
    is_champion:         int
    championship_chance: str
    verdict:             str


@app.get("/")
def root():
    return FileResponse(os.path.join(TEMPLATES_DIR, "index.html"))


@app.get("/health")
def health():
    return {
        "status":       "ok",
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictionResult)
def predict(stats: DriverStats):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Run src/train.py first."
        )

    features = np.array([[
        stats.points,
        stats.wins,
        stats.podiums,
        stats.dnfs,
        stats.races_entered
    ]])

    features_scaled = scaler.transform(features)
    prediction      = model.predict(features_scaled)[0]
    probability     = model.predict_proba(features_scaled)[0][1]

    verdict = (
        "🏆 This driver is likely the WORLD CHAMPION!"
        if prediction == 1
        else "❌ This driver probably won't win the championship."
    )

    return PredictionResult(
        is_champion         = int(prediction),
        championship_chance = f"{probability * 100:.1f}%",
        verdict             = verdict
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)