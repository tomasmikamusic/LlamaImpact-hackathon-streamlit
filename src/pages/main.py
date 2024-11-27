import streamlit as st
from openai import OpenAI

# Inicializar el cliente de OpenAI/Llama con la clave directamente
client = OpenAI(
    base_url="https://api.llama.ai/v1",  # Reemplaza esto si tienes una URL específica para tu API
    api_key="af0cb46bb4664d0e8b887c7d5c6693d9",  # Tu clave API
)

def generate_class_plan(class_details):
    """Genera un plan de clase utilizando la API de IA."""
    prompt = (
        f"Genera un plan de clase detallado basado en la siguiente información:\n\n"
        f"Tema de la clase: {class_details['subject']}\n"
        f"Número de estudiantes: {class_details['num_students']}\n"
        f"Tiempo disponible: {class_details['time_available']} minutos\n"
        f"Nivel: {class_details['level']}\n"
        f"Modalidad: {class_details['modality']}\n"
        f"Propósito: {class_details['purpose']}\n"
        f"Idioma: Español\n"
    )

    # Configurar la temperatura para controlar la creatividad del modelo
    temperature = 0.7
    if class_details["field"] == "STEM":
        temperature = 0.3
    elif class_details["field"] == "Ciencias Sociales":
        temperature = 0.5
    elif class_details["field"] == "Artes Liberales":
        temperature = 0.8

    # Llamar a la API para generar el plan de clase
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.2-3B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente educativo experto."},
                {"role": "user", "content": prompt},
            ],
            temperature=temperature,
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error al conectar con la API de IA: {str(e)}")
        return "No se pudo generar el plan de clase debido a un error de conexión."

def app():
    """Aplicación principal para generar planes de clase."""
    st.title("Generador de Plan de Clase")
    st.write("Sigue las instrucciones para generar un plan de clase basado en tus detalles.")

    # Verificar si los detalles de la clase están en el estado de sesión
    if "class_details" not in st.session_state:
        st.error("No se han proporcionado detalles de la clase. Configura los detalles primero.")
        return

    class_details = st.session_state["class_details"]

    st.subheader("Detalles de la Clase")
    st.json(class_details)

    # Botón para generar el plan de clase
    if st.button("Generar Plan de Clase"):
        with st.spinner("Generando el plan de clase..."):
            plan = generate_class_plan(class_details)
        st.subheader("Plan de Clase Generado")
        st.write(plan)

if __name__ == "__main__":
    app()
