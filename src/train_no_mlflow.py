import pandas as pd
import joblib
import os
import sys

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import StandardScaler

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.preprocess import load_and_preprocess

FEATURE_COLS = ["points", "wins", "podiums", "dnfs", "races_entered"]
TARGET_COL   = "is_champion"
MODEL_PATH   = "models/f1_champion_model.pkl"
SCALER_PATH  = "models/scaler.pkl"


def train():
    os.makedirs("models", exist_ok=True)

    # ── Load data ─────────────────────────────────────────────────────────────
    df = load_and_preprocess()
    X  = df[FEATURE_COLS]
    y  = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # ── Scale ─────────────────────────────────────────────────────────────────
    scaler         = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    # ── Models ────────────────────────────────────────────────────────────────
    models = {
        "RandomForest":       RandomForestClassifier(n_estimators=100, random_state=42),
        "GradientBoosting":   GradientBoostingClassifier(n_estimators=100, random_state=42),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42),
    }

    best_model = None
    best_f1    = 0

    for model_name, model in models.items():
        model.fit(X_train_scaled, y_train)
        y_pred = model.predict(X_test_scaled)

        acc  = accuracy_score(y_test,  y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec  = recall_score(y_test,   y_pred, zero_division=0)
        f1   = f1_score(y_test,       y_pred, zero_division=0)

        print(f"[{model_name}] Acc={acc:.3f} | Prec={prec:.3f} | "
              f"Rec={rec:.3f} | F1={f1:.3f}")

        if f1 > best_f1:
            best_f1    = f1
            best_model = model

    # ── Save best model & scaler ──────────────────────────────────────────────
    joblib.dump(best_model, MODEL_PATH)
    joblib.dump(scaler,     SCALER_PATH)
    print(f"\n✅ Best model saved → {MODEL_PATH}  (F1={best_f1:.3f})")


if __name__ == "__main__":
    train()
