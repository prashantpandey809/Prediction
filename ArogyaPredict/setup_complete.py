"""
Complete setup script for ArogyaPredict
One command to install packages, generate data, train model, and start app
"""

import os
import sys
import subprocess
import time
import webbrowser

print("\n" + "="*80)
print("🏥 AROGYA PREDICT - COMPLETE SETUP")
print("="*80)
print("\nThis script will:")
print("  1. Install Python packages (if needed)")
print("  2. Generate large hospital dataset (1500+ records)")
print("  3. Train the ML model")
print("  4. Start the Flask server")
print("  5. Open the dashboard in your browser")
print("\nEverything is AUTOMATIC - just wait!\n")

def run_command(description, command, show_output=False):
    """Run a shell command and handle errors"""
    print(f"\n{'='*80}")
    print(f"📍 Step: {description}")
    print(f"{'='*80}")
    
    try:
        if show_output:
            result = subprocess.run(command, shell=True, check=True)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
            if result.stdout:
                print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed!")
        if e.stderr:
            print(f"Details: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

# Step 1: Install packages
print("\n📦 STEP 1: Installing Python Packages")
print("-" * 80)
success = run_command(
    "Installing required packages",
    "pip install -r requirements.txt",
    show_output=False
)
if not success:
    print("\n❌ Failed to install packages. Make sure pip is installed.")
    print("   Try: python -m pip install --upgrade pip")
    sys.exit(1)

time.sleep(2)

# Step 2: Generate large dataset
print("\n\n📊 STEP 2: Generating Large Hospital Dataset")
print("-" * 80)
success = run_command(
    "Generating 1500+ realistic hospital records",
    "python generate_large_dataset.py",
    show_output=True
)
if not success:
    print("\n❌ Failed to generate dataset")
    sys.exit(1)

time.sleep(2)

# Step 3: Train model
print("\n\n🤖 STEP 3: Training Machine Learning Model")
print("-" * 80)
success = run_command(
    "Training RandomForest model (this takes 1-2 minutes)",
    "python scripts/train_model.py",
    show_output=True
)
if not success:
    print("\n❌ Failed to train model")
    sys.exit(1)

time.sleep(3)

# Step 4: Start Flask server
print("\n\n🚀 STEP 4: Starting Flask Server")
print("-" * 80)
print("Starting server at http://127.0.0.1:5000/")
print("Opening dashboard in browser in 5 seconds...")

# Start Flask server in background
try:
    import platform
    if platform.system() == "Windows":
        subprocess.Popen("python -m app.app", shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        subprocess.Popen("python -m app.app", shell=True)
    
    # Wait for server to start
    time.sleep(5)
    
    # Try to open browser
    try:
        webbrowser.open("http://127.0.0.1:5000/")
        print("\n✅ Browser opened! Dashboard is loading...")
    except:
        print("\n⚠️  Could not open browser automatically.")
        print("   Please open: http://127.0.0.1:5000/ in your web browser")
        
except Exception as e:
    print(f"\n❌ Error starting server: {e}")
    print("   Try running manually: python -m app.app")
    sys.exit(1)

print("\n" + "="*80)
print("✅ SETUP COMPLETE!")
print("="*80)
print("\n🎉 Your Hospital Dashboard is LIVE!")
print("\nWhat you can do now:")
print("  • View the dashboard at http://127.0.0.1:5000/")
print("  • Make predictions using the form")
print("  • Check medicine stock recommendations")
print("  • View different disease types and weather conditions")
print("\nTo STOP the server: Press Ctrl+C in the Flask terminal window")
print("\nTo START again next time: Just run this script again")
print("  Or manually: python -m app.app")
print("\nFor API testing: python test_all_endpoints.py")
print("="*80 + "\n")

# Keep this process alive
try:
    print("Setup complete! Server is running...")
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nShutdown requested. You can close this window.")
