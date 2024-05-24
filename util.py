import os
import json
import pickle
import numpy as np

__locations = None
__data_columns = None
__model = None

def get_location_names():
    return load_saved_artifacts()

def load_saved_artifacts():
    global __data_columns
    global __locations
    global __model

    # Get the directory path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct the absolute file paths
    model_dir = os.path.join(script_dir, "artifacts")
    columns_file = os.path.join(model_dir, "columns.json")

    print("Model Directory Path:", model_dir)  # Print the model directory path
    print("Columns File Path:", columns_file)  # Print the columns file path

    # Check if the model file exists
    model_files = [f for f in os.listdir(model_dir) if f.endswith(".pickle")]
    if model_files:
        # Take the first model file found, assuming there's only one
        model_file = os.path.join(model_dir, model_files[0])
        try:
            with open(model_file, 'rb') as f:
                __model = pickle.load(f)
        except Exception as e:
            print("Error loading model:", e)
            return None
    else:
        print("Model file not found in directory:", model_dir)
        return None

    try:
        with open(columns_file, 'r') as f:
            data = json.load(f)
            if 'data_columns' in data:
                __data_columns = data['data_columns']
                __locations = __data_columns[3:]  # Excluding the first 3 elements
                return __locations
            else:
                print("Key 'data_columns' not found in columns file:", columns_file)
                return None
    except FileNotFoundError:
        print("Columns file not found:", columns_file)
        return None
    except Exception as e:
        print("Error loading columns:", e)
        return None

def get_estimated_price(total_sqft, location, bhk, bath):
    if __model is None:
        print("Model is not loaded. Cannot make predictions.")
        return None

    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        print("Location '{}' not found in saved data columns.".format(location))
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)

if __name__ == "__main__":
    locations = get_location_names()
    if locations is not None:
        print("Loaded locations:", locations)
        # Call the get_estimated_price function with the provided values
        estimated_price = get_estimated_price(1000, "1st phase jp Nagar", 3, 3)
        print("Estimated Price:", estimated_price)
    else:
        print("Failed to load locations. Check previous error messages.")
