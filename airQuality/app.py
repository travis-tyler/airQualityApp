# Import libraries
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
app = Flask(__name__)

#################################################
# Database Setup
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create engine
# Note: User will need to supply their own PostgreSQL password under variable below
user = 'postgres'
host = 'localhost'
password = 'postgres-2002'
port = '5432'
database = 'avg_aqi'
uri = f'postgresql://{user}:{password}@{host}:{port}/{database}'
db = create_engine(uri)

#Query DB for list of states and counties
all_states = []
states = db.execute(f"SELECT DISTINCT state FROM aqi_2020 ORDER BY state")
for s in states:
    all_states.append(s[0])
all_counties = []
counties = db.execute(f"SELECT DISTINCT county FROM aqi_2020 ORDER BY county")
for c in counties:
    all_counties.append(c[0])

# create route that renders index.html template
@app.route("/")
def home():
    # return jsonify(all_states)
    return render_template('index.html', state_list=all_states, county_list=all_counties)

# Route to get county name, query DB, and create JSON data for app.js
@app.route("/county_data")
def county_data():

    county = request.args.get('county')

    # Query DB based on user-selected county
    # Create list of dates
    dates = []
    query_dates = db.execute(f"SELECT date FROM aqi_2020 WHERE county = '{county}' ORDER BY date")
    for date in query_dates:
        dates.append(date[0])

    # Create list of 2020 AQI numbers
    aqi_2020 = []
    query_api_2020 = db.execute(f"SELECT aqi FROM aqi_2020 WHERE county = '{county}' ORDER BY date")
    for api in query_api_2020:
        aqi_2020.append(api[0])

    # Create list of 5Y avg. AQI numbers
    aqi_5y = []
    query_api_5y = db.execute(f"SELECT five_year_avg FROM aqi_2020 WHERE county = '{county}' ORDER BY date")
    for api in query_api_5y:
        aqi_5y.append(api[0])

    # Set lists as values in dictionary to be used as JSON
    aqi_data = {
        "date": dates,
        "aqi_2020": aqi_2020,
        "avg_5y": aqi_5y
    }

    # Send to "/county_data"
    return jsonify(aqi_data)

# Run app
if __name__ == "__main__":
    app.run(debug=True)