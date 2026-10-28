
import streamlit as st
from google import genai

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="📚",
    layout="wide"
)

st.title("📚 AI Study Planner")
st.write("Create a personalized study plan using Gemini AI.")

api_key = st.secrets.get("GEMINI_API_KEY", "")

with st.form("study_form"):
    subjects = st.text_area(
        "Enter your subjects",
        placeholder="Artificial Intelligence, Database Systems, Python"
    )

    hours = st.slider(
        "Available study hours per day",
        min_value=1,
        max_value=12,
        value=4
    )

    exam_date = st.date_input("Next exam date")

    submitted = st.form_submit_button("Generate Study Plan")

if submitted:
    if not subjects.strip():
        st.error("Please enter at least one subject.")

    elif not api_key:
        st.error("Gemini API key is not configured.")

    else:
        prompt = f"""
        Create a beginner-friendly study plan for a university student.

        Subjects: {subjects}
        Daily available study hours: {hours}
        Next exam date: {exam_date}

        Include:
        - Daily study sessions
        - Subject priorities
        - Revision and practice questions
        - Short breaks
        - Practical study advice

        Use clear headings and bullet points.
        """

        try:
            with st.spinner("Generating your study plan..."):
                client = genai.Client(api_key=api_key)

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            if response.text:
                st.subheader("Your Personalized Study Plan")
                st.markdown(response.text)

                st.download_button(
                    "Download Study Plan",
                    data=response.text,
                    file_name="study_plan.md",
                    mime="text/markdown"
                )
            else:
                st.warning("No text was returned. Please try again.")

        except Exception:
            st.error(
                "The AI request failed. Check the API key, "
                "model availability, internet connection and quota."
            )
