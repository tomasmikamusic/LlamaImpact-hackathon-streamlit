import os
import streamlit as st
import json

# Función para cargar las traducciones en español
def load_translations():
    try:
        file_path = os.path.abspath('../languages/es.json')
        st.write(f"Buscando el archivo en: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"El archivo de traducción en español no se encontró en: {file_path}")
        return {}
    except json.JSONDecodeError:
        st.error("El archivo de traducción en español no es un JSON válido.")
        return {}


# Lógica principal de la aplicación
def app():
    # Cargar las traducciones directamente en español
    translations = load_translations()

    # Validar que las traducciones estén disponibles
    if not translations:
        st.error("No se pudieron cargar las traducciones. Verifica tu configuración.")
        return

    # Título y secciones principales
    if 'class_plan_generator' in translations:
        st.title(translations['class_plan_generator'])
    else:
        st.error("Falta la traducción para 'class_plan_generator'.")
        return

    st.write(translations.get('use_saved_details', "Instrucción por defecto"))

    # Detalles de la clase
    if "class_details" not in st.session_state:
        st.error(translations.get('no_class_details', "No hay detalles de clase guardados."))
        return

    class_details = st.session_state["class_details"]
    st.subheader(translations.get('class_details_title', "Detalles de la clase"))
    st.json(class_details)

    # Subir archivos de referencia
    st.sidebar.header(translations.get('upload_reference_materials', "Subir materiales de referencia"))
    uploaded_files = st.sidebar.file_uploader(
        translations.get('upload_documents', "Subir documentos"),
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    if st.button(translations.get('generate_class_plan_2', "Generar plan de clase")):
        st.write(translations.get('generated_class_plan', "Plan de clase generado"))
        st.write("Funcionalidad en desarrollo.")  # Aquí agregarías la lógica para generar el plan de clase

# Ejecutar la aplicación
if __name__ == "__main__":
    app()


