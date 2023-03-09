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
	return "💻"

@api.route("/v1/upload", methods=["POST"])
def uploadFile():
	file = request.files.get("sharex")

	name = escape(file.filename)
	size = file.stream.seek(0, os.SEEK_END)

	if (request.form.get("token") != os.getenv("FLASK_TOKEN")):
		return "ERROR: 'token' is incorrect."
	if (not file):
		return "ERROR: 'file' field in body is corrupted or doesn't exist."
	if (size >= 1e+8):
		return "ERROR: size of the file is too big (>100mb)"
	if (not os.access("files/", os.F_OK)):
		os.mkdir("files/")

	file.stream.seek(0, os.SEEK_SET)
	file.save(f"files/{name}")

	return f"{request.host_url.replace('api.', '')}f/{name}"

@api.route("/v1/shorten", methods=["POST"])
def shortenURL():
	full = request.form.get("url")
	short = "".join(random.choices(string.ascii_letters + string.digits, k=6))

	if (not full):
		return "ERROR: 'full' field in body is pointing not to a link or doesn't exist."
	if (request.form.get("token") != os.getenv("FLASK_TOKEN")):
		return "ERROR: 'token' is incorrect."

	exec(f"INSERT INTO shortened_urls (full, short, clicks) VALUES (?, ?, 0)", (full, short,))

	return f"{request.host_url.replace('api.', '')}s/{short}"