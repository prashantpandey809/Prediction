"""
Flask API Module - ArogyaPredict
REST API for patient inflow prediction and medicine stock recommendations.

Endpoints:
  /predict (POST) - Predict patient count based on environmental data
  /recommend (POST) - Get medicine stock recommendations
  /health (GET) - API health check
"""

from flask import Flask, request, jsonify, render_template, send_from_directory
import pickle
import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime, timedelta
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    MODEL_PATH,
    ENCODER_PATH,
    MEDICINE_DATABASE,
    LOW_STOCK_THRESHOLD,
    CRITICAL_STOCK_THRESHOLD,
    STOCK_INCREASE_PERCENT,
    STOCK_DECREASE_PERCENT,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
    static_url_path='/static'
)
app.config["JSON_SORT_KEYS"] = False

# Global variables to store model and encoders
model = None
encoders = None


def load_model_and_encoders():
    """Load trained model and encoders from disk."""
    global model, encoders
    
    try:
        # Load model
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                model = pickle.load(f)
            logger.info(f"✓ Model loaded from {MODEL_PATH}")
        else:
            logger.error(f"Model file not found: {MODEL_PATH}")
            return False
        
        # Load encoders
        if os.path.exists(ENCODER_PATH):
            with open(ENCODER_PATH, "rb") as f:
                encoders = pickle.load(f)
            logger.info(f"✓ Encoders loaded from {ENCODER_PATH}")
        else:
            logger.warning(f"Encoders file not found: {ENCODER_PATH}")
            encoders = {}
        
        return True
        
    except Exception as e:
        logger.error(f"Error loading model/encoders: {e}")
        return False


def validate_prediction_input(data):
    """
    Validate input data for prediction endpoint.
    
    Args:
        data (dict): Input data
        
    Returns:
        tuple: (is_valid, error_message, cleaned_data)
    """
    required_fields = ["temperature", "humidity", "aqi"]
    optional_fields = {
        "disease_type": "Heart Disease",
        "weather_condition": "Haze",
        "is_holiday": 0,
        "holiday_name": "None",
        "expected_multiplier": 1.0,
        "days_after_holiday": 0,
    }
    
    # Check required fields
    for field in required_fields:
        if field not in data:
            return False, f"Missing required field: '{field}'", None
    
    # Validate numeric fields
    try:
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        aqi = float(data["aqi"])
        
        # Validate ranges
        if not (0 <= humidity <= 100):
            return False, "Humidity must be between 0 and 100", None
        if aqi < 0:
            return False, "AQI must be non-negative", None
        if temperature < -50 or temperature > 60:
            return False, "Temperature must be between -50 and 60°C", None
            
    except ValueError:
        return False, "Temperature, humidity, and AQI must be numeric values", None
    
    # Get optional fields with defaults
    disease_type = data.get("disease_type", optional_fields["disease_type"])
    weather_condition = data.get("weather_condition", optional_fields["weather_condition"])
    is_holiday = int(data.get("is_holiday", optional_fields["is_holiday"]))
    holiday_name = data.get("holiday_name", optional_fields["holiday_name"])
    expected_multiplier = float(data.get("expected_multiplier", optional_fields["expected_multiplier"]))
    days_after_holiday = int(data.get("days_after_holiday", optional_fields["days_after_holiday"]))
    
    cleaned_data = {
        "temperature": temperature,
        "humidity": humidity,
        "aqi": aqi,
        "disease_type": disease_type,
        "weather_condition": weather_condition,
        "is_holiday": is_holiday,
        "holiday_name": holiday_name,
        "expected_multiplier": expected_multiplier,
        "days_after_holiday": days_after_holiday,
    }
    
    return True, None, cleaned_data


def prepare_features(data):
    """
    Prepare features for model prediction with robust encoding.
    
    Args:
        data (dict): Cleaned input data
        
    Returns:
        pd.DataFrame: Features for model
    """
    # Known disease types for fallback encoding
    DISEASE_TYPE_CLASSES = [
        "Heart Disease", "Respiratory Infection", "Gastroenteritis",
        "Pediatric Illness", "Malaria", "Diabetes", "Hypertension",
        "Kidney Disease"
    ]
    
    # Known weather conditions for fallback encoding
    WEATHER_CONDITIONS = [
        "Haze", "Clear", "Smoke", "Rain", "Cloudy", "Sunny", "Rainy"
    ]
    
    # Known holiday names for fallback encoding
    HOLIDAY_NAMES = [
        "New Year's Day", "Lohri", "Makar Sankranti", "Pongal", "Holi",
        "Diwali", "Christmas", "None"
    ]
    
    # Create features dict with all required columns
    features = {
        "expected_multiplier": data.get("expected_multiplier", 1.0),
        "temperature": data["temperature"],
        "humidity": data["humidity"],
        "aqi": data["aqi"],
        "is_holiday": int(data.get("is_holiday", 0)),
        "days_after_holiday": int(data.get("days_after_holiday", 0)),
    }
    
    # Encode disease_type
    try:
        if "disease_type" in encoders:
            disease_encoded = encoders["disease_type"].transform([data["disease_type"]])[0]
            features["disease_type_encoded"] = disease_encoded
        else:
            # Fallback: use class index from known list
            disease_idx = DISEASE_TYPE_CLASSES.index(data["disease_type"]) % 5
            features["disease_type_encoded"] = disease_idx
    except (ValueError, KeyError, AttributeError):
        # Unknown disease type - use default
        logger.warning(f"Unknown disease_type: {data.get('disease_type')} - using default")
        features["disease_type_encoded"] = 0
    
    # Encode weather_condition
    try:
        weather_val = data.get("weather_condition", "Haze")
        if "weather_condition" in encoders:
            weather_encoded = encoders["weather_condition"].transform([weather_val])[0]
            features["weather_condition_encoded"] = weather_encoded
        else:
            # Fallback: hash-based encoding for unknown weather
            weather_idx = WEATHER_CONDITIONS.index(weather_val) % 7
            features["weather_condition_encoded"] = weather_idx
    except (ValueError, KeyError, AttributeError):
        logger.warning(f"Unknown weather_condition: {data.get('weather_condition')} - using default")
        features["weather_condition_encoded"] = 0
    
    # Encode holiday_name
    try:
        holiday_val = data.get("holiday_name", "None")
        if "holiday_name" in encoders:
            holiday_encoded = encoders["holiday_name"].transform([holiday_val])[0]
            features["holiday_name_encoded"] = holiday_encoded
        else:
            # Fallback: use class index from known list
            holiday_idx = HOLIDAY_NAMES.index(holiday_val) % 5
            features["holiday_name_encoded"] = holiday_idx
    except (ValueError, KeyError, AttributeError):
        logger.warning(f"Unknown holiday_name: {data.get('holiday_name')} - using default")
        features["holiday_name_encoded"] = 4  # Default to "None" equivalent
    
    # Create DataFrame with features in correct order (matching training order)
    feature_order = [
        'expected_multiplier', 'temperature', 'humidity', 'aqi', 
        'is_holiday', 'days_after_holiday', 'disease_type_encoded',
        'weather_condition_encoded', 'holiday_name_encoded'
    ]
    
    features_df = pd.DataFrame([features])
    features_df = features_df[feature_order]  # Reorder columns to match training
    
    logger.info(f"✓ Features prepared: disease={data['disease_type']}, weather={data.get('weather_condition', 'Haze')}, holiday={data.get('holiday_name', 'None')}")
    return features_df


