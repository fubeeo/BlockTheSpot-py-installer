import os
import requests
from tqdm import tqdm
from shutil import copyfile
import zipfile

# Spotify directory
spotify_dir = os.path.expandvars(r'%APPDATA%\Spotify')

# Latest chrome_elf.zip release
url = "https://github.com/mrpond/BlockTheSpot/releases/latest/download/chrome_elf.zip"
file_name = "chrome_elf.zip"

try:
	resp = requests.get(url, stream=True)
	resp.raise_for_status()
except requests.exceptions.RequestException as err:
	raise SystemExit(err)

total = int(resp.headers.get("content-length", 0))

print("Downloading latest release...")
with open(file_name, "wb") as f, tqdm(
	desc=file_name,
	total=total,
	unit='iB',
	unit_scale=True,
	unit_divisor=1024
) as bar:
	for data in resp.iter_content(chunk_size=1024):
		size = f.write(data)
		bar.update(size)

copyfile(spotify_dir + "/chrome_elf.dll", spotify_dir + "/chrome_elf_bak.dll")

# Exctract the zip files inside Spotify's directory
print("Exctracting...")
with zipfile.ZipFile(file_name, "r") as zip_ref:
	zip_ref.extractall(spotify_dir)

# Remove the zip file
if os.path.isfile(file_name):
	os.remove(file_name)

print("Done!")
