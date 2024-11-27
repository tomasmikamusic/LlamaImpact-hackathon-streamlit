import streamlit as st
import requests

# Función para generar el plan de clase
def generate_class_plan(details):
    try:
        # Endpoint de la API
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyCpl4_OsbQ916NPSGGAJyd7ft9-eOlqKP0"
        payload = {
            "prompt": {
                "text": (
                    f"Genera un plan de clase en español basado en los siguientes detalles:\n"
                    f"- Materia: {details['materia']}\n"
                    f"- Nivel: {details['nivel']}\n"
                    f"- Número de estudiantes: {details['num_estudiantes']}\n"
                    f"- Tiempo disponible: {details['tiempo_disponible']} minutos\n"
                    f"- Modalidad: {details['modalidad']}\n"
                    f"- Propósito: {details['proposito']}\n"
                )
            }
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Ocurrió un error al generar el plan de clase: {e}"

# Aplicación principal
def app():
    st.title("Plan de Clase Generado")
    st.write("Aquí está el plan de clase generado basado en los detalles configurados.")

    # Verificar si los detalles de la clase existen en session_state
    if "class_details" not in st.session_state:
        st.error("No se han configurado los detalles de la clase en la sección Config. Por favor, configúralos primero.")
        return

    # Recuperar los detalles de la clase
    class_details = st.session_state["class_details"]

    # Mostrar los detalles de contexto
    st.subheader("Detalles del Contexto")
    st.json(class_details)

    # Botón para generar el plan
    if st.button("Generar Plan de Clase"):
        with st.spinner("Generando plan de clase..."):
            plan = generate_class_plan(class_details)
        st.subheader("Plan de Clase Generado")
        st.write(plan)

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
