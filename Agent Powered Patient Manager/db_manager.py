#!/usr/bin/env python3
"""
Database Management Script for Patient Management System
This script provides utilities for managing the SQLite database
"""

import sqlite3
import sys
from database import PatientDatabase

def show_database_stats():
    """Show database statistics"""
    db = PatientDatabase()
    
    print("=== Patient Management Database Statistics ===")
    
    # Count patients
    patients = db.get_all_patients()
    print(f"Total Patients: {len(patients)}")
    
    # Count by floor
    floors = {}
    for patient in patients:
        floor = patient['floor']
        floors[floor] = floors.get(floor, 0) + 1
    
    print("\nPatients by Floor:")
    for floor in sorted(floors.keys()):
        print(f"  Floor {floor}: {floors[floor]} patients")
    
    # Count critical/warning/normal patients
    critical = db.get_critical_patients()
    warning = db.get_warning_patients()
    normal = db.get_normal_patients()
    
    print(f"\nPatient Status:")
    print(f"  Critical: {len(critical)} patients")
    print(f"  Warning: {len(warning)} patients")
    print(f"  Normal: {len(normal)} patients")
    
    # Count alerts
    alerts = db.get_unacknowledged_alerts()
    print(f"\nUnacknowledged Alerts: {len(alerts)}")
    
    if alerts:
        print("\nRecent Alerts:")
        for alert in alerts[:5]:  # Show last 5 alerts
            print(f"  - {alert['patient_name']}: {alert['alert_type']} {alert['severity']} ({alert['value']})")

def reset_database():
    """Reset the database to initial state"""
    import os
    if os.path.exists("patients.db"):
        os.remove("patients.db")
        print("Database reset successfully!")
    else:
        print("Database file not found.")

def add_sample_patient():
    """Add a sample patient for testing"""
    db = PatientDatabase()
    
    sample_patient = {
        "id": "P999",
        "name": "Test Patient",
        "age": 30,
        "condition": "Test Condition",
        "last_visit": "2024-01-20",
        "floor": 1,
        "respiratory_rate": 20,
        "airflow": 80
    }
    
    success = db.add_patient(sample_patient)
    if success:
        print("Sample patient added successfully!")
    else:
        print("Failed to add sample patient.")

def show_patient_details(patient_id):
    """Show detailed information about a specific patient"""
    db = PatientDatabase()
    patient = db.get_patient_by_id(patient_id)
    
    if patient:
        print(f"\n=== Patient Details: {patient['name']} ===")
        print(f"ID: {patient['id']}")
        print(f"Age: {patient['age']}")
        print(f"Condition: {patient['condition']}")
        print(f"Floor: {patient['floor']}")
        print(f"Last Visit: {patient['last_visit']}")
        print(f"Respiratory Rate: {patient['respiratory_rate']} bpm")
        print(f"Airflow: {patient['airflow']}%")
        
        # Show vital signs history
        vitals = db.get_patient_vitals_history(patient_id, 5)
        if vitals:
            print(f"\nRecent Vital Signs History:")
            for vital in vitals:
                print(f"  {vital['timestamp']}: RR={vital['respiratory_rate']} bpm, AF={vital['airflow']}%")
    else:
        print(f"Patient {patient_id} not found.")

def main():
    """Main function to handle command line arguments"""
    if len(sys.argv) < 2:
        print("Usage: python db_manager.py <command>")
        print("Commands:")
        print("  stats - Show database statistics")
        print("  reset - Reset database to initial state")
        print("  add_sample - Add a sample patient")
        print("  patient <id> - Show patient details")
        return
    
    command = sys.argv[1].lower()
    
    if command == "stats":
        show_database_stats()
    elif command == "reset":
        reset_database()
    elif command == "add_sample":
        add_sample_patient()
    elif command == "patient" and len(sys.argv) > 2:
        patient_id = sys.argv[2]
        show_patient_details(patient_id)
    else:
        print("Invalid command. Use 'python db_manager.py' to see available commands.")

if __name__ == "__main__":
    main()
