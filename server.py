"""Movie Ratings."""

from jinja2 import StrictUndefined
import twitter
import os
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Truck, Food_Category, Schedule, Location, Truck_Food, User_Food, User_Truck 
from flask.json import JSONEncoder
import json
from datetime import date, time
# This is for phone number string manipulation
import re
# pdb is for debugging
import pdb



app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "BooBooLah1234"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

#make jsonify able to work its magic on dates, too
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
       if isinstance(obj, (date, time)):
           return obj.isoformat()
       else:
           return JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder
counter = 0

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
    t_phone = request.form["phone"]
    zipcode = request.form["zipcode"]

    # Remove hyphens from the phone number before storing in DB
    phone =  phone.replace("(","")
    phone =  phone.replace(")","")
    phone =  phone.replace("-","")

    
    # create User object for DB table users
    new_user = User(email=email, password=password, fname=fname, lname=lname, phone=phone, zipcode=zipcode)
    

    # insert User object into DB
    db.session.add(new_user)
    db.session.commit()

    # create a session variable for later reference 
    session["current_user"] = new_user.user_id
    
    # send a message 
    flash("User %s added." % email)

    return redirect("/users/%s" % new_user.user_id)

#########################################################################
# Get login credentials
@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login_form.html")

##########################################################################
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



#########################################################################
# Log the user out and remove the session variable
@app.route('/logout')
def logout():
    """Log out."""

    del session["current_user"]
    flash("Logged Out.")
    return redirect("/")


#########################################################################
# dynamic route to display the registered user
# and the trucks they follow
@app.route("/users/<int:user_id>")
def user_detail(user_id):
    """Show the user page."""

    # query the db for the user object and pass through to 
    # to the user.html jinja template for display
    # because of the ORM this includes the truck info for trucks user followers
    # example:  for item in user.trucks:
    #           truck_id    name
    #           4           El Gondo
    #           6           Drums & Crumbs  

    user = User.query.get(user_id)

    # Generates a list of the trucks a user does not follow
    #new_trucks = db.session.query(Truck.truck_id).outerjoin(User_Truck).filter(User_Truck.user_id !=user_id).group_by(Truck.truck_id).all()
    

    # Get all of the trucks the current user is following from association table
    my_trucks = db.session.query(User_Truck.truck_id).filter(User_Truck.user_id == user_id).all()
    my_trucks = set(my_trucks)

    # Get all the trucks 
    all_trucks = db.session.query(Truck.truck_id).all()
    all_trucks = set(all_trucks)

    # remove the trucks a user follows from the all_trucks list
    new_trucks = all_trucks - my_trucks

    # Strip out the truck id's from the list of tuples returned by the 
    # query.  Then pass the 'new' list to the next db.query which creats a 
    # iterable set of objects that are passed on to user.html jinja template
    # temp_truck = []
    # for i in new_trucks:
    #     temp_truck.append(i[0])

    truck_list = db.session.query(Truck).filter(Truck.truck_id.in_(new_trucks)).all()
    

    return render_template("user.html", user=user, truck_list=truck_list)

