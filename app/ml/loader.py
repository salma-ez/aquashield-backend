import joblib
from pathlib import Path

MODEL_PATH = Path(__file__).parent / "leak_detector.pkl"

def load_model():
    model = joblib.load(MODEL_PATH)
    print(f"[ML] Loaded {MODEL_PATH.name} — "
          f"{len(model.estimators_)} trees, "
          f"features: {list(model.feature_names_in_)}")
    return model
