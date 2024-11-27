import streamlit as st
import os
import PyPDF2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Configuración de la página
st.set_page_config(page_title="Generador de Plan de Clase", page_icon="🎓")

# Función para extraer texto de PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Función para dividir el texto en fragmentos
def chunk_text(text, chunk_size=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# Función para procesar archivos subidos
def process_uploaded_files(uploaded_files):
    document_chunks = []
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
            chunks = chunk_text(text)
            document_chunks.extend(chunks)
        else:
            text = uploaded_file.read().decode("utf-8")
            chunks = chunk_text(text)
            document_chunks.extend(chunks)
    return document_chunks

# Función para generar similitudes de texto
def find_relevant_chunks(embeddings, query_embedding, chunks, top_k=3):
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

# Función principal de la aplicación
def app():
    st.title("Generador de Plan de Clase")
    st.write("Sigue las instrucciones para generar un plan de clase basado en tus detalles.")

    # Verifica si existen detalles de la clase
    if "class_details" not in st.session_state:
        st.error("No se han proporcionado detalles de la clase. Configura los detalles primero.")
        return

    class_details = st.session_state["class_details"]

    st.subheader("Detalles de la Clase")
    st.json(class_details)

    # Subir archivos para contexto adicional
    st.sidebar.header("Subir materiales de referencia")
    uploaded_files = st.sidebar.file_uploader(
        "Sube tus documentos en formato PDF o texto",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    if st.button("Generar Plan de Clase"):
        document_chunks = process_uploaded_files(uploaded_files)
        if document_chunks:
            st.write(f"Se procesaron {len(document_chunks)} fragmentos de documentos.")

        # Generar plan (simulación para esta versión simplificada)
        st.subheader("Plan de Clase Generado")
        st.write("Aquí estaría el plan de clase generado basado en los detalles proporcionados.")

# Ejecutar la aplicación
if __name__ == "__main__":
    app()
