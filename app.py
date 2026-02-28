from flask import Flask, render_template, request, redirect, url_for
import os
import PyPDF2

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists('uploads'):
    os.makedirs('uploads')

users = {}

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        users[email] = password
        return redirect(url_for("upload"))

    return render_template("login.html")


# ---------------- UPLOAD ----------------
@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["resume"]

        if file.filename == "":
            return "No file selected"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        resume_text = ""
        with open(filepath, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text

        return analyze_resume(resume_text)

    return render_template("upload.html")


# ---------------- ANALYSIS ----------------
def analyze_resume(resume_text):

    resume_lower = resume_text.lower()
    word_count = len(resume_text.split())

    required_skills = [
        "python", "java", "html", "css",
        "sql", "machine learning",
        "javascript", "flask", "git"
    ]

    found_skills = []
    missing_skills = []

    for skill in required_skills:
        if skill in resume_lower:
            found_skills.append(skill.title())
        else:
            missing_skills.append(skill.title())

    score = int((len(found_skills) / len(required_skills)) * 100)

    # -------- Strengths --------
    strengths = []

    if word_count > 300:
        strengths.append("Good resume length with sufficient details.")

    if "project" in resume_lower:
        strengths.append("Projects section is included.")

    if "experience" in resume_lower:
        strengths.append("Work experience mentioned.")

    if len(found_skills) >= 5:
        strengths.append("Strong technical skill set.")

    # -------- Weaknesses --------
    weaknesses = []

    if word_count < 250:
        weaknesses.append("Resume is too short. Add more details.")

    if "project" not in resume_lower:
        weaknesses.append("No projects section found.")

    if "experience" not in resume_lower:
        weaknesses.append("Work experience not clearly mentioned.")

    if len(found_skills) < 4:
        weaknesses.append("Limited technical skills detected.")

    # -------- Suggestions --------
    suggestions = []

    if missing_skills:
        suggestions.append("Consider adding these missing skills: " + ", ".join(missing_skills))

    if word_count < 300:
        suggestions.append("Increase resume length with achievements and measurable results.")

    suggestions.append("Use action verbs like Developed, Built, Designed.")
    suggestions.append("Ensure resume formatting is clean and ATS-friendly.")

    return render_template(
        "result.html",
        score=score,
        word_count=word_count,
        found_skills=found_skills,
        missing_skills=missing_skills,
        strengths=strengths,
        weaknesses=weaknesses,
        suggestions=suggestions
    )


if __name__ == "__main__":
    app.run(debug=True)