def get_medicine_recommendations(disease_type, predicted_count, current_count=100):
    """
    Generate medicine stock recommendations based on predicted patient count.
    
    Args:
        disease_type (str): Type of disease
        predicted_count (float): Predicted number of patients
        current_count (int): Current stock level (default 100)
        
    Returns:
        list: List of medicine recommendations
    """
    recommendations = []
    
    # Get medicines for this disease type
    medicines = MEDICINE_DATABASE.get(disease_type, MEDICINE_DATABASE.get("Heart Disease"))
    
    for medicine in medicines:
        med_name = medicine["name"]
        base_qty = medicine["base_qty"]
        expiry_days = medicine["expiry_critical_days"]
        
        # Calculate recommended quantity based on predicted patient count
        multiplier = predicted_count / 5.0  # Assume 5 patients as baseline
        recommended_qty = int(base_qty * max(multiplier, 1.0))
        
        # Determine action based on stock levels
        if current_count < CRITICAL_STOCK_THRESHOLD:
            action = "URGENT: Order immediately"
            new_qty = int(recommended_qty * (1 + (STOCK_INCREASE_PERCENT + 50) / 100))
        elif current_count < LOW_STOCK_THRESHOLD:
            action = "Order soon"
            new_qty = int(recommended_qty * (1 + STOCK_INCREASE_PERCENT / 100))
        elif predicted_count > 10:
            action = "Increase stock"
            new_qty = int(recommended_qty * (1 + STOCK_INCREASE_PERCENT / 100))
        elif predicted_count < 3:
            action = "Decrease stock"
            new_qty = int(recommended_qty * (1 - STOCK_DECREASE_PERCENT / 100))
        else:
            action = "Maintain current stock"
            new_qty = recommended_qty
        
        # Expiry warning
        expiry_warning = f"Check expiry within {expiry_days} days" if current_count > LOW_STOCK_THRESHOLD else "Prioritize stock with latest expiry dates"
        
        recommendations.append({
            "medicine": med_name,
            "current_stock": current_count,
            "recommended_quantity": new_qty,
            "action": action,
            "expiry_warning": expiry_warning,
            "criticality": "CRITICAL" if current_count < CRITICAL_STOCK_THRESHOLD else ("HIGH" if current_count < LOW_STOCK_THRESHOLD else "NORMAL")
        })
    
    return recommendations


@app.route("/", methods=["GET"])
def root():
    """
    Root endpoint - serves the dashboard or API information.
    
    Returns:
        HTML or JSON: Dashboard page or API welcome message
    """
    # Check if Accept header requests HTML (browser)
    if 'text/html' in request.headers.get('Accept', 'application/json'):
        try:
            return render_template('dashboard.html')
        except Exception as e:
            logger.error(f"Error rendering dashboard: {e}")
            # Fallback to JSON if template fails
            pass
    
    # Return JSON API information
    return jsonify({
        "message": "ArogyaPredict API - Hospital Patient Inflow Prediction",
        "version": "1.0",
        "status": "running",
        "available_endpoints": {
            "GET /": "API information or Dashboard (this endpoint)",
            "GET /dashboard": "View interactive dashboard",
            "GET /health": "Health check and system status",
            "POST /predict": "Predict patient count based on environmental data",
            "POST /recommend": "Get medicine stock recommendations",
            "GET /api/medicines": "Get comprehensive medicine database"
        },
        "documentation": "See ARCHITECTURE.md and API_TESTING_EXAMPLES.md",
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    Dashboard endpoint - serves the interactive dashboard page.
    
    Returns:
        HTML: Dashboard page
    """
    try:
        return render_template('dashboard.html')
    except Exception as e:
        logger.error(f"Error rendering dashboard: {e}")
        return jsonify({
            "error": "Error loading dashboard",
            "details": str(e)
        }), 500


@app.route("/favicon.ico", methods=["GET"])
def favicon():
    """
    Favicon endpoint - returns 204 No Content.
    """
    return "", 204


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    
    Returns:
        JSON: Status of the API
    """
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": model is not None,
        "endpoints": ["/health", "/predict", "/recommend", "/api/medicines", "/dashboard"],
        "medicine_database": {
            "total_diseases": len(MEDICINE_DATABASE),
            "total_medicines": sum(len(meds) for meds in MEDICINE_DATABASE.values())
        }
    })


