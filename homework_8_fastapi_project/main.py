from fastapi import FastAPI
from pydantic import BaseModel
import onnxruntime as ort
import numpy as np

session = ort.InferenceSession("diabetes_model.onnx", providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name

app = FastAPI()

class DiabetesFeatures(BaseModel):
    Pregnancies: float
    Glucose: float
    BMI: float
    Age: float

@app.post("/predict")
def predict(features: DiabetesFeatures):
    input_data = np.array([[
        features.Pregnancies,
        features.Glucose,
        features.BMI,
        features.Age
    ]], dtype=np.float32)

    output = session.run(None, {input_name: input_data})
    prediction = int(output[0][0] > 0.5)
    return {"prediction": prediction}
