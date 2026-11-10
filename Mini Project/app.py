
from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash
from database import get_db_connection
from dotenv import load_dotenv
import os
import re

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not password or not confirm_password:
            flash("Please fill all fields!")
            return redirect(url_for("register"))

        if len(name) < 2 or len(name) > 100:
            flash("Name must contain 2 to 100 characters!")
            return redirect(url_for("register"))

        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            flash("Enter a valid email!")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters!")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = None
        cur = None

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                """
                INSERT INTO users (name, email, password)
                VALUES (%s, %s, %s)
                """,
                (name, email, hashed_password)
            )

            conn.commit()

            flash("Registration successful!")
            return redirect(url_for("home"))

        except Exception as e:

            if conn:
                conn.rollback()

            app.logger.exception("Registration error")
            flash("Email already registered or database error!")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template("register.html")


from werkzeug.security import check_password_hash

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter email and password!")
            return redirect(url_for("login"))

        conn = None
        cur = None

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute(
                "SELECT id, name, email, password FROM users WHERE email = %s",
                (email,)
            )

            user = cur.fetchone()

            if user and check_password_hash(user[3], password):

                session["user_id"] = user[0]
                session["user_name"] = user[1]

                return redirect(url_for("dashboard"))

            flash("Invalid email or password!")

        except Exception:
            app.logger.exception("Login error")
            flash("Database error! Please try again.")

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

    return render_template("login.html")

# Dashboard Page
@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "dashboard.html",
        name=session["user_name"]
    )


# Logout Page
@app.route("/logout")
def logout():

    session.clear()

    flash("You have logged out successfully!")

    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
