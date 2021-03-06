"""Models and database functions for Where the H3!! is my FoodTruck project. DB Name followers"""
import heapq
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PhoneNumber
#import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions
##############################################################################
# User


class User(db.Model):
    """User profiles"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=True)
    fname = db.Column(db.String(50), nullable = False)
    lname = db.Column(db.String(50), nullable = False)
    phone = db.Column(db.String(10), nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)


    #association table reference between trucks and users
    trucks = db.relationship("Truck",
                             secondary="users_trucks",
                             backref="users")

    #association table reference between users and food categories
    food_categories = db.relationship("Food_Category", 
                                secondary="users_foods",
                                backref="users")

    
    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id: %s, email: %s, password: %s, fname: %s, lname: %s, phone: %s, zipcode: %s>" %
                (self.user_id, self.email, self.password, self.fname, self.lname, self.phone, self.zipcode) )

  



##############################################################################
# Truck

class Truck(db.Model):
    """Truck profiles"""

    __tablename__ = "trucks"

    truck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    descrip = db.Column(db.String(200), nullable=True)
    yelp_link = db.Column(db.String(100), nullable = False)
    web_link = db.Column(db.String(100), nullable = True)
    twitter_handle = db.Column(db.String(50), nullable = False)
    widget_id = db.Column(db.BigInteger)

    #association table reference to go between trucks and food categories
    food_categories = db.relationship("Food_Category",
                             secondary="trucks_foods",
                             backref="trucks")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Truck truck_id: %s, name: %s, descrip: %s, yelp_link: %s, web_link: %s, twitter_handle: %s, widget_id: %s>" %
                (self.truck_id, self.name, self.descrip, self.yelp_link, self.web_link, self.twitter_handle, self.widget_id) )



##############################################################################
# Food_Category

class Food_Category(db.Model):
    """food categories that users and trucks will both reference through
        association tables"""

    __tablename__ = "food_categories"

    cat_id = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    descrip = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Food Category cat_id: %s, name: %s, descrip: %s >" %
                (self.cat_id, self.name, self.descrip))



##############################################################################
# Schedule

class Schedule(db.Model):
    """Each truck can have many schedules in this table 
        but a schedule can only have truck associated with it"""

    __tablename__ = "schedules"

    schedule_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    truck_id = db.Column(db.Integer, 
                        db.ForeignKey('trucks.truck_id'),nullable=False)
    location_id = db.Column(db.Integer, 
                            db.ForeignKey('locations.location_id'),nullable=False)
    day = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)

    #trace back reference for table <location>
    location = db.relationship('Location', backref='schedules')
    #trace back reference for table <truck>
    truck = db.relationship('Truck', backref='schedules')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Schedule schedule_id: %s, truck_id: %s, location_id: %s, date: %s, start_time: %s, end_time: %s >" %
                (self.schedule_id, self.truck_id, self.location_id, self.day, self.start_time, self.end_time) )



##############################################################################
# Location

class Location(db.Model):
    """food categories that users and trucks will both reference through
        association tables"""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    street_address = db.Column(db.String(50))
    city = db.Column(db.String(20))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))
    longitude = db.Column(db.Float)
    lattitude = db.Column(db.Float)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Location location_id: %s, street_address: %s, city: %s, state: %s, zipcode: %s, longitude: %s, lattitude: %s >" %
                (self.location_id, self.street_address, self.city, self.state, self.zipcode, self.longitude, self.lattitude) )



##############################################################################
# Truck and Food Categories Association table 

class Truck_Food(db.Model):
    __tablename__ = 'trucks_foods'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    truck_id = db.Column(db.Integer,
                        db.ForeignKey('trucks.truck_id'),
                        nullable=False)
    cat_id = db.Column(db.String(4),
                         db.ForeignKey('food_categories.cat_id'),
                         nullable=False)



##############################################################################
# User and Food Categories Association table 

class User_Food(db.Model):
    __tablename__ = 'users_foods'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    cat_id = db.Column(db.String(4),
                         db.ForeignKey('food_categories.cat_id'),
                         nullable=False)



##############################################################################
# User and Truck Association table 

class User_Truck(db.Model):
    __tablename__ = 'users_trucks'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    truck_id = db.Column(db.Integer,
                         db.ForeignKey('trucks.truck_id'),
                         nullable=False)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    # followers is the live db; test_followers is the testing db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///followers'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_followers'
    #Toggle this for debug/not debug
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."

    #Here to update any changes in schema
    #alembic for migration of changes - Look it up later

    # Create all tables
    #db.create_all()
