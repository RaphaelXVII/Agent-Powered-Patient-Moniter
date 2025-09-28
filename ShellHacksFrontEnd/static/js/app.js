// Global variables
let currentUser = null;
const loginForm = document.getElementById('login-form');
const userInfo = document.getElementById('user-info');
const currentUserSpan = document.getElementById('current-user');
let airflowUpdateInterval = null;
let notificationQueue = [];
let isNotificationShowing = false;

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on the patients page
    if (window.location.pathname === '/patients') {
        loadPatients();
        setupPatientEventListeners();
        startAirflowUpdates();
    } else {
        // Just show login form for home page
        showLoginForm();
    }
});

// Login functionality
function handleLogin() {
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    
    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }
    
    // Simple demo login
    if (username === 'admin' && password === 'password') {
        currentUser = username;
        // Redirect to patients page instead of showing alert
        window.location.href = '/patients';
    } else {
        alert('Invalid username or password. Try: admin/password');
    }
}

function handleLogout() {
    currentUser = null;
    // Redirect back to login page
    window.location.href = '/';
}

function showUserInfo() {
    loginForm.style.display = 'none';
    userInfo.style.display = 'flex';
    currentUserSpan.textContent = currentUser;
}

function showLoginForm() {
    loginForm.style.display = 'flex';
    userInfo.style.display = 'none';
    document.getElementById('username').value = '';
    document.getElementById('password').value = '';
}

// Patient management functions
function setupPatientEventListeners() {
    // Only setup floor filter functionality
    const floorSelect = document.getElementById('floor-select');
    if (floorSelect) {
        floorSelect.addEventListener('change', handleFloorFilter);
    }
}

// Load patients data
async function loadPatients() {
    try {
        const response = await fetch('/api/patients');
        if (response.ok) {
            const patients = await response.json();
            window.allPatients = patients;
            renderPatients(patients);
        }
    } catch (error) {
        console.error('Error loading patients:', error);
    }
}

// Render patients on the page
function renderPatients(patients) {
    const container = document.getElementById('patients-container');
    
    if (patients.length === 0) {
        container.innerHTML = '<div class="empty-state"><h3>No patients found</h3></div>';
        return;
    }
    
    const patientsHTML = patients.map(patient => `
        <div class="patient-card">
            <div class="patient-info">
                <div class="patient-name">${patient.name}</div>
                <div class="ventilation-data">
                    <span class="respiratory-rate-value" data-status="${getRespiratoryStatus(patient.respiratory_rate)}">Respiratory Rate: ${patient.respiratory_rate} bpm</span>
                    <span class="airflow-value" data-status="${getAirflowStatus(patient.airflow)}">Airflow: ${patient.airflow}%</span>
                </div>
            </div>
            <div class="patient-id">${patient.id}</div>
            <div class="patient-actions">
                <button class="btn-view" onclick="viewPatient('${patient.id}')">View</button>
            </div>
        </div>
    `).join('');
    
    container.innerHTML = patientsHTML;
}

// Patient action functions
function viewPatient(patientId) {
    // Redirect to patient detail page
    window.location.href = `/patient/${patientId}`;
}




function handleFloorFilter(event) {
    const selectedFloor = event.target.value;
    filterPatientsByFloor(selectedFloor);
}

function filterPatientsByFloor(filter) {
    // Get all patients from the current page
    const allPatients = window.allPatients || [];
    
    if (filter === 'all') {
        renderPatients(allPatients);
    } else if (filter === 'critical') {
        const criticalPatients = allPatients.filter(patient => 
            getAirflowStatus(patient.airflow) === 'critical' || 
            getRespiratoryStatus(patient.respiratory_rate) === 'critical'
        );
        renderPatients(criticalPatients);
    } else if (filter === 'warning') {
        const warningPatients = allPatients.filter(patient => 
            getAirflowStatus(patient.airflow) === 'warning' || 
            getRespiratoryStatus(patient.respiratory_rate) === 'warning'
        );
        renderPatients(warningPatients);
    } else if (filter === 'normal') {
        const normalPatients = allPatients.filter(patient => 
            getAirflowStatus(patient.airflow) === 'normal' && 
            getRespiratoryStatus(patient.respiratory_rate) === 'normal'
        );
        renderPatients(normalPatients);
    } else {
        // Filter by floor number
        const filteredPatients = allPatients.filter(patient => patient.floor == filter);
        renderPatients(filteredPatients);
    }
}

// Real-time airflow updates
function startAirflowUpdates() {
    // Clear any existing interval
    if (airflowUpdateInterval) {
        clearInterval(airflowUpdateInterval);
    }
    
    // Update airflow values every 15 seconds
    airflowUpdateInterval = setInterval(updateAirflowValues, 15000);
}

