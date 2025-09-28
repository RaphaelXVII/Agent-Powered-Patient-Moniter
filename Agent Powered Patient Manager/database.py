import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional

class PatientDatabase:
    def __init__(self, db_path: str = "patients.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                condition TEXT NOT NULL,
                last_visit TEXT NOT NULL,
                floor INTEGER NOT NULL,
                respiratory_rate INTEGER NOT NULL,
                airflow INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create patient_vitals table for tracking historical vital signs
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patient_vitals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                respiratory_rate INTEGER NOT NULL,
                airflow INTEGER NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        # Create alerts table for tracking critical conditions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                patient_id TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                value REAL NOT NULL,
                message TEXT,
                acknowledged BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
        # Populate with initial data if database is empty
        self._populate_initial_data()
    
    def _populate_initial_data(self):
        """Populate the database with initial patient data"""
        if self.get_all_patients():
            return  # Database already has data
        
        initial_patients = [
            {"id": "P001", "name": "John Smith", "age": 45, "condition": "Diabetes", "last_visit": "2024-01-15", "floor": 1, "respiratory_rate": 18, "airflow": 85},
            {"id": "P002", "name": "Sarah Johnson", "age": 32, "condition": "Hypertension", "last_visit": "2024-01-10", "floor": 2, "respiratory_rate": 25, "airflow": 65},
            {"id": "P003", "name": "Mike Davis", "age": 58, "condition": "Heart Disease", "last_visit": "2024-01-12", "floor": 3, "respiratory_rate": 14, "airflow": 100},
            {"id": "P004", "name": "Emily Brown", "age": 28, "condition": "Asthma", "last_visit": "2024-01-08", "floor": 4, "respiratory_rate": 30, "airflow": 45},
            {"id": "P005", "name": "Robert Wilson", "age": 67, "condition": "Arthritis", "last_visit": "2024-01-05", "floor": 5, "respiratory_rate": 23, "airflow": 85},
            {"id": "P006", "name": "Russell Wilson", "age": 33, "condition": "Chicken Pox", "last_visit": "2024-01-05", "floor": 1, "respiratory_rate": 17, "airflow": 94},
            {"id": "P007", "name": "Larry Bird", "age": 72, "condition": "Respiratory Problems", "last_visit": "2024-01-05", "floor": 2, "respiratory_rate": 13, "airflow": 85},
            {"id": "P008", "name": "Kevin Durant", "age": 83, "condition": "General Checkup", "last_visit": "2024-01-05", "floor": 3, "respiratory_rate": 22, "airflow": 80}
        ]
        
        for patient in initial_patients:
            self.add_patient(patient)
    
    def add_patient(self, patient_data: Dict) -> bool:
        """Add a new patient to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO patients (id, name, age, condition, last_visit, floor, respiratory_rate, airflow)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient_data['id'],
                patient_data['name'],
                patient_data['age'],
                patient_data['condition'],
                patient_data['last_visit'],
                patient_data['floor'],
                patient_data['respiratory_rate'],
                patient_data['airflow']
            ))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error adding patient: {e}")
            return False
    
    def get_all_patients(self) -> List[Dict]:
        """Get all patients from the database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients ORDER BY name')
        patients = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return patients
    
    def get_patient_by_id(self, patient_id: str) -> Optional[Dict]:
        """Get a specific patient by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def update_patient_vitals(self, patient_id: str, respiratory_rate: int, airflow: int) -> bool:
        """Update patient vital signs and log the change"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Update patient table
            cursor.execute('''
                UPDATE patients 
                SET respiratory_rate = ?, airflow = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (respiratory_rate, airflow, patient_id))
            
            # Log the vital signs change
            cursor.execute('''
                INSERT INTO patient_vitals (patient_id, respiratory_rate, airflow)
                VALUES (?, ?, ?)
            ''', (patient_id, respiratory_rate, airflow))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error updating patient vitals: {e}")
            return False
    
    def get_patient_vitals_history(self, patient_id: str, limit: int = 10) -> List[Dict]:
        """Get historical vital signs for a patient"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patient_vitals 
            WHERE patient_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (patient_id, limit))
        
        vitals = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return vitals
    
    def add_alert(self, patient_id: str, alert_type: str, severity: str, value: float, message: str = None) -> bool:
        """Add an alert to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO alerts (patient_id, alert_type, severity, value, message)
                VALUES (?, ?, ?, ?, ?)
            ''', (patient_id, alert_type, severity, value, message))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error adding alert: {e}")
            return False
    
    def get_unacknowledged_alerts(self) -> List[Dict]:
        """Get all unacknowledged alerts"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.*, p.name as patient_name 
            FROM alerts a 
            JOIN patients p ON a.patient_id = p.id 
            WHERE a.acknowledged = FALSE 
            ORDER BY a.created_at DESC
        ''')
        
        alerts = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return alerts
    
    def acknowledge_alert(self, alert_id: int) -> bool:
        """Acknowledge an alert"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE alerts 
                SET acknowledged = TRUE 
                WHERE id = ?
            ''', (alert_id,))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.Error as e:
            print(f"Error acknowledging alert: {e}")
            return False
    
    def get_patients_by_floor(self, floor: int) -> List[Dict]:
        """Get all patients on a specific floor"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE floor = ? ORDER BY name', (floor,))
        patients = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return patients
    
    def search_patients(self, search_term: str) -> List[Dict]:
        """Search patients by name or ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            WHERE name LIKE ? OR id LIKE ? 
            ORDER BY name
        ''', (f'%{search_term}%', f'%{search_term}%'))
        
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patients
    
    def get_critical_patients(self) -> List[Dict]:
        """Get patients with critical vital signs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            WHERE respiratory_rate >= 26 OR airflow <= 59
            ORDER BY name
        ''')
        
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patients
    
    def get_warning_patients(self) -> List[Dict]:
        """Get patients with warning vital signs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            WHERE (respiratory_rate >= 21 AND respiratory_rate < 26) 
               OR (airflow <= 79 AND airflow > 59)
            ORDER BY name
        ''')
        
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patients
    
    def get_normal_patients(self) -> List[Dict]:
        """Get patients with normal vital signs"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            WHERE respiratory_rate < 21 AND airflow > 79
            ORDER BY name
        ''')
        
        patients = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return patients
