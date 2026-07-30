from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
import os
import logging
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained model
model_path = os.path.join('models', 'random_forest.joblib')
scaler_path = os.path.join('models', 'scaler.joblib')

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    logger.info("Model and scaler loaded successfully")
except FileNotFoundError as e:
    logger.warning(f"Model files not found: {e}. Running in demo mode.")
    model = None
    scaler = None

# Load demo scenarios
demo_scenarios_path = 'demo_scenarios/demo_scenarios.csv'
demo_scenarios = None
try:
    if os.path.exists(demo_scenarios_path):
        demo_scenarios = pd.read_csv(demo_scenarios_path)
        logger.info(f"Loaded {len(demo_scenarios)} demo scenarios")
except Exception as e:
    logger.warning(f"Could not load demo scenarios: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        data = request.form
        logger.info(f"Received prediction request: {dict(data)}")
        
        # Validate required fields
        required_fields = ['booking_date', 'flight_date', 'fare_class', 'route', 'customer_type', 'booking_lead_time']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                })
        
        # Convert dates to datetime objects
        try:
            booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d')
            flight_date = datetime.strptime(data['flight_date'], '%Y-%m-%d')
        except ValueError as e:
            return jsonify({
                'success': False,
                'error': f'Invalid date format: {str(e)}'
            })
        
        # Validate dates
        if flight_date <= booking_date:
            return jsonify({
                'success': False,
                'error': 'Flight date must be after booking date'
            })
        
        # Calculate days to flight
        days_to_flight = (flight_date - booking_date).days
        
        # Validate lead time
        lead_time = int(data['booking_lead_time'])
        if lead_time < 1 or lead_time > 365:
            return jsonify({
                'success': False,
                'error': 'Lead time must be between 1 and 365 days'
            })
        
        # Create feature dictionary
        features = {
            'fare_class': data['fare_class'],
            'route': data['route'],
            'customer_type': data['customer_type'],
            'days_to_flight': days_to_flight,
            'booking_lead_time': lead_time
        }
        
        if model is None:
            # Demo mode - return a mock prediction based on some logic
            mock_probability = generate_mock_prediction(features)
            return jsonify({
                'success': True,
                'prediction': mock_probability,
                'input_data': features,
                'demo_mode': True,
                'confidence': 0.75
            })
        
        # Prepare features for model prediction
        # Note: You may need to adjust this based on your actual model's expected features
        try:
            # Convert to DataFrame and apply any necessary preprocessing
            input_df = pd.DataFrame([features])
            
            # Apply scaling if scaler is available
            if scaler is not None:
                # Select only numeric features for scaling
                numeric_features = ['days_to_flight', 'booking_lead_time']
                input_df[numeric_features] = scaler.transform(input_df[numeric_features])
            
            # Make prediction
            prediction = model.predict_proba(input_df)[0]
            no_show_probability = prediction[1]  # Probability of no-show
            
            # Calculate confidence based on prediction certainty
            confidence = abs(prediction[0] - prediction[1]) * 2
            
            return jsonify({
                'success': True,
                'prediction': float(no_show_probability),
                'input_data': features,
                'demo_mode': False,
                'confidence': float(confidence)
            })
            
        except Exception as model_error:
            logger.error(f"Model prediction error: {str(model_error)}")
            # Fallback to demo mode if model fails
            mock_probability = generate_mock_prediction(features)
            return jsonify({
                'success': True,
                'prediction': mock_probability,
                'input_data': features,
                'demo_mode': True,
                'confidence': 0.5,
                'warning': 'Model error, using fallback prediction'
            })
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'An unexpected error occurred: {str(e)}'
        })

def generate_mock_prediction(features):
    """Generate a mock prediction based on simple heuristics"""
    base_probability = 0.2  # Base 20% no-show rate
    
    # Adjust based on fare class
    if features['fare_class'] == 'First':
        base_probability *= 0.5  # First class passengers less likely to no-show
    elif features['fare_class'] == 'Business':
        base_probability *= 0.7
    # Economy stays at base rate
    
    # Adjust based on customer type
    if features['customer_type'] == 'Business':
        base_probability *= 0.6  # Business travelers more reliable
    
    # Adjust based on lead time
    lead_time = features['booking_lead_time']
    if lead_time > 30:
        base_probability *= 1.3  # Longer lead time = higher no-show risk
    elif lead_time < 7:
        base_probability *= 0.8  # Short lead time = lower no-show risk
    
    # Add some randomness
    import random
    base_probability *= random.uniform(0.8, 1.2)
    
    return min(max(base_probability, 0.05), 0.8)  # Clamp between 5% and 80%

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None
    })

@app.route('/stats')
def get_stats():
    """Get some basic statistics about the system"""
    return jsonify({
        'total_predictions': 0,  # You could track this in a database
        'model_accuracy': 0.85,  # Example accuracy
        'last_updated': datetime.now().isoformat()
    })

@app.route('/demo-scenarios')
def get_demo_scenarios():
    """Get available demo scenarios"""
    if demo_scenarios is not None:
        scenarios = demo_scenarios.to_dict('records')
        return jsonify({
            'success': True,
            'scenarios': scenarios
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Demo scenarios not available'
        })

@app.route('/demo-scenario/<int:scenario_id>')
def get_demo_scenario(scenario_id):
    """Get a specific demo scenario by ID"""
    if demo_scenarios is not None and 0 <= scenario_id < len(demo_scenarios):
        scenario = demo_scenarios.iloc[scenario_id].to_dict()
        return jsonify({
            'success': True,
            'scenario': scenario
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Scenario not found'
        })

@app.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Handle batch predictions for multiple scenarios"""
    try:
        data = request.get_json()
        scenarios = data.get('scenarios', [])
        
        if not scenarios:
            return jsonify({
                'success': False,
                'error': 'No scenarios provided'
            })
        
        results = []
        for scenario in scenarios:
            # Create a mock prediction for each scenario
            mock_prob = generate_mock_prediction(scenario)
            results.append({
                'scenario': scenario,
                'prediction': mock_prob,
                'risk_level': get_risk_level(mock_prob)
            })
        
        return jsonify({
            'success': True,
            'results': results,
            'demo_mode': True
        })
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Batch prediction failed: {str(e)}'
        })

def get_risk_level(probability):
    """Determine risk level based on probability"""
    if probability < 0.2:
        return 'Low'
    elif probability < 0.5:
        return 'Medium'
    else:
        return 'High'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True) 