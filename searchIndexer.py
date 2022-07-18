from levenshteinSearch import LevenshteinSearch
from main import outputFolder, encodeB64, decodeB64
import keyboard
import os

lev = LevenshteinSearch()
files = os.listdir(f"./{outputFolder}")
encodedFilesByName = [file.split('.')[0] for file in files]
print(encodedFilesByName)
lev.loadList(encodedFilesByName)

userInput = ""


def doSearch(input):
	results = lev.search(encodeB64(input), 2)
	for result in results:
		print(f'{decodeB64(result[0])} - {result[0]}')


def keyboardCallback(key):
	global userInput
	key = key.name
	if key == "backspace" and len(userInput) > 0:
		userInput = userInput[:-1]
	elif key == "space":
		userInput += " "
	elif key == 'alt':
		keyboard.unhook_all()
	elif len(key) == 1:
		userInput += key
	os.system('cls')
	print(userInput)
	doSearch(userInput)


keyboard.on_press(keyboardCallback, True)
keyboard.wait()
