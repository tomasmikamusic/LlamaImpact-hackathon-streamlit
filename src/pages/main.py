import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import PyPDF2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    base_url=os.getenv("LLAMA_BASE_URL"),
    api_key=os.getenv("LLAMA_API_KEY"),
)

# Load GloVe embeddings


def load_glove_model(glove_file=os.path.join("..", "data", "glove.6B.50d.txt")):
    """Loads the GloVe model from a file."""
    embeddings_index = {}
    with open(glove_file, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
    return embeddings_index


glove_model = load_glove_model()  # Ensure the file path is correct


def get_embedding_glove(text, embeddings_index):
    """Generates a GloVe embedding for a given text."""
    words = text.split()
    embeddings = [
        embeddings_index.get(word, np.zeros(50)) for word in words
    ]  # Default to zero vector if word not in vocab
    if embeddings:
        # Average word vectors to get sentence embedding
        return np.mean(embeddings, axis=0)
    else:
        return np.zeros(50)  # Return zero vector for empty input

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

# Function to generate embeddings using GloVe


def generate_embeddings(chunks):
    embeddings = []
    for chunk in chunks:
        embedding = get_embedding_glove(chunk, glove_model)
        embeddings.append(embedding)
    return embeddings


def find_relevant_chunks(embeddings, query_embedding, chunks, top_k=3):
    similarities = cosine_similarity([query_embedding], embeddings)[0]
    top_indices = similarities.argsort()[-top_k:][::-1]
    return [chunks[i] for i in top_indices]


# Function to generate the class plan


def generate_class_plan(class_details, embeddings, document_chunks):
    """Generates a class plan using the OpenAI Llama API."""
    with st.spinner("Generating class plan..."):
        # Process uploaded files
        # document_chunks = process_uploaded_files(uploaded_files)
        # reference_materials = (
        #     "None provided."
        #     if not document_chunks
        #     else f"{len(document_chunks)} chunks extracted from uploaded files."
        # )

        # Combine all embeddings into a single vector
        if embeddings:
            # Use combined embedding to retrieve relevant chunks
            query_embedding = get_embedding_glove("class topic", glove_model)
            relevant_chunks = find_relevant_chunks(
                embeddings, query_embedding, document_chunks)
            context = " ".join(relevant_chunks)
        else:
            context = "No reference materials provided."

        print(context)

        user_input = (
            f"Class topic: {class_details['subject']}, Number of students: {
                class_details['num_students']}, "
            f"Time available: {class_details['time_available']} minutes, Class level: {
                class_details['level']}, "
            f"Modality: {class_details['modality']}, Purpose: {
                class_details['purpose']}, "
            f"Language: {class_details.get('language', 'English')}, Special instructions: {
                class_details.get('instructions', 'None')}, "
            f"Reference materials context: {context}"
        )

        temp = 0.7

        if class_details["field"] == "STEM":
            temp = 0.2
        elif class_details["field"] == "Social Sciences":
            temp = 0.65
        elif class_details["field"] == "Liberal Arts":
            temp = 0.8

        # Use OpenAI client for generating class plans
        completion = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": os.getenv("SYSTEM_PROMPT")},
                {"role": "user", "content": f"Please generate a class plan using the following information: {
                    user_input}"},
            ],
            temperature=temp,
        )

        return completion.choices[0].message.content

# Main app logic


def app():
    st.title("Class Plan Generator")
    st.write("Use the saved class details to generate your class plan.")

    if "class_details" not in st.session_state:
        st.error("No class details found! Please fill in the Welcome Page first.")
        return

    class_details = st.session_state["class_details"]

    st.subheader("Class Details:")
    st.json(class_details)

    # File upload for additional context
    st.sidebar.header("Upload Reference Materials")
    uploaded_files = st.sidebar.file_uploader(
        "Upload documents (optional):",
        type=["txt", "pdf"],
        accept_multiple_files=True,
    )

    if st.button("Generate Class Plan"):
        document_chunks = process_uploaded_files(uploaded_files)
        # Optionally, generate embeddings
        embeddings = []
        if document_chunks:
            with st.spinner("Generating embeddings..."):
                embeddings = generate_embeddings(document_chunks)
                st.write(f"Generated embeddings for {len(embeddings)} chunks.")

        print(f"document_chunks: {document_chunks}")
        print(f"embeddings: {embeddings}")

        class_plan = generate_class_plan(
            class_details, embeddings, document_chunks)
        st.subheader("Generated Class Plan:")
        st.write(class_plan)


# Run app
if __name__ == "__main__":
    app()
