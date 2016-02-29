"""Utility file to seed ROCKETMEN database from Open Notify API data"""

from model import Country
from model import Astronaut

from model import connect_to_db, db
from server import app

from bs4 import BeautifulSoup
import urllib

###########################################################################

all_rows = []


def get_html_from_wiki():
    """From wikipedia get all rows from tables with class "wikitable" """

    # Pointing to url of the page I am going to scrape and parsing it with BeautifulSoup
    read = urllib.urlopen('https://en.wikipedia.org/wiki/List_of_astronauts_by_first_flight').read()
    soup = BeautifulSoup(read, "html.parser")

    tables = soup.find_all("table", class_="wikitable")

    # Get all the rows from the tables on the webpage
    for table in tables:
        table_rows = table.find_all("tr")
        all_rows.append(table_rows)

    return all_rows


list_of_lists = []


def get_name_date():
    """Get text between <td> tags and store necessary information
        (from table row get text in 2nd and 3rd colums) in the list of lists"""

    for row in all_rows:  # for list of lists representing rows
        for item in row:  # for item in list representing a row
            cells = item.find_all("td")
            if cells:
                new_list = []
                new_list.append(cells[1].get_text())
                new_list.append(cells[2].get_text())
                list_of_lists.append(new_list)


def load_astronauts():
    """Load information from list_of_lists into database"""

    print "Astronauts"

    get_html_from_wiki()
    get_name_date()

    for item in list_of_lists:
        name, first_flight_start = item

        astronaut = Astronaut(name=name, first_flight_start=first_flight_start)

        # Add to the session
        db.session.add(astronaut)

    # Commit
    db.session.commit()


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

    load_astronauts()
