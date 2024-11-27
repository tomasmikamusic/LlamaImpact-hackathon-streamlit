import openai
import streamlit as st
import os

# Configurar la clave de la API de OpenAI
openai.api_key = "Your_API_Key"  # Reemplaza con tu clave real

# Función para generar el plan de clase utilizando la API de OpenAI
def generate_class_plan(class_details):
    """Genera un plan de clase basado en los detalles proporcionados."""
    try:
        st.spinner("Generando el plan de clase...")
        user_input = (
            f"Class topic: {class_details['subject']}, "
            f"Number of students: {class_details['num_students']}, "
            f"Time available: {class_details['time_available']} minutes, "
            f"Class level: {class_details['level']}, "
            f"Modality: {class_details['modality']}, "
            f"Purpose: {class_details['purpose']}, "
            f"Language: Spanish, "
            f"Special instructions: {class_details.get('instructions', 'None')}."
        )
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for generating class plans."},
                {"role": "user", "content": f"Generate a class plan with the following details: {user_input}"}
            ],
            temperature=0.7,
        )
        return response.choices[0].message["content"]
    except openai.error.OpenAIError as e:
        st.error(f"Error al conectar con la API de OpenAI: {e}")
        return None

# Aplicación principal
def app():
    st.title("Generador de Plan de Clase")
    st.write("Sigue las instrucciones para generar un plan de clase basado en tus detalles.")

    # Validar si los detalles de la clase están en la sesión
    if "class_details" not in st.session_state:
        st.error("No se han proporcionado detalles de la clase. Configura los detalles primero.")
        return

    # Mostrar detalles de la clase
    class_details = st.session_state["class_details"]
    st.subheader("Detalles de la Clase")
    st.json(class_details)

    # Botón para generar el plan de clase
    if st.button("Generar Plan de Clase"):
        plan = generate_class_plan(class_details)
        if plan:
            st.subheader("Plan de Clase Generado")
            st.write(plan)

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
