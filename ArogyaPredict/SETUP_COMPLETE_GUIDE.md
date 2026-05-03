# Complete Setup Guide - One Command to Run Everything

## Option 1: AUTOMATIC SETUP (Easiest - One Command!)

If you want everything done automatically:

```
python setup_complete.py
```

This will:

1. ✅ Install all required packages
2. ✅ Generate large realistic dataset (1500+ records)
3. ✅ Train the ML model
4. ✅ Start the Flask server
5. ✅ Open dashboard in browser

**That's it! Everything else is automatic.**

---

## Option 2: MANUAL STEP BY STEP

If you want to do each step:

### Step 1: Open Terminal and go to project folder

```
cd E:\BCA\Final\ArogyaPredict
```

### Step 2: Install packages one time only

```
pip install -r requirements.txt
```

### Step 3: Generate larger dataset (one time or when you want more data)

```
python generate_large_dataset.py
```

### Step 4: Train the model (run after adding new data)

```
python scripts/train_model.py
```

### Step 5: Start the website/app

```
python -m app.app
```

### Step 6: Open in Browser

Go to: http://127.0.0.1:5000/

---

## What is the dataset size?

**Before:** 15 records (Too small)  
**After:** 1500+ records (Realistic for large hospital)

---

## Is the website static or dynamic?

**It's DYNAMIC!**

You can:

- Enter temperature, humidity, air quality
- Select disease type, weather, holidays
- Click "Predict" button
- See results instantly
- Get medicine stock recommendations

---

## Once model is trained, is that enough?

**Yes!** The trained model stays saved. But:

- If you add MORE data → Retrain the model
- If you add NEW disease types → Retrain the model
- If you change features → Retrain the model
- Otherwise → Just use it as-is

---

## Do I need to restart everything?

**Once started:**

- Website keeps running
- Just refresh browser if needed
- To stop: Press Ctrl+C in terminal

**To start again next time:**

```
python -m app.app
```

---

## Testing

To test that everything works:

```
python test_all_endpoints.py
```

---

## File Structure After Setup

```
ArogyaPredict/
├── data/
│   └── final_dataset.csv          <- Auto-generated (1500+ rows)
├── models/
│   ├── patient_inflow_model.pkl   <- Auto-trained model
│   └── encoders.pkl               <- Auto-trained encoders
├── scripts/
│   ├── preprocess.py              <- Data cleaning
│   ├── train_model.py             <- Model training
│   └── ... (other scripts)
├── app/
│   ├── app.py                     <- Web server
│   ├── templates/
│   │   └── dashboard.html         <- Web interface (DYNAMIC)
│   └── static/
│       ├── css/
│       └── js/
└── setup_complete.py              <- Run this for automatic setup
```

---

## Troubleshooting

**Q: "pip: command not found"**  
A: Install Python from python.org

**Q: "ModuleNotFoundError"**  
A: Run `pip install -r requirements.txt`

**Q: "Address already in use"**  
A: Port 5000 is busy. Kill it: `netstat -ano | findstr :5000` then `taskkill /PID <PID> /F`

**Q: "Model file not found"**  
A: Run `python scripts/train_model.py`

**Q: Dataset not updated**  
A: Run `python generate_large_dataset.py`

---

## Next Steps

1. Run: `python setup_complete.py`
2. Wait for everything to complete (~5 mins)
3. Browser opens automatically
4. Use the dashboard!
5. Make predictions
6. Check medical stock recommendations

**Questions? Check ARCHITECTURE.md and API_TESTING_EXAMPLES.md**
