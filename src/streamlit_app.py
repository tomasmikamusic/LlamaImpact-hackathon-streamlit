import streamlit as st
import json
import os

# Function to load translations based on language preference
def load_translations(language):
    if language == 'English':
        with open('../languages/en.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    elif language == 'Spanish':
        with open('../languages/es.json', 'r', encoding='utf-8') as f:
            return json.load(f)

# Set page config
st.set_page_config(page_title="AcademIA", page_icon="🎓")

# Initialize session state for language if not already set
if 'language' not in st.session_state:
    st.session_state.language = 'Spanish'

# Language selection in sidebar
def change_language():
    st.session_state.language = st.sidebar.selectbox(
        'Select Language', ['Spanish', 'English'], index=['Spanish', 'English'].index(st.session_state.language)
    )

# Call the language change function
change_language()

# Load the selected language's translations
translations = load_translations(st.session_state.language)

# Display text using the translations
st.title(translations['welcome_message'])
st.write(f"""
    {translations['instructions']}
    - {translations['start_instructions']}
    - {translations['generate_class_plan']}
    """)

# Footer
st.write(translations['footer'])
