from flask import Flask, render_template, jsonify, request
from nurse_agent import NurseAgent

app = Flask(__name__)

# Initializes the nurse agent
nurse_agent = NurseAgent()

# Patient routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients')
def patients():
    return render_template('patients.html')

# Patient data
patients_data = [
    {"id": "P001", "name": "John Smith", "age": 45, "condition": "Diabetes", "last_visit": "2024-01-15", "floor": 1, "respiratory_rate": 18, "airflow": 85},
    {"id": "P002", "name": "Sarah Johnson", "age": 32, "condition": "Hypertension", "last_visit": "2024-01-10", "floor": 2, "respiratory_rate": 25, "airflow": 65},
    {"id": "P003", "name": "Mike Davis", "age": 58, "condition": "Heart Disease", "last_visit": "2024-01-12", "floor": 3, "respiratory_rate": 14, "airflow": 100},
    {"id": "P004", "name": "Emily Brown", "age": 28, "condition": "Asthma", "last_visit": "2024-01-08", "floor": 4, "respiratory_rate": 30, "airflow": 45},
    {"id": "P005", "name": "Robert Wilson", "age": 67, "condition": "Arthritis", "last_visit": "2024-01-05", "floor": 5, "respiratory_rate": 23, "airflow": 85},
    {"id": "P006", "name": "Russell Wilson", "age": 33, "condition": "Chicken Pox", "last_visit": "2024-01-05", "floor": 1, "respiratory_rate": 17, "airflow": 94},
    {"id": "P007", "name": "Larry Bird", "age": 72, "condition": "Respiratory Problems", "last_visit": "2024-01-05", "floor": 2, "respiratory_rate": 13, "airflow": 85},
    {"id": "P008", "name": "Kevin Durant", "age": 83, "condition": "General Checkup", "last_visit": "2024-01-05", "floor": 3, "respiratory_rate": 22, "airflow": 80}
]
# returns the ventilation status if patients airflow or respiratory rate is off
def get_ventilation_status(patient):
    if patient['respiratory_rate'] >= 26 or patient['airflow'] <= 59:
        return 'critical'
    elif patient['respiratory_rate'] >= 21 or patient['airflow'] <= 79:
        return 'warning'
    else:
        return 'normal'
#grabs the # of patients
@app.route('/api/patients')
def get_patients():
    return jsonify(patients_data)

@app.route('/api/patient-chat', methods=['POST'])
def handle_patient_chat():
    """Handle chat messages for specific patients"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        patient_id = data.get('patient_id', '').strip()
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        if not patient_id:
            return jsonify({'error': 'No patient ID provided'}), 400
        
        # Finds the patient
        patient = None
        for p in patients_data:
            if p['id'] == patient_id:
                patient = p
                break
        
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404
        
        print(f"Received message for {patient['name']}: {message}")
        
        # Process message with nurse agent
        response = nurse_agent.process_message(message, patient)
        
        return jsonify({'message': response})
        
    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({'message': 'Sorry, I encountered an error processing your request. Please try again.'}), 500
# grabbing the patients ID's
@app.route('/patient/<patient_id>')
def patient_detail(patient_id):
    # Find the specific patient
    patient = None
    for p in patients_data:
        if p['id'] == patient_id:
            patient = p
            break
    
    if patient:
        return render_template('patient_detail.html', patient=patient)
    else:
        return "Patient not found", 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)