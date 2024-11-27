import streamlit as st
import requests

# Función para generar el plan de clase
def generate_class_plan(details):
    try:
        # Realizar la solicitud a la API
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent",
            headers={"Content-Type": "application/json"},
            json={"contents": [{"parts": [{"text": f"Generate a class plan for: {details}"}]}]},
            params={"key": "AIzaSyCpl4_OsbQ916NPSGGAJyd7ft9-eOlqKP0"},
        )

        # Convertir la respuesta a JSON
        response_json = response.json()

        # Depurar respuesta completa en la interfaz
        st.write("API Response:", response_json)

        # Manejar la estructura de la respuesta
        if "contents" in response_json and len(response_json["contents"]) > 0:
            return response_json["contents"][0]["parts"][0]["text"]
        else:
            raise KeyError("Estructura inesperada en la respuesta de la API.")
    except KeyError as e:
        st.error("La API no devolvió un resultado válido.")
        st.write("Error Details:", response_json)  # Línea de depuración
        raise e
    except requests.exceptions.RequestException as e:
        st.error("Error al conectarse con la API.")
        st.write("Detalles del error:", str(e))
        raise e

# Configurar la página principal de Streamlit
def app():
    st.title("Generador de Plan de Clase")
    st.write("Sigue las instrucciones para generar un plan de clase basado en los detalles proporcionados.")

    # Comprobar si los detalles de la clase están en el estado de sesión
    if "class_details" not in st.session_state:
        st.error("No se han proporcionado detalles de la clase. Configura los detalles primero en la pestaña de configuración.")
        return

    # Obtener los detalles de la clase desde el estado de sesión
    details = st.session_state["class_details"]

    # Mostrar los detalles en la interfaz
    st.subheader("Detalles de la Clase")
    st.json(details)

    # Botón para generar el plan de clase
    if st.button("Generar Plan de Clase"):
        st.info("Generando el plan de clase, por favor espera...")
        try:
            plan = generate_class_plan(details)
            st.subheader("Plan de Clase Generado")
            st.write(plan)
        except Exception as e:
            st.error("Ocurrió un error al generar el plan de clase.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
