import re
import json
from datetime import datetime

class NurseAgent:
    def __init__(self):
        # Medical knowledge base for common conditions
        self.medical_knowledge = {
            "diabetes": {
                "description": "Diabetes is a chronic condition that affects how your body processes blood sugar (glucose).",
                "medications": ["Insulin", "Metformin", "Glipizide"],
                "care_instructions": [
                    "Monitor blood glucose levels regularly",
                    "Maintain a balanced diet with controlled carbohydrates",
                    "Take medications as prescribed",
                    "Exercise regularly",
                    "Check feet daily for any wounds or infections"
                ],
                "vital_monitoring": "Monitor blood glucose levels 2-4 times daily, blood pressure, and weight"
            },
            "hypertension": {
                "description": "Hypertension (high blood pressure) is a condition where the force of blood against artery walls is too high.",
                "medications": ["Lisinopril", "Losartan", "Amlodipine", "Hydrochlorothiazide"],
                "care_instructions": [
                    "Monitor blood pressure daily",
                    "Limit sodium intake",
                    "Maintain regular exercise",
                    "Take medications as prescribed",
                    "Avoid smoking and excessive alcohol"
                ],
                "vital_monitoring": "Monitor blood pressure twice daily, heart rate, and weight"
            },
            "heart disease": {
                "description": "Heart disease refers to conditions that affect the heart's structure and function.",
                "medications": ["Aspirin", "Atorvastatin", "Metoprolol", "Lisinopril"],
                "care_instructions": [
                    "Monitor heart rate and blood pressure",
                    "Follow a heart-healthy diet",
                    "Exercise as recommended by physician",
                    "Take medications as prescribed",
                    "Report any chest pain or shortness of breath immediately"
                ],
                "vital_monitoring": "Monitor heart rate, blood pressure, weight, and oxygen saturation"
            },
            "asthma": {
                "description": "Asthma is a chronic respiratory condition that causes inflammation and narrowing of airways.",
                "medications": ["Albuterol inhaler", "Fluticasone", "Montelukast"],
                "care_instructions": [
                    "Use rescue inhaler as needed",
                    "Avoid known triggers (allergens, smoke)",
                    "Monitor peak flow readings",
                    "Take controller medications as prescribed",
                    "Keep emergency medications accessible"
                ],
                "vital_monitoring": "Monitor respiratory rate, peak flow, oxygen saturation, and airflow"
            },
            "arthritis": {
                "description": "Arthritis is inflammation of one or more joints, causing pain and stiffness.",
                "medications": ["Ibuprofen", "Naproxen", "Methotrexate", "Prednisone"],
                "care_instructions": [
                    "Apply heat or cold therapy as needed",
                    "Maintain gentle range of motion exercises",
                    "Take pain medications as prescribed",
                    "Use assistive devices if needed",
                    "Maintain healthy weight to reduce joint stress"
                ],
                "vital_monitoring": "Monitor pain levels, joint mobility, and medication effectiveness"
            },
            "respiratory problems": {
                "description": "Respiratory problems can include various conditions affecting breathing and lung function.",
                "medications": ["Albuterol", "Prednisone", "Azithromycin"],
                "care_instructions": [
                    "Monitor breathing patterns and oxygen levels",
                    "Use oxygen therapy as prescribed",
                    "Practice deep breathing exercises",
                    "Avoid respiratory irritants",
                    "Maintain good hydration"
                ],
                "vital_monitoring": "Monitor respiratory rate, oxygen saturation, and airflow"
            },
            "chicken pox": {
                "description": "Chicken pox is a viral infection causing itchy rash and flu-like symptoms.",
                "medications": ["Acyclovir", "Calamine lotion", "Acetaminophen"],
                "care_instructions": [
                    "Keep patient isolated to prevent spread",
                    "Apply calamine lotion for itching",
                    "Keep fingernails short to prevent scratching",
                    "Maintain good hygiene",
                    "Monitor for complications"
                ],
                "vital_monitoring": "Monitor temperature, rash progression, and signs of secondary infection"
            },
            "general checkup": {
                "description": "Routine health examination to assess overall health and detect any issues early.",
                "medications": ["Multivitamins", "Calcium supplements"],
                "care_instructions": [
                    "Maintain regular exercise routine",
                    "Follow balanced diet",
                    "Get adequate sleep",
                    "Stay hydrated",
                    "Schedule regular follow-ups"
                ],
                "vital_monitoring": "Monitor vital signs, weight, and general well-being"
            }
        }

    def process_message(self, message, patient_data):
        """Process a message about a specific patient"""
        message = message.lower()
        patient_name = patient_data['name']
        patient_condition = patient_data['condition'].lower()
        
        # Extract medical knowledge for patient's condition
        condition_info = self.medical_knowledge.get(patient_condition, {})
        
        # --- General greetings ---
        if any(word in message for word in ["hello", "hi", "hey"]):
            return f"Hello! I'm your AI Nurse Assistant for {patient_name}. I can help you with information about this patient's condition, medications, care instructions, and vital signs. How can I assist you today?"
        
        if "how are you" in message:
            return f"I'm functioning perfectly and ready to assist you with {patient_name}'s care. What would you like to know?"
        
        if any(word in message for word in ["thank", "thanks"]):
            return f"You're welcome! I'm here to help with {patient_name}'s care. Is there anything else you need to know?"
        
        # --- Patient condition queries ---
        if any(phrase in message for phrase in ["condition", "diagnosis", "what wrong", "what's wrong", "illness", "disease"]):
            if condition_info:
                return f"{patient_name} has {patient_data['condition']}. {condition_info.get('description', '')}"
            else:
                return f"{patient_name} has {patient_data['condition']}. For more detailed information about this condition, please consult with the attending physician."
        
        # --- Medication queries ---
        if any(word in message for word in ["medication", "medicine", "drug", "prescription", "pills", "tablets"]):
            if condition_info and condition_info.get('medications'):
                meds = ", ".join(condition_info['medications'])
                return f"For {patient_name}'s {patient_data['condition']}, common medications include: {meds}. Please verify the specific prescription with the attending physician."
            else:
                return f"Please check {patient_name}'s medical chart for current medications. I recommend consulting with the attending physician for the most up-to-date prescription information."
        
        # --- Care instructions ---
        if any(phrase in message for phrase in ["care instructions", "care plan", "what should i do", "how to care", "nursing care"]):
            if condition_info and condition_info.get('care_instructions'):
                instructions = "\n• ".join(condition_info['care_instructions'])
                return f"Care instructions for {patient_name} with {patient_data['condition']}:\n\n• {instructions}"
            else:
                return f"Please refer to {patient_name}'s care plan in the medical chart. For specific care instructions, consult with the attending physician or charge nurse."
        
        # --- Vital signs queries ---
        if any(phrase in message for phrase in ["vital signs", "vitals", "monitoring", "what to monitor"]):
            current_vitals = f"Current vital signs for {patient_name}:\n• Respiratory Rate: {patient_data['respiratory_rate']} bpm\n• Airflow: {patient_data['airflow']}%"
            
            if condition_info and condition_info.get('vital_monitoring'):
                monitoring = condition_info['vital_monitoring']
                return f"{current_vitals}\n\nFor {patient_data['condition']}, also monitor: {monitoring}"
            else:
                return f"{current_vitals}\n\nPlease refer to the care plan for additional monitoring requirements."
        
        # --- Specific vital sign queries ---
        if any(phrase in message for phrase in ["respiratory rate", "breathing", "breath rate"]):
            status = self._get_respiratory_status(patient_data['respiratory_rate'])
            return f"{patient_name}'s current respiratory rate is {patient_data['respiratory_rate']} bpm ({status}). Normal range is 12-20 bpm for adults."
        
        if any(phrase in message for phrase in ["airflow", "oxygen", "oxygenation"]):
            status = self._get_airflow_status(patient_data['airflow'])
            return f"{patient_name}'s current airflow is {patient_data['airflow']}% ({status}). Normal range is 80-100%."
        
        # --- Patient information queries ---
        if any(word in message for word in ["age", "how old"]):
            return f"{patient_name} is {patient_data['age']} years old."
        
        if any(phrase in message for phrase in ["last visit", "when last", "last time"]):
            return f"{patient_name}'s last visit was on {patient_data['last_visit']}."
        
        if any(word in message for word in ["floor", "room", "location"]):
            return f"{patient_name} is currently on Floor {patient_data['floor']}."
        
        if any(word in message for word in ["id", "patient id", "patient number"]):
            return f"{patient_name}'s patient ID is {patient_data['id']}."
        
        # --- Emergency/critical queries ---
        if any(word in message for word in ["emergency", "urgent", "critical", "alarm"]):
            resp_status = self._get_respiratory_status(patient_data['respiratory_rate'])
            airflow_status = self._get_airflow_status(patient_data['airflow'])
            
            if resp_status == "critical" or airflow_status == "critical":
                return f"⚠️ ATTENTION: {patient_name} has critical vital signs!\n• Respiratory Rate: {patient_data['respiratory_rate']} bpm ({resp_status})\n• Airflow: {patient_data['airflow']}% ({airflow_status})\n\nPlease notify the physician immediately and implement emergency protocols."
            elif resp_status == "warning" or airflow_status == "warning":
                return f"⚠️ WARNING: {patient_name} has concerning vital signs that require monitoring:\n• Respiratory Rate: {patient_data['respiratory_rate']} bpm ({resp_status})\n• Airflow: {patient_data['airflow']}% ({airflow_status})\n\nPlease increase monitoring frequency and consider notifying the physician."
            else:
                return f"✅ {patient_name}'s vital signs are currently within normal ranges:\n• Respiratory Rate: {patient_data['respiratory_rate']} bpm\n• Airflow: {patient_data['airflow']}%\n\nContinue routine monitoring."
        
        # --- General patient summary ---
        if any(phrase in message for phrase in ["summary", "overview", "tell me about", "patient info"]):
            resp_status = self._get_respiratory_status(patient_data['respiratory_rate'])
            airflow_status = self._get_airflow_status(patient_data['airflow'])
            
            summary = f"Patient Summary for {patient_name}:\n\n"
            summary += f"• Patient ID: {patient_data['id']}\n"
            summary += f"• Age: {patient_data['age']} years\n"
            summary += f"• Condition: {patient_data['condition']}\n"
            summary += f"• Floor: {patient_data['floor']}\n"
            summary += f"• Last Visit: {patient_data['last_visit']}\n"
            summary += f"• Current Vital Signs:\n"
            summary += f"  - Respiratory Rate: {patient_data['respiratory_rate']} bpm ({resp_status})\n"
            summary += f"  - Airflow: {patient_data['airflow']}% ({airflow_status})\n"
            
            if condition_info and condition_info.get('description'):
                summary += f"\n• Condition Details: {condition_info['description']}"
            
            return summary
        
        # --- Default response ---
        return f"I can help you with information about {patient_name}. You can ask about:\n• Patient condition and diagnosis\n• Medications and prescriptions\n• Care instructions\n• Vital signs and monitoring\n• Patient summary\n\nWhat would you like to know?"
    
    def _get_respiratory_status(self, respiratory_rate):
        """Determine respiratory rate status"""
        if respiratory_rate >= 26:
            return "critical"
        elif respiratory_rate >= 21:
            return "warning"
        else:
            return "normal"
    
    def _get_airflow_status(self, airflow):
        """Determine airflow status"""
        if airflow <= 59:
            return "critical"
        elif airflow <= 79:
            return "warning"
        else:
            return "normal"
