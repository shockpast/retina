import os
import random
import string

from markupsafe import escape

from flask import request
from flask import Blueprint

from database import exec

api = Blueprint("api", __name__, subdomain="api")

@api.route("/", methods=["GET"])
def index():
	return "developer? t.me/shockpast"

@api.route("/v1/upload", methods=["POST"])
def uploadFile():
	file = request.files.get("sharex")
	name = escape(file.filename)

	if (not file):
		return { "statusCode": 400, "error": { "code": "if (not file):" } }
	if (request.form.get("token") != os.getenv("FLASK_TOKEN")):
		return { "statusCode": 401, "error": { "code": "if (request.form.get(\"token\") != os.getenv(\"FLASK_TOKEN\")):" } }
	if (not os.access("files/", os.F_OK)):
		os.mkdir("files/")

	file.save(f"files/{name}")

	return f"{request.host_url.replace('api.', '')}f/{name}"

@api.route("/v1/shorten", methods=["POST"])
def shortenURL():
	full = request.form.get("url")
	short = "".join(random.choices(string.ascii_letters + string.digits, k=6))

	if (not full):
		return { "statusCode": 400, "error": { "code": "if (not full):" } }
	if (request.form.get("token") != os.getenv("FLASK_TOKEN")):
		return { "statusCode": 401, "error": { "code": "if (request.form.get(\"token\") != os.getenv(\"FLASK_TOKEN\")):" } }

	exec(f"INSERT INTO shortened_urls (full, short, clicks) VALUES (?, ?, 0)", (full, short,))

	return f"{request.host_url.replace('api.', '')}s/{short}"