from fastapi import FastAPI
import joblib
from pydantic import BaseModel

# Load the model
model = joblib.load("regression.joblib")

app = FastAPI()

class HouseInfo(BaseModel):
    size: float
    bedrooms: int
    garden: bool

@app.get("/")
def read_root():
    return {"message": "Welcome to the House Price Prediction API"}

@app.post("/predict")
def predict_price(info: HouseInfo):
    garden_value = 1 if info.garden else 0
    prediction = model.predict([[info.size, info.bedrooms, garden_value]])
    return {"predicted_price": prediction[0]}