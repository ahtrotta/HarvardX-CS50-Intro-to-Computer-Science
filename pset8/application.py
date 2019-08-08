import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # Retrieve necessary data from database
    rows = db.execute(
        "SELECT * FROM shares, stocks WHERE shares.stockId = stocks.stockId AND id = :user_id ORDER BY symbol", user_id=session["user_id"])

    # Retrieve user's cash
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    cash = cash[0]["cash"]
    total = cash
    cash = usd(cash)

    # Update each row with current price information
    for row in rows:
        stock_quote = lookup(row["symbol"])
        row["price"] = usd(stock_quote["price"])
        row["total"] = stock_quote["price"] * row["shares"]
        total += row["total"]
        row["total"] = usd(row["total"])

    return render_template("index.html", total=usd(total), rows=rows, cash=cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        # Ensure valid stock symbol
        if lookup(request.form.get("symbol")) == None:
            return apology("invalid stock symbol")

        # Ensure number of shares was submitted
        if not request.form.get("shares"):
            return apology("provide the number of shares you wish to purchase")

        # Ensure user input an integer
        try:
            int(request.form.get("shares"))
        except ValueError:
            return apology("provide a valid number of shares")

        # Ensure valid number of shares
        if int(request.form.get("shares")) <= 0:
            return apology("provide a valid number of shares")

        # Look up user's cash
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        cash = cash[0]["cash"]

        # Look up price of stock
        stock_quote = lookup(request.form.get("symbol"))

        # Determine total cost of purchase
        cost = stock_quote["price"] * int(request.form.get("shares"))

        # Ensure user has enough cash for purchase
        if cash < cost:
            return apology("not enough cash")

        # Update list of stocks
        if db.execute("SELECT symbol FROM stocks WHERE symbol = :symbol", symbol=stock_quote["symbol"]) == []:
            db.execute("INSERT INTO stocks (symbol, name) VALUES(:symbol, :name)",
                       symbol=stock_quote["symbol"], name=stock_quote["name"])

        # Store stockId
        stockId = db.execute("SELECT stockId FROM stocks WHERE symbol = :symbol", symbol=stock_quote["symbol"])
        stockId = stockId[0]['stockId']

        # Add to purchase history
        db.execute("INSERT INTO purchases (id, stockId, shares, price) VALUES(:user_id, :stock_id, :shares, :price)",
                   user_id=session["user_id"], stock_id=stockId, shares=int(request.form.get("shares")), price=stock_quote["price"])

        # Check if user already owns stock
        if db.execute("SELECT stockId FROM shares WHERE id = :user_id AND stockId = :stock_id", user_id=session["user_id"], stock_id=stockId) == []:

            # Add to user's stocks
            db.execute("INSERT INTO shares (id, stockId, shares) VALUES(:user_id, :stock_id, :shares)",
                       user_id=session["user_id"], stock_id=stockId, shares=int(request.form.get("shares")))

        else:

            # Get current number of shares
            current_shares = db.execute("SELECT shares FROM shares WHERE id = :user_id AND stockId = :stock_id",
                                        user_id=session["user_id"], stock_id=stockId)
            current_shares = int(current_shares[0]["shares"])

            # Update stock amounts
            db.execute("UPDATE shares SET shares = :shares WHERE id = :user_id AND stockId = :stock_id",
                       shares=(current_shares + int(request.form.get("shares"))), user_id=session["user_id"], stock_id=stockId)

        # Update user's cash
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=(cash - cost), user_id=session["user_id"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Store username
    username = request.args.get("username")

    if username == '':
        return jsonify(False)
    elif db.execute("SELECT username FROM users WHERE username = :username", username=username) != []:
        return jsonify(False)
    else:
        return jsonify(True)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Retrieve necessary data from database
    rows = db.execute(
        "SELECT * FROM purchases, stocks WHERE purchases.stockId = stocks.stockId AND purchases.id = :user_id ORDER BY transacted DESC", user_id=session["user_id"])

    # Convert price to usd format
    for row in rows:
        row["price"] = usd(row["price"])

    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

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

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        # Ensure valid stock symbol
        if lookup(request.form.get("symbol")) == None:
            return apology("invalid stock symbol")

        # Look up price
        stock_quote = lookup(request.form.get("symbol"))

        # Convert price from float to usd
        stock_quote["price"] = usd(stock_quote["price"])

        return render_template("quoted.html", name=stock_quote["name"], price=stock_quote["price"], symbol=stock_quote["symbol"])

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password")

        # Check if passwords match
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Store username
        username = request.form.get("username")

        # Ensure username isn't taken
        if db.execute("SELECT username FROM users WHERE username = :username", username=username) != []:
            return apology("username already exists")
        elif len(username) < 1:
            return apology("invalide username")

        # Insert user into database
        db.execute("INSERT INTO users (username, hash) VALUES(:username, :hashvalue)",
                   username=username, hashvalue=generate_password_hash(request.form.get("password")))

        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")

        # Retrieve current stock information
        stock_quote = lookup(request.form.get("symbol"))

        # Ensure valid stock symbol
        if stock_quote == None:
            return apology("invalid stock symbol")

        # Ensure number of shares was submitted
        if not request.form.get("shares"):
            return apology("provide the number of shares you wish to purchase")

        # Ensure valid number of shares
        if int(request.form.get("shares")) <= 0:
            return apology("provide a valid number of shares")

        # Store stockId
        stockId = db.execute("SELECT stockId FROM stocks WHERE symbol = :symbol", symbol=stock_quote["symbol"])

        # Check if stockId exists in database
        if stockId == []:
            return apology("you don't own that stock")

        # Get stockId value
        stockId = stockId[0]['stockId']

        # Get current number of shares
        current_shares = db.execute("SELECT shares FROM shares WHERE stockId = :stock_id AND id = :user_id",
                                    stock_id=stockId, user_id=session["user_id"])

        # Ensure user owns stock
        if current_shares == []:
            return apology("you don't own that stock")

        # Get value of current shares
        current_shares = int(current_shares[0]["shares"])

        # Ensure user has enough shares
        sold_shares = int(request.form.get("shares"))
        if current_shares < sold_shares:
            return apology("you don't own enough shares")

        # Update stock amounts
        db.execute("UPDATE shares SET shares = :shares WHERE id = :user_id AND stockId = :stock_id",
                   shares=(current_shares - sold_shares), user_id=session["user_id"], stock_id=stockId)

        # Update user's cash
        value = stock_quote["price"] * sold_shares
        current_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        current_cash = current_cash[0]["cash"]
        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=(current_cash + value), user_id=session["user_id"])

        # Add to purchase history
        db.execute("INSERT INTO purchases (id, stockId, shares, price) VALUES(:user_id, :stock_id, :shares, :price)",
                   user_id=session["user_id"], stock_id=stockId, shares=(sold_shares * -1), price=stock_quote["price"])

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:

        # Retrieve symbols of all stocks owned by user
        stocks = db.execute(
            "SELECT symbol FROM shares, stocks WHERE shares.stockId = stocks.stockId AND shares.id = :user_id", user_id=session["user_id"])

        return render_template("sell.html", stocks=stocks)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Allow user to change password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure old password was submitted
        if not request.form.get("old-password"):
            return apology("must provide old password")

        # Ensure new password was submitted
        if not request.form.get("new-password"):
            return apology("must provide new password")

        # Store passwords
        new_password = request.form.get("new-password")
        old_password = request.form.get("old-password")

        # Check if passwords match
        if new_password != request.form.get("confirmation"):
            return apology("passwords do not match")

        # Get old password hash
        old_hash = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Confirm old password is correct
        if not check_password_hash(old_hash[0]["hash"], old_password):
            return apology("current password is incorrect")

        # Update password
        db.execute("UPDATE users SET hash = :hashvalue WHERE id = :user_id",
                   user_id=session["user_id"], hashvalue=generate_password_hash(new_password))

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("settings.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
