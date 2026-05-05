import pandas as pd

def run_inference(model, device_id: str, flow: float, pressure: float) -> dict:
    df = pd.DataFrame({"flow": [flow], "pressure": [pressure]})
    prediction = model.predict(df)[0]
    score = model.decision_function(df)[0]
    return {
        "device_id": str(device_id),
        "is_anomaly": bool(prediction == -1),
        "score": round(float(score), 4),
        "prediction": int(prediction),
    }
