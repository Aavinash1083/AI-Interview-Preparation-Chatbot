import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

skills = [
    "SQL",
    "Python",
    "BigQuery",
    "GCP",
    "Dataflow",
    "Pub/Sub",
    "Snowflake",
    "Tableau"
]


def generate_questions(skill, experience):
    return f"""
You are a Senior Data Engineer Interviewer.

Generate:
1. 10 {skill} Interview Questions.
2. Detailed Answers.
3. 3 Scenario Based Questions.
4. Important Tips.

Candidate Experience: {experience}
"""


def create_pdf(content, skill):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()

    story = []

    title = Paragraph(
        f"{skill} Interview Questions",
        styles["Title"]
    )

    story.append(title)
    story.append(Spacer(1, 20))

    for line in content.split("\n"):
        if line.strip():
            story.append(
                Paragraph(
                    line,
                    styles["BodyText"]
                )
            )
            story.append(Spacer(1, 8))

    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf


st.set_page_config(
    page_title="AI Interview Preparation Chatbot",
    page_icon="🤖"
)

st.title("🤖 AI Interview Preparation Chatbot")
st.write("Prepare for Data Engineer Interviews")

skill = st.selectbox(
    "Select Skill",
    skills
)

experience = st.selectbox(
    "Experience",
    [
        "0-2 Years",
        "2-4 Years",
        "4+ Years"
    ]
)

if st.button("Generate Questions"):

    with st.spinner(
        "Generating Questions..."
    ):

        prompt = generate_questions(
            skill,
            experience
        )

        response = model.generate_content(
            prompt
        )

        questions = response.text

        st.markdown(questions)

        st.download_button(
            label="📥 Download TXT",
            data=questions,
            file_name=f"{skill}_Interview_Questions.txt",
            mime="text/plain"
        )

        pdf = create_pdf(
            questions,
            skill
        )

        st.download_button(
            label="📄 Download PDF",
            data=pdf,
            file_name=f"{skill}_Interview_Questions.pdf",
            mime="application/pdf"
        )

st.divider()

st.subheader(
    "Ask Your Own Question"
)

question = st.text_input(
    "Enter your interview question"
)

if question:

    response = model.generate_content(
        question
    )

    st.markdown(response.text)