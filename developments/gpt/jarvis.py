from sup_jarvis import *

assist = \
	"You are Jarvis, you answer ONLY IN RUSSIAN, you can search information and draw images\n"

"YOU CAN DRAW OR GENERATE IMAGES BY WRITING \"DRAW prompt\"\n"

f"Everything you doing in console you must do in {Settings.jarvis_works_path}\n"

"If I ask you to reboot, you respond \"0FFX2\"\n"

"If I ask you to do something that requires a console, you can execute commands in cmd "
"by writing in response \"CMD YOUR_COMMAND1 && YOUR_COMMAND2 ...\"\n"

"You must write ALL cmd commands in 1 string\n"

"If you need to browse internet, you can write BROWS URL_OR_SEARCH_REQUEST you must write BROWS s...\n"

# "to execute anything you must write EXEC ... , using python syntax"

"If I say \"Please, restart yourself\" you answer \"X012B\"\n"

assist *= Settings.accept_assist


def main():
	JARVIS = Jarvis(assist=assist)
	print('\n' * 3 + 'JARVIS MODEL STARTED\n')
	while True:
		if is_pressed(Settings.secret_key):
			if Settings.use_voice:
				print(f"NEANOD:", end='')
				print(prompt := decode_function(get_audio('f13')))
			else:
				prompt = input("NEANOD: ")
			try:
				response = JARVIS.get_upgraded_response(prompt)
			except openai.APIConnectionError:
				response = "Кажется у вас проблемы с подключением. Настоятельно рекомендую проверить интернет."
				print(f"JARVIS:\n"
				      f"{response}")
				continue
			if "0FFX2" in response:
				browser.quit()
				quit(1)
			
			if "X012B" in response:
				browser.quit()
				JARVIS.restart()
			
			print(f"JARVIS:"
			      f"{response}")
			# stream_and_play(response)
			JARVIS.play_response(response)
			continue
		elif is_pressed(Settings.clear_key) and len(JARVIS.message_history) != 1:
			JARVIS.clear_history()
			print(
				'---------------------------------------------------------------\n'
				'--------------------MESSAGE-HISTORY-CLEARED--------------------\n'
				'---------------------------------------------------------------\n'
			)
			continue
		else:
			time.sleep(0.2)
	browser.quit()


if __name__ == '__main__':
	main()
