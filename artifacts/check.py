import pickle
import os
model_file = "C:/Users/arora/Desktop/Ansh programs/Real_Estate_Price_Prediction_Project/server/artifacts/Bangalore_house_prices_model.pickle"

try:
    with open(model_file, 'rb') as f:
        model = pickle.load(f)
    print("Model loaded successfully!")
except FileNotFoundError:
    print("Model file not found:", model_file)
except Exception as e:
    print("Error loading model:", e)

print("Current Working Directory:", os.getcwd())
