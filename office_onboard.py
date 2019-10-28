#! python3.7

from dialog_bot_sdk.bot import DialogBot
from dialog_bot_sdk import interactive_media
from time import sleep
import grpc

def on_msg(*params):
	global btn_group
	global themes
	global answers
	global greets
	user_message = params[0].message.textMessage.text.lower()
	user_id = get_user_peer_by_id(params[0].sender_uid)
	if '/start' == user_message:#if user creates a dialog with the bot
		bot.messaging.send_message(params[0].peer, greets[1])
		sleep(12)
		bot.messaging.send_message(params[0].peer, "У вас есть какие-либо вопросы?", btn_group)
	elif user_message != "" and user_message != "help":
		token_list = user_message.split()
		for i in token_list:
			for j in themes:
				if j in i:
					bot.messaging.send_message(params[0].peer, answers[themes.index(j)])
					sleep(5)
					bot.messaging.send_message(params[0].peer, "Что еще вам подсказать?", btn_group)
					return
				elif token_list.index(i) == len(token_list) - 1 and themes.index(j) == len(themes) - 1:
					sleep(2)
					bot.messaging.send_message(params[0].peer, "Не понял вопроса.")
					return
	elif user_message == "help" or user_message == "":
		sleep(2)
		bot.messaging.send_message(params[0].peer, greets[0])#sending help msg

def on_click(*params):
	global btn_group
	global answers
	user_peer = bot.users.get_user_outpeer_by_id(params[0].uid)
	bot.messaging.send_message(user_peer, answers[int(params[0].value)])
	sleep(5)
	bot.messaging.send_message(user_peer, "Что еще вам подсказать??", btn_group)

if __name__ == "__main__":
	bot = DialogBot.get_secure_bot(
		"hackathon-mob.transmit.im",
		grpc.ssl_channel_credentials(),
		"331256a6a80bbb4d729011b54ad6b76d2546756c"
	)
	with open("./greets.txt", "r") as greet_file:
		greets = greet_file.read().split(';')
	with open("./answers.txt", "r") as answers_file:
		answers = answers_file.read().split(';')
	with open("./themes.txt", "r") as themes_file:
		themes = themes_file.read().split('\n')
		if themes[len(themes) - 1] == "":
			themes = themes[:len(themes) - 1]#trying to remove '' element
	btn_group = [interactive_media.InteractiveMediaGroup([])]#preparing bot FAQ buttons
	for i in range(len(themes)):
		if i < 5:
			btn_group[0].actions.append(
				interactive_media.InteractiveMedia(
					str(i), interactive_media.InteractiveMediaButton(str(i), themes[i])
				)
			)
	bot.messaging.on_message(on_msg, on_click)