@app.route("/api/medicines", methods=["GET"])
def get_medicines():
    """
    API endpoint to get complete medicine database.
    
    Query Parameters:
        disease_type (optional): Filter by disease type
    
    Returns:
        JSON: Complete medicine database or filtered by disease
    """
    try:
        disease_type = request.args.get('disease_type', None)
        
        if disease_type and disease_type in MEDICINE_DATABASE:
            # Return medicines for specific disease
            medicines = {disease_type: MEDICINE_DATABASE[disease_type]}
        else:
            # Return all medicines
            medicines = MEDICINE_DATABASE
        
        # Calculate statistics
        total_medicines = sum(len(meds) for meds in medicines.values())
        
        response = {
            "status": "success",
            "data": medicines,
            "statistics": {
                "total_diseases": len(medicines),
                "total_medicines": total_medicines,
                "timestamp": datetime.now().isoformat()
            }
        }
        
        logger.info(f"✓ Medicine database returned: {total_medicines} medicines across {len(medicines)} diseases")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error retrieving medicines: {e}")
        return jsonify({
            "error": f"Error retrieving medicines: {str(e)}",
            "status": "error"
        }), 500


@app.route("/api/predictions/weekly", methods=["GET"])
def get_weekly_predictions():
    """
    Get aggregated weekly predictions summary.
    
    Returns:
        JSON: Weekly prediction statistics
    """
    try:
        # Generate sample weekly data (in production, use actual predictions)
        week_predictions = []
        for i in range(7):
            date = datetime.now() - timedelta(days=i)
            predicted = np.random.randint(5, 25)
            week_predictions.append({
                "date": date.strftime("%Y-%m-%d"),
                "day": date.strftime("%A"),
                "predicted_patients": predicted,
                "confidence": 0.85
            })
        
        response = {
            "status": "success",
            "period": "last 7 days",
            "data": week_predictions,
            "summary": {
                "avg_daily_patients": np.mean([p["predicted_patients"] for p in week_predictions]),
                "max_patients": max(p["predicted_patients"] for p in week_predictions),
                "min_patients": min(p["predicted_patients"] for p in week_predictions)
            },
            "timestamp": datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error getting weekly predictions: {e}")
        return jsonify({
            "error": str(e),
            "status": "error"
        }), 500


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict patient count based on environmental data.
    
    Request JSON:
    {
        "temperature": 28.5,
        "humidity": 65,
        "aqi": 150,
        "disease_type": "Heart Disease",  (optional)
        "hospital_area": "General Ward"    (optional)
    }
    
    Returns:
        JSON: Predicted patient count and confidence metrics
    """
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                "error": "Model not loaded. Please train the model first.",
                "status": "error"
            }), 503
        
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "No JSON data provided",
                "status": "error"
            }), 400
        
        # Validate input
        is_valid, error_msg, cleaned_data = validate_prediction_input(data)
        if not is_valid:
            return jsonify({
                "error": error_msg,
                "status": "error"
            }), 400
        
        # Prepare features
        try:
            features_df = prepare_features(cleaned_data)
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return jsonify({
                "error": f"Error preparing features: {str(e)}",
                "status": "error"
            }), 500
        
        # Make prediction
        try:
            predicted_count = float(model.predict(features_df)[0])
            predicted_count = max(0, predicted_count)  # Ensure non-negative
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return jsonify({
                "error": f"Error making prediction: {str(e)}",
                "status": "error"
            }), 500
        
        # Prepare response
        response = {
            "status": "success",
            "prediction": {
                "predicted_patient_count": round(predicted_count, 2),
                "rounded_count": int(round(predicted_count)),
                "confidence_range": {
                    "lower": round(max(0, predicted_count - 2), 2),
                    "upper": round(predicted_count + 2, 2)
                }
            },
            "input": {
                "temperature": cleaned_data["temperature"],
                "humidity": cleaned_data["humidity"],
                "aqi": cleaned_data["aqi"],
                "disease_type": cleaned_data["disease_type"],
                "weather_condition": cleaned_data["weather_condition"],
                "is_holiday": cleaned_data["is_holiday"],
                "holiday_name": cleaned_data["holiday_name"],
                "expected_multiplier": cleaned_data["expected_multiplier"],
                "days_after_holiday": cleaned_data["days_after_holiday"]
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✓ Prediction: {predicted_count:.2f} patients for {cleaned_data['disease_type']}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in /predict: {e}")
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }), 500


@app.route("/recommend", methods=["POST"])
def recommend_medicines():
    """
    Get medicine stock recommendations based on predicted patient count.
    
    Request JSON:
    {
        "predicted_patient_count": 15,
        "disease_type": "Heart Disease",
        "current_stock": 100
    }
    
    Returns:
        JSON: Medicine stock recommendations
    """
    try:
        # Get JSON data
        data = request.get_json()
        if not data:
            return jsonify({
                "error": "No JSON data provided",
                "status": "error"
            }), 400
        
        # Validate required fields
        required_fields = ["predicted_patient_count", "disease_type"]
        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"Missing required field: '{field}'",
                    "status": "error"
                }), 400
        
        # Parse and validate data
        try:
            predicted_count = float(data["predicted_patient_count"])
            disease_type = str(data["disease_type"])
            current_stock = int(data.get("current_stock", 100))
            
            if predicted_count < 0:
                return jsonify({
                    "error": "Predicted patient count must be non-negative",
                    "status": "error"
                }), 400
                
        except ValueError as e:
            return jsonify({
                "error": f"Invalid data format: {str(e)}",
                "status": "error"
            }), 400
        
        # Get recommendations
        recommendations = get_medicine_recommendations(
            disease_type,
            predicted_count,
            current_stock
        )
        
        # Prepare response
        response = {
            "status": "success",
            "input": {
                "predicted_patient_count": predicted_count,
                "disease_type": disease_type,
                "current_stock": current_stock
            },
            "recommendations": recommendations,
            "summary": {
                "total_medicines": len(recommendations),
                "critical_count": sum(1 for r in recommendations if r["criticality"] == "CRITICAL"),
                "high_count": sum(1 for r in recommendations if r["criticality"] == "HIGH"),
            },
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"✓ Recommendations generated for {disease_type} with {predicted_count} predicted patients")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Unexpected error in /recommend: {e}")
        return jsonify({
            "error": f"Unexpected error: {str(e)}",
            "status": "error"
        }), 500


@app.errorhandler(400)
def bad_request(error):
    """Handle 400 errors."""
    return jsonify({
        "error": "Bad request",
        "status": "error",
        "message": str(error.description) if hasattr(error, 'description') else "Invalid request format"
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "error": "Endpoint not found",
        "status": "error",
        "message": f"The requested endpoint does not exist. Try GET / for API information.",
        "available_endpoints": ["/", "/health", "/predict", "/recommend"],
        "hint": "Check the URL and HTTP method (GET vs POST)"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Handle 405 errors."""
    return jsonify({
        "error": "Method not allowed",
        "status": "error",
        "message": f"HTTP method not allowed for this endpoint",
        "hint": "/predict and /recommend require POST, /health and / require GET"
    }), 405


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"500 Internal Server Error: {error}")
    return jsonify({
        "error": "Internal server error",
        "status": "error",
        "message": "Something went wrong on the server side"
    }), 500


def main():
    """Main function to run Flask app."""
    logger.info("=" * 60)
    logger.info("ArogyaPredict - Flask API Server")
    logger.info("=" * 60)
    
    # Load model and encoders
    if not load_model_and_encoders():
        logger.error("\n✗ Failed to load model and encoders!")
        logger.error("Please train the model first by running train_model.py")
        sys.exit(1)
    
    logger.info("\n✓ Model and encoders loaded successfully!")
    logger.info("✓ API Server is ready to receive requests")
    logger.info("\nAvailable endpoints:")
    logger.info("  GET  /health - Health check")
    logger.info("  POST /predict - Predict patient count")
    logger.info("  POST /recommend - Get medicine recommendations")
    logger.info("\n" + "=" * 60)
    
    # Run Flask app
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False,
        use_reloader=False
    )


if __name__ == "__main__":
    main()
