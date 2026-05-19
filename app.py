from flask import Flask, render_template, request
import pdfplumber
import os
import random
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# =========================
# EMAIL CONFIG
# =========================

EMAIL_ADDRESS = "kk22122005@gmail.com"
EMAIL_PASSWORD = "soaeuvookyjugdjr"

# =========================
# OTP STORAGE
# =========================

OTP_STORAGE = {}

# =========================
# UPLOAD FOLDER
# =========================

UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    return render_template("index.html")


# =========================
# LOGIN PAGE
# =========================

@app.route("/login")
def login():
    return render_template("login.html")


# =========================
# SIGNUP PAGE
# =========================

@app.route("/signup")
def signup():
    return render_template("signup.html")


# =========================
# ABOUT PAGE
# =========================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================
# DASHBOARD PAGE
# =========================

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


# =========================
# SIGNUP SUCCESS
# =========================

@app.route("/signup-success", methods=["POST"])
def signup_success():

    name = request.form["name"]

    return f"""

    <html>

    <head>

    <title>Signup Success</title>

    <style>

    body{{
        font-family:Arial;
        background:linear-gradient(135deg,#36d1dc,#5b86e5);
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
    }}

    .box{{
        background:white;
        padding:40px;
        border-radius:20px;
        text-align:center;
        width:400px;
    }}

    h1{{
        color:green;
        margin-bottom:20px;
    }}

    button{{
        padding:12px 25px;
        border:none;
        border-radius:10px;
        background:#2575fc;
        color:white;
        cursor:pointer;
        margin-top:20px;
    }}

    </style>

    </head>

    <body>

    <div class="box">

        <h1>Signup Successful 🎉</h1>

        <p>Welcome {name}</p>

        <a href="/login">
            <button>
                Go To Login
            </button>
        </a>

    </div>

    </body>

    </html>

    """


# =========================
# LOGIN SUCCESS
# =========================

@app.route("/login-success", methods=["POST"])
def login_success():

    email = request.form["email"]

    return f"""

    <html>

    <head>

    <title>Login Success</title>

    <style>

    body{{
        font-family:Arial;
        background:linear-gradient(135deg,#36d1dc,#5b86e5);
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
    }}

    .box{{
        background:white;
        padding:40px;
        border-radius:20px;
        text-align:center;
        width:400px;
    }}

    h1{{
        color:green;
        margin-bottom:20px;
    }}

    button{{
        padding:12px 25px;
        border:none;
        border-radius:10px;
        background:#2575fc;
        color:white;
        cursor:pointer;
        margin-top:20px;
    }}

    </style>

    </head>

    <body>

    <div class="box">

        <h1>Login Successful ✅</h1>

        <p>Welcome {email}</p>

        <a href="/dashboard">
            <button>
                Go To Dashboard
            </button>
        </a>

    </div>

    </body>

    </html>

    """


# =========================
# FORGOT PASSWORD
# =========================

@app.route("/forgot", methods=["GET", "POST"])
def forgot():

    if request.method == "POST":

        email = request.form["email"]

        otp = str(random.randint(1000, 9999))

        OTP_STORAGE[email] = otp

        msg = MIMEText(f"Your OTP is: {otp}")

        msg["Subject"] = "Password Reset OTP"

        msg["From"] = EMAIL_ADDRESS

        msg["To"] = email

        try:

            server = smtplib.SMTP("smtp.gmail.com", 587)

            server.starttls()

            server.login(
                EMAIL_ADDRESS,
                EMAIL_PASSWORD
            )

            server.send_message(msg)

            server.quit()

            return render_template(
                "verify_otp.html",
                email=email
            )

        except Exception as e:

            return f"""

            <h1>Email Error ❌</h1>

            <p>{e}</p>

            """

    return render_template("forgot.html")


# =========================
# VERIFY OTP
# =========================

@app.route("/verify-otp", methods=["POST"])
def verify_otp():

    email = request.form["email"]

    entered_otp = request.form["otp"]

    real_otp = OTP_STORAGE.get(email)

    if entered_otp == real_otp:

        return render_template(
            "new_password.html",
            email=email
        )

    return """

    <html>

    <body style='
        font-family:Arial;
        background:linear-gradient(135deg,#36d1dc,#5b86e5);
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
    '>

    <div style='
        background:white;
        padding:40px;
        border-radius:20px;
        text-align:center;
    '>

    <h1>Wrong OTP ❌</h1>

    <a href='/forgot'>
        <button style='
            padding:12px 25px;
            border:none;
            background:#2575fc;
            color:white;
            border-radius:10px;
            cursor:pointer;
        '>
            Try Again
        </button>
    </a>

    </div>

    </body>

    </html>

    """


# =========================
# RESET PASSWORD
# =========================

@app.route("/reset-password", methods=["POST"])
def reset_password():

    return """

    <html>

    <body style='
        font-family:Arial;
        background:linear-gradient(135deg,#36d1dc,#5b86e5);
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
    '>

    <div style='
        background:white;
        padding:40px;
        border-radius:20px;
        text-align:center;
    '>

    <h1>Password Reset Successful ✅</h1>

    <a href='/login'>
        <button style='
            padding:12px 25px;
            border:none;
            background:#2575fc;
            color:white;
            border-radius:10px;
            cursor:pointer;
        '>
            Go To Login
        </button>
    </a>

    </div>

    </body>

    </html>

    """


# =========================
# RESUME ANALYSIS
# =========================

@app.route("/analyze", methods=["POST"])
def analyze():

    file = request.files["resume"]

    skills = request.form["skills"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    resume_text = ""

    with pdfplumber.open(filepath) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:
                resume_text += text.lower()

    required_skills = skills.lower().split(",")

    matched = []

    missing = []

    for skill in required_skills:

        skill = skill.strip()

        if skill in resume_text:

            matched.append(skill)

        else:

            missing.append(skill)

    score = int(
        (len(matched) / len(required_skills)) * 100
    )

    return f"""

    <html>

    <head>

    <title>Resume Result</title>

    <style>

    body{{
        font-family:Arial;
        background:linear-gradient(135deg,#36d1dc,#5b86e5);
        height:100vh;
        display:flex;
        justify-content:center;
        align-items:center;
    }}

    .box{{
        width:500px;
        background:white;
        padding:40px;
        border-radius:20px;
    }}

    .score{{
        font-size:40px;
        text-align:center;
        color:green;
        margin:20px 0;
    }}

    .skills{{
        background:#f4f4f4;
        padding:10px;
        border-radius:10px;
        margin-top:10px;
    }}

    .btn{{
        display:block;
        margin-top:30px;
        text-align:center;
        background:#2575fc;
        color:white;
        padding:12px;
        border-radius:10px;
        text-decoration:none;
    }}

    </style>

    </head>

    <body>

    <div class="box">

    <h1>Resume Analysis Result</h1>

    <div class="score">
        {score}% Match
    </div>

    <h3>✅ Matched Skills</h3>

    <div class="skills">
        {matched}
    </div>

    <h3>❌ Missing Skills</h3>

    <div class="skills">
        {missing}
    </div>

    <a href="/" class="btn">
        Analyze Another Resume
    </a>

    </div>

    </body>

    </html>

    """


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)