function updateAirflowValues() {
    if (!window.allPatients) return;
    
    // Update airflow and respiratory rate values for all patients
    window.allPatients.forEach(patient => {
        const oldAirflow = patient.airflow;
        const oldRespiratoryRate = patient.respiratory_rate;
        
        // Generate realistic airflow changes (-5 to +5 range)
        const airflowChange = Math.floor(Math.random() * 11) - 5; // -5 to +5
        const newAirflow = Math.max(1, Math.min(100, patient.airflow + airflowChange));
        patient.airflow = newAirflow;
        
        // Generate realistic respiratory rate changes (-3 to +3 range)
        const respiratoryChange = Math.floor(Math.random() * 7) - 3; // -3 to +3
        const newRespiratoryRate = Math.max(1, Math.min(40, patient.respiratory_rate + respiratoryChange));
        patient.respiratory_rate = newRespiratoryRate;
        
        // Check for critical conditions and create alerts
        checkForCriticalConditions(patient, oldAirflow, oldRespiratoryRate);
    });
    
    // Re-render the current view
    const floorSelect = document.getElementById('floor-select');
    if (floorSelect) {
        filterPatientsByFloor(floorSelect.value);
    } else {
        renderPatients(window.allPatients);
    }
}

// Helper function to determine airflow status
function getAirflowStatus(airflow) {
    if (airflow <= 59) return 'critical';
    if (airflow <= 79) return 'warning';
    return 'normal';
}

// Helper function to determine respiratory rate status
function getRespiratoryStatus(respiratoryRate) {
    if (respiratoryRate >= 26) return 'critical';
    if (respiratoryRate >= 21) return 'warning';
    return 'normal';
}

// Check for critical conditions and create alerts
function checkForCriticalConditions(patient, oldAirflow, oldRespiratoryRate) {
    const airflowStatus = getAirflowStatus(patient.airflow);
    const respiratoryStatus = getRespiratoryStatus(patient.respiratory_rate);
    const oldAirflowStatus = getAirflowStatus(oldAirflow);
    const oldRespiratoryStatus = getRespiratoryStatus(oldRespiratoryRate);
    
    // Check if airflow became critical (red alert)
    if (airflowStatus === 'critical' && oldAirflowStatus !== 'critical') {
        createAlert(patient, 'airflow', patient.airflow, 'critical');
    }
    // Check if airflow became warning (yellow alert)
    else if (airflowStatus === 'warning' && oldAirflowStatus === 'normal') {
        createAlert(patient, 'airflow', patient.airflow, 'warning');
    }
    
    // Check if respiratory rate became critical (red alert)
    if (respiratoryStatus === 'critical' && oldRespiratoryStatus !== 'critical') {
        createAlert(patient, 'respiratory', patient.respiratory_rate, 'critical');
    }
    // Check if respiratory rate became warning (yellow alert)
    else if (respiratoryStatus === 'warning' && oldRespiratoryStatus === 'normal') {
        createAlert(patient, 'respiratory', patient.respiratory_rate, 'warning');
    }
}

// Create alert notification (warning or critical)
function createAlert(patient, metric, value, severity) {
    const alert = {
        id: Date.now(),
        patient: patient,
        metric: metric,
        value: value,
        severity: severity, // 'warning' or 'critical'
        timestamp: new Date(),
        acknowledged: false
    };
    
    notificationQueue.push(alert);
    showNextNotification();
}

// Show next notification in queue
function showNextNotification() {
    if (isNotificationShowing || notificationQueue.length === 0) return;
    
    const alert = notificationQueue[0];
    isNotificationShowing = true;
    
    showCriticalNotification(alert);
}

// Display notification popup (warning or critical)
function showCriticalNotification(alert) {
    const metricText = alert.metric === 'airflow' ? 'Airflow' : 'Respiratory Rate';
    const unit = alert.metric === 'airflow' ? '%' : ' bpm';
    
    // Set alert styling based on severity
    const isCritical = alert.severity === 'critical';
    const alertClass = isCritical ? 'critical-notification' : 'warning-notification';
    const alertIcon = isCritical ? '🚨' : '⚠️';
    const urgency = isCritical ? 
        `URGENT CARE - ${metricText.toUpperCase()}` : 
        `SO-SO - ${metricText.toUpperCase()}`;
    
    const notification = document.createElement('div');
    notification.className = alertClass;
    notification.innerHTML = `
        <div class="notification-content">
            <div class="alert-icon">${alertIcon}</div>
            <div class="alert-text">
                <div class="alert-title">${urgency}</div>
                <div class="patient-name">${alert.patient.name}</div>
                <div class="metric-value">${metricText}: ${alert.value}${unit}</div>
            </div>
            <button class="close-btn" onclick="closeNotification(${alert.id})">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove timing based on severity
    const autoRemoveTime = isCritical ? 30000 : 20000; // Critical: 30s, Warning: 20s
    setTimeout(() => {
        if (notification.parentNode && !alert.acknowledged) {
            closeNotification(alert.id);
        }
    }, autoRemoveTime);
}

// Close notification
function closeNotification(alertId) {
    const notification = document.querySelector('.critical-notification, .warning-notification');
    if (notification) {
        notification.remove();
    }
    
    // Remove from queue
    notificationQueue = notificationQueue.filter(alert => alert.id !== alertId);
    isNotificationShowing = false;
    
    // Show next notification if any
    setTimeout(() => {
        showNextNotification();
    }, 500);
}

// Acknowledge alert
function acknowledgeAlert(alertId) {
    const alert = notificationQueue.find(a => a.id === alertId);
    if (alert) {
        alert.acknowledged = true;
    }
    closeNotification(alertId);
}

// Stop airflow updates when leaving the page
window.addEventListener('beforeunload', function() {
    if (airflowUpdateInterval) {
        clearInterval(airflowUpdateInterval);
    }
});
