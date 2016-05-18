"""Movie Ratings."""

from jinja2 import StrictUndefined
import twitter
import os
from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Truck, Food_Category, Schedule, Location, Truck_Food, User_Food, User_Truck 


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "BooBooLah1234"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# default route
@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

# registration route for new users
@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user registration."""

    return render_template("register_form.html")


# Route for getting the form entries and creating new user
@app.route('/register-process', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables from reg form
    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    phone = request.form["phone"]
    zipcode = request.form["zipcode"]

    # create object to enter into DB
    new_user = User(email=email, password=password, fname=fname, lname=lname, phone=phone, zipcode=zipcode)
    
    #Debug
    # print '###############################'
    # print '###############################'
    # print (('email: %s, password: %s, fname: %s, lname: %s, phone: %s, zipcode: %s')%
    #         (new_user.email, new_user.password, new_user.fname, new_user.lname, new_user.phone, new_user.zipcode))
    # print '###############################'
    # print '###############################'

    # insert object into DB
    db.session.add(new_user)
    db.session.commit()

    # create a session variable for later reference 
    session["current_user"] = new_user.user_id
    
    # send a message 
    flash("User %s added." % email)

    return redirect("/users/%s" % new_user.user_id)

# Get login credentials
@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")

# Check login credentials
@app.route('/login-process', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables from login page
    email = request.form["email"]
    password = request.form["password"]

    # quick db query to retrieve user 
    user = User.query.filter_by(email=email).first()

    # if no object flash message warning user and return to
    # login route
    if not user:
        flash("No such user")
        return redirect("/login")

    # if user exists check the form password against the 
    # returned password. If check fails return to login route
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    # setting a session variable 
    session["current_user"] = user.user_id

    # flash message to user
    flash("Logged in")
    

    return redirect("/users/%s" % user.user_id)

# Log the user out and remove the session variable
@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


# dynamic route to display the registered user
# and the trucks they follow
@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show the user page."""

    # query the db for the user object and pass through to 
    # to the user.html jinja template for display
    user = User.query.get(user_id)
    return render_template("user.html", user=user)


# Display truck details
@app.route("/trucks/<int:truck_id>")
def truck_detail(truck_id):
    """Truck information"""

    # Double check the user is logged onto the system
    user_id = session.get("current_user")
    if not user_id:
        raise Exception("No user logged in.")


    # This was for debugging 
    truck = Truck.query.get(truck_id)
    # print "********************************"
    # print truck.name
    # print truck.yelp_link
    # print"*********************************"

    return render_template("truck.html", truck=truck)



@app.route("/truck_schedule", methods=['POST'])
def display_schedule():
    """This route is so I can get the date from the form on truck.html page; 
    then retrieve schedule and location from DB based on date and truck_id ."""

    truck_id = request.form.get("truck-id")
    day = request.form.get("day")

    # add an order to our database here
    # Need to fix the other side of this now.
    mySchedule = Schedule.query.filter_by(truck_id=truck_id, day=day).first()
    myDict ={longitude: mySchedule.longitude, lattitude: mySchedule.lattitude}
    #I need to make long: mySchedule.longitude and lang:mySchedule.lattitude
    return (jsonify(myDict))


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
