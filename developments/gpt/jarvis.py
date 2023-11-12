import os
import subprocess
import webbrowser
import openai
import tldextract
from selenium import webdriver
from keyboard import is_pressed
from gpt_instruments import GPT
from speech_tools.alternate_speech_to_text import speech_to_text as alternate_speech_to_text
from speech_tools.speech_to_text import speech_to_text
from speech_tools.text_to_speech import stream_and_play
from speech_tools.audio_get import get_audio


class Settings:
	jarvis_works_path = 'C:\\jarvis_works\\'
	secret_key = 'f13'
	clear_key = 'f8'
	smart_file_name = True


def generate_random_filename():
	from random import randint
	return 'rand' + str(randint(100000, 999999)).replace('0', 'a') \
		.replace('1', 'b') \
		.replace('2', 'c') \
		.replace('3', 'd') \
		.replace('4', 'e') \
		.replace('5', 'f') \
		.replace('6', 'g') \
		.replace('7', 'h') \
		.replace('8', 'i') \
		.replace('9', 'g') + '.txt'


def restart():
	print("Restarting...")
	subprocess.call(["C:\\my_works\\pythonProjects\\game-dev-with-git\\venv\\Scripts\\python.exe", "jarvis.py"])


decode_function = speech_to_text
browser = webdriver.Chrome()


class CmdCommand:
	def __init__(self, text, output):
		self.text = text
		self.output = output


def upgrade_response(_text) -> str:
	result = str()
	text = _text.split('```')
	cmd_returns = str()
	cmd_commands: list[CmdCommand] = list()
	for text_fragment_n in range(0, len(text)):
		text_fragment = text[text_fragment_n]
		if not text_fragment_n % 2:
			result += text_fragment
			for string in text_fragment.split('\n'):
				if 'CMD_P ' in string:
					cmd_commands.append(CmdCommand(string.replace('CMD_P ', str()), True))
				elif 'CMD_N ' in string:
					cmd_commands.append(CmdCommand(string.replace('CMD_P ', str()), False))
				elif 'BROWS ' in string:
					string = string.replace("BROWS ", str())
					if tldextract.extract(string).suffix:
						webbrowser.open(string)
					else:
						to_search = '+'.join(string.split(" "))
						try:
							browser.get(url=f'https://yandex.ru/search/?clid=2285101&text={to_search}')
						except Exception as e:
							print(f"ПРОБЛЕМА С ОТКРЫТИЕМ URL:\n{e}")
		
		else:
			if not Settings.smart_file_name:
				filename = generate_random_filename()
			else:
				deny_names = str()
				
				for file in os.listdir(Settings.jarvis_works_path):
					deny_names += f"{file}, "
				deny_names = deny_names[:-2]
				
				temp_bot = GPT(
					assist="ты создан чтобы давать названия файлам с кодом. ты всегда отвечаешь одним словом - название файла с расширением, без пробелов.")
				filename = temp_bot.get_response(
					f"Как бы ты назвал файл одним словом с этим кодом внутри?\n```{text_fragment}```\n {f'Эти имена уже заняты: {deny_names}' if not not deny_names else str()}\nНе пиши ничего кроме названия файла. Расширение нужно.")
				print(f">SAVED TO {filename}")
			
			with open(Settings.jarvis_works_path + filename, 'w') as f:
				f.write('\n'.join(text_fragment.split('\n')[1:]))
			try:
				os.system(f"explorer {Settings.jarvis_works_path + filename}")
			except Exception as e:
				print(f">ОШИБКА СОХРАНЕНИЯ ФАЙЛА:\n{e}")
	# executing in cmd
	
	for com in cmd_commands:
		if com.output:
			try:
				out = subprocess.run(com.text, shell=True, capture_output=True,
				                     text=True).stdout
				if out:
					print(f"CMD OUTPUT:\n{out}")
			except Exception as e:
				print(f"ОШИБКА ПРИ ВЫПОЛНЕНИИ В CMD:\n{e}")
		else:
			try:
				cmd_returns += subprocess.run(com.text, shell=True, capture_output=True, text=True).stdout + '\n'
			except Exception as e:
				print(f"ОШИБКА ПРИ ВЫПОЛНЕНИИ В CMD:\n{e}")
	
	result = result.replace('BROWS ', "Открыл в браузере: ")
	return result


def main():
	JARVIS = GPT(assist="You are Jarvis, you answer ONLY IN RUSSIAN\n"
	                    f"Everything you doing in console you must do in {Settings.jarvis_works_path}\n"
	                    "If I ask you to turn off, restart, etc., you respond \"0FFX2\"\n"
	                    "If I ask you to do something that requires a console, you can execute commands in cmd by writing in response CMD_P YOUR_COMMAND1 && YOUR_COMMAND2 ...\n"
	                    "if you want to print result or CMD_N YOUR_COMMAND1 && YOUR_COMMAND2 ... if you not\n"
	                    "You must write ALL cmd commands in 1 string\n"
	                    "If you cannot use internet, you can write BROWS URL_OR_SEARCH_REQUEST you must write BROWS ... in single string\n"
	                    "If I say \"Please, restart yourself\" you answer \"X012B\"\n"
	             )
	
	while True:
		while True:
			if is_pressed(Settings.secret_key):
				print(f"NEANOD:\n"
				      f"{(prompt := decode_function(get_audio('f13')))}")
				try:
					response = JARVIS.get_response(prompt)
				except openai.APIConnectionError:
					response = "Кажется у вас проблемы с подключением. Настоятельно рекомендую проверить интернет."
					print(f"JARVIS:\n"
					      f"{response}")
					break
				if "0FFX2" in response:
					browser.quit()
					quit(1)
				
				if "X012B" in response:
					browser.quit()
					restart()
				
				print(f"JARVIS:"
				      f"{response}")
				stream_and_play(upgrade_response(response))
				break
			elif is_pressed(Settings.clear_key) and len(JARVIS.message_history) != 1:
				JARVIS.clear_history()
				print('---------------------------------------------------------------')
				print('--------------------Message history cleared--------------------')
				print('---------------------------------------------------------------')
				while is_pressed(Settings.clear_key):
					pass
				break
	browser.quit()


if __name__ == '__main__':
	main()
