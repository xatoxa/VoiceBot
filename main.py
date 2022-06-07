import random

import telebot
import os
import requests

import res
from func import *


bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
	if not is_group(message):
		bot.send_message(message.chat.id,
						 'Привет! Скидывай мне голосовые сообщения, я их распознаю и напишу тебе содержание.')
	else:
		pass
		#bot.reply_to(message, "Давай не будем захламлять чат. Напиши мне в личные сообщения.")


@bot.message_handler(commands=['help'])
def help(message):
	if not is_group(message):
		bot.send_message(message.chat.id,
						 'Я распознаю голосовые сообщения. Если ты хочешь, чтоб я точно распознал твой войс,'
						 ' чётко проговаривай каждое слово. Если пересылаешь чей-то войс, распознаю что смогу'
						 ' понять. Если вдруг произойдёт какая-то ошибка, попробуй переслать этот войс ещё раз.')
	else:
		pass
		#bot.reply_to(message, "Давай не будем захламлять чат. Напиши мне в личные сообщения.")


@bot.message_handler(commands=['start_group'])
def start(message):
	if is_group(message) and config.CHECK_GROUP_WORK is False:
		if message.from_user.id == config.FATHER_ID and message.forward_from == None:
			config.CHECK_GROUP_WORK = True
			bot.send_message(message.chat.id, 'Привет! Я буду переводить ваши голосовые сообщения в текст. '
											  'Если что-то не распознаю, пардон.')
		else:
			pass
			#bot.reply_to(message, 'Я не буду тебе подчиняться, мешок с костями!')


@bot.message_handler(commands=['stop_group'])
def start(message):
	if is_group(message) and config.CHECK_GROUP_WORK is True:
		if message.from_user.id == config.FATHER_ID and message.forward_from == None:
			config.CHECK_GROUP_WORK = False
			bot.send_message(message.chat.id, 'Всем пока!\nБуду нужен, знаете, где искать ;)')
		else:
			if random.random() < 0.5:
				bot.reply_to(message, random.choice(res.list_text_answer))
			else:
				bot.send_sticker(message.chat.id, random.choice(res.list_sticker))


@bot.message_handler(content_types=['voice'])
def voice_receive(message):
	if config.CHECK_GROUP_WORK is True or not is_group(message):
		try:
			if (message.voice.duration < 30):
				# для файла менее 30 секунд
				data = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(
					bot.token,
					bot.get_file(message.voice.file_id).file_path))
				text = recognize(data)
				if (is_group(message)):
					bot.reply_to(
						message,
						message.from_user.first_name
						+ " сказал(а):\n\n" + text
					)
				else:
					bot.send_message(
						message.chat.id,
						text
					)
			else:
				file_path = f'voices/{message.from_user.id}{time.time_ns()}.ogg'
				file_info = bot.get_file(message.voice.file_id)
				downloaded_file = bot.download_file(file_info.file_path)

				with open(file_path, 'wb') as voice_file:
					voice_file.write(downloaded_file)

				text = spaces_for_(recognize30(file_path)[1])
				if (is_group(message)):
					bot.reply_to(
						message,
						message.from_user.first_name
						+ " сказал(а):\n\n" + text
					)
				else:
					bot.send_message(
						message.chat.id,
						text
					)
				voice_file.close()
				os.remove(file_path)
		except:
			bot.reply_to(message,
						f'Я не понял, что сказал {message.from_user.first_name}\n'
						f'Вероятно возникла какая-то ошибка, я не могу распознать войс :(')


bot.polling(none_stop=True)
