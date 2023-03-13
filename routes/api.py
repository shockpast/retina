import os
import random
import string

from werkzeug.utils import secure_filename

from flask import request
from flask import Blueprint

from utils.image import clear_exif, get_size

from database import exec

api = Blueprint("api", __name__, subdomain="api")

@api.route("/", methods=["GET"])
def index():
	return "💻"

@api.route("/v1/upload", methods=["POST"])
def uploadFile():
	file = request.files.get("sharex")

	name = secure_filename(file.filename)
	size = get_size(file)

	if (request.form.get("token") != os.getenv("FLASK_TOKEN")):
		return "ERROR: 'token' is incorrect."
	if (not file):
		return "ERROR: 'file' field in body is corrupted or doesn't exist."
	if (size >= 1e+8):
		return "ERROR: size of the file is too big (>100mb)"
	if (not os.access("files/", os.F_OK)):
		os.mkdir(f"files/")

	file.save(f"files/{name}")

	clear_exif(name, "files")

	return f"{request.host_url.replace('api.', '')}f/{name}"

@api.route("/v1/shorten", methods=["POST"])
def shortenURL():
	full = request.form.get("url")
	short = "".join(random.choices(string.ascii_letters + string.digits, k=6))

	if (request.form.get("token") != os.getenv("FLASK_TOKEN")):
		return "ERROR: 'token' is incorrect."
	if (not full):
		return "ERROR: 'full' field in body is pointing not to a link or doesn't exist."

	exec(f"INSERT INTO shortened_urls (full, short, clicks) VALUES (?, ?, 0)", (full, short,))

	return f"{request.host_url.replace('api.', '')}s/{short}"