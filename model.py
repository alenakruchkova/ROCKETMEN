"""Models and database functions for ROCKETMEN project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions.

db = SQLAlchemy()


##############################################################################
# Model definitions

class Country(db.Model):
    """Countries list."""

    __tablename__ = "countries"

    country_id = db.Column(db.String(2), primary_key=True)
    name = db.Column(db.String(35), nullable=False)
    flag = db.Column(db.String(400), nullable=True)

    #Define relationship to astronaut
    astronaut = db.relationship("Astronaut", backref=db.backref("countries"))


class Astronaut(db.Model):
    """Astronauts list."""

    __tablename__ = "astronauts"

    astronaut_id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    name = db.Column(db.String(300), nullable=False)
    gender = db.Column(db.String(1), nullable=True)
    dob = db.Column(db.String(10), nullable=True)
    status = db.Column(db.String(300), nullable=True)

    country_id = db.Column(db.String(2),
                            db.ForeignKey("countries.country_id"),
                            nullable=True)

    first_flight_start = db.Column(db.String(100), nullable=False)

    current_flight_start = db.Column(db.String(100), nullable=True)
    current_flight_spacecraft = db.Column(db.String(100), nullable=True)

    num_completed_flights = db.Column(db.Integer, nullable=True)
    duration_completed_flights = db.Column(db.String(100), nullable=True)

    num_evas = db.Column(db.Integer, nullable=True)
    duration_evas = db.Column(db.String(100), nullable=True)

    photo = db.Column(db.String(400), nullable=True)
    twitter = db.Column(db.String(80), nullable=True)
    instagram = db.Column(db.String(400), nullable=True)

    #Define relationship to country
    country = db.relationship("Country", backref=db.backref("astronauts"))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Astronaut astronaut_id=%s name=%s>" % (
            self.astronaut_id, self.name)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///rocketmendb'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # If we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
