"""Utility file to seed ROCKETMEN database from Open Notify API data"""

from sqlalchemy import func
from model import Country
# from model import Astronaut

# from datetime import datetime

from model import connect_to_db, db
from server import app

###########################################################################
def load_countries():
    """Load countries from countres.csv into database."""

    print "Countries"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Country.query.delete()

    # Read countries.csv file and insert data
    for row in open("seed_data/output.txt"):
        r = row.splitlines()

    for rn in r:
        name, country_id = rn.split(",")

        country = Country(name=name, country_id=country_id)

    # Add to the session
        db.session.add(country)

    # Commit
    db.session.commit()


#####################################################################
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import data

    load_countries()
