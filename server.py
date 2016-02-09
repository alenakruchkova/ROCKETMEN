"""Rocketmen"""
from jinja2 import StrictUndefined

from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension

### from model import connect_to_db, db

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"
# Raises an error if undentified variable is used in Jinja2
#  (otherwise Jinja fails scilently)
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("home.html")


if __name__ == "__main__":
    # debug=True , since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

##    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run()

    # app.config['SECRET_KEY'] = "ABC"
    # toolbar = DebugToolbarExtension(app)
    # app = create_app('the-config.cfg')
    # toolbar.init_app(app)
