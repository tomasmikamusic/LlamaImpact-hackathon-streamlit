import streamlit as st


def app():
    st.title("Settings")
    st.write("Please provide the details for the class.")

    # Required Fields
    subject = st.text_input("What is the subject of the class?")
    field = st.selectbox(
        "field type:", ["STEM", "Social Sciences", "Liberal Arts"])
    num_students = st.number_input("Number of students:", min_value=1, step=1)
    time_available = st.slider("Class Duration (in minutes):", 15, 180, 60)

    # Dropdowns for options
    level = st.selectbox(
        "Class type:", ["Primary", "Secondary", "Higher Education", "Other"])
    modality = st.radio("Modality:", ["Virtual", "Presential"])
    purpose = st.selectbox(
        "Class Purpose:", ["Initial Class", "Review", "Integration"])

    # Optional Fields
    language = st.text_input("Language (default: English):", value="English")
    instructions = st.text_area("Special Instructions (optional):")

    # Save details to session state
    if st.button("Save Class Details"):
        st.session_state.class_details = {
            "subject": subject,
            "field": field,
            "num_students": num_students,
            "time_available": time_available,
            "level": level,
            "modality": modality,
            "purpose": purpose,
            "language": language,
            "instructions": instructions,
        }
        st.success("Class details saved successfully! Proceed to the next page.")


# Run app
if __name__ == "__main__":
    app()
