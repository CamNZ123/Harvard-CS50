from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from passlib.context import CryptContext
from datetime import datetime, timedelta
import math
import time
import pytz
from dateutil import tz

from helpers import *

studentcount = 0

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

@app.route("/")
@login_required
def index():

    students = db.execute("SELECT * FROM students WHERE id = :user", user = session["user_id"])

    i = 0;

    for item in students:
        i = i + 1

    # render the template
    return render_template("index.html", students = students, count = i)

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():

    if request.method == "POST":
        return redirect(url_for("index"))
    else:
        students = db.execute("SELECT * FROM students WHERE id = :user", user = session["user_id"])
        return render_template("historychoice.html", students = students)

@app.route("/historychoice", methods=["GET", "POST"])
@login_required
def historychoice():

    if request.method == "POST":
        student = request.form.get("students")
        rows = db.execute("SELECT * FROM history WHERE count_id = :user", user = student)
        rows.reverse()
        i = 0;

        for item in rows:
            i = i + 1

        return render_template("history.html", student = rows, count = i)
    else:
        students = db.execute("SELECT * FROM students WHERE id = :user", user = session["user_id"])
        return render_template("historychoice.html", students = students)

@app.route("/addstudent", methods=["GET", "POST"])
@login_required
def addstudent():

    if request.method == "POST":

        studentcount = int(request.form.get("studentcount"))
        for i in range(studentcount):
            rows = db.execute("INSERT INTO students (first_name, last_name, id, here_or_not) VALUES (:fn, :ln, :idinfo, :h_or_n)", fn = request.form.get("firstname" + str(i + 1)), ln = request.form.get("lastname" + str(i + 1)), idinfo = session["user_id"], h_or_n = "")

        return redirect(url_for("index"))
    else:

        return render_template("addstudent.html", num = int(studentcount))

@app.route("/addstudentnum", methods=["GET", "POST"])
@login_required
def addstudentnum():

    if request.method == "POST":
        studentcount = request.form.get("num")
        classes = db.execute("SELECT * FROM classes WHERE owner_id = :user", user = session["user_id"])
        return render_template("addstudent.html", num = int(studentcount))
    else:
        return render_template("addstudentnum.html")

@app.route("/removestudent", methods=["GET", "POST"])
@login_required
def removestudent():

    if request.method == "POST":
        rows = db.execute("SELECT * FROM students WHERE id = :user", user = session["user_id"])
        y = "Yes"
        n = ""
        j = 0

        for i in rows:
            if request.form.get("student[" + str(j) + "]") != None:
                students = db.execute("DELETE FROM students WHERE count_id = :idinfo", idinfo = int(i["count_id"]))
            j = j + 1


        return redirect(url_for("index"))

    else:
        students = db.execute("SELECT * FROM students WHERE id = :user", user = session["user_id"])
        return render_template("removestudent.html", students = students)


@app.route("/check", methods=["GET", "POST"])
@login_required
def check():

    if request.method == "POST":
        rows = db.execute("SELECT * FROM students WHERE id = :user", user = session["user_id"])
        y = "Yes"
        n = ""
        j = 0

        timezone = db.execute("SELECT * FROM owners WHERE id = :user", user = session["user_id"])

        for i in timezone:
            time = datetime.now() + timedelta(hours=int(i["timezone"]))
        time = str(time)[:19]
        for i in rows:
            if request.form.get("student[" + str(j) + "]") != None:
                students = db.execute("UPDATE students SET here_or_not = :y WHERE count_id = :idinfo", y = y, idinfo = int(i["count_id"]))
                students = db.execute("INSERT INTO history (here_or_not, count_id, time) VALUES (:y, :idinfo, :time)", y = y, idinfo = int(i["count_id"]), time = time)
            else:
                students = db.execute("UPDATE students SET here_or_not = :n WHERE count_id = :idinfo", n = n, idinfo = int(i["count_id"]))
                students = db.execute("INSERT INTO history (here_or_not, count_id, time) VALUES (:n, :idinfo, :time)", n = n, idinfo = int(i["count_id"]), time = time)
            j = j + 1


        return redirect(url_for("index"))

    else:
        students = db.execute("SELECT * FROM students WHERE id = :user", user = session["user_id"])
        return render_template("check.html", students = students)

def print2(num):
    for i in range(num):
        print()


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM owners WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["password"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register the user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        elif not request.form.get("passwordcheck"):
            return apology("must provide the second password")

        elif not request.form.get("password") == request.form.get("passwordcheck"):
            return apology("passwords aren't the same")

        # ensure name was submitted
        if not request.form.get("classname"):
            return apology("must provide name")

        rows = db.execute("SELECT * FROM classes WHERE name = :name", name = request.form.get("classname"))

        if len(rows) != 0:
            return apology("Classname taken")


        rows = db.execute("SELECT * FROM owners WHERE username = :username", username=request.form.get("username"))

        if len(rows) != 0:
            return apology("Username taken")

        # insert into users table
        rows = db.execute("INSERT INTO owners (username, password, timezone) VALUES(:username, :hashpass, :timezone)", username = request.form.get("username"), hashpass = pwd_context.hash(request.form.get("password")), timezone = request.form.get("timezone"))

        # login user
        session["user_id"] = rows


        rows = db.execute("INSERT INTO classes (name, owner_id) VALUES(:name, :owner)", name = request.form.get("classname"), owner = session["user_id"])

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")





