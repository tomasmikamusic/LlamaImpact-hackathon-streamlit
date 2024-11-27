import streamlit as st
import requests

# Función para generar el plan de clase
def generate_class_plan(details):
    try:
        # Endpoint de la API
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyCpl4_OsbQ916NPSGGAJyd7ft9-eOlqKP0"
        
        # Datos de entrada para la API
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Genera un plan de clase con los siguientes detalles: {details}"}
                    ]
                }
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        
        # Solicitud a la API
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        # Verificar si la respuesta contiene candidatos
        if "candidates" in response_data:
            plan_text = response_data["candidates"][0]["content"]["parts"][0]["text"]
            return plan_text
        else:
            st.error("La API no devolvió un resultado válido.")
            st.json(response_data)  # Mostrar la respuesta para depuración
            return None
    except Exception as e:
        st.error(f"Ocurrió un error al generar el plan de clase: {str(e)}")
        return None

# Función principal de la app
def app():
    st.title("Generador de Plan de Clase")
    st.write("Proporciona los detalles necesarios para generar un plan de clase personalizado.")
    
    if "class_details" not in st.session_state:
        st.session_state["class_details"] = {}
    
    # Formulario para ingresar detalles de la clase
    with st.form("class_details_form"):
        subject = st.text_input("Materia", key="subject")
        level = st.text_input("Nivel", key="level")
        num_students = st.number_input("Número de estudiantes", min_value=1, step=1, key="num_students")
        time_available = st.number_input("Tiempo disponible (en minutos)", min_value=1, step=1, key="time_available")
        modality = st.text_input("Modalidad (presencial/virtual)", key="modality")
        purpose = st.text_input("Propósito de la clase", key="purpose")
        submit_button = st.form_submit_button("Guardar detalles")
    
    # Guardar detalles en el estado de sesión
    if submit_button:
        st.session_state["class_details"] = {
            "subject": subject,
            "level": level,
            "num_students": num_students,
            "time_available": time_available,
            "modality": modality,
            "purpose": purpose,
        }
        st.success("Detalles guardados exitosamente.")
    
    # Mostrar detalles guardados
    if st.session_state["class_details"]:
        st.write("### Detalles de la clase:")
        st.json(st.session_state["class_details"])
        
        # Generar plan de clase
        if st.button("Generar Plan de Clase"):
            with st.spinner("Generando plan de clase..."):
                details = st.session_state["class_details"]
                details_str = (
                    f"Materia: {details['subject']}, Nivel: {details['level']}, "
                    f"Número de estudiantes: {details['num_students']}, Tiempo disponible: {details['time_available']} minutos, "
                    f"Modalidad: {details['modality']}, Propósito: {details['purpose']}"
                )
                plan = generate_class_plan(details_str)
                if plan:
                    st.subheader("Plan de Clase Generado")
                    st.write(plan)

# Ejecutar la app
if __name__ == "__main__":
    app()
