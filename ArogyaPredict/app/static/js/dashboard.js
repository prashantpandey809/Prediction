// Chart instances
let patientChart = null;
let diseaseChart = null;

// Initialize on page load
document.addEventListener("DOMContentLoaded", function () {
  updateTimestamp();
  initializeCharts();
  loadMedicineDatabase();
  generateTodayPrediction();
  generateMonthlySummary();

  // Auto-update timestamp
  setInterval(updateTimestamp, 60000);
});

// Update timestamp
function updateTimestamp() {
  const now = new Date();
  const options = {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  };
  document.getElementById("timestamp").textContent = now.toLocaleDateString(
    "en-US",
    options,
  );
}

// Initialize charts
function initializeCharts() {
  // Patient forecast chart
  const patientCtx = document.getElementById("patientChart").getContext("2d");
  patientChart = new Chart(patientCtx, {
    type: "line",
    data: {
      labels: generateDayLabels(30),
      datasets: [
        {
          label: "Predicted Patients",
          data: generatePatientData(30),
          borderColor: "#2563eb",
          backgroundColor: "rgba(37, 99, 235, 0.1)",
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointBackgroundColor: "#2563eb",
          pointBorderColor: "#1e40af",
          pointBorderWidth: 2,
          pointHoverRadius: 7,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          display: false,
        },
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: "Number of Patients",
          },
        },
      },
    },
  });

  // Disease distribution chart
  const diseaseCtx = document.getElementById("diseaseChart").getContext("2d");
  diseaseChart = new Chart(diseaseCtx, {
    type: "doughnut",
    data: {
      labels: [
        "Heart Disease",
        "Diabetes",
        "Respiratory",
        "Hypertension",
        "Other",
      ],
      datasets: [
        {
          data: [20, 18, 22, 15, 25],
          backgroundColor: [
            "#ef4444",
            "#3b82f6",
            "#f97316",
            "#8b5cf6",
            "#06b6d4",
          ],
          borderColor: "#ffffff",
          borderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: "bottom",
        },
      },
    },
  });
}

// Generate day labels for 30 days
function generateDayLabels(days) {
  const labels = [];
  const today = new Date();
  for (let i = 0; i < days; i++) {
    const date = new Date(today);
    date.setDate(date.getDate() + i);
    labels.push(
      date.getDate() +
        " " +
        date.toLocaleDateString("en-US", { month: "short" }),
    );
  }
  return labels;
}

// Generate random patient data for demo
function generatePatientData(days) {
  const data = [];
  for (let i = 0; i < days; i++) {
    data.push(Math.floor(Math.random() * 20) + 5);
  }
  return data;
}

// Generate today's prediction
async function generateTodayPrediction() {
  try {
    // Get today's average data
    const temperature = 28.5;
    const humidity = 65;
    const aqi = 150;
    const disease_type = "Heart Disease";
    const weather_condition = "Haze";
    const is_holiday = 0;
    const holiday_name = "None";
    const expected_multiplier = 1.0;
    const days_after_holiday = 0;

    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        temperature: temperature,
        humidity: humidity,
        aqi: aqi,
        disease_type: disease_type,
        weather_condition: weather_condition,
        is_holiday: is_holiday,
        holiday_name: holiday_name,
        expected_multiplier: expected_multiplier,
        days_after_holiday: days_after_holiday,
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      const predicted = Math.round(data.prediction.predicted_patient_count);
      const lower = Math.round(data.prediction.confidence_range.lower);
      const upper = Math.round(data.prediction.confidence_range.upper);

      document.getElementById("todayPatients").textContent = predicted;
      document.getElementById("todayRange").textContent =
        `Range: ${lower} - ${upper} patients`;

      // Calculate monthly estimate
      const monthEstimate = Math.round(predicted * 25); // Rough estimate for 25 working days
      document.getElementById("monthPatients").textContent = monthEstimate;
      document.getElementById("avgDaily").textContent = Math.round(
        monthEstimate / 25,
      );
    }
  } catch (error) {
    console.error("Error generating today prediction:", error);
  }
}

// Generate monthly summary
function generateMonthlySummary() {
  // This is a simplified calculation - in production, you'd aggregate actual predictions
  const avgDaily =
    parseInt(document.getElementById("avgDaily").textContent) || 8;
  const monthTotal = avgDaily * 25;

  // Count critical medicines (sample data)
  document.getElementById("criticalMeds").textContent = "5";
  document.getElementById("expiringSoon").textContent = "3";
}

// Load medicine database and display
async function loadMedicineDatabase() {
  try {
    const response = await fetch("/api/medicines");
    const medicines = await response.json();

    displayAllMedicines(medicines);
  } catch (error) {
    // Display sample medicine database if API fails
    console.log("Loading sample medicine database");
    displaySampleMedicines();
  }
}

// Display all medicines
function displayAllMedicines(medicines) {
  const container = document.getElementById("medicineContainer");
  container.innerHTML = "";

  let medicineCount = 0;

  for (const [disease, meds] of Object.entries(medicines)) {
    meds.forEach((med) => {
      const card = createMedicineCard(med, disease);
      container.appendChild(card);
      medicineCount++;
    });
  }

  console.log(`Loaded ${medicineCount} medicines`);
}

// Display sample medicines (fallback)
function displaySampleMedicines() {
  const sampleMedicines = {
    "Heart Disease": [
      {
        name: "Aspirin",
        base_qty: 200,
        expiry_critical_days: 30,
        dosage: "100mg",
        form: "Tablet",
      },
      {
        name: "Atorvastatin",
        base_qty: 150,
        expiry_critical_days: 60,
        dosage: "20mg",
        form: "Tablet",
      },
      {
        name: "Lisinopril",
        base_qty: 150,
        expiry_critical_days: 60,
        dosage: "10mg",
        form: "Tablet",
      },
      {
        name: "Metoprolol",
        base_qty: 120,
        expiry_critical_days: 60,
        dosage: "50mg",
        form: "Tablet",
      },
    ],
    Diabetes: [
      {
        name: "Insulin Glargine",
        base_qty: 250,
        expiry_critical_days: 7,
        dosage: "100IU/ml",
        form: "Injection",
      },
      {
        name: "Metformin",
        base_qty: 300,
        expiry_critical_days: 90,
        dosage: "500mg",
        form: "Tablet",
      },
      {
        name: "Glipizide",
        base_qty: 200,
        expiry_critical_days: 90,
        dosage: "10mg",
        form: "Tablet",
      },
      {
        name: "Sitagliptin",
        base_qty: 150,
        expiry_critical_days: 90,
        dosage: "100mg",
        form: "Tablet",
      },
    ],
    "Respiratory Infection": [
      {
        name: "Amoxicillin",
        base_qty: 300,
        expiry_critical_days: 60,
        dosage: "500mg",
        form: "Tablet",
      },
      {
        name: "Azithromycin",
        base_qty: 250,
        expiry_critical_days: 60,
        dosage: "500mg",
        form: "Tablet",
      },
      {
        name: "Salbutamol",
        base_qty: 200,
        expiry_critical_days: 90,
        dosage: "100mcg",
        form: "Inhaler",
      },
    ],
    Hypertension: [
      {
        name: "Amlodipine",
        base_qty: 250,
        expiry_critical_days: 90,
        dosage: "5mg",
        form: "Tablet",
      },
      {
        name: "Atenolol",
        base_qty: 200,
        expiry_critical_days: 90,
        dosage: "50mg",
        form: "Tablet",
      },
      {
        name: "Losartan",
        base_qty: 200,
        expiry_critical_days: 90,
        dosage: "50mg",
        form: "Tablet",
      },
    ],
    "Kidney Disease": [
      {
        name: "Furosemide",
        base_qty: 200,
        expiry_critical_days: 60,
        dosage: "40mg",
        form: "Tablet",
      },
      {
        name: "Potassium Supplement",
        base_qty: 150,
        expiry_critical_days: 90,
        dosage: "20mEq",
        form: "Tablet",
      },
      {
        name: "Calcium Carbonate",
        base_qty: 180,
        expiry_critical_days: 90,
        dosage: "500mg",
        form: "Tablet",
      },
    ],
  };

  displayAllMedicines(sampleMedicines);
}

// Create medicine card
function createMedicineCard(medicine, disease) {
  const card = document.createElement("div");
  card.className = `medicine-card disease-${disease}`;

  const dosageText = medicine.dosage || "N/A";
  const formText = medicine.form || "N/A";

  card.innerHTML = `
        <div class="medicine-disease">${disease}</div>
        <div class="medicine-name">${medicine.name}</div>
        <div class="medicine-details">
            <div class="medicine-detail-item">
                <span class="medicine-detail-label">Dosage:</span> ${dosageText}
            </div>
            <div class="medicine-detail-item">
                <span class="medicine-detail-label">Form:</span> ${formText}
            </div>
            <div class="medicine-detail-item">
                <span class="medicine-detail-label">Base Qty:</span> ${medicine.base_qty} units
            </div>
            <div class="medicine-detail-item">
                <span class="medicine-detail-label">Expiry Alert:</span> Within ${medicine.expiry_critical_days} days
            </div>
        </div>
    `;

  return card;
}

// Filter medicines by disease
function filterMedicines() {
  const searchTerm = document
    .getElementById("medicineSearch")
    .value.toLowerCase();
  const diseaseFilter = document.getElementById("diseaseFilter").value;
  const cards = document.querySelectorAll(".medicine-card");

  cards.forEach((card) => {
    const disease = card
      .getAttribute("class")
      .match(/disease-([^ ]+)/)[1]
      .replace(/\%20/g, " ");
    const medicineName = card
      .querySelector(".medicine-name")
      .textContent.toLowerCase();

    const matchesDisease = !diseaseFilter || disease === diseaseFilter;
    const matchesSearch = !searchTerm || medicineName.includes(searchTerm);

    card.style.display = matchesDisease && matchesSearch ? "block" : "none";
  });
}

