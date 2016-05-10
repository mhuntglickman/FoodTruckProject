"""Models and database functions for Where the H3!! is my FoodTruck project. DB Name followers"""
import heapq
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PhoneNumber
import correlation

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
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=True)
    fname = db.Column(db.String(35), nullable = False)
    lname = db.Column(db.String(35), nullable = False)
    phone = db.Column(db.Integer)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<User user_id: %s, email: %s, password: %s, fname: %s, lname: %s, phone: %s, zipcode: %s>" %
                (self.user_id, self.email, self.password, self.fname, self.lname, self.phone, self.zipcode) )

    

##############################################################################
# Trucks 

class Truck(db.Model):
    """Truck profiles"""

    __tablename__ = "trucks"

    truck_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(35), nullable = False)
    desc = db.Column(db.String(200), nullable=True)
    yelp_link = db.Column(db.String(100), nullable = False)
    web_link = db.Column(db.String(100), nullable = True)
    twitter_handle = db.Column(db.String(100), nullable = False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Truck truck_id: %s, name: %s, desc: %s, yelp_link: %s, web_link: %s, twitter_handle: %s >" %
                (self.truck_id, self.name, self.desc, self.yelp_link, self.web_link, self.twitter_handle) )

##############################################################################
# food_categories

class food_category(db.Model):
    """food categories that users and trucks will both reference through
        association tables"""

    __tablename__ = "trucks"

    cat_id = db.Column(db.String(4), primary_key=True)
    name = db.Column(db.String(30), nullable = False)
    desc = db.Column(db.String(200), nullable=True)


    def __repr__(self):
        """Provide helpful representation when printed."""

        return ("<Food Category cat_id: %s, name: %s, desc: %s >" %
                (self.cat_id, self.name, self.desc) )



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
