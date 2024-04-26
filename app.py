import sys

sys.path.append("/home/sholim/Documents/work/Surveilance")
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
from admin.admin import admin_bp
from security.security import security_bp

app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(security_bp, url_prefix="/security")


def get_db_connection():
    conn = sqlite3.connect("surveillancedb.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/login", methods=["GET"])
def login():
    return render_template("login.html")


@app.route("/logout")
def logout():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM User WHERE username = ? AND password = ?", (username, password)
    )
    user = cursor.fetchone()

    conn.close()

    if user:
        if user["userType"] == "admin":
            return jsonify({"message": "Login successful", "userType": "admin"})
        elif user["userType"] == "security":
            return jsonify({"message": "Login successful", "userType": "security"})
    else:
        return (
            jsonify(
                {
                    "message": "Invalid username or password"
                    + str(username)
                    + str(password)
                }
            ),
            401,
        )


@app.route("/users")
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM User")
        users = cursor.fetchall()
        conn.close()

        users_json = [dict(user) for user in users]
        return jsonify({"users": users_json})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/add_user", methods=["POST"])
def add_user():
    data = request.json
    full_name = data.get("fullName")
    email = data.get("email")
    user_type = data.get("userType")
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO User (fullName,username, email,password, userType) VALUES (?, ?, ?,?,?)",
        (full_name, username, email, password, user_type),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "User added successfully"})


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM User WHERE userID=?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": "User deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        data = request.json
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE User SET fullName=?, username=?, email=?, password=?, userType=? WHERE userID=?",
            (
                data["fullName"],
                data["username"],
                data["email"],
                data["password"],
                data["userType"],
                user_id,
            ),
        )
        conn.commit()
        conn.close()
        return jsonify({"message": "User updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/attendance")
def get_attendance():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT Attendance.*, User.fullName,
                   CASE WHEN Attendance.status = 'Out' THEN Attendance.check_out_datentime
                        ELSE Attendance.check_in_datentime
                   END AS check_time
            FROM Attendance
            INNER JOIN User ON Attendance.userID = User.userID
        """
        )
        attendance = cursor.fetchall()
        conn.close()

        attendance_json = [dict(att) for att in attendance]
        return jsonify({"attendance": attendance_json})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/admin")
def admin():
    return render_template("recorded-motion.html")


@app.route("/security")
def security():
    return render_template("security-recorded-motion.html")


@app.route("/videos")
def get_videos():
    videos = fetch_videos_from_database()  # Replace this with your actual function
    return jsonify({"videos": videos})


if __name__ == "__main__":
    app.run(debug=True)
