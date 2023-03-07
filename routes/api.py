import os
import random
import string

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

	if (not file):
		return { "statusCode": 400, "error": { "code": "if (not file):" } }
	if (request.form.get("token") != os.getenv("FLASK_TOKEN")):
		return { "statusCode": 401, "error": { "code": "if (request.form.get(\"token\") != os.getenv(\"FLASK_TOKEN\")):" } }

	file.save(f"files/{file.filename}")

	return f"{request.host_url.replace('api.', '')}f/{file.filename}"

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