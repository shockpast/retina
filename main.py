from flask import Flask
from flask import send_from_directory, redirect

from routes.api import api

from database import exec, init

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

@app.route("/f/<name>", methods=["GET"])
def findFile(name):
	return send_from_directory("files", name)

@app.route("/s/<id>", methods=["GET"])
def findURL(id):
	data = exec("SELECT * FROM shortened_urls WHERE short = ?", (id,)).fetchall()[0]
	exec("UPDATE shortened_urls SET clicks = ? WHERE short = ?", (data[2] + 1, data[1]))

	return redirect("http://" + data[0]) or { "statusCode": 401, "error": { "code": "@app.route(\"/s/<id:id>\", methods=[\"GET\"])" } }

if (__name__ == "__main__"):
	init()

	app.config["SERVER_NAME"] = "localhost:5000"
	app.run()