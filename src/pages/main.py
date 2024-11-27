import streamlit as st
import requests
import json

# Configuración de la API de Google Generative Language
API_KEY = "AIzaSyCpl4_OsbQ916NPSGGAJyd7ft9-eOlqKP0"
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Función para generar el plan de clase usando la API
def generate_class_plan(details):
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": f"Generate a class plan for: {details}"}
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(
            f"{BASE_URL}?key={API_KEY}",
            headers=headers,
            data=json.dumps(payload)
        )
        if response.status_code == 200:
            result = response.json()
            return result["contents"][0]["parts"][0]["text"]
        else:
            st.error(f"Error al conectar con la API: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API: {e}")
        return None

# Aplicación principal
def app():
    st.title("Generador de Plan de Clase")
    st.write("Proporciona los detalles de la clase para generar un plan.")

    # Formulario para ingresar detalles de la clase
    with st.form(key="class_plan_form"):
        subject = st.text_input("Tema de la clase")
        num_students = st.number_input("Número de estudiantes", min_value=1)
        time_available = st.number_input("Duración de la clase (minutos)", min_value=1)
        level = st.selectbox("Nivel de la clase", ["Primaria", "Secundaria", "Universitaria"])
        modality = st.selectbox("Modalidad", ["Presencial", "Online"])
        purpose = st.text_area("Propósito de la clase")
        submitted = st.form_submit_button("Generar Plan de Clase")

    # Generar el plan de clase si se envía el formulario
    if submitted:
        if subject and purpose:
            st.info("Generando plan de clase...")
            details = {
                "subject": subject,
                "num_students": num_students,
                "time_available": time_available,
                "level": level,
                "modality": modality,
                "purpose": purpose
            }
            plan = generate_class_plan(details)
            if plan:
                st.subheader("Plan de Clase Generado")
                st.write(plan)
        else:
            st.error("Por favor, completa todos los campos requeridos.")

# Ejecutar la app
if __name__ == "__main__":
    app()
