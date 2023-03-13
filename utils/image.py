from PIL import Image

from werkzeug.datastructures import FileStorage

def clear_exif(name: str, dir: str) -> None:
	img = Image.open(f"{dir}/{name}")

	data = list(img.getdata())
	without_exif = Image.new(img.mode, img.size)
	without_exif.putdata(data)

	return without_exif.save(f"{dir}/{name}")

def get_size(fobj: FileStorage) -> int:
	if (fobj.content_length):
		return fobj.content_length

	try:
		pos = fobj.stream.tell()
		fobj.stream.seek(0, 2)

		size = fobj.stream.tell()
		fobj.stream.seek(pos)

		return size
	except (AttributeError, IOError):
		pass

	return 0