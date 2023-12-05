import gpt4all as gpt
import colorama
from colorama import Back
from keyboard import is_pressed

colorama.init()


bot = gpt.GPT4All(
	# model_name='gpt4all-falcon-q4_0.gguf',
	model_name='mistral-7b-instruct-v0.1.Q4_0.gguf',
	model_path='C:/Users/smesh/AppData/Local/nomic.ai/GPT4All/',
	model_type=None,
	allow_download=True,
	n_threads=8,
	device='cpu',
)

print('#' * 30)
print('>MODEL_STARTED')
print('#' * 30)


def form(m):
	m = m.replace('\\begin', Back.GREEN).replace('\\end', Back.RESET)
	res = []
	
	return m


while True:
	response = bot.generate(
		prompt=input("\n\nUSER: "),
		streaming=True,
		max_tokens=800,
	)
	
	print("NEURO_RESPONSE: ")
	
	incode = 0
	
	for message in response:
		if '```' in message:
			incode = not incode
			if incode:
				print(Back.GREEN, end=str())
			else:
				print(Back.RESET, end=str())
		print(form(message), flush=True, end='')
		if is_pressed('f13'):
			print(f"\n{'#'*3}ABORTED{'#'*3}\n")
			break
