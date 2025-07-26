from flask import Flask, request, send_from_directory
import json
import os

app = Flask(__name__)

# Đường dẫn đến thư mục chứa file index.html
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_DIR = BASE_DIR  # Vì index.html cùng cấp với server.py

# Đường dẫn đến thư mục employees nằm ở cấp trên
EMPLOYEES_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "employees"))

@app.route("/")
def index():
    return send_from_directory(HTML_DIR, "index.html")

@app.route("/register", methods=["POST"])
def register():
    email = request.form["email"]
    secret = request.form["secret"]

    try:
        department = email.split("@")[1].split(".")[0].lower()
    except:
        return "❌ Invalid email format", 400

    json_file = os.path.join(EMPLOYEES_DIR, f"employees_{department}.json")

    if not os.path.exists(json_file):
        with open(json_file, "w") as f:
            json.dump([], f, indent=2)

    with open(json_file, "r") as f:
        data = json.load(f)

    # 🚫 Giới hạn tối đa 8 người trong 1 bộ phận
    if len(data) >= 8:
        return f"❌ Sorry, the {department.upper()} department is full (max 8 employees). Please contact admin.", 400

    # 🚫 Không cho trùng email trong cùng bộ phận
    if any(entry["email"].lower() == email.lower() for entry in data):
        return f"❌ Email already exists in {department.upper()} department", 400

    data.append({"email": email, "secret": secret})

    with open(json_file, "w") as f:
        json.dump(data, f, indent=2)

    return f"✅ Registered successfully to {department.upper()} department"


if __name__ == "__main__":
    app.run(debug=True)
