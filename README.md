# 🤖 Google Agent Powered Patient Manager

A sophisticated AI-powered Agent chat interface powered by Googles Agent Development Kit for patient management, built with Flask and SQLite database integration.

## 🚀 Features

### 🤖 **Agent Chat Interface**
- **Natural Language Processing**: Ask questions about patients data and information
- **Real-time Responses**: Get instant answers about patient status, vital signs, and alerts
- **Context**: AI understands patient IDs, floor numbers, and medical conditions

### 📊 **Patient Management**
- **Real-time Monitoring**: Automatic vital signs updates every 15 seconds
- **Critical Alerts**: Instant notifications for critical patient conditions
- **Floor Organization**: Patients organized by hospital floors and organized by condition
- **Historical Tracking**: Complete vital signs history for each patient

### 🗄️ **Database Integration**
- **SQLite Database**: Persistent storage with tracking patient data and being able to scale a larger batch of data
- **Patient Records**: Complete patient information and medical history
- **Alert Management**: Track and acknowledge critical condition alerts
- **Vital Signs Logging**: Historical tracking of respiratory rate and airflow

## 🎯 **AI Capabilities**

The AI assistant can help you with:

- **Patient Information**: "Show me patient P001 details"
- **Critical Patients**: "Show me all critical patients"
- **Floor Management**: "How many patients are on floor 1?"
- **Vital Signs**: "What are the vital signs for P002?"
- **Alerts**: "What are the current alerts?"
- **Patient Count**: "How many patients do we have?"
- **Search**: "Find patients with diabetes"

## 🛠️ **Technical Stack**

- **Backend**: Flask (Python)
- **Database**: SQLite with custom schema
- **AI Engine**: Custom "Nurse" agent powered by Google's ADK kit with patient data integration
- **Frontend**: HTML5, CSS3, JavaScript
- **Real-time Updates**: Background threading for vital signs monitoring

## 🚀 **Getting Started**

### Necessities
- Python 3.7+
- pip package manager

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
```bash
python app.py
```

The application will start on `http://localhost:5001`

### Login Credentials
- **Username**: `doctorHacks`
- **Password**: `shellhacks2025`

## 📱 **Usage**

1. **Login**: Use the provided credentials to access the system
2. **Chat Interface**: Ask questions about patients using natural language
3. **Real-time Monitoring**: Watch as vital signs update automatically
4. **Alert Management**: Respond to critical patient alerts

## 🎨 **Interface Features**

- **Modern Design**: Clean, responsive chat interface
- **Typing Indicators**: Visual feedback during AI processing
- **Message History**: Persistent chat conversation
- **Suggestion Chips**: Quick access to common queries
- **Mobile Responsive**: Works on all device sizes

## 🔧 **API Endpoints**

- `POST /api/chat` - Send messages to AI assistant
- `GET /api/patients` - Get all patients
- `GET /api/patients/critical` - Get critical patients
- `GET /api/patients/warning` - Get warning patients
- `GET /api/patients/normal` - Get normal patients
- `GET /api/patients/floor/<floor>` - Get patients by floor
- `GET /api/alerts` - Get unacknowledged alerts

## 🏥 **Patient Data**

The system comes pre-loaded with 8 sample patients across 5 floors but can scale up to 50+ patients:
- **Floor 1**: John Smith (Diabetes), Russell Wilson (Chicken Pox)
- **Floor 2**: Sarah Johnson (Hypertension), Larry Bird (Respiratory Problems)
- **Floor 3**: Mike Davis (Heart Disease), Kevin Durant (General Checkup)
- **Floor 4**: Emily Brown (Asthma)
- **Floor 5**: Robert Wilson (Arthritis)

## 🚨 **Alert System**

The system automatically monitors:
- **Respiratory Rate**: Critical ≥26 bpm, Warning ≥21 bpm
- **Airflow**: Critical ≤59%, Warning ≤79%
- **Real-time Notifications**: Instant alerts for critical conditions
- **Alert Acknowledgment**: Track and manage alert responses




---

**Built with ❤️ for healthcare innovation powered by Google Cloud**
