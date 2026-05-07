from flask import Flask, render_template, request, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret"

# 🔗 MySQL Connection
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ishvariw2005",   
        database="sqlshield"
    )

# 🛑 Log attacks
def log_attack(payload, status):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO logs (payload, status) VALUES (%s, %s)", (payload, status))
    db.commit()
    cursor.close()
    db.close()

# 🔐 Vulnerable Login
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        cursor = db.cursor()

        # ❌ Vulnerable query
        query = f"SELECT * FROM users WHERE username='{user}' AND password='{pwd}'"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            session["user"] = result[1]
            session["role"] = result[3]
            return redirect("/dashboard")
        else:
            log_attack(user + " | " + pwd, "FAILED")

        cursor.close()
        db.close()

    return render_template("login.html")

# ✅ Secure Login
@app.route("/secure_login", methods=["POST"])
def secure_login():
    user = request.form["username"]
    pwd = request.form["password"]

    db = get_db()
    cursor = db.cursor()

    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (user, pwd))
    result = cursor.fetchone()

    cursor.close()
    db.close()

    if result:
        session["user"] = result[1]
        session["role"] = result[3]
        return redirect("/dashboard")

    return "Secure login failed"

# 📊 Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", user=session.get("user"))

# 🧪 Playground
@app.route("/playground", methods=["GET", "POST"])
def playground():
    result = None

    if request.method == "POST":
        payload = request.form["payload"]

        db = get_db()
        cursor = db.cursor()

        try:
            query = f"SELECT * FROM users WHERE username='{payload}'"
            cursor.execute(query)
            result = cursor.fetchall()
            log_attack(payload, "SUCCESS")
        except:
            log_attack(payload, "ERROR")

        cursor.close()
        db.close()

    return render_template("playground.html", result=result)

# 🛡️ Admin Panel
@app.route("/admin")
def admin():
    if session.get("role") != "admin":
        return "Access Denied"

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin.html", logs=logs)

# 📈 Report
@app.route("/report")
def report():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM logs")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM logs WHERE status='SUCCESS'")
    success = cursor.fetchone()[0]

    cursor.close()
    db.close()

    return render_template("report.html", total=total, success=success)

if __name__ == "__main__":
    app.run(debug=True)