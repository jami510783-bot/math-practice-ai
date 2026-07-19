# AI Math Practice Generator

An AI-powered app that generates math practice problems, lets students submit
answers, and gives instant AI grading with a step-by-step explanation —
built for the ACT AI Program Final Course Project.

## The Problem

Students practicing math often have plenty of textbook problems but no way
to check their work or understand *why* an answer is wrong until they see
a tutor. This app closes that gap: it generates a fresh problem on demand
and gives immediate, explained feedback — like having a tutor available
any time.

## The Idea

As someone who has tutored math online and created math education content
on YouTube, I built this around the most common friction point I see with
students: they can attempt a problem, but they often can't tell *where*
their reasoning went wrong without a tutor walking them through it. This
app uses AI to play that role — generating the problem, grading the
answer, and explaining the correct steps in plain language.

## Features

- Choose a topic (algebra, calculus, trigonometry) and difficulty level
- AI generates a fresh, original practice problem on demand
- Submit your answer and get instant grading
- If incorrect, get a clear step-by-step explanation of the correct solution
- If correct, get a short confirmation of why it's right

## Tech Stack

- **Frontend + backend:** [Streamlit](https://streamlit.io) (Python)
- **AI:** Google Gemini API (`gemini-1.5-flash`)
- **Deployment:** Streamlit Community Cloud

## Live Demo

🔗(https://math-practice-ai-fw7y42ztczxqxqevj6ybye.streamlit.app)

## How to Run Locally

```bash
git clone https://github.com/<your-username>/math-practice-ai.git
cd math-practice-ai
pip install -r requirements.txt

# Add your Gemini API key
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# then edit .streamlit/secrets.toml and paste in your real key

streamlit run app.py
```

Get a free Gemini API key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

## Screenshots

![App screenshot](screenshots/Screenshot 2026-07-19 165844.png)

## Challenges & Learnings

The biggest challenge wasn't the AI logic itself, but keeping up with how fast the Gemini API changes. The model I originally built with was fully shut down mid-project, and even the next one I tried turned out to be restricted for new accounts. I eventually switched to Google's auto-updating "latest" alias to avoid this happening again. I also had to migrate from an older Google AI library to a newer one with a different way of calling the API. On the deployment side, I ran into a tricky issue where a config file got saved in a format Streamlit couldn't read, and I learned Git and GitHub from scratch to get the project online.

## Future Improvements

- Track a student's progress/history across sessions
- Support more topics (fractional differential equations, numerical methods)
- Adjustable difficulty based on performance
- Multi-step problems with partial credit

---
Built for the ACT AI Program (HEC × AI SkillBridge × PMYP) Final Course Project.
