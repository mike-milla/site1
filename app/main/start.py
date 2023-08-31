from datetime import timedelta

from flask import Flask
from flask_cors import CORS

from . import *

app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
CORS(app)
jwt = JWTManager(app)
api = Api(app)

from . import endpoints

for endpoint in endpoints.e:
    api.add_resource(endpoint['conf'], '/api/' + endpoint['name'])


@app.route("/files/<filedir>/<path:name>")
def app_file(filedir, name):
    try:
        if "img" == filedir:
            filedir = "HesaImages"
        if "vid" == filedir:
            filedir = "HesaVids"
        return send_from_directory(f"static/media/hesa-media/data/{filedir}", name)
    except FileNotFoundError:
        return "File not found", 404


@app.route("/files/<name>")
def app_filee(name):
    return send_from_directory(f"static/media/hesa-media/data/HesaImages", name)
