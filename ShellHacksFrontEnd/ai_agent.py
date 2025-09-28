import json
import re
from typing import Dict, List, Optional
from database import PatientDatabase

class PatientAIAgent:
    def __init__(self, db: PatientDatabase):
        self.db = db
        self.context = {}
    
    def process_message(self, message: str) -> str:
        """Process user message and return AI response"""
        message_lower = message.lower()
        
        # Extract intent and entities
        intent = self._extract_intent(message_lower)
        entities = self._extract_entities(message_lower)
        
        # Generate response based on intent
        if intent == "critical_patients":
            return self._get_critical_patients_response()
        elif intent == "floor_info":
            floor = entities.get('floor')
            return self._get_floor_info_response(floor)
        elif intent == "patient_details":
            patient_id = entities.get('patient_id')
            return self._get_patient_details_response(patient_id)
        elif intent == "alerts":
            return self._get_alerts_response()
        elif intent == "patient_count":
            return self._get_patient_count_response()
        elif intent == "vital_signs":
            patient_id = entities.get('patient_id')
            return self._get_vital_signs_response(patient_id)
        elif intent == "search_patients":
            search_term = entities.get('search_term')
            return self._search_patients_response(search_term)
        elif intent == "greeting":
            return self._get_greeting_response()
        elif intent == "help":
            return self._get_help_response()
        else:
            return self._get_general_response(message)
    
    def _extract_intent(self, message: str) -> str:
        """Extract intent from user message"""
        if any(word in message for word in ['critical', 'urgent', 'emergency', 'danger']):
            return "critical_patients"
        elif any(word in message for word in ['floor', 'level']):
            return "floor_info"
        elif any(word in message for word in ['patient', 'details', 'info', 'information']):
            return "patient_details"
        elif any(word in message for word in ['alert', 'warning', 'notification']):
            return "alerts"
        elif any(word in message for word in ['how many', 'count', 'total', 'number of']):
            return "patient_count"
        elif any(word in message for word in ['vital', 'signs', 'respiratory', 'airflow', 'breathing']):
            return "vital_signs"
        elif any(word in message for word in ['search', 'find', 'look for']):
            return "search_patients"
        elif any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
            return "greeting"
        elif any(word in message for word in ['help', 'what can you do', 'commands']):
            return "help"
        else:
            return "general"
    
    def _extract_entities(self, message: str) -> Dict[str, str]:
        """Extract entities from user message"""
        entities = {}
        
        # Extract patient ID (P001, P002, etc.)
        patient_id_match = re.search(r'\bp\d{3}\b', message)
        if patient_id_match:
            entities['patient_id'] = patient_id_match.group().upper()
        
        # Extract floor number
        floor_match = re.search(r'\bfloor\s*(\d+)\b', message)
        if floor_match:
            entities['floor'] = int(floor_match.group(1))
        
        # Extract search terms
        if 'search' in message or 'find' in message:
            # Extract words after search/find
            search_match = re.search(r'(?:search|find)\s+(?:for\s+)?(.+)', message)
            if search_match:
                entities['search_term'] = search_match.group(1).strip()
        
        return entities
    
    def _get_critical_patients_response(self) -> str:
        """Get response about critical patients"""
        critical_patients = self.db.get_critical_patients()
        
        if not critical_patients:
            return "✅ Great news! There are currently no critical patients requiring immediate attention."
        
        response = f"🚨 **Critical Patients Alert**\n\nFound {len(critical_patients)} critical patients:\n\n"
        
        for patient in critical_patients:
            status = []
            if patient['respiratory_rate'] >= 26:
                status.append(f"High respiratory rate ({patient['respiratory_rate']} bpm)")
            if patient['airflow'] <= 59:
                status.append(f"Low airflow ({patient['airflow']}%)")
            
            response += f"• **{patient['name']}** (ID: {patient['id']})\n"
            response += f"  - Floor: {patient['floor']}\n"
            response += f"  - Condition: {patient['condition']}\n"
            response += f"  - Issues: {', '.join(status)}\n\n"
        
        return response
    
    def _get_floor_info_response(self, floor: Optional[int]) -> str:
        """Get response about floor information"""
        if floor is None:
            # Get overview of all floors
            patients = self.db.get_all_patients()
            floor_counts = {}
            for patient in patients:
                floor_num = patient['floor']
                floor_counts[floor_num] = floor_counts.get(floor_num, 0) + 1
            
            response = "🏥 **Floor Overview**\n\n"
            for floor_num in sorted(floor_counts.keys()):
                response += f"**Floor {floor_num}**: {floor_counts[floor_num]} patients\n"
            
            return response
        
        # Get specific floor info
        floor_patients = self.db.get_patients_by_floor(floor)
        
        if not floor_patients:
            return f"Floor {floor} is currently empty - no patients assigned."
        
        response = f"🏥 **Floor {floor} Information**\n\n"
        response += f"Total patients: {len(floor_patients)}\n\n"
        
        for patient in floor_patients:
            status_icon = "🟢" if patient['respiratory_rate'] < 21 and patient['airflow'] > 79 else "🟡" if patient['respiratory_rate'] < 26 and patient['airflow'] > 59 else "🔴"
            response += f"{status_icon} **{patient['name']}** (ID: {patient['id']})\n"
            response += f"   - Condition: {patient['condition']}\n"
            response += f"   - Respiratory Rate: {patient['respiratory_rate']} bpm\n"
            response += f"   - Airflow: {patient['airflow']}%\n\n"
        
        return response
    
    def _get_patient_details_response(self, patient_id: Optional[str]) -> str:
        """Get detailed patient information"""
        if patient_id is None:
            return "Please specify a patient ID (e.g., P001, P002) to get detailed information."
        
        patient = self.db.get_patient_by_id(patient_id)
        
        if not patient:
            return f"❌ Patient {patient_id} not found. Please check the patient ID and try again."
        
        # Get vital signs history
        vitals_history = self.db.get_patient_vitals_history(patient_id, 5)
        
        response = f"👤 **Patient Details: {patient['name']}**\n\n"
        response += f"**Basic Information:**\n"
        response += f"• ID: {patient['id']}\n"
        response += f"• Age: {patient['age']} years\n"
        response += f"• Condition: {patient['condition']}\n"
        response += f"• Floor: {patient['floor']}\n"
        response += f"• Last Visit: {patient['last_visit']}\n\n"
        
        response += f"**Current Vital Signs:**\n"
        response += f"• Respiratory Rate: {patient['respiratory_rate']} bpm\n"
        response += f"• Airflow: {patient['airflow']}%\n\n"
        
        # Determine status
        if patient['respiratory_rate'] >= 26 or patient['airflow'] <= 59:
            response += "🚨 **Status: CRITICAL** - Requires immediate attention\n\n"
        elif patient['respiratory_rate'] >= 21 or patient['airflow'] <= 79:
            response += "⚠️ **Status: WARNING** - Monitor closely\n\n"
        else:
            response += "✅ **Status: NORMAL** - Stable condition\n\n"
        
        if vitals_history:
            response += f"**Recent Vital Signs History:**\n"
            for vital in vitals_history[:3]:  # Show last 3 readings
                response += f"• {vital['timestamp'][:16]}: RR={vital['respiratory_rate']} bpm, AF={vital['airflow']}%\n"
        
        return response
    
    def _get_alerts_response(self) -> str:
        """Get current alerts information"""
        alerts = self.db.get_unacknowledged_alerts()
        
        if not alerts:
            return "✅ No unacknowledged alerts at this time. All patients are being monitored normally."
        
        response = f"🚨 **Current Alerts**\n\n"
        response += f"Found {len(alerts)} unacknowledged alerts:\n\n"
        
        for alert in alerts[:10]:  # Show max 10 alerts
            severity_icon = "🔴" if alert['severity'] == 'critical' else "🟡"
            response += f"{severity_icon} **{alert['patient_name']}**\n"
            response += f"   - Type: {alert['alert_type'].replace('_', ' ').title()}\n"
            response += f"   - Severity: {alert['severity'].title()}\n"
            response += f"   - Value: {alert['value']}\n"
            response += f"   - Time: {alert['created_at'][:16]}\n\n"
        
        if len(alerts) > 10:
            response += f"... and {len(alerts) - 10} more alerts"
        
        return response
    
    def _get_patient_count_response(self) -> str:
        """Get patient count information"""
        all_patients = self.db.get_all_patients()
        critical = self.db.get_critical_patients()
        warning = self.db.get_warning_patients()
        normal = self.db.get_normal_patients()
        
        response = f"📊 **Patient Statistics**\n\n"
        response += f"**Total Patients:** {len(all_patients)}\n"
        response += f"• 🟢 Normal: {len(normal)}\n"
        response += f"• 🟡 Warning: {len(warning)}\n"
        response += f"• 🔴 Critical: {len(critical)}\n\n"
        
        # Floor breakdown
        floor_counts = {}
        for patient in all_patients:
            floor_num = patient['floor']
            floor_counts[floor_num] = floor_counts.get(floor_num, 0) + 1
        
        response += f"**By Floor:**\n"
        for floor_num in sorted(floor_counts.keys()):
            response += f"• Floor {floor_num}: {floor_counts[floor_num]} patients\n"
        
        return response
    
    def _get_vital_signs_response(self, patient_id: Optional[str]) -> str:
        """Get vital signs information"""
        if patient_id is None:
            return "Please specify a patient ID to get vital signs information (e.g., 'vital signs for P001')."
        
        patient = self.db.get_patient_by_id(patient_id)
        
        if not patient:
            return f"❌ Patient {patient_id} not found."
        
        vitals_history = self.db.get_patient_vitals_history(patient_id, 10)
        
        response = f"💓 **Vital Signs: {patient['name']}**\n\n"
        response += f"**Current Readings:**\n"
        response += f"• Respiratory Rate: {patient['respiratory_rate']} bpm\n"
        response += f"• Airflow: {patient['airflow']}%\n\n"
        
        # Status assessment
        rr_status = "Normal" if patient['respiratory_rate'] < 21 else "Warning" if patient['respiratory_rate'] < 26 else "Critical"
        af_status = "Normal" if patient['airflow'] > 79 else "Warning" if patient['airflow'] > 59 else "Critical"
        
        response += f"**Status Assessment:**\n"
        response += f"• Respiratory Rate: {rr_status}\n"
        response += f"• Airflow: {af_status}\n\n"
        
        if vitals_history:
            response += f"**Recent History (Last {len(vitals_history)} readings):**\n"
            for vital in vitals_history:
                response += f"• {vital['timestamp'][:16]}: RR={vital['respiratory_rate']} bpm, AF={vital['airflow']}%\n"
        
        return response
    
    def _search_patients_response(self, search_term: Optional[str]) -> str:
        """Search for patients"""
        if not search_term:
            return "Please specify what you're looking for (e.g., 'search for John' or 'find patients with diabetes')."
        
        patients = self.db.search_patients(search_term)
        
        if not patients:
            return f"❌ No patients found matching '{search_term}'. Please try a different search term."
        
        response = f"🔍 **Search Results for '{search_term}'**\n\n"
        response += f"Found {len(patients)} patient(s):\n\n"
        
        for patient in patients:
            status_icon = "🟢" if patient['respiratory_rate'] < 21 and patient['airflow'] > 79 else "🟡" if patient['respiratory_rate'] < 26 and patient['airflow'] > 59 else "🔴"
            response += f"{status_icon} **{patient['name']}** (ID: {patient['id']})\n"
            response += f"   - Floor: {patient['floor']}\n"
            response += f"   - Condition: {patient['condition']}\n"
            response += f"   - Age: {patient['age']}\n"
            response += f"   - Status: RR={patient['respiratory_rate']} bpm, AF={patient['airflow']}%\n\n"
        
        return response
    
    def _get_greeting_response(self) -> str:
        """Get greeting response"""
        patient_count = len(self.db.get_all_patients())
        critical_count = len(self.db.get_critical_patients())
        
        response = f"👋 Hello! I'm your AI Patient Assistant.\n\n"
        response += f"Currently monitoring {patient_count} patients"
        
        if critical_count > 0:
            response += f" with {critical_count} critical cases requiring attention"
        
        response += f".\n\nI can help you with:\n"
        response += f"• Patient information and status\n"
        response += f"• Vital signs monitoring\n"
        response += f"• Floor assignments\n"
        response += f"• Critical alerts\n"
        response += f"• Medical conditions\n\n"
        response += f"What would you like to know?"
        
        return response
    
    def _get_help_response(self) -> str:
        """Get help response"""
        response = f"🤖 **AI Patient Assistant Help**\n\n"
        response += f"**Available Commands:**\n\n"
        response += f"• **Patient Info**: 'Show me patient P001' or 'Details for P002'\n"
        response += f"• **Critical Patients**: 'Show critical patients' or 'Any emergencies?'\n"
        response += f"• **Floor Info**: 'How many patients on floor 1?' or 'Floor 2 patients'\n"
        response += f"• **Vital Signs**: 'Vital signs for P001' or 'Breathing status'\n"
        response += f"• **Alerts**: 'Current alerts' or 'Any warnings?'\n"
        response += f"• **Patient Count**: 'How many patients?' or 'Total count'\n"
        response += f"• **Search**: 'Find John' or 'Search for diabetes'\n\n"
        response += f"**Examples:**\n"
        response += f"• 'Show me all critical patients'\n"
        response += f"• 'Patient P001 details'\n"
        response += f"• 'How many patients on floor 3?'\n"
        response += f"• 'What are the current alerts?'\n"
        response += f"• 'Vital signs for P002'\n\n"
        response += f"Just ask naturally - I understand context!"
        
        return response
    
    def _get_general_response(self, message: str) -> str:
        """Get general response for unrecognized queries"""
        response = f"I understand you're asking about '{message}', but I'm not sure how to help with that specific request.\n\n"
        response += f"I specialize in patient information and can help you with:\n"
        response += f"• Patient details and status\n"
        response += f"• Critical patient alerts\n"
        response += f"• Floor assignments\n"
        response += f"• Vital signs monitoring\n\n"
        response += f"Try asking something like:\n"
        response += f"• 'Show me critical patients'\n"
        response += f"• 'Patient P001 details'\n"
        response += f"• 'How many patients on floor 1?'\n"
        response += f"• 'What are the current alerts?'\n\n"
        response += f"Or type 'help' for more options!"
        
        return response
