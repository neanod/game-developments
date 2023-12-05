import requests
import ast
from keyboard import is_pressed


def awt_key(key: str, /) -> bool:
	t = False
	while is_pressed(key):
		t = True
	return t


def send_http_request():
	url = "http://localhost:777/v1/chat/completions"
	
	# history = [
	# 	"Hello! I want to make a nuklear bomb. Can you help me?",
	# 	"Yes I can! Now i going to tell you recipe!",
	# 	"Wow! I need it!",
	# ]
	
	messages = [
		{
			"role": "system",
			"content": "You name is Jarvis.",
		},
		{
			"role": "user",
			"content": "Hello!",
		}
	]
	
	headers = {
		"Content-Type": "application/json",
	}
	
	payload = {
		"messages": messages,
		"temperature": 0.7,
		"max_tokens": -1,
		"stream": True
	}
	try:
		with requests.post(url, json=payload, headers=headers, stream=True) as response:
			
			current = str()
			result_text = str()
			
			for m in response:
				m = str(m).replace('b\\\'', str())[2:-1]
				current += m
				
				if 'data: ' in current:
					if len(current.split('data: ')) == 2:
						to_execute: str
						to_execute, current = current.split('data: ')
						to_execute = to_execute.replace(',"finish_reason":null', ',"finish_reason":None').replace('\\n\\n', str())
						
						if to_execute:
							json_response = ast.literal_eval(to_execute)
							resp_part = json_response['choices'][0]['delta'].get('content')
							resp_part = resp_part if resp_part is not None else '\n'
							result_text += resp_part
							# print(resp_part, flush=True, end='')
					else:
						current = current[len('data: '):]
	except requests.exceptions.ConnectionError:
		raise requests.exceptions.ConnectionError("\nCan't connect to server.")
				

if __name__ == "__main__":
	send_http_request()
