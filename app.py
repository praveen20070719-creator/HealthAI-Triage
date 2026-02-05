import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from brain import get_triage_advice

# --- 1. Initializing MediaPipe (The 'Pro' Vision Look) ---
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1)
mp_drawing = mp.solutions.drawing_utils

st.set_page_config(page_title="AI Health Triage", layout="wide", page_icon="🚑")

# --- 2. Title & Header ---
st.title("🚑 Urgency-Aware AI Triage & Care Navigation")
st.write("Real-time assessment for emergency medical support.")

# Create two columns for the dashboard
col1, col2 = st.columns([1, 1])

# --- 3. Column 1: Live Assessment (Input) ---
with col1:
    st.header("1. Patient Input")
    
    # Live Camera Input
    img_file_buffer = st.camera_input("Scan face for vitals or take injury photo")
    
    # Symptom Text (Support for Tanglish)
    user_symptoms = st.text_area(
        "Describe Symptoms:", 
        placeholder="Example: Enaku romba nenju valikudhu, sariya moochu vida mudiyala...",
        help="You can type in English or Tanglish."
    )

# --- 4. Column 2: AI Diagnosis (Output) ---
with col2:
    st.header("2. AI Analysis Dashboard")
    
    if st.button("🚀 Start AI Triage", use_container_width=True):
        if user_symptoms:
            with st.spinner('AI Nurse is evaluating...'):
                # Call Gemini Logic from brain.py
                result = get_triage_advice(user_symptoms)
                
                # Visualizing Urgency Level
                if "Red" in result:
                    st.error("### 🚨 STATUS: EMERGENCY (RED)")
                    st.warning("Immediate medical attention required.")
                    st.button("📲 CALL NEAREST AMBULANCE", type="primary")
                elif "Yellow" in result:
                    st.warning("### ⚠️ STATUS: URGENT (YELLOW)")
                    st.info("Visit a clinic within 4-6 hours.")
                else:
                    st.success("### ✅ STATUS: STABLE (GREEN)")
                
                # Show the detailed JSON or summary
                st.markdown("### Triage Summary")
                st.write(result)
        else:
            st.warning("Please enter symptoms before starting the triage.")

# --- 5. Footer Navigation Map ---
st.markdown("---")
st.subheader("📍 Nearest Hospital Navigation")
# Hardcoded KSR / Tiruchengode area for the demo
map_data = {"lat": [11.3615], "lon": [77.9300]} 
st.map(map_data)
