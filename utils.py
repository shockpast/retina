from PIL import Image

def clear_exif(name: str, dir: str) -> None:
	img = Image.open(f"{dir}/{name}")

	data = list(img.getdata())
	without_exif = Image.new(img.mode, img.size)
	without_exif.putdata(data)

	return without_exif.save(f"{dir}/{name}")