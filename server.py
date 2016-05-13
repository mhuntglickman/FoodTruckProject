"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Truck, Food_Category, Schedule, Location, Truck_Food, User_Food, User_Truck 


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "BooBooLah1234"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register_form.html")


@app.route('/register-process', methods=['POST','GET'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    phone = request.form["phone"]
    zipcode = request.form["zipcode"]


    new_user = User(email=email, password=password, fname=fname, lname=lname, phone=phone, zipcode=zipcode)
    
    #Debug
    # print '###############################'
    # print '###############################'
    # print (('email: %s, password: %s, fname: %s, lname: %s, phone: %s, zipcode: %s')%
    #         (new_user.email, new_user.password, new_user.fname, new_user.lname, new_user.phone, new_user.zipcode))
    # print '###############################'
    # print '###############################'


    db.session.add(new_user)
    db.session.commit()
    session["current_user"] = new_user.user_id
    flash("User %s added." % email)

    return redirect("/users/%s" % new_user.user_id)


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")


@app.route('/login-process', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()
    print "***********************************"
    print user
    print user.trucks

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")

    # Creates a walk through set of object from the user to the trucks
    # that they follow
    # User -> User_Truck -> Truck
    # This information needs to be passed through to the jinja template
    # where it will be formatted into a set of clickable links.
    # 5/12
    

    return redirect("/users/%s" % user.user_id)


@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    flash("Logged Out.")
    return redirect("/")


#dynamic route to display the new user
@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show info about user."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


# Not ready for this route yet.
# @app.route("/trucks/<int:truck_id>", methods=['POST'])
# def movie_detail_process(truck_id):
#     """Truck information"""

#     user_id = session.get("user_id")
#     if not user_id:
#         raise Exception("No user logged in.")

#     return redirect("/trucks/%s" % truck_id)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
