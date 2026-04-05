# 🏎️ F1 Championship Predictor — MLOps Project

An end-to-end MLOps pipeline that predicts whether an F1 driver will win the **Formula 1 World Championship** based on their season statistics (points, wins, podiums, DNFs).

---

## 🧠 Problem Statement
Given a driver's mid-season performance stats, predict if they will become World Champion that year. Binary classification problem trained on 70+ years of F1 data (1950–2024).

---

## 🗂️ Project Structure
```
f1-championship-predictor/
├── data/                  # F1 CSV datasets (tracked via DVC)
├── src/
│   ├── preprocess.py      # Data loading & feature engineering
│   └── train.py           # Model training with MLflow tracking
├── app/
│   └── main.py            # FastAPI inference API
├── models/                # Saved model & scaler (tracked via DVC)
├── .github/workflows/     # GitHub Actions CI pipeline
├── conda.yml              # Conda environment
├── requirements.txt       # Python dependencies
└── README.md
```

---

## ⚙️ Setup

### 1. Clone & create environment

**Option A: Using Conda (Recommended if available)**
1.  Check if conda is in your PATH. If `conda --version` fails, use the full path or **Anaconda Prompt**.
2.  `conda env create -f conda.yml`
3.  `conda activate f1-mlops`

**Option B: Using venv & pip (Alternative)**
1.  `python -m venv venv`
2.  `venv\Scripts\activate`
3.  `pip install -r requirements.txt`

### 2. Download Dataset
Download the Formula 1 dataset from Kaggle: [F1 Dataset](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)

Place these files in the `/data` folder:
- `driver_standings.csv`
- `results.csv`
- `races.csv`
- `drivers.csv`

*(Note: Use `python generate_mock_data.py` to create small mock files for testing.)*

### 3. Initialize DVC (Optional)
```bash
dvc init
dvc add data/
git add data.dvc .gitignore
git commit -m "Track data with DVC"
```

---

## 🏋️ Train the Model

```bash
python src/train.py
```

This will:
- Preprocess the F1 dataset
- Train 3 models: RandomForest, GradientBoosting, LogisticRegression
- Log all metrics & params to **MLflow**
- Save the best model to `models/`

### View MLflow UI
```bash
mlflow ui
# Open http://localhost:5000
```

---

## 🚀 Run the API

```bash
uvicorn app.main:app --reload
# Open http://localhost:8000/docs
```

### Example prediction:
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"points": 400, "wins": 12, "podiums": 17, "dnfs": 1, "races_entered": 22}'
```

**Response:**
```json
{
  "is_champion": 1,
  "championship_chance": "94.2%",
  "verdict": "🏆 This driver is likely the WORLD CHAMPION!"
}
```

---

## 🔁 CI/CD Pipeline (GitHub Actions)

On every push to `main`, the pipeline:
1. Sets up Python environment
2. Installs all dependencies
3. Runs linting (flake8)
4. Validates app imports

See `.github/workflows/train.yml`

---

## 📊 Features Used

| Feature | Description |
|---|---|
| `points` | Total championship points |
| `wins` | Number of race wins |
| `podiums` | Top-3 finishes |
| `dnfs` | Did Not Finish count |
| `races_entered` | Total races in the season |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data Versioning | DVC |
| Experiment Tracking | MLflow |
| ML Model | Scikit-learn |
| API | FastAPI + Uvicorn |
| CI/CD | GitHub Actions |
| Environment | Conda |

---

## 📈 Results

| Model | Accuracy | F1 Score |
|---|---|---|
| Random Forest | ~96% | ~0.89 |
| Gradient Boosting | ~95% | ~0.87 |
| Logistic Regression | ~93% | ~0.82 |

---

Built as part of MLOps coursework — AI & Data Science Engineering.
