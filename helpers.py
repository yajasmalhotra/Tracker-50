import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


flights = []

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def lookup(flight):
    """Look up information for a flight."""


    # Contact API
    api_key = os.environ.get("API_KEY")

    params = {
      'access_key': api_key,
      'airline_name': request.form['airline'],
      'flight_number': request.form['flight_number'],
      'limit': '5'
    }

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
            flights.append(flight['airline']['name'])

        else:
            print('{} flight {} from {} ({}) to {} ({}) has landed.'.format(
                flight['airline']['name'],
                flight['flight']['iata'],
                flight['departure']['airport'],
                flight['departure']['iata'],
                flight['arrival']['airport'],
                flight['arrival']['iata']))
            flights.append(flight['airline']['name'])


    print(flights)


"""
    for flight in api_response['data']:
        if flight.get('live') and not flight['live']['is_ground']:
            print('{} flight {} from {} ({}) to {} ({}) is in the air.'.format(
                flight['airline']['name'],
                flight['flight']['iata'],
                flight['departure']['airport'],
                flight['departure']['iata'],
                flight['arrival']['airport'],
                flight['arrival']['iata']))
            flights.append(flight['airline']['name'])
            flights.extend(flight['flight']['iata'],
                           flight['departure']['airport'],
                           flight['departure']['iata'],
                           flight['arrival']['airport'],
                           flight['arrival']['iata'])
            print(flights)
        else:
            print('{} flight {} from {} ({}) to {} ({}) has landed.'.format(
                flight['airline']['name'],
                flight['flight']['iata'],
                flight['departure']['airport'],
                flight['departure']['iata'],
                flight['arrival']['airport'],
                flight['arrival']['iata']))
            flights.append(flight['airline']['name'])
            flights.extend(flight['flight']['iata'],
                           flight['departure']['airport'],
                           flight['departure']['iata'],
                           flight['arrival']['airport'],
                           flight['arrival']['iata'])
            print(flights)
"""

