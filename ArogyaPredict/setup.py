"""
Complete Setup and Execution Script for ArogyaPredict
This script guides you through the entire workflow: data enrichment, preprocessing, 
model training, and API deployment.
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}  {text}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")

def print_step(step_num, text):
    """Print step header."""
    print(f"{Colors.CYAN}[STEP {step_num}] {text}{Colors.END}")

def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    """Print warning message."""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")

def check_python_version():
    """Check if Python version is 3.8 or higher."""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_error(f"Python 3.8+ required (you have {version.major}.{version.minor})")
        sys.exit(1)
    
    print_success(f"Python {version.major}.{version.minor}.{version.micro} installed")
    return True

def check_project_structure():
    """Check if project structure exists."""
    print_step(2, "Checking Project Structure")
    
    base_dir = Path(__file__).parent
    required_dirs = ["data", "scripts", "models", "app"]
    required_files = ["config.py", "requirements.txt", "README.md"]
    
    for dir_name in required_dirs:
        dir_path = base_dir / dir_name
        if dir_path.exists():
            print_success(f"Directory '{dir_name}' found")
        else:
            print_error(f"Directory '{dir_name}' not found")
            return False
    
    for file_name in required_files:
        file_path = base_dir / file_name
        if file_path.exists():
            print_success(f"File '{file_name}' found")
        else:
            print_error(f"File '{file_name}' not found")
            return False
    
    return True

def install_dependencies():
    """Install required Python packages."""
    print_step(3, "Installing Dependencies")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        print_info("Installing packages from requirements.txt...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)],
            check=True,
            capture_output=True,
            timeout=600
        )
        print_success("All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print_error(f"Failed to install dependencies: {e}")
        return False
    except Exception as e:
        print_error(f"Error during installation: {e}")
        return False

def setup_environment():
    """Setup .env file."""
    print_step(4, "Setting Up Environment Variables")
    
    base_dir = Path(__file__).parent
    env_file = base_dir / ".env"
    env_example = base_dir / ".env.example"
    
    if env_file.exists():
        print_warning(".env file already exists")
    else:
        if env_example.exists():
            print_info("Creating .env from .env.example...")
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print_success(".env file created")
        
        print_info("Please edit .env file and add your OpenWeather API key:")
        print_info("  1. Visit: https://openweathermap.org/api")
        print_info("  2. Get your API key")
        print_info("  3. Add to .env: OPENWEATHER_API_KEY=your_key_here")
    
    return True

def run_data_enrichment():
    """Run data enrichment script."""
    print_step(5, "Running Data Enrichment (fetch_data.py)")
    
    script_path = Path(__file__).parent / "scripts" / "fetch_data.py"
    
    try:
        print_info("Enriching hospital dataset with environmental data...")
        print_info("This will fetch data from OpenAQ and OpenWeather APIs...")
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(Path(__file__).parent),
            timeout=120,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Data enrichment completed successfully")
            return True
        else:
            print_error("Data enrichment failed")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Data enrichment timed out")
        return False
    except Exception as e:
        print_error(f"Error running data enrichment: {e}")
        return False

def run_preprocessing():
    """Run data preprocessing script."""
    print_step(6, "Running Data Preprocessing (preprocess.py)")
    
    script_path = Path(__file__).parent / "scripts" / "preprocess.py"
    
    try:
        print_info("Preprocessing data: handling missing values, encoding...")
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(Path(__file__).parent),
            timeout=60,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Data preprocessing completed successfully")
            return True
        else:
            print_error("Data preprocessing failed")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Data preprocessing timed out")
        return False
    except Exception as e:
        print_error(f"Error running preprocessing: {e}")
        return False

def run_model_training():
    """Run model training script."""
    print_step(7, "Running Model Training (train_model.py)")
    
    script_path = Path(__file__).parent / "scripts" / "train_model.py"
    
    try:
        print_info("Training RandomForestRegressor model...")
        print_info("This may take a moment...")
        
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(Path(__file__).parent),
            timeout=300,
            capture_output=False
        )
        
        if result.returncode == 0:
            print_success("Model training completed successfully")
            return True
        else:
            print_error("Model training failed")
            return False
            
    except subprocess.TimeoutExpired:
        print_error("Model training timed out")
        return False
    except Exception as e:
        print_error(f"Error running model training: {e}")
        return False

def verify_model_files():
    """Verify trained model and encoder files exist."""
    print_step(8, "Verifying Model Files")
    
    base_dir = Path(__file__).parent
    model_file = base_dir / "models" / "patient_inflow_model.pkl"
    encoder_file = base_dir / "models" / "encoders.pkl"
    
    if model_file.exists():
        size_mb = model_file.stat().st_size / (1024 * 1024)
        print_success(f"Model file found ({size_mb:.2f} MB)")
    else:
        print_error("Model file not found!")
        return False
    
    if encoder_file.exists():
        print_success("Encoder file found")
    else:
        print_warning("Encoder file not found (will be created during inference)")
    
    return True

def start_api_server():
    """Start Flask API server."""
    print_step(9, "Starting Flask API Server")
    
    app_path = Path(__file__).parent / "app" / "app.py"
    
    print_info("Starting API server on http://0.0.0.0:5000")
    print_info("Press Ctrl+C to stop the server")
    print_warning("Note: This step blocks. Run in a separate terminal to use test_api.py")
    
    try:
        subprocess.run(
            [sys.executable, str(app_path)],
            cwd=str(Path(__file__).parent),
            timeout=None
        )
    except KeyboardInterrupt:
        print_info("API server stopped")
        return True
    except Exception as e:
        print_error(f"Error starting API server: {e}")
        return False

def display_usage_guide():
    """Display usage guide."""
    print_header("USAGE GUIDE")
    
    print_info("The ArogyaPredict system is now ready!")
    print_info("")
    print_info("Available commands:")
    print_info("  1. Run data enrichment:")
    print_info("     python scripts/fetch_data.py")
    print_info("")
    print_info("  2. Preprocess data:")
    print_info("     python scripts/preprocess.py")
    print_info("")
    print_info("  3. Train model:")
    print_info("     python scripts/train_model.py")
    print_info("")
    print_info("  4. Start API server:")
    print_info("     python app/app.py")
    print_info("")
    print_info("  5. Run API tests (in another terminal):")
    print_info("     python test_api.py")
    print_info("")
    print_info("API Endpoints:")
    print_info("  GET  /health           - Health check")
    print_info("  POST /predict          - Predict patient count")
    print_info("  POST /recommend        - Medicine recommendations")
    print_info("")
    print_info("Full documentation: See README.md")

def main():
    """Main execution function."""
    print_header("AROGYA PREDICT - Complete Setup and Execution")
    
    print_info("Welcome to ArogyaPredict!")
    print_info("This script will guide you through the complete setup process.")
    print("")
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 2: Check project structure
    if not check_project_structure():
        print_error("Project structure is incomplete!")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 3: Install dependencies
    if not install_dependencies():
        print_error("Failed to install dependencies!")
        sys.exit(1)
    
    time.sleep(1)
    
    # Step 4: Setup environment
    if not setup_environment():
        print_warning("Environment setup incomplete. Please edit .env manually.")
    
    time.sleep(1)
    
    # Step 5: Data enrichment
    print_info("")
    user_input = input(f"{Colors.CYAN}Run data enrichment step? (y/n): {Colors.END}")
    if user_input.lower() == 'y':
        if not run_data_enrichment():
            print_error("Data enrichment failed!")
            sys.exit(1)
        time.sleep(1)
    else:
        print_warning("Skipping data enrichment")
    
    # Step 6: Preprocessing
    print_info("")
    user_input = input(f"{Colors.CYAN}Run data preprocessing step? (y/n): {Colors.END}")
    if user_input.lower() == 'y':
        if not run_preprocessing():
            print_error("Data preprocessing failed!")
            sys.exit(1)
        time.sleep(1)
    else:
        print_warning("Skipping preprocessing")
    
    # Step 7: Model training
    print_info("")
    user_input = input(f"{Colors.CYAN}Run model training step? (y/n): {Colors.END}")
    if user_input.lower() == 'y':
        if not run_model_training():
            print_error("Model training failed!")
            sys.exit(1)
        time.sleep(1)
    else:
        print_warning("Skipping model training")
    
    # Step 8: Verify model
    if not verify_model_files():
        print_warning("Model files not ready!")
    
    time.sleep(1)
    
    # Display usage guide
    display_usage_guide()
    
    # Step 9: Start API
    print_info("")
    user_input = input(f"{Colors.CYAN}Start Flask API server now? (y/n): {Colors.END}")
    if user_input.lower() == 'y':
        print_info("Starting API server...")
        print_info("To test API endpoints, run 'python test_api.py' in another terminal")
        time.sleep(2)
        start_api_server()
    else:
        print_info("Setup complete! Run 'python app/app.py' to start the API later.")
    
    print_header("Setup Complete!")
    print_success("ArogyaPredict system is ready for use!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print_info("\nSetup interrupted by user")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
