def generate_questions(skill, experience):
    return f"""
You are a Senior Data Engineer Interviewer.

Generate:

1. 10 {skill} interview questions.
2. Detailed answers.
3. 3 scenario-based questions.
4. Important tips.

Candidate Experience: {experience}
"""