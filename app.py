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
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>House Price Predictor | ML Service</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <style>
            :root {
                --primary-color: #2563eb;
                --primary-hover: #1d4ed8;
                --success-color: #059669;
                --error-color: #dc2626;
                --background-color: #f8fafc;
                --card-background: #ffffff;
                --text-primary: #1e293b;
                --text-secondary: #64748b;
                --border-color: #e2e8f0;
            }

            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }

            body {
                font-family: 'Inter', sans-serif;
                background-color: var(--background-color);
                color: var(--text-primary);
                line-height: 1.5;
                min-height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 2rem 1rem;
            }

            .container {
                max-width: 800px;
                width: 100%;
                background: var(--card-background);
                padding: 2rem;
                border-radius: 1rem;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            }

            .header {
                text-align: center;
                margin-bottom: 2rem;
            }

            .header h1 {
                font-size: 2rem;
                font-weight: 600;
                color: var(--text-primary);
                margin-bottom: 0.5rem;
            }

            .header p {
                color: var(--text-secondary);
                font-size: 1rem;
            }

            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1.5rem;
                margin-bottom: 2rem;
            }

            .input-group {
                display: flex;
                flex-direction: column;
            }

            .input-group label {
                font-size: 0.875rem;
                font-weight: 500;
                margin-bottom: 0.5rem;
                color: var(--text-primary);
            }

            .input-group input {
                padding: 0.75rem;
                border: 1px solid var(--border-color);
                border-radius: 0.5rem;
                font-size: 1rem;
                transition: border-color 0.2s, box-shadow 0.2s;
            }

            .input-group input:focus {
                outline: none;
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
            }

            .input-group input::placeholder {
                color: var(--text-secondary);
            }

            .button-container {
                text-align: center;
            }

            button {
                background-color: var(--primary-color);
                color: white;
                padding: 0.75rem 2rem;
                border: none;
                border-radius: 0.5rem;
                font-size: 1rem;
                font-weight: 500;
                cursor: pointer;
                transition: background-color 0.2s;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
            }

            button:hover {
                background-color: var(--primary-hover);
            }

            button:disabled {
                opacity: 0.7;
                cursor: not-allowed;
            }

            .spinner {
                width: 1.25rem;
                height: 1.25rem;
                border: 2px solid #ffffff;
                border-top: 2px solid transparent;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                display: none;
            }

            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            #result {
                margin-top: 2rem;
                padding: 1rem;
                border-radius: 0.5rem;
                text-align: center;
                font-weight: 500;
                display: none;
            }

            .success {
                background-color: #ecfdf5;
                color: var(--success-color);
                border: 1px solid #a7f3d0;
            }

            .error {
                background-color: #fef2f2;
                color: var(--error-color);
                border: 1px solid #fecaca;
            }

            @media (max-width: 640px) {
                .container {
                    padding: 1.5rem;
                }

                .header h1 {
                    font-size: 1.5rem;
                }

                .form-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>House Price Predictor</h1>
                <p>Enter the house details below to get an accurate price prediction</p>
            </div>
            <div class="form-grid">
                <div class="input-group">
                    <label for="sqft">Square Footage</label>
                    <input type="number" id="sqft" placeholder="e.g., 2000" min="1000" max="5000">
                </div>
                <div class="input-group">
                    <label for="bedrooms">Number of Bedrooms</label>
                    <input type="number" id="bedrooms" placeholder="e.g., 3" min="1" max="5">
                </div>
                <div class="input-group">
                    <label for="bathrooms">Number of Bathrooms</label>
                    <input type="number" id="bathrooms" placeholder="e.g., 2" min="1" max="3" step="0.5">
                </div>
                <div class="input-group">
                    <label for="year">Year Built</label>
                    <input type="number" id="year" placeholder="e.g., 2000" min="1960" max="2023">
                </div>
            </div>
            <div class="button-container">
                <button onclick="makePrediction()" id="predictButton">
                    <span class="spinner" id="spinner"></span>
                    <span id="buttonText">Predict Price</span>
                </button>
            </div>
            <div id="result"></div>
        </div>
        <script>
            const predictButton = document.getElementById('predictButton');
            const spinner = document.getElementById('spinner');
            const buttonText = document.getElementById('buttonText');
            const resultDiv = document.getElementById('result');

            async function makePrediction() {
                const sqft = parseFloat(document.getElementById('sqft').value);
                const bedrooms = parseFloat(document.getElementById('bedrooms').value);
                const bathrooms = parseFloat(document.getElementById('bathrooms').value);
                const year = parseFloat(document.getElementById('year').value);
                
                if (!sqft || !bedrooms || !bathrooms || !year) {
                    showResult('Please fill in all fields with valid numbers.', 'error');
                    return;
                }

                // Show loading state
                predictButton.disabled = true;
                spinner.style.display = 'inline-block';
                buttonText.textContent = 'Predicting...';
                resultDiv.style.display = 'none';

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

                    if (!response.ok) {
                        throw new Error('Prediction failed');
                    }

                    const data = await response.json();
                    const price = new Intl.NumberFormat('en-US', {
                        style: 'currency',
                        currency: 'USD',
                        maximumFractionDigits: 0
                    }).format(data.prediction[0]);
                    
                    showResult(`Predicted House Price: ${price}`, 'success');
                } catch (error) {
                    showResult('An error occurred while making the prediction. Please try again.', 'error');
                } finally {
                    // Reset button state
                    predictButton.disabled = false;
                    spinner.style.display = 'none';
                    buttonText.textContent = 'Predict Price';
                }
            }

            function showResult(message, type) {
                resultDiv.textContent = message;
                resultDiv.className = type;
                resultDiv.style.display = 'block';
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