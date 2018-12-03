import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("must provide symbol", 403)

        symbol = lookup(symbol)
        if not symbol:
            return apology("symbol invalid", 400)

        shares = int(request.form.get("shares"))
        if not shares:
            return apology("no share amount", 403)

        price = symbol.get("price")
        if price <= 0:
            return apology("shares be positive", 403)

        ID=session["user_id"]
        cash = db.execute("SELECT cash FROM users WHERE id = :ID", ID=ID)[0]['cash']

        if (price * shares > cash):
            return apology("not enough cash", 403)

        symbol = symbol.get("symbol")
        print(db.execute("SELECT MAX(id) FROM history")[0]['MAX(id)'])

        # Insert Buy data into database
        db.execute("INSERT INTO history(user_id, id, purchase, symbol, price, amount) VALUES (:uID, :ID, 'true', :symbol, :price, :amount)", uID=ID, ID=db.execute("SELECT MAX(id) FROM history")[0]['MAX(id)']+1, symbol=symbol, price=price, amount=shares)
        db.execute("UPDATE users SET cash = :cash WHERE id = :ID", cash=cash-price*shares, ID=ID)

        if db.execute("SELECT COUNT(*) FROM shares WHERE symbol = :symbol", symbol=symbol)[0]['COUNT(*)'] == 1:
            db.execute("UPDATE shares SET amount = amount + :amount WHERE user_id = :ID AND symbol = :symbol", amount=shares, ID=ID, symbol=symbol)
        else:
            db.execute("INSERT INTO shares VALUES (:ID, :symbol, :amount)", ID=ID, symbol=symbol, amount=shares)

        return redirect("/")

    else:
        return render_template("buy.html")



@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        symbol = request.form.get("symbol")
        if not symbol:
            return apology("invalid symbol", 403)

        symbol = lookup(symbol)
        if not symbol:
            return apology("symbol invalid", 400)

        return render_template("quoted.html", name=symbol.get("name"), price=symbol.get("price"), symbol=symbol.get("symbol"))

    else:
        return render_template("quote.html")

# Implemented through adaption of login function
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)
        else:
            username = request.form.get("username")

        # Ensure username is unique
        if db.execute("SELECT * FROM users WHERE username = :username", username=username):
            return apology("username already given", 403)

        # Ensure password was submitted once
        if not request.form.get("password"):
            return apology("must provide password", 403)
        password = request.form.get("password")

        # Ensure password was submitted twice

        if not  request.form.get("confirmation"):
            return apology("must confirm password", 403)
        confirmation = request.form.get("confirmation")

        # Ensure password is actually confirmed //-> passwords match
        if not (password == confirmation):
            return apology("passwords do not match", 403)

        # Insert user into table
        db.execute("INSERT INTO users(username, hash) VALUES (:uname, :pw_hash)", uname=username, pw_hash=generate_password_hash(password))

        # Also logs user in after registration
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :uname", uname=username)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
