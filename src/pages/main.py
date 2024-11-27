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
    st.title("Plan de Clase Generado")
    
    # Verificar si los detalles están en el estado de sesión
    if "class_details" not in st.session_state or not st.session_state["class_details"]:
        st.error("No se encontraron detalles de la clase. Configúralos primero en la pestaña 'Config'.")
        return
    
    # Mostrar resumen del contexto
    st.write("### Resumen de los detalles de la clase:")
    st.json(st.session_state["class_details"])
    
    # Generar el plan de clase
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
