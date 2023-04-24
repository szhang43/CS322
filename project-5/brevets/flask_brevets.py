"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import os
import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config

import logging
from pymongo import MongoClient
from mongo import get_data, insert_new

##
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()
app.logger.setLevel(logging.DEBUG)


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)

    #Getting Brevet Distance
    brevet_dist = request.args.get("dist", type = int) 
    t = request.args.get("start_t", type = str)

    start_time = arrow.get(t, "YYYY-MM-DDTHH:mm")

    open_time = acp_times.open_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brevet_dist, start_time).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}

    return flask.jsonify(result=result)


@app.route("/submit", methods=["POST"])
def submit(): 
    try: 
        input_json = request.json 
        print(input_json)
        distance = input_json["distance"]
        other = input_json["other"]
        brevet_id = insert_new(distance, other)

        return flask.jsonify(result={},
                        message="Submitted!",   
                        status=1, # This is defined by you. You just read this value in your javascript.
                        mongo_id=brevet_id)

    except: 
        return flask.jsonify(result={},
                        message="Oh no! Server error!", 
                        status=0, 
                        mongo_id='None')

@app.route("/display")
def display(): 
    try: 
        distance, other = get_data(); 
        return flask.jsonify(
            result = {"distance":distance, "other": other},
            status=1,
            message = "Succesfully displayed the data"
        )
    except: 
        return flask.jsonify(
            result = {},
            status=0,
            message = "Something went wrong...."
        )


#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
