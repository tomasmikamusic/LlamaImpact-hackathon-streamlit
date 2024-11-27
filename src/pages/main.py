import os
import streamlit as st
from dotenv import load_dotenv
import PyPDF2

# Load environment variables
load_dotenv()

# Function for extracting text from PDF
def extract_text_from_pdf(uploaded_file):
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function for chunking text
def chunk_text(text, chunk_size=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))
    return chunks

# Function for processing uploaded files
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

# Function to generate the class plan
def generate_class_plan(class_details, document_chunks):
    """Generates a class plan."""
    with st.spinner("Generating class plan..."):
        # Combine document chunks into context
        if document_chunks:
            context = " ".join(document_chunks[:5])  # Use only the first 5 chunks for brevity
        else:
            context = "No reference materials provided."

        user_input = (
            f"Class topic: {class_details['subject']}, Number of students: {class_details['num_students']}, "
            f"Time available: {class_details['time_available']} minutes, Class level: {class_details['level']}, "
            f"Modality: {class_details['modality']}, Purpose: {class_details['purpose']}, "
            f"Language: {class_details.get('language', 'Spanish')}, Special instructions: {class_details.get('instructions', 'None')}, "
            f"Reference materials context: {context}"
        )

        # Simulated response for the sake of the demo
        return f"Generated class plan based on the details: {user_input}"

# Load translations
def load_translations(language):
    if language == 'eng':
        with open('../languages/en.json', 'r') as f:
            return json.load(f)
    elif language == 'esp':
        with open('../languages/es.json', 'r') as f:
            return json.load(f)

# Main application logic
def app():
    # Language selection
    language = st.session_state.get('language', {})
    translations = load_translations(language)

    # Title and instructions
    st.title(translations['class_plan_generator'])
    st.write(translations['use_saved_details'])

    if "class_details" not in st.session_state:
        st.error(translations['no_class_details'])
        return

    class_details = st.session_state["class_details"]

    st.subheader(translations['class_details_title'])
    st.json(class_details)

    # File upload for additional context
    st.sidebar.header(translations['upload_reference_materials'])
    uploaded_files = st.sidebar.file_uploader(
        translations['upload_documents'],
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    if st.button(translations['generate_class_plan_2']):
        document_chunks = process_uploaded_files(uploaded_files)

        class_plan = generate_class_plan(class_details, document_chunks)
        st.subheader(translations['generated_class_plan'])
        st.write(class_plan)

# Run app
if __name__ == "__main__":
    app()

