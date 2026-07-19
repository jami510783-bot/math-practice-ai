"""
AI Math Practice Generator
---------------------------
A Streamlit app that generates math practice problems by topic and
difficulty, lets the student submit an answer, and uses an AI model
(Google Gemini) to grade the answer and explain the correct steps.
"""

import json
import re

import streamlit as st
from google import genai

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

st.set_page_config(page_title="AI Math Practice Generator", page_icon="🧮")

API_KEY = st.secrets.get("GEMINI_API_KEY", "")

TOPICS = [
    "Algebra (linear equations)",
    "Algebra (quadratic equations)",
    "Calculus (derivatives)",
    "Calculus (integrals)",
    "Trigonometry",
]

DIFFICULTIES = ["Easy", "Medium", "Hard"]

MODEL_NAME = "gemini-flash-latest"


def get_client():
    return genai.Client(api_key=API_KEY)


def generate_problem(topic: str, difficulty: str) -> dict:
    client = get_client()
    prompt = f"""You are a math teacher creating a practice problem.

Topic: {topic}
Difficulty: {difficulty}

Return ONLY a JSON object (no markdown, no extra text) with exactly these keys:
- "problem": a single, well-posed practice question (string)
- "answer": the correct final answer, in simplest form (string)

Example format:
{{"problem": "Solve for x: 2x + 3 = 11", "answer": "x = 4"}}
"""
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    text = response.text.strip()
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(text)


def grade_answer(problem: str, correct_answer: str, student_answer: str) -> dict:
    client = get_client()
    prompt = f"""You are a supportive math tutor grading a student's work.

Problem: {problem}
Correct answer: {correct_answer}
Student's answer: {student_answer}

Return ONLY a JSON object (no markdown, no extra text) with exactly these keys:
- "correct": true or false (boolean) — whether the student's answer is mathematically correct
- "feedback": a short, encouraging explanation. If correct, briefly confirm why.
  If incorrect, explain the correct step-by-step solution clearly, in plain language.
"""
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    text = response.text.strip()
    text = re.sub(r"^```(json)?|```$", "", text.strip(), flags=re.MULTILINE).strip()
    return json.loads(text)


if "problem" not in st.session_state:
    st.session_state.problem = None
if "answer" not in st.session_state:
    st.session_state.answer = None
if "result" not in st.session_state:
    st.session_state.result = None


st.title("🧮 AI Math Practice Generator")
st.write(
    "Pick a topic and difficulty, get a fresh practice problem, "
    "submit your answer, and get instant AI feedback with a full explanation."
)

if not API_KEY:
    st.warning(
        "No Gemini API key found. Add `GEMINI_API_KEY` to `.streamlit/secrets.toml` "
        "locally, or to your app's Secrets in Streamlit Cloud when deployed."
    )

col1, col2 = st.columns(2)
with col1:
    topic = st.selectbox("Topic", TOPICS)
with col2:
    difficulty = st.selectbox("Difficulty", DIFFICULTIES)

if st.button("Generate New Problem", type="primary", disabled=not API_KEY):
    with st.spinner("Generating a problem..."):
        try:
            st.session_state.problem = generate_problem(topic, difficulty)
            st.session_state.result = None
        except Exception as e:
            st.error(f"Couldn't generate a problem: {e}")

if st.session_state.problem:
    st.subheader("Problem")
    st.write(st.session_state.problem["problem"])

    student_answer = st.text_input("Your answer")

    if st.button("Submit Answer", disabled=not student_answer):
        with st.spinner("Grading..."):
            try:
                st.session_state.result = grade_answer(
                    st.session_state.problem["problem"],
                    st.session_state.problem["answer"],
                    student_answer,
                )
            except Exception as e:
                st.error(f"Couldn't grade the answer: {e}")

    if st.session_state.result:
        if st.session_state.result["correct"]:
            st.success("✅ Correct!")
        else:
            st.error("❌ Not quite.")
        st.write(st.session_state.result["feedback"])

st.divider()
st.caption("Built for the ACT AI Program Final Course Project.")