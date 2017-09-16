from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from passlib.context import CryptContext
from datetime import datetime

from helpers import *


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
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    # Get user history
    history = db.execute("SELECT * FROM history WHERE user = :user", user = session["user_id"])


    symboldict = {}
    totalsharecost = 0

    # for each transaction
    for transaction in history:

        # if the symbol is in the dict of symbols
        if transaction["Symbol"] in symboldict:

            # add (or minus) to the total share count
            totalsharecost += transaction["Shares_boughtorsold"] * symboldict[transaction["Symbol"]]["price"]
            symboldict[transaction["Symbol"]]["Shares_boughtorsold"] += transaction["Shares_boughtorsold"]

            # if the shares = 0
            if symboldict[transaction["Symbol"]]["Shares_boughtorsold"] == 0:

                # delete the symbol from the symboldict
                del symboldict[transaction["Symbol"]]

        # if the symbol is not in the dict of symbols
        else:

            # declare it
            symboldict[transaction["Symbol"]] = transaction

            # look at its price
            symboldict[transaction["Symbol"]]["price"] = lookup(transaction["Symbol"])["price"]

            # add (or minus) to the total share count
            totalsharecost += transaction["Shares_boughtorsold"] * symboldict[transaction["Symbol"]]["price"]

    # get the cash
    cash = db.execute("SELECT cash FROM users WHERE id = :userId", userId=session["user_id"])[0]["cash"]

    # add the money from the shares
    total = cash + totalsharecost

    # render the template
    return render_template("index.html", transactions = symboldict, cash = usd(cash), total = usd(total))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    # if it is a form
    if request.method == "POST":

        # if it is a number
        try:

            # try to turn the str to a float
            shares = float(request.form.get("shares"))

        # if error (not a number)
        except ValueError:

            return apology("invalid shares")

        # if not positive shares
        if shares <= 0:

            return apology("invalid shares")

        # if no symbol
        if not request.form.get("symbol"):

            return apology("must provide symbol")

        # if no shares
        elif not request.form.get("shares"):

            return apology("must provide shares")

        # if shares not integer
        elif not shares.is_integer():

            return apology("invaild shares")

        # lookup the symbol
        seller = lookup(request.form.get("symbol"))

        # check if proper symbol
        if seller == None:
            return apology("invalid symbol")

        # get user's cash
        usercash = db.execute("SELECT cash FROM users WHERE id = :user", user = session["user_id"])[0]["cash"]

        # get cash after transaction
        soldcash = usercash - seller["price"] * shares

        # if not enough money
        if soldcash < 0:
            return apology("not enough money")

        # add to history and update cash
        history = db.execute("INSERT INTO history (User, Time, Symbol, Old_bal, New_bal, Price_change, Shares_boughtorsold, buyorsell, Price) VALUES(:userid, :time, :symbol, :oldbal, :newbal, :price_change, :shares, :bs, :price )", userid = session["user_id"], time = str(datetime.now()), symbol = seller["symbol"], oldbal = usd(usercash), newbal = usd(usercash - seller["price"]), price_change = usd(seller["price"] * shares), shares = shares, bs = "Bought", price = seller["price"])
        updateCash = db.execute("UPDATE users SET cash = cash - :soldcash WHERE id = :userId", soldcash = seller["price"] * shares, userId=session["user_id"])

        # return to home page
        return redirect(url_for("index"))

    else:

        # if a get, render template
        return render_template("buy.html")

@app.route("/history")
@login_required
def history():

    # get history
    history = db.execute("SELECT * FROM history WHERE user = :userId", userId=session["user_id"])

    # latest transactions first
    history.reverse()

    # render the template
    return render_template("history.html", transactions = history)

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
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
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

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":

        # ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol")

        # lookup symbol
        lookupinfo = lookup(request.form.get("symbol"))

        # check if invalid
        if lookupinfo == None:
            return apology("invalid symbol")

        # then render template
        return render_template("quoted.html", name = lookupinfo["name"], symbol = lookupinfo["symbol"], price = usd(lookupinfo["price"]))

    else:

        # return render_template
        return render_template("quote.html")


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


        # insert into users table
        rows = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hashpass)", username = request.form.get("username"), hashpass = pwd_context.hash(request.form.get("password")))


        # login user
        session["user_id"] = rows

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    if request.method == "POST":

        # ensure valid shares
        try:

            shares = float(request.form.get("shares"))

        except ValueError:
            return apology("invalid shares")

        if shares <= 0:
            return apology("invalid shares")

        # ensure symbol was submitted
        elif not request.form.get("symbol"):
            return apology("must provide symbol")

        # ensure shares was submitted
        elif not request.form.get("shares"):
            return apology("must provide shares")

        # ensure symbol is valid
        elif lookup(request.form.get("symbol")) == None:
            return apology("invalid symbol")

        # ensure valid shares
        elif not shares.is_integer():
            return apology("invaild shares")

        # set symbol to uppercase
        symbol = request.form.get("symbol").upper()

        # look it up
        seller = lookup(symbol)

        # ensure symbol is valid
        if seller == None:
            return apology("invalid symbol")

        # get cash from user
        cash = db.execute("SELECT cash FROM users WHERE id = :userId", userId = session["user_id"])[0]["cash"]

        # get history for this symbol for this user
        history = db.execute("SELECT * FROM history WHERE user = :userId AND Symbol = :symbol", userId = session["user_id"], symbol = symbol)

        quantity = 0

        # get share count
        for transaction in history:
            quantity += transaction["Shares_boughtorsold"]

        # check if enough shares
        if quantity < shares:
            return apology("not enough shares")

        # add it to the history table
        history = db.execute("INSERT INTO history (User, Time, Symbol, Old_bal, New_bal, Price_change, Shares_boughtorsold, buyorsell, Price) VALUES(:userid, :time, :symbol, :oldbal, :newbal, :price_change, :shares, :bs, :price )", userid = session["user_id"], time = str(datetime.now()), symbol = seller["symbol"], oldbal = usd(cash), newbal = usd(cash + (seller["price"] * quantity)), price_change = usd(seller["price"] * quantity), shares = -1 * shares, bs = "Sold", price = seller["price"])

        # update cash and redirect
        updateCash = db.execute("UPDATE users SET cash = :cash WHERE id = :userId", cash = cash + quantity * seller["price"], userId = session["user_id"])
        return redirect(url_for("index"))

    else:
        return render_template("sell.html")



@app.route("/addcash", methods=["GET", "POST"])
@login_required
def addcash():
    """Add money to the user."""
    if request.method == "POST":

        # ensure amount is valid
        try:
            amount = float(request.form.get("amount"))
        except ValueError:
            return apology("invalid amount")

        if amount < 1 or not amount:
            return apology("Invalid amount")

        # add cash
        updateCash = db.execute("UPDATE users SET cash = cash + :amount WHERE id = :userId", amount = amount, userId=session["user_id"])

        return redirect(url_for("index"))

    else:
        return render_template("addcash.html")





