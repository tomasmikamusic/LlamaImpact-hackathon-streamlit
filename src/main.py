import streamlit as st
import os
import requests
from elasticsearch import Elasticsearch

# Elasticsearch setup
es = Elasticsearch(os.getenv('ELASTICSEARCH_URL', "http://localhost:9200"))

# Llama API Configuration
LLAMA_API_URL = os.getenv('LLAMA_API_URL')  # "https://api.llama.ai/v3.1/query"
LLAMA_API_KEY = os.getenv('LLAMA_API_KEY')

# Streamlit UI
st.title("RAG-Powered Q&A System")
st.sidebar.header("Upload Documents")

# Document Upload
uploaded_file = st.sidebar.file_uploader(
    "Choose a document", type=["txt", "pdf"])

if uploaded_file is not None:
    # Save file locally
    file_content = uploaded_file.read().decode("utf-8")  # Assuming text file
    st.sidebar.success("File uploaded successfully!")

    # Preprocess and index document in Elasticsearch
    chunks = file_content.split("\n\n")  # Chunking by paragraphs
    for idx, chunk in enumerate(chunks):
        es.index(index="documents", id=idx, document={"content": chunk})
    st.sidebar.success("Document indexed successfully!")

# User Input
question = st.text_input("Ask a question:")
if st.button("Get Answer"):
    # Retrieve relevant documents
    response = es.search(index="documents", query={
                         "match": {"content": question}})
    top_docs = [hit["_source"]["content"] for hit in response["hits"]["hits"]]

    # Prepare prompt
    context = " ".join(top_docs)
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"

    # Call Llama API
    llama_response = requests.post(
        LLAMA_API_URL,
        headers={"Authorization": f"Bearer {LLAMA_API_KEY}"},
        json={"prompt": prompt}
    )
    if llama_response.status_code == 200:
        answer = llama_response.json()["choices"][0]["text"]
        st.success(f"Answer: {answer}")
    else:
        st.error("Failed to retrieve an answer. Check API settings.")

# Streamlit Footer
st.write("Powered by Llama")
