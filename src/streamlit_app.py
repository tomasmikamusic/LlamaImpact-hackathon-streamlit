import streamlit as st

# Set page config
st.set_page_config(page_title="AcademIA", page_icon="🎓")

st.title("Welcome to the AcademIA App")
st.write(
    """
    Use the sidebar to navigate:
    - Start by providing class details on the **SettingsPage**.
    - Then, generate your class plan on the **main**(class plan generator) page.
    """
)

# Footer
st.write("Powered by Llama and AI/ML API")
