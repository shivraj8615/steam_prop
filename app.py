from flask import Flask, request, jsonify
import pandas as pd
#from flask_cors import CORS
# Load the CSV file
df = pd.read_csv("steam_properties.csv")

# Initialize Flask app
app = Flask(__name__)
#CORS(app)

@app.route("/get_properties", methods=["GET"])
def get_properties():
    try:
        # Get pressure from request parameters
        pressure = float(request.args.get("pressure"))
        # Validate input
        if pressure is None:
            return jsonify({"error": "Pressure parameter is required."}), 400
        try:
            pressure = float(pressure)
        except ValueError:
            return jsonify({"error": "Invalid pressure value. Must be a number."}), 400

        # Search for the corresponding row
        row = df[df["P"] == pressure]
        if row.empty:
            return jsonify({"error": "Pressure value not found."}), 404

        # Convert row to dictionary
        result = row.to_dict(orient="records")[0]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
