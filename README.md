# 🎙️ Voice Agent Appointment System Using VAPI

An AI-powered voice appointment system for Al Shifa Medical Center that enables patients to schedule, check availability, and cancel medical appointments through natural voice conversations.

## ✨ Features

- 📞 **Voice-Based Scheduling** - Book appointments naturally via phone calls using VAPI
- 📅 **Doctor Availability Check** - Ask about available time slots for specific dates
- ❌ **Voice Cancellation** - Cancel existing appointments through voice commands
- 📊 **Real-Time Dashboard** - Monitor all appointments via Streamlit web interface
- 🔄 **Automatic Sync** - Instant updates between voice agent and dashboard
- 🕐 **12-Hour Time Format** - User-friendly AM/PM time display

## 🛠️ Tech Stack

- **Voice AI**: [VAPI](https://vapi.ai) - Natural language voice interface
- **Backend**: FastAPI + SQLAlchemy
- **Frontend**: Streamlit
- **Database**: SQLite
- **Tunneling**: Ngrok (for VAPI webhooks)

## 📁 Project Structure

```
appointment-voice-agent/
├── backend/
│   ├── database/
│   │   └── database.py          # Database models and configuration
│   ├── routes/
│   │   └── appointment.py       # API endpoints
│   ├── schemas/
│   │   └── appointment.py       # Pydantic models
│   └── interactors/
│       └── appointment.py       # Business logic
├── frontend/
│   └── app.py                   # Streamlit dashboard
├── main.py                      # FastAPI application entry point
└── appointments.db              # SQLite database
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- [Ngrok](https://ngrok.com/) account (for VAPI integration)

### Installation

1. **Clone the repository**
   ```bash
   git clone <[your-repo-url>](https://github.com/iqbal-waqar/Vapi-voice-agent-appointment-system)
   cd appointment-voice-agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Run the backend**
   ```bash
   uv run uvicorn main:app --reload --host 127.0.0.1 --port 4444
   ```

4. **Run the frontend** (in a new terminal)
   ```bash
   cd frontend
   uv run streamlit run app.py
   ```

5. **Expose backend to internet** (in a new terminal)
   ```bash
   ngrok http 4444
   ```

## 🔗 VAPI Configuration

Configure these endpoints in your VAPI dashboard:

### 1. Schedule Appointment
- **URL**: `https://your-ngrok-url.ngrok-free.app/schedule_appointment`
- **Method**: POST
- **Parameters**: `patient_name`, `reason`, `start_time`

### 2. Check Doctor Availability
- **URL**: `https://your-ngrok-url.ngrok-free.app/list_appointment`
- **Method**: POST
- **Parameters**: `date`

### 3. Cancel Appointment
- **URL**: `https://your-ngrok-url.ngrok-free.app/cancle_appointment`
- **Method**: POST
- **Parameters**: `patient_name`, `date`

## 📊 Dashboard Access

Once running, access the Streamlit dashboard at:
```
http://localhost:8501
```

The dashboard provides:
- 📈 Overview statistics (total, active, canceled appointments)
- 📋 Recent appointments list
- ➕ Manual appointment scheduling
- 📅 Date-based appointment search
- ❌ Manual appointment cancellation

## 🎯 Usage Example

**Patient**: "I need to schedule an appointment"  
**VAPI Agent**: "Sure! What's your name?"  
**Patient**: "Ahmed"  
**VAPI Agent**: "What's the reason for your visit?"  
**Patient**: "Headache"  
**VAPI Agent**: "When would you like to schedule it?"  
**Patient**: "Tomorrow at 10 AM"  
**VAPI Agent**: "Perfect! I've scheduled your appointment for tomorrow at 10:00 AM."

✅ Appointment instantly appears on the dashboard!

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/schedule_appointment` | POST | Create new appointment |
| `/list_appointment` | POST | Get appointments for a date |
| `/cancle_appointment` | POST | Cancel patient's appointment |
| `/docs` | GET | Interactive API documentation |

## 📝 Database Schema

**Appointments Table**:
- `id` - Primary key
- `patient_name` - Patient's full name
- `reason` - Reason for visit
- `start_time` - Appointment date & time
- `canceled` - Cancellation status (boolean)
- `created_at` - Record creation timestamp

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [VAPI](https://vapi.ai) for voice AI capabilities
- Powered by [FastAPI](https://fastapi.tiangolo.com/) and [Streamlit](https://streamlit.io/)

---

**Made with ❤️ for Al Shifa Medical Center**
