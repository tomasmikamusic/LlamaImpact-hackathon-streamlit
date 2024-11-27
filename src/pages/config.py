import streamlit as st

# Configuración de la página
st.set_page_config(page_title="Configuración de Clase", page_icon="🛠️")

# Función principal
def app():
    st.title("Configuración de Clase")
    st.write("Proporciona los detalles de la clase para generar un plan.")

    # Formularios para configurar detalles de la clase
    with st.form(key="class_details_form"):
        subject = st.text_input("Tema de la clase", value="Matemáticas")
        num_students = st.number_input("Número de estudiantes", min_value=1, value=20)
        time_available = st.number_input("Tiempo disponible (minutos)", min_value=1, value=60)
        level = st.selectbox("Nivel de la clase", ["Primaria", "Secundaria", "Universidad"])
        modality = st.selectbox("Modalidad", ["Presencial", "Virtual"])
        purpose = st.text_area("Propósito de la clase", value="Enseñar conceptos básicos.")
        field = st.selectbox("Campo", ["STEM", "Ciencias Sociales", "Humanidades"])
        instructions = st.text_area("Instrucciones especiales", value="Ninguna")

        submit_button = st.form_submit_button("Guardar detalles")

    # Guardar detalles en la sesión
    if submit_button:
        st.session_state["class_details"] = {
            "subject": subject,
            "num_students": num_students,
            "time_available": time_available,
            "level": level,
            "modality": modality,
            "purpose": purpose,
            "field": field,
            "instructions": instructions,
        }
        st.success("¡Detalles de la clase guardados exitosamente!")

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
