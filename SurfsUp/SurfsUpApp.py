# Import dependencies
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Database Setup
# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask Setup
app = Flask(__name__)

# Flask Routes
# Homepage with available api routes
@app.route("/")
def home():
    """List all available routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<start><br/>"
        f"/api/v1.0/2016-08-23/2017-08-23"
    )

# Precipitation API route
@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results from precipitation analysis to a dictionary."""
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    prcp_data = {date: prcp for date, prcp in prcp_results}
    return jsonify(prcp_data)

# Stations API route
@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations from the dataset."""
    station_results = session.query(Station.station).all()
    station_list = [station[0] for station in station_results]
    return jsonify(station_list)

# Tobs API route
@app.route("/api/v1.0/tobs")
def tobs():
    """Query the dates and temperature observations of the most-active station for the previous year of data."""
    most_active_station = "USC00519281"
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station == most_active_station)\
        .filter(Measurement.date >= prev_year).all()
    temperature_data = [{'date': date, 'temperature': tobs} for date, tobs in tobs_results]
    return jsonify(temperature_data)
# Specified start API route
@app.route("/api/v1.0/<start>")
def temperature_start(start):
    """Return a JSON list of the minimum, average, and maximum temperature for a specified start date."""
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).all()
    temperature_data = {
        'TMIN': start_results[0][0],
        'TAVG': start_results[0][1],
        'TMAX': start_results[0][2]
    }
    return jsonify(temperature_data)

# Specified start/end API route
@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start, end):
    """Return a JSON list of the minimum, average, and maximum temperature for a specified start-end date range."""
    start_end_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
        .filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    temperature_data = {
        'TMIN': start_end_results[0][0],
        'TAVG': start_end_results[0][1],
        'TMAX': start_end_results[0][2]
    }
    return jsonify(temperature_data)
if __name__ == "__main__":
    app.run(debug=True)
