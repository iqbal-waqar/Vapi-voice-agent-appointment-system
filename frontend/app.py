import streamlit as st
import requests
import datetime as dt
import pandas as pd
from typing import List, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.database import SessionLocal, Appointment, init_db

init_db()

BACKEND_URL = "http://127.0.0.1:4444"

st.set_page_config(
    page_title="Al Shifa Medical Center - Appointment Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0052a3;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #0066cc;
    }
    h1 {
        color: #0066cc;
    }
    .success-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Al Shifa Medical Center - Appointment Management Dashboard")
st.markdown("---")

with st.sidebar:
    st.header("📋 Navigation")
    page = st.radio(
        "Select Page",
        ["📊 Dashboard Overview", "➕ Schedule Appointment", "📅 View Appointments", "❌ Cancel Appointment"]
    )
    
    st.markdown("---")
    st.info("**Voice Agent Integration**\n\nThis dashboard displays appointments scheduled through the VAPI voice agent system.")

def get_all_appointments():
    db = SessionLocal()
    try:
        appointments = db.query(Appointment).order_by(Appointment.start_time.desc()).all()
        return appointments
    finally:
        db.close()

def get_appointments_for_date(date):
    db = SessionLocal()
    try:
        start_dt = dt.datetime.combine(date, dt.time.min)
        end_dt = start_dt + dt.timedelta(days=1)
        appointments = db.query(Appointment).filter(
            Appointment.start_time >= start_dt,
            Appointment.start_time < end_dt,
            Appointment.canceled == False
        ).order_by(Appointment.start_time.asc()).all()
        return appointments
    finally:
        db.close()

def get_statistics():
    db = SessionLocal()
    try:
        total = db.query(Appointment).count()
        active = db.query(Appointment).filter(Appointment.canceled == False).count()
        canceled = db.query(Appointment).filter(Appointment.canceled == True).count()
        today = dt.date.today()
        start_dt = dt.datetime.combine(today, dt.time.min)
        end_dt = start_dt + dt.timedelta(days=1)
        today_appointments = db.query(Appointment).filter(
            Appointment.start_time >= start_dt,
            Appointment.start_time < end_dt,
            Appointment.canceled == False
        ).count()
        return {
            "total": total,
            "active": active,
            "canceled": canceled,
            "today": today_appointments
        }
    finally:
        db.close()