##########################################################################
# Follow new trucks and un-follow trucks route from the user profile page
@app.route ('/update-trucks', methods=['POST'])
def change_trucks():
    """Update users trucks they follow"""
    # TO DO:
    # The user will see check boxes DONE: 5/24
    # iterate through the checkboxes named w/ id =truck_id DONE: 5/24
    # 
    # 
    # create db queries 5/27/2016
    # run db quereris either adding new records to users_trucks table 5/27/2016
    # create a custom dictionary to send back 5/27/2015
    # send back the new list of trucks they are either following or not following

    #intialize the dictionary needed to send back info through json
    print "?????????????????????????????????????????????????????"
    print("Request Form:",request.form.get('tid'))
    print "?????????????????????????????????????????????????????"
    print "?????????????????????????????????????????????????????"
    truck = request.form.get('tid')
    

    my_dict = {'trucks': {'name':[],
                           'truck_id':[]
                           },
               'other_trucks':{'name':[],
                               'truck_id':[]
                                }
               }
    
    # example output: [('8', u'on'), ('4', u'on'), ('7', u'on'), ('6', u'on')]
    # truck_list = request.form.items()
    
    


    # TO DO: Make this a function instead of a loop
    
    # grab the user_id from session
    user_id = session.get("current_user")
   
    # for truck in truck_list:
        # I don't like asking for '.all' because in reality this should be 
        # a '.one' as it is an association table.  However when no
        # record is returned Alchemy does not raise a 'No Result Found' error
        # therefore only work around is to use the '.all' and then 
        # test for an empty response query. 5/26/2016
    result1 = db.session.query(User_Truck).filter_by(user_id=user_id, truck_id=truck).first()
        
        # if a record is found then delete it
    if result1:
        # print "***********************************"
        # print result1.truck_id, result1.user_id
        # print "***********************************"
        # print "***********************************"
        db.session.delete(result1)
        db.session.commit()
    # else no record create one
    else:
        # Reptative but for the moment it is working 
        # best method would be add them all to the session and commit once 6/26/2016
        new_item = User_Truck(user_id=user_id,truck_id=truck)
        db.session.add(new_item)
        db.session.commit()
    #end of if 

    #end of for loop


    # query the db for the user object and pass through to 
    # to the user.html template for display
    # because of the ORM this includes the truck info for trucks user followers
    # example:  for truck_obj in user_obj.trucks:
    #           truck_id    name
    #           4           El Gondo
    #           6           Drums & Crumbs  

    user_obj = User.query.get(user_id)

    for truck_obj in user_obj.trucks:
        my_dict['trucks']['name'].append(truck_obj.name)
        my_dict['trucks']['truck_id'].append(truck_obj.truck_id)    

        
        
    # Strip out the truck id's from the list of tuples returned by the 
    # query.  Then pass the 'new' list to the next db.query which creats a 
    # iterable set of objects that are inserted into the dictionary and wind back to
    # the AJAX call. 5/27/2016
    not_following = db.session.query(Truck.truck_id).outerjoin(User_Truck).filter(User_Truck.user_id !=user_id).group_by(Truck.truck_id).all()
    
    temp_truck_list = []
    
    for items in not_following:
         temp_truck_list.append(items[0])

    truck_objs= db.session.query(Truck).filter(Truck.truck_id.in_(temp_truck_list)).all()
    for truck in truck_objs:
        my_dict['other_trucks']['name'].append(truck.name)
        my_dict['other_trucks']['truck_id'].append(truck.truck_id)    

   

    # TO DO: jsonify the returned set of objects from the two db queries and send them back to the 
    # AJAX route
    
    return jsonify(my_dict)

#########################################################################
# Display truck details
@app.route("/trucks/<int:truck_id>")
def truck_detail(truck_id):
    """Truck information"""

    # Double check the user is logged onto the system
    user_id = session.get("current_user")
    if not user_id:
        raise Exception("No user logged in.")
        return redirect("/")


    # This was for debugging 
    truck = Truck.query.get(truck_id)
    # day = time.strftime("%Y/%m/%d")
    day = "2016/06/03"
    mySchedule = Schedule.query.filter_by(truck_id=truck_id, day=day).first()
    # print "********************************"
    # print truck.name
    # print truck.yelp_link
    # print"*********************************"

    return render_template("truck.html", truck=truck, mySchedule=mySchedule)


#########################################################################
# process the 
@app.route("/truck_schedule", methods=['GET'])
def display_schedule():
    """This route is so I can get the date from the form on truck.html page; 
    then retrieve schedule and location from DB based on date and truck_id ."""
    
    # Double check the user is logged onto the system and if not throw back to homepage
    user_id = session.get("current_user")
    if not user_id:
        raise Exception("No user logged in.")
        redirect 
    

    truck_id = request.args.get("truck_id")
    day = request.args.get("day")

    # debug purposes
    # TO DO: comment out before deployement
    # print "*******************************"
    # print "truck id:", truck_id
    # print "day: ", day
    # print "*******************************"
   
    # This query will return the schedule associated with the truck_id on the day
    # the user as has selected.  Logic is in here for in the event a None is returned
    mySchedule = Schedule.query.filter_by(truck_id=truck_id, day=day).first()
    #need to requery for the truck information and send to the javascript
    truck_info = Truck.query.filter_by(truck_id=truck_id).first()
    
    # if the db returns a record then jsonify needed attributes and return to javascript
    if mySchedule:
        myScheduleDict = {
            'street_address': mySchedule.location.street_address,
            'city': mySchedule.location.city,
            'longitude': mySchedule.location.longitude, 
            'lattitude': mySchedule.location.lattitude,
            'start_time': mySchedule.start_time,
            'end_time': mySchedule.end_time,
            'truck_name': truck_info.name
        }
        # This is using an overwritten jsonfiy method to handle date and time objects
        result = jsonify(myScheduleDict)
        
        return result

    #if the db returns None then flash a message and redirect to the truck page
    elif mySchedule is None:

        # Debugging
        # print "*******************************"
        # print "Returned a NONE, create and empty json object"
        # print "*******************************"

        # Create an empty json object to return because the AJAX call has to get something
        # back - will use logic on the js side to determine if an empty list and break out 
        # of the success function.
        result = jsonify()
        return result



#########################################################################
if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
