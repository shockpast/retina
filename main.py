from flask import Flask
from flask import send_from_directory, redirect

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from routes.api import api

from database import cursor
from database import init

app = Flask(__name__)
limiter = Limiter(get_remote_address, app = app, storage_uri = "memory://")

limiter.limit("40/minute")(api)
app.register_blueprint(api)

@app.route("/", methods=["GET"])
def index():
	return "Hello World from <a href='https://github.com/shockpast/retina'>Retina</a>!"

@app.route("/f/<name>", methods=["GET"])
def findFile(name):
	return send_from_directory("files", name)

@app.route("/s/<id>", methods=["GET"])
def findURL(id):
	data = cursor.execute("SELECT * FROM shortened_urls WHERE short = ?", (id,)).fetchall()

	if (not data):
		return f"ERROR: {id} doesn't exist in DB."

	return redirect(data[0][0] if ("https://" in data[0][0] or "http://" in data[0][0]) else f"http://{data[0][0]}")

if (__name__ == "__main__"):
	init()

	app.config["SERVER_NAME"] = "localhost:5000"
	app.run()