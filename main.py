import sqlite3

from flask import Flask
from flask import send_from_directory

from routes.api import api

sqlite = sqlite3.connect("server.db")
cursor = sqlite.cursor()

app = Flask(__name__)
app.register_blueprint(api)

@app.route("/", methods=["GET"])
def index():
	return {
		"technologies": {
			"os": "windows 11",
			"editor": "visual studio code",
			"shell": "powershell"
		}
	}

@app.route("/f/<path:path>", methods=["GET"])
def handle(path):
	return send_from_directory("files", path)

if (__name__ == "__main__"):
	cursor.execute("CREATE TABLE IF NOT EXISTS shorten_url ('full' varchar, 'short' varchar, 'clicks' INTEGER)")

	app.run()