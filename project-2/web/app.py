"""
John Doe's Flask API.
"""

from flask import Flask, send_from_directory, abort
import os
import configparser

app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "UOCIS docker demo!\n"
path = "pages/"

@app.route("/<path:request>")

def file_check(request):
    if "~" in request or ".." in request:
        abort(403)
    elif os.path.exists(f"{path}{request}"):
        return send_from_directory(path, f"{request}"), 200
    else: 
        abort(404)

@app.errorhandler(403)
def forbidden(e): 
    #print("Forbidden characters in filename!")
    return send_from_directory(path, "403.html"), 403

@app.errorhandler(404)
def file_not_found(e): 
   #print("File not found!")
    return send_from_directory(path, "404.html"), 404


def parse_config(config_paths):
    config_path = None
    for f in config_paths:
        if os.path.isfile(f):
            config_path = f
            break

    if config_path is None:
        raise RuntimeError("Configuration file not found!")

    config = configparser.ConfigParser()
    config.read(config_path)
    return config

config = parse_config(["credentials.ini", "default.ini"])
message = config["SERVER"]["PORT"]

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=message)
