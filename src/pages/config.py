import streamlit as st
import os
import json

# Define the path to the languages directory
LANGUAGES_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../languages'))

def load_translations(language):
    """Load translations based on the selected language."""
    try:
        if language == 'esp':
            file_path = os.path.join(LANGUAGES_DIR, 'es.json')
        elif language == 'eng':
            file_path = os.path.join(LANGUAGES_DIR, 'en.json')
        else:
            raise ValueError(f"Unsupported language: {language}")

        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError as e:
        st.error(f"Translation file not found: {e}")
        raise
    except Exception as e:
        st.error(f"An error occurred while loading translations: {e}")
        raise

def app():
    """Main app function for the config page."""
    # Set page config
    st.set_page_config(page_title="Config Page", page_icon="⚙️")

    # Ensure the language is set in session state
    if 'language' not in st.session_state:
        st.session_state.language = 'esp'

    # Sidebar for language selection
    language = st.sidebar.selectbox(
        'Select Language', ['esp', 'eng'], index=['esp', 'eng'].index(st.session_state.language)
    )
    st.session_state.language = language

    # Load translations
    translations = load_translations(language)

    # Page title
    st.title(translations.get('config_title', 'Configuration'))

    # Example content
    st.write(translations.get('config_instructions', 'No instructions available'))

    # Footer
    st.write(translations.get('footer', 'No footer available'))

# Call the app function
if __name__ == "__main__":
    app()

