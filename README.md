# Tracker 50
#### Video Demo:  <https://vimeo.com/527457182>
#### Description:

A simple website built with Flask with the sole purpose of searching up information about a given flight.
Users can use the airline name, flight number, and date to find whether an airline is still in the air or whether it has landed at
its destination.

My biggest task while creating this website was implementing the lookup functionality such that it worked with the AviationStack API.
Initiallly, a function in the helpers.py file was meant to handle it, and send its output to the main application, which then passed it
onto results.html. However, this led to bugs arising from my database, so the helper was made a nested function within the search function
in application.py. A large part of the problem was limited API call attempts given in the free plan of the API (the plan I was using). That,
along with limited funtionality offered by the plan meant that the app is not as feature-filled as I had envisioned, however, if required,
the functionalities offered by premium versions of the API plan can be implemented with little effort.

I debated creating an all new UI, but I settled on reworking the UI used in CS50's Finance Problem Set, since I found it very intuitive, and
I wanted my website to be beginner friendly. I did implement a dark mode, to make the website easier on the eyes.

User information (usernames and passwords) are stored on tracker.db, a SQLite3 database. The files named testing.py and testing2.py are
versions of the helper function I implemented to communicate with the API being used. The files are labelled according to the functions they handle.

1. styles.css contains the stylistic choices and basis for the UI for Tracker 50. As I mentioned earlier, I was inspired by the design for CS50 Finance, with the exception of the color scheme.
2. apology.html contains the code to display error messages when user input is invalid, or when the website runs into an internal server error.
3. change_password.html contains the forms required for a user to change their password in the case they forget it.
4. homepage.html is a simple landing page with a greeting, and a brief description of the websites function.
5. layout.html contains the bulk of the JavaScript used for this applet, and is once again, derived from the design used in CS50 Finance.
6. login.html contains the forms required for a user to enter their username and password.
7. register.html contains forms letting a user enter their username, password, and to confirm their password. Usernames must be unique.
8. results.html displays the final result message showing whether or not the flight searched has landed.
9. usage.html provides usage instructions to those using the website for the first time.
10. application.py contains most the code required to make this website run. Most of the code relating to the Flask framework is present in this file.
11. helpers.py contains helper methods that are called my methods in application.py.
12. README.md contains the video URL and the project description.
13. tracker.db is the database that contains user date (username and password hash), and is based in SQLite3.