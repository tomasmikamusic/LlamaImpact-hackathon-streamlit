import streamlit as st
import json
import os

# Define the path to the languages directory
LANGUAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../languages'))

# Function to load translations
def load_translations(language):
    try:
        if language == 'esp':
            with open(os.path.join(LANGUAGES_DIR, 'es.json'), 'r', encoding='utf-8') as f:
                return json.load(f)
        elif language == 'eng':
            with open(os.path.join(LANGUAGES_DIR, 'en.json'), 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported language: {language}")
    except FileNotFoundError as e:
        st.error(f"Translation file not found: {e}")
        raise
    except Exception as e:
        st.error(f"An error occurred while loading translations: {e}")
        raise

# Set page config
st.set_page_config(page_title="AcademIA", page_icon="🎓")

# Print the languages directory for debugging purposes
st.write(f"Languages directory: {LANGUAGES_DIR}")

# Initialize session state for language if not already set
if 'language' not in st.session_state:
    st.session_state.language = 'esp'

# Language selection in sidebar
def change_language():
    st.session_state.language = st.sidebar.selectbox(
        'Select Language', ['esp', 'eng'], index=['esp', 'eng'].index(st.session_state.language)
    )

# Call the language change function
change_language()

# Load the selected language's translations
translations = load_translations(st.session_state.language)

# Display text using the translations
st.title(translations['welcome_message'])
col1, col2, col3 = st.columns([1, 6, 1])  # Adjust these numbers to control the spacing
with col2:
    try:
        st.image(os.path.join(os.path.dirname(__file__), "../assets/academ-ia-2.png"), 
                 caption="AcademIA logo", width=250, clamp=True)
    except FileNotFoundError as e:
        st.error(f"Logo file not found: {e}")
    except Exception as e:
        st.error(f"An error occurred while loading the logo: {e}")

st.write(f"""
    {translations['instructions']}
    - {translations['start_instructions']}
    - {translations['generate_class_plan']}
    """)

# Footer
st.write(translations['footer'])

