from flask import Flask, request, jsonify,render_template
import util

app = Flask(__name__)

# Add CORS headers for all routes
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

''' @app.route("/home")
def home():
    return render_template('index.html')'''

@app.route('/get_location_names', methods=["GET"])
def get_location_names():
    locations = util.get_location_names()
    print("Locations:", locations)  # Check if this prints the list of locations
    response = jsonify({
        "locations": locations
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/predict_house_price", methods=["POST"])
def predict_house_price():
    if "total_sqft" not in request.form or "location" not in request.form \
        or "bhk" not in request.form or "bath" not in request.form:
        return jsonify({"error": "Missing form data. Send total_sqft, location, bhk, and bath."}), 400

    try:
        total_sqft = float(request.form["total_sqft"])
        location = request.form["location"]
        bhk = int(request.form["bhk"])
        bath = int(request.form["bath"])

        estimated_price = util.get_estimated_price(total_sqft, location, bhk, bath)
        response = {
            "estimated_price": estimated_price
        }
        return jsonify(response), 200

    except ValueError:
        return jsonify({"error": "Invalid data types. total_sqft must be a number, bhk and bath must be integers."}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("Starting python flask server for Real estate price prediction")
    app.run(debug=True)