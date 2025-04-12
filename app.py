from flask import Flask, request, jsonify, render_template_string
import pickle
import numpy as np

# Load the model and scaler
with open("model.pkl", "rb") as f:
    saved_data = pickle.load(f)
    model = saved_data["model"]
    scaler = saved_data["scaler"]

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"})

@app.route("/", methods=["GET"])
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>House Price Prediction API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .container { background: #f5f5f5; padding: 20px; border-radius: 5px; }
            .input-group { margin: 10px 0; }
            label { display: block; margin-bottom: 5px; }
            input[type="number"] { padding: 5px; width: 200px; }
            button { padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer; }
            button:hover { background: #0056b3; }
            #result { margin-top: 20px; padding: 15px; border-radius: 5px; }
            .success { background: #d4edda; color: #155724; }
            .error { background: #f8d7da; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>House Price Prediction</h1>
            <p>Enter the house details to get a price prediction:</p>
            <div class="input-group">
                <label for="sqft">Square Footage:</label>
                <input type="number" id="sqft" placeholder="e.g., 2000" min="1000" max="5000">
            </div>
            <div class="input-group">
                <label for="bedrooms">Number of Bedrooms:</label>
                <input type="number" id="bedrooms" placeholder="e.g., 3" min="1" max="5">
            </div>
            <div class="input-group">
                <label for="bathrooms">Number of Bathrooms:</label>
                <input type="number" id="bathrooms" placeholder="e.g., 2" min="1" max="3" step="0.5">
            </div>
            <div class="input-group">
                <label for="year">Year Built:</label>
                <input type="number" id="year" placeholder="e.g., 2000" min="1960" max="2023">
            </div>
            <button onclick="makePrediction()">Predict Price</button>
            <div id="result"></div>
        </div>
        <script>
            async function makePrediction() {
                const sqft = parseFloat(document.getElementById('sqft').value);
                const bedrooms = parseFloat(document.getElementById('bedrooms').value);
                const bathrooms = parseFloat(document.getElementById('bathrooms').value);
                const year = parseFloat(document.getElementById('year').value);
                
                if (!sqft || !bedrooms || !bathrooms || !year) {
                    document.getElementById('result').innerHTML = 
                        `<p class="error">Please fill in all fields with valid numbers.</p>`;
                    return;
                }

                try {
                    const response = await fetch('/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            features: [sqft, bedrooms, bathrooms, year]
                        })
                    });
                    const data = await response.json();
                    const price = new Intl.NumberFormat('en-US', {
                        style: 'currency',
                        currency: 'USD',
                        maximumFractionDigits: 0
                    }).format(data.prediction[0]);
                    
                    document.getElementById('result').innerHTML = 
                        `<p class="success">Predicted House Price: ${price}</p>`;
                } catch (error) {
                    document.getElementById('result').innerHTML = 
                        `<p class="error">Error: ${error.message}</p>`;
                }
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    features = np.array(data["features"]).reshape(1, -1)
    features_scaled = scaler.transform(features)
    prediction = model.predict(features_scaled).tolist()
    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)