"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""
import os
import arrow
import logging
import acp_times 
import requests # The library we use to send requests to the API
# Not to be confused with flask.request.
import flask
from flask import request

# Set up Flask app
app = flask.Flask(__name__)
app.debug = True if "DEBUG" not in os.environ else os.environ["DEBUG"]
port_num = True if "PORT" not in os.environ else os.environ["PORT"]
app.logger.setLevel(logging.DEBUG)

# Globals
###

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api/"


###
# Pages
###


def get_data():
    lists = requests.get(f"{API_URL}/brevets").json() #Not sure if this is right
    brevets = lists[-1]
    return brevets["distance"], brevets['checkpoint'], brevets["start_time"]


def insert_new(distance, checkpoint, start_time): 
    _id = requests.post(f"{API_URL}/brevets", 
                        json={"distance": distance, 
                         "checkpoint" : checkpoint,
                        "start_time": start_time}).json()
    return _id


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


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
        print("The input JSON ", input_json)
        distance = input_json["distance"]
        checkpoint = input_json["checkpoint"]
        start_time = input_json["start_time"]

        brevet_id = insert_new(distance, checkpoint, start_time)
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
        distance, checkpoint, start_time = get_data(); 
        return flask.jsonify(
            result = {"distance":distance , "checkpoint" : checkpoint,  "start_time": start_time},
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
if __name__ == "__main__":
    app.run(port=port_num, host="0.0.0.0")

