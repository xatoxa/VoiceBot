import json
import random
import urllib
import time
from speechkit import RecognitionLongAudio, Session
from speechkit.auth import generate_jwt

import config
from create_token import *


def is_group(message):
	if message.chat.type == "group" or message.chat.type == "supergroup":
		return True


def spaces_for_(text:str):
	result = text[0]
	for letter in text[1:]:
		if letter.isupper():
			result += f'. {letter}'
		else:
			result += letter
	return result


def recognize(data):
	params = "&".join([
		"profanityFilter=false",
		"folderId=%s" % config.ID_FOLDER
	])

	try:
		url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize?%s" % params, data=data)
		url.add_header("Authorization", "Bearer %s" % create_token(config.OAUTH_TOKEN)[0])

		responseData = urllib.request.urlopen(url).read().decode('UTF-8')
		decodedData = json.loads(responseData)

		if decodedData.get("error_code") is None:
			return decodedData.get("result")
	finally:
		pass


def recognize30(filename):
	jwt = generate_jwt(config.SERVICE_ACCOUNT_ID,
					   config.YANDEX_KEY_ID,
					   config.YANDEX_PRIVATE_KEY
					   )

	session = Session.from_jwt(jwt)

	recognize_long_audio = RecognitionLongAudio(session, config.SERVICE_ACCOUNT_ID, config.BUCKET_NAME)

	print("Sending file for recognition...")
	recognize_long_audio.send_for_recognition(
		filename, audioEncoding='OGG_OPUS', sampleRateHertz='48000',
		audioChannelCount=1, rawResults=False, profanityFilter='false'
	)
	while True:
		time.sleep(2)
		if recognize_long_audio.get_recognition_results():
			break
		print("Recognizing...")

	data = recognize_long_audio.get_data()
	print("DATA:\n\n", data)

	text = recognize_long_audio.get_raw_text()
	print("TEXT:\n\n", text)

	return data, text


def stop_group_text_answer():
	random.choice()