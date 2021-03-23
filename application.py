import os
import requests

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import helpers
from helpers import apology, login_required, lookup

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

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///tracker.db")

@app.route("/")
@login_required
def index():
    """Show welcome message"""

    return render_template("homepage.html")


@app.route("/usage")
@login_required
def usage():
    """Show usage instructions"""

    return render_template("usage.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Make sure API key is set
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")

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

@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    """Get flight details."""

    flights_arr = []


    def lookup():
        """Look up information for a flight."""


        # Contact API
        api_key = os.environ.get("API_KEY")

        params = {
          'access_key': api_key,
          'airline_name': request.form['airline'],
          'flight_number': request.form['flight_number'],
          'limit': '1'
        }

        """params = {
          'access_key': '97e40ff9c669b83b8cd111aa181ba9a5',
          'airline_name': 'Air Canada',
          'flight_number': 45
        }"""

        api_result = requests.get('http://api.aviationstack.com/v1/flights', params=params)

        api_response = api_result.json()

        for flight in api_response['data']:
            if flight.get('live') and not flight['live']['is_ground']:
                print('{} flight {} from {} ({}) to {} ({}) is in the air.'.format(
                    flight['airline']['name'],
                    flight['flight']['iata'],
                    flight['departure']['airport'],
                    flight['departure']['iata'],
                    flight['arrival']['airport'],
                    flight['arrival']['iata']))

                return('{} flight {} from {} ({}) to {} ({}) is in the air.'.format(
                    flight['airline']['name'],
                    flight['flight']['iata'],
                    flight['departure']['airport'],
                    flight['departure']['iata'],
                    flight['arrival']['airport'],
                    flight['arrival']['iata']))

            else:
                print('{} flight {} from {} ({}) to {} ({}) has landed.'.format(
                    flight['airline']['name'],
                    flight['flight']['iata'],
                    flight['departure']['airport'],
                    flight['departure']['iata'],
                    flight['arrival']['airport'],
                    flight['arrival']['iata']))

                return('{} flight {} from {} ({}) to {} ({}) has landed.'.format(
                    flight['airline']['name'],
                    flight['flight']['iata'],
                    flight['departure']['airport'],
                    flight['departure']['iata'],
                    flight['arrival']['airport'],
                    flight['arrival']['iata']))



        print(flights_arr)

    # User reached route via POST
    if request.method == "POST":

        lookup()

        flights_arr.append(lookup())

        print(flights_arr)
        return render_template("results.html", search=search, flights=flights_arr)

    # User reached route via GET
    else:
        return render_template("search.html")

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

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was confirmed
        elif not (request.form.get("confirmation") == request.form.get("password")):
            return apology("passwords does not match", 403)

        # Query (add) database for username
        new_user = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)",
                            username=request.form.get("username"),
                            hash=generate_password_hash(request.form.get("password")))

        # Check if old user
        if not new_user:
            return apology("This username is already taken", 400)

        # Remember which user has registered
        session["user_id"] = new_user

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link of via rediect)
    else:
        return render_template("register.html")

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    """Allow user to change their password"""

    if request.method == "POST":

        # Ensure current password is not empty
        if not request.form.get("current_password"):
            return apology("must provide current password", 400)

        # Query database for user_id
        rows = db.execute("SELECT hash FROM users WHERE id = :user_id", user_id=session["user_id"])

        # Ensure current password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("current_password")):
            return apology("invalid password", 400)

        # Ensure new password is not empty
        if not request.form.get("new_password"):
            return apology("must provide new password", 400)

        # Ensure new password confirmation is not empty
        elif not request.form.get("new_password_confirmation"):
            return apology("must provide new password confirmation", 400)

        # Ensure new password and confirmation match
        elif request.form.get("new_password") != request.form.get("new_password_confirmation"):
            return apology("new password and confirmation must match", 400)

        # Update database
        hash = generate_password_hash(request.form.get("new_password"))
        rows = db.execute("UPDATE users SET hash = :hash WHERE id = :user_id", user_id=session["user_id"], hash=hash)

        # Show flash
        flash("Password Updated!")

    return render_template("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
