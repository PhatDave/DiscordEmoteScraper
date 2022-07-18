import requests as re
import shutil
import json
import os
from tqdm import tqdm
import base64

file = r'emotes.json'
outputFolder = r'.\output'


def encodeB64(command):
	return base64.b64encode(command.encode('ascii')).decode('ascii')


def decodeB64(command):
	return base64.b64decode(command.encode('ascii')).decode('ascii')


if __name__ == '__main__':
	with open(file) as f:
		data = json.load(f)
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)

	for key in data.keys():
		command = data[key]
		data[key] = encodeB64(command)


	def downloadFile(filename, url, extension):
		# filename = decodeCommand(filename)
		if os.path.exists(f'{outputFolder}\\{filename}{extension}'):
			return True
		response = re.get(url, stream=True)
		if response.status_code == 200:
			with open(f'{outputFolder}\\{filename}{extension}', 'wb') as f:
				response.raw.decode_content = True
				shutil.copyfileobj(response.raw, f)
		return os.path.exists(f'{outputFolder}\\{filename}{extension}')


	def tryDownload256Gif(url, filename):
		# print(f"Trying to download {filename} with size 256 as a gif")
		if '.gif' not in url:
			return False
		url = url.replace('size=48', 'size=256')
		return downloadFile(filename, url, '.gif')


	def tryDownload256Png(url, filename):
		# print(f"Trying to download {filename} with size 256 as a png")
		url = url.replace('size=48', 'size=256')
		url = url.replace('.webp', '.png')
		return downloadFile(filename, url, '.png')


	def tryDownload96Png(url, filename):
		# print(f"Trying to download {filename} with size 96 as a png")
		url = url.replace('size=48', 'size=96')
		url = url.replace('.webp', '.png')
		return downloadFile(filename, url, '.png')


	def tryDownload48Png(url, filename):
		# print(f"Trying to download {filename} with size 48 as a png")
		url = url.replace('.webp', '.png')
		return downloadFile(filename, url, '.png')


	def tryDownload96Webp(url, filename):
		# print(f"Trying to download {filename} with size 48 as a webp")
		url = url.replace('size=48', 'size=96')
		return downloadFile(filename, url, '.webp')


	def tryDownload48Webp(url, filename):
		# print(f"Trying to download {filename} with size 48 as a webp")
		return downloadFile(filename, url, '.webp')


	downloadMethods = [
		tryDownload256Gif,
		tryDownload256Png,
		tryDownload96Png,
		tryDownload48Png,
		tryDownload96Webp,
		tryDownload48Webp,
	]

	downloaded = []
	for url in tqdm(set(data.keys()), ncols=200):
		command = data[url]
		for method in downloadMethods:
			if method(url, command):
				downloaded.append(url)
				# print(f"Downloaded {command} using {method.__name__}")
				break

	print(data.values().__len__())
	print(downloaded.__len__())

	print(f'Downloaded {set(os.listdir(outputFolder)).__len__()} files')
	print(f'Failed {(set(downloaded) - set(data.keys())).__len__()} items')
