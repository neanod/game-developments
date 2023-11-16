import os
import subprocess
import webbrowser
import time
import openai
import requests
import tldextract
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from keyboard import is_pressed
from gpt_instruments import GPT
from speech_tools.speech_to_text import speech_to_text
from image_generator import generate as generate_image
from speech_tools.text_to_speech import stream_and_play
from speech_tools.audio_get import get_audio
from get_token import google_token


class Jarvis(GPT):
	def __init__(self, assist=None, model=None):
		if assist is None:
			self.assist_text = "You are helpful bot"
		else:
			self.assist_text = assist
		if model is None:
			self.model = 'gpt-3.5-turbo'
		else:
			self.model = model
		GPT.__init__(self, assist, model)
	
	@staticmethod
	def restart():
		print("Restarting...")
		subprocess.call(["C:\\my_works\\pythonProjects\\game-dev-with-git\\venv\\Scripts\\python.exe", "jarvis.py"])
	
	def upgrade_response(self, _text) -> str:
		message_to_jarvis = str()
		text = _text.split('```')
		cmd_returns = str()
		cmd_commands: list[CmdCommand] = list()
		for text_fragment_n in range(0, len(text)):
			text_fragment = text[text_fragment_n]
			if not text_fragment_n % 2:
				message_to_jarvis += text_fragment
				for string in text_fragment.split('\n'):
					if 'CMD ' in string:
						cmd_commands.append(CmdCommand(string.replace('CMD ', str()), True))
					elif 'BROWS ' in string:
						string = string.replace("BROWS ", str())
						if tldextract.extract(string).suffix:
							webbrowser.open(string)
						else:
							if Settings.use_PARVIS:
								message_to_jarvis = self.parse_with_parvis(string, string)
								self.get_response(message_to_jarvis)
							else:
								to_search = '+'.join(string.split(" "))
								try:
									browser.get(url=f'https://yandex.ru/search/?clid=2285101&text={to_search}')
								except Exception as e:
									print(f"ПРОБЛЕМА С ОТКРЫТИЕМ URL:\n{e}")
					elif 'GENERATE ' in string:
						prompt = string.replace('GENERATE ', str())
						url, re_prompt = generate_image(prompt)
						print(f"\n{re_prompt}:\n{url}\n")
			
			else:
				if not Settings.smart_file_name:
					filename = generate_random_filename()
				else:
					deny_names = str()
					
					for file in os.listdir(Settings.jarvis_works_path):
						deny_names += f"{file}, "
					deny_names = deny_names[:-2]
					
					temp_bot = GPT(
						assist="ты создан чтобы давать названия файлам с кодом."
						       "ты всегда отвечаешь одним словом - название файла с расширением, без пробелов.")
					filename = temp_bot.get_response(
						f"Как бы ты назвал файл одним словом с этим кодом внутри?\n```{text_fragment}```\n "
						f"{f'Эти имена уже заняты: {deny_names}' if not not deny_names else str()}\n"
						f"Не пиши ничего кроме названия файла. Расширение нужно.")
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
		
		message_to_jarvis = message_to_jarvis.replace('BROWS ', "Открыл в браузере: ")
		to_return = str()
		for string in message_to_jarvis.split('\n'):
			to_return += (string + '\n') * all(
				["CMD " not in string, "GENERATE " not in string])
		return to_return
	
	@staticmethod
	def get_search_results(search_query):
		
		def google_search(query) -> list:
			url = f"https://www.googleapis.com/customsearch/v1"
			params = {
				"key": Settings.g_token,
				"cx": Settings.cx,
				"q": query
			}
			
			response = requests.get(url, params=params)
			if response.status_code == 200:
				results = response.json()
				return results
			else:
				return []
		
		return google_search(search_query)
	
	def get_upgraded_response(self, text):
		if text:
			return self.upgrade_response(self.get_response(text))
		else:
			return False
	
	def parse_with_parvis(self, query: str, question: str):
		# site variants
		search_results = self.get_search_results(query)
		# print(f"{search_results=}")
		PARVIS = GPT(
			assist='Ты Parvis, ты создан чтобы искать информацию на сайтах.\n'
			       'Если на сайте нет информации пиши в ответ: NO_INFORMATION\n'
			       'Ты должен отвечать Джарвису так:\n'
			       'This is information, you browsed - ... or NO_INFORMATION. use this information to '
			       'respond to the user.\n\n'
			       'Тебе будет дана информация в виде:\n'
			       'ТЕКСТ_ВОПРОСА\n'
			       'Site:\nHTML_WITHOUT_TAGS',
			model='gpt-3.5-turbo-16k',
		)
		# parse sites and return result to jarvis as "this is information, you browsed -  "...""
		for search_result in search_results['items']:
			url: str = search_result['link']
			name: str = search_result['title']
			
			print(f">parsing {name} ({url})")
			
			html_without_tags: str = remove_html_tags(self.get_html(url))
			
			if Settings.show_throw_gpt_messenger:
				print(f'\tJARVIS: {question.upper()}\\n Site: {len(html_without_tags)} symbols.')
			
			parvis_response = PARVIS.get_response(
				f"{question.upper()}\n"
				f"Site:\n{html_without_tags}"
			)
			if "NOINFORMATION" in parvis_response.upper().replace('_', str()).replace(' ', ''):
				PARVIS.clear_history()
				continue
			if "This is information, you browsed - " in parvis_response or "This is information, you browsed = " in parvis_response:
				result = parvis_response.replace('This is information, you browsed - ', str()).replace(
					'This is information, you browsed = ', str())
			else:
				print(f"ОШИБКА PARVIS: INVALID RESPONSE: {parvis_response}")
				PARVIS.clear_history()
				continue
			if Settings.show_throw_gpt_messenger:
				print(f'\tPARVIS: {parvis_response}')
			return result
		else:
			return "Не удалось найти необходимую информацию"
	
	@staticmethod
	def get_html(url) -> str:
		response = requests.get(url)
		return response.text
	
	@staticmethod
	def play_response(response) -> None:
		if response.replace(' ', str()) and Settings.use_voice:
			stream_and_play(response)


class Settings:
	jarvis_works_path = 'C:\\jarvis_works\\'
	secret_key = 'f13'
	clear_key = 'f8'
	use_PARVIS = True
	cx = "8255d5ccd353d4ae2"
	g_token = google_token()
	use_voice = False
	
	# debug
	show_throw_gpt_messenger = False
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


def remove_html_tags(text: str):
	text = text.replace('<', '>').split('>')
	result = str()
	for i in range(0, len(text), 2):
		result += text[i]
	return result


chrome_options = Options()
chrome_options.add_argument('--headless')
decode_function = speech_to_text
browser = webdriver.Chrome(options=chrome_options)


class CmdCommand:
	def __init__(self, text, output):
		self.text = text
		self.output = output


def main():
	input("Этот файл не предназначен для запуска")


if __name__ == '__main__':
	main()
