"""
Quick Start Guide and Testing Script for ArogyaPredict API
"""

import requests
import json
import sys
import time

# API Base URL
API_URL = "http://localhost:5000"

def print_header(text):
    """Print formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_health_check():
    """Test the health check endpoint."""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Could not connect to API. Is the server running?")
        print(f"   Run: python app/app.py")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False

def test_prediction():
    """Test the prediction endpoint."""
    print_header("TEST 2: Patient Count Prediction")
    
    test_cases = [
        {
            "name": "Normal Environmental Conditions",
            "data": {
                "temperature": 28.5,
                "humidity": 65,
                "aqi": 150,
                "disease_type": "Heart Disease",
                "hospital_area": "General Ward"
            }
        },
        {
            "name": "High Temperature and Humidity",
            "data": {
                "temperature": 35.0,
                "humidity": 85,
                "aqi": 200,
                "disease_type": "Respiratory Infection",
                "hospital_area": "OPD"
            }
        },
        {
            "name": "Low Environmental Stress",
            "data": {
                "temperature": 20.0,
                "humidity": 45,
                "aqi": 80,
                "disease_type": "Diabetes",
                "hospital_area": "Pediatrics"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Input: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                f"{API_URL}/predict",
                json=test_case['data'],
                timeout=5
            )
            print(f"Status Code: {response.status_code}")
            result = response.json()
            
            if response.status_code == 200:
                pred = result['prediction']['predicted_patient_count']
                rounded = result['prediction']['rounded_count']
                print(f"✓ Predicted Count: {pred} (rounded: {rounded})")
                print(f"  Confidence Range: {result['prediction']['confidence_range']}")
            else:
                print(f"✗ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")

def test_recommendations():
    """Test the medicine recommendation endpoint."""
    print_header("TEST 3: Medicine Stock Recommendations")
    
    test_cases = [
        {
            "name": "Low Patient Count",
            "data": {
                "predicted_patient_count": 3,
                "disease_type": "Heart Disease",
                "current_stock": 150
            }
        },
        {
            "name": "High Patient Count",
            "data": {
                "predicted_patient_count": 20,
                "disease_type": "Diabetes",
                "current_stock": 80
            }
        },
        {
            "name": "Critical Stock Level",
            "data": {
                "predicted_patient_count": 15,
                "disease_type": "Respiratory Infection",
                "current_stock": 15
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"Input: {json.dumps(test_case['data'], indent=2)}")
        
        try:
            response = requests.post(
                f"{API_URL}/recommend",
                json=test_case['data'],
                timeout=5
            )
            print(f"Status Code: {response.status_code}")
            result = response.json()
            
            if response.status_code == 200:
                summary = result['summary']
                print(f"✓ Recommendations Generated:")
                print(f"  Total Medicines: {summary['total_medicines']}")
                print(f"  Critical: {summary['critical_count']}")
                print(f"  High: {summary['high_count']}")
                print(f"\n  Recommendations:")
                for rec in result['recommendations']:
                    print(f"    - {rec['medicine']}: {rec['action']} (qty: {rec['recommended_quantity']})")
            else:
                print(f"✗ Error: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")

def test_error_handling():
    """Test error handling."""
    print_header("TEST 4: Error Handling")
    
    error_cases = [
        {
            "name": "Missing Required Field",
            "endpoint": "/predict",
            "data": {"temperature": 28.5}
        },
        {
            "name": "Invalid Data Type",
            "endpoint": "/predict",
            "data": {"temperature": "not_a_number", "humidity": 65, "aqi": 150}
        },
        {
            "name": "Invalid Humidity",
            "endpoint": "/predict",
            "data": {"temperature": 28.5, "humidity": 150, "aqi": 150}
        },
        {
            "name": "Non-existent Endpoint",
            "endpoint": "/invalid",
            "data": {}
        }
    ]
    
    for test_case in error_cases:
        print(f"\nTest: {test_case['name']}")
        
        try:
            response = requests.post(
                f"{API_URL}{test_case['endpoint']}",
                json=test_case['data'],
                timeout=5
            )
            result = response.json()
            
            if response.status_code != 200:
                print(f"✓ Error handled correctly (Status: {response.status_code})")
                print(f"  Message: {result.get('error', 'No error message')}")
            else:
                print(f"✗ Unexpected success for error test")
                
        except Exception as e:
            print(f"✗ ERROR: {e}")

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("  ArogyaPredict API - Test Suite")
    print("=" * 60)
    print("\nRunning comprehensive API tests...")
    print("Make sure the API server is running: python app/app.py")
    
    # Wait a bit for potential server startup
    time.sleep(1)
    
    # Run tests
    results = []
    
    results.append(("Health Check", test_health_check()))
    if results[0][1]:  # Only run other tests if health check passes
        test_prediction()
        test_recommendations()
        test_error_handling()
    
    # Summary
    print_header("TEST SUMMARY")
    print(f"Health Check: {'✓ PASSED' if results[0][1] else '✗ FAILED'}")
    
    if results[0][1]:
        print("\n✓ All tests completed successfully!")
        print("\nNext steps:")
        print("1. Verify predictions are reasonable")
        print("2. Check medicine recommendations")
        print("3. Test with your own data")
    else:
        print("\n✗ API server is not running or not accessible")
        print("\nTo start the API:")
        print("  cd app")
        print("  python app.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