// Make prediction
async function makePrediction() {
  const temperature = parseFloat(document.getElementById("temperature").value);
  const humidity = parseFloat(document.getElementById("humidity").value);
  const aqi = parseFloat(document.getElementById("aqi").value);
  const disease_type = document.getElementById("disease_type").value;
  const weather_condition = document.getElementById("weather_condition").value;
  const is_holiday = parseInt(document.getElementById("is_holiday").value);
  const holiday_name = document.getElementById("holiday_name").value;

  // Basic validation
  if (!temperature || !humidity || !aqi) {
    alert("Please fill in all required fields");
    return;
  }

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        temperature: temperature,
        humidity: humidity,
        aqi: aqi,
        disease_type: disease_type,
        weather_condition: weather_condition,
        is_holiday: is_holiday,
        holiday_name: holiday_name,
        expected_multiplier: 1.0,
        days_after_holiday: 0,
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      displayPredictionResults(data);
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    alert("Error making prediction: " + error.message);
  }
}

// Display prediction results
function displayPredictionResults(data) {
  const resultsSection = document.getElementById("resultsSection");
  const predicted = data.prediction.predicted_patient_count;
  const lower = data.prediction.confidence_range.lower;
  const upper = data.prediction.confidence_range.upper;

  document.getElementById("predictionResult").textContent =
    Math.round(predicted);
  document.getElementById("predictionRange").textContent =
    `Range: ${Math.round(lower)} - ${Math.round(upper)} patients`;

  resultsSection.style.display = "block";
  resultsSection.scrollIntoView({ behavior: "smooth" });
}

// Get medicine recommendations
async function getRecommendations() {
  const patientCount = parseFloat(
    document.getElementById("patientCountRec").value,
  );
  const disease_type = document.getElementById("diseaseRec").value;
  const current_stock = parseInt(
    document.getElementById("currentStockRec").value,
  );

  if (!patientCount || !disease_type) {
    alert("Please fill in all required fields");
    return;
  }

  try {
    const response = await fetch("/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        predicted_patient_count: patientCount,
        disease_type: disease_type,
        current_stock: current_stock,
      }),
    });

    const data = await response.json();

    if (data.status === "success") {
      displayRecommendations(data);
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    alert("Error getting recommendations: " + error.message);
  }
}

// Display recommendations
function displayRecommendations(data) {
  const container = document.getElementById("recResultsContainer");
  container.innerHTML = "";

  const summary = document.createElement("div");
  summary.style.marginBottom = "20px";
  summary.innerHTML = `
        <h3>Recommendation Summary</h3>
        <p><strong>Total Medicines:</strong> ${data.summary.total_medicines}</p>
        <p><strong>Critical Items:</strong> ${data.summary.critical_count}</p>
        <p><strong>High Priority Items:</strong> ${data.summary.high_count}</p>
        <hr style="margin: 15px 0; border: none; border-top: 2px solid #e5e7eb;">
    `;
  container.appendChild(summary);

  data.recommendations.forEach((rec) => {
    const card = document.createElement("div");
    card.className = `recommendation-card ${rec.criticality.toLowerCase()}`;

    card.innerHTML = `
            <div class="recommendation-header">
                <span class="medicine-name-rec">${rec.medicine}</span>
                <span class="criticality-badge ${rec.criticality.toLowerCase()}">${rec.criticality}</span>
            </div>
            <div class="rec-details">
                <div class="rec-detail">
                    <span class="rec-label">Current Stock:</span> ${rec.current_stock} units
                </div>
                <div class="rec-detail">
                    <span class="rec-label">Recommended Qty:</span> ${rec.recommended_quantity} units
                </div>
                <div class="rec-detail">
                    <span class="rec-label">Action:</span> <strong>${rec.action}</strong>
                </div>
                <div class="rec-detail">
                    <span class="rec-label">⚠️ ${rec.expiry_warning}</span>
                </div>
            </div>
        `;

    container.appendChild(card);
  });
}

// Search medicines
document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("medicineSearch");
  if (searchInput) {
    searchInput.addEventListener("input", filterMedicines);
  }
});

// Export data functionality
function exportData() {
  const todayPatients = document.getElementById("todayPatients").textContent;
  const monthPatients = document.getElementById("monthPatients").textContent;

  const csv = `Date,Today Patients,Monthly Patients\n${new Date().toISOString()},${todayPatients},${monthPatients}`;

  const blob = new Blob([csv], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "arogyapredict-data.csv";
  a.click();
}
