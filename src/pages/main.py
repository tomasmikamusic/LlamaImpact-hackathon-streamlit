import streamlit as st
import requests
import json

# API endpoint y clave (asegúrate de usar la clave correcta)
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
API_KEY = "AIzaSyCpl4_OsbQ916NPSGGAJyd7ft9-eOlqKP0"

def generate_class_plan(class_details):
    """
    Genera un plan de clase usando la API de IA.
    """
    # Asegúrate de que los detalles se conviertan a texto entendible para la API
    prompt = (
        f"Genera un plan de clase sobre el tema '{class_details['subject']}' para {class_details['num_students']} "
        f"estudiantes. Duración: {class_details['time_available']} minutos. Nivel: {class_details['level']}. "
        f"Modalidad: {class_details['modality']}. Propósito: {class_details['purpose']}. "
        f"Instrucciones adicionales: {class_details.get('instructions', 'Ninguna')}. "
    )

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }

    try:
        response = requests.post(
            f"{API_URL}?key={API_KEY}",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload),
        )
        response.raise_for_status()
        result = response.json()

        # Verifica si el resultado tiene la estructura correcta
        if "contents" in result and result["contents"]:
            return result["contents"][0]["parts"][0]["text"]
        else:
            st.error("La API no devolvió un resultado válido.")
            return "No se pudo generar el plan de clase."
    except requests.exceptions.RequestException as e:
        st.error(f"Error al conectar con la API de IA: {e}")
        return "No se pudo conectar con la API."

def app():
    st.title("Generador de Plan de Clase")
    st.write("Genera un plan de clase basado en los detalles proporcionados en Configuración.")

    # Verifica si hay detalles configurados
    if "class_details" not in st.session_state:
        st.error("No se han configurado detalles de la clase. Ve a Configuración primero.")
        return

    class_details = st.session_state["class_details"]

    # Muestra los detalles de la clase
    st.subheader("Detalles de la Clase")
    st.json(class_details)

    # Botón para generar el plan de clase
    if st.button("Generar Plan de Clase"):
        st.write("Generando el plan de clase...")
        plan = generate_class_plan(class_details)
        st.subheader("Plan de Clase Generado")
        st.write(plan)

if __name__ == "__main__":
    app()