if page == "📊 Dashboard Overview":
    st.header("📊 Dashboard Overview")
    
    stats = get_statistics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📋 Total Appointments",
            value=stats["total"]
        )
    
    with col2:
        st.metric(
            label="✅ Active Appointments",
            value=stats["active"]
        )
    
    with col3:
        st.metric(
            label="❌ Canceled Appointments",
            value=stats["canceled"]
        )
    
    with col4:
        st.metric(
            label="📅 Today's Appointments",
            value=stats["today"]
        )
    
    st.markdown("---")

    st.subheader("🕒 Recent Appointments")
    appointments = get_all_appointments()
    
    if appointments:
        data = []
        for apt in appointments[:10]:  
            data.append({
                "ID": apt.id,
                "Patient Name": apt.patient_name,
                "Reason": apt.reason,
                "Appointment Time": apt.start_time.strftime("%Y-%m-%d %I:%M %p"),
                "Status": "❌ Canceled" if apt.canceled else "✅ Active",
                "Created At": apt.created_at.strftime("%Y-%m-%d %I:%M %p")
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No appointments found in the system.")

elif page == "➕ Schedule Appointment":
    st.header("➕ Schedule New Appointment")
    
    with st.form("schedule_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            patient_name = st.text_input("Patient Name *", placeholder="Enter patient's full name")
            reason = st.text_input("Reason for Visit *", placeholder="e.g., General Checkup, Consultation")
        
        with col2:
            appointment_date = st.date_input("Appointment Date *", min_value=dt.date.today())
            appointment_time = st.time_input("Appointment Time *")
        
        submit = st.form_submit_button("📅 Schedule Appointment")
        
        if submit:
            if not patient_name or not reason:
                st.error("❌ Please fill in all required fields!")
            else:
                start_time = dt.datetime.combine(appointment_date, appointment_time)
                
                db = SessionLocal()
                try:
                    new_appointment = Appointment(
                        patient_name=patient_name,
                        reason=reason,
                        start_time=start_time
                    )
                    db.add(new_appointment)
                    db.commit()
                    db.refresh(new_appointment)
                    
                    st.success(f"✅ Appointment scheduled successfully for {patient_name} on {start_time.strftime('%Y-%m-%d at %I:%M %p')}!")
                    st.balloons()
                except Exception as e:
                    st.error(f"❌ Error scheduling appointment: {str(e)}")
                finally:
                    db.close()

elif page == "📅 View Appointments":
    st.header("📅 View Appointments")
    
    selected_date = st.date_input("Select Date", value=dt.date.today())
    
    if st.button("🔍 Search Appointments"):
        appointments = get_appointments_for_date(selected_date)
        
        if appointments:
            st.success(f"Found {len(appointments)} appointment(s) for {selected_date.strftime('%Y-%m-%d')}")
            
            for apt in appointments:
                with st.expander(f"🕐 {apt.start_time.strftime('%I:%M %p')} - {apt.patient_name}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Patient:** {apt.patient_name}")
                        st.write(f"**Reason:** {apt.reason}")
                    with col2:
                        st.write(f"**Time:** {apt.start_time.strftime('%Y-%m-%d %I:%M %p')}")
                        st.write(f"**Status:** {'❌ Canceled' if apt.canceled else '✅ Active'}")
                        st.write(f"**Created:** {apt.created_at.strftime('%Y-%m-%d %I:%M %p')}")
        else:
            st.info(f"No appointments found for {selected_date.strftime('%Y-%m-%d')}")
    
    st.markdown("---")
    
    if st.checkbox("Show All Appointments"):
        all_appointments = get_all_appointments()
        
        if all_appointments:
            data = []
            for apt in all_appointments:
                data.append({
                    "ID": apt.id,
                    "Patient Name": apt.patient_name,
                    "Reason": apt.reason,
                    "Appointment Time": apt.start_time.strftime("%Y-%m-%d %I:%M %p"),
                    "Status": "❌ Canceled" if apt.canceled else "✅ Active",
                    "Created At": apt.created_at.strftime("%Y-%m-%d %I:%M %p")
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No appointments in the system.")

elif page == "❌ Cancel Appointment":
    st.header("❌ Cancel Appointment")
    
    with st.form("cancel_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            cancel_patient_name = st.text_input("Patient Name *", placeholder="Enter patient's full name")
        
        with col2:
            cancel_date = st.date_input("Appointment Date *", value=dt.date.today())
        
        cancel_submit = st.form_submit_button("🗑️ Cancel Appointment")
        
        if cancel_submit:
            if not cancel_patient_name:
                st.error("❌ Please enter the patient name!")
            else:
                db = SessionLocal()
                try:
                    start_dt = dt.datetime.combine(cancel_date, dt.time.min)
                    end_dt = start_dt + dt.timedelta(days=1)
                    
                    appointments = db.query(Appointment).filter(
                        Appointment.patient_name == cancel_patient_name,
                        Appointment.start_time >= start_dt,
                        Appointment.start_time < end_dt,
                        Appointment.canceled == False
                    ).all()
                    
                    if not appointments:
                        st.warning(f"⚠️ No active appointments found for {cancel_patient_name} on {cancel_date.strftime('%Y-%m-%d')}")
                    else:
                        for apt in appointments:
                            apt.canceled = True
                        db.commit()
                        
                        st.success(f"✅ Successfully canceled {len(appointments)} appointment(s) for {cancel_patient_name}!")
                except Exception as e:
                    st.error(f"❌ Error canceling appointment: {str(e)}")
                finally:
                    db.close()

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>🏥 Al Shifa Medical Center Appointment System | Powered by VAPI Voice Agent</p>
    </div>
    """,
    unsafe_allow_html=True
)
