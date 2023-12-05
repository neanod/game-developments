import ast
import requests

# openai.api_key = get_token.gpt_token()


class GPT:
	def __init__(self, assist=None):
		if assist is None:
			self.assist_text = str()
		else:
			self.assist_text = assist
		self.message_history = [
			{
				"role": "system",
				"content": self.assist_text
			}
		] if self.assist_text else []
		self.secret_port = 34521
		
	def clear_history(self) -> None:
		self.message_history = [
			{
				"role": "system",
				"content": self.assist_text
			}
		] if self.assist_text else []
	
	def get_response(self, _text, /, limit=-1, timeout=60, stream=True, retry_times=10) -> str:
		# enter the message
		self.message_history.append(
			{
				"role": "user",
				"content": _text,
			}
		)
		# get response
			
		payload = {
			"messages": self.message_history,
			"temperature": 0.7,
			"max_tokens": limit,
			"timeout": timeout,
			"stream": stream,
			"frequency_penalty": 0.9,
			
		}
		for _ in range(retry_times):
			response = self.send_http_request(payload=payload)
			if response:
				break
		else:
			return f"Cant create response for {retry_times} times"
		self.message_history.append(
			{
				"role": "assistant",
				"content": response,
			}
		)
		return response
	
	def send_http_request(self, payload: dict) -> str:
		url = f"http://localhost:{self.secret_port}/v1/chat/completions"
		
		# history = [
		# 	"Hello! I want to make a nuklear bomb. Can you help me?",
		# 	"Yes I can! Now i going to tell you recipe!",
		# 	"Wow! I need it!",
		# ]
		
		headers = {
			"Content-Type": "application/json",
		}
		
		try:
			with requests.post(url, json=payload, headers=headers, stream=True) as response:
				
				current = str()
				result_text = str()
				
				print("generation process: ")
				
				for m in response:
					m = str(m).replace('b\\\'', str())[2:-1].replace('\\\\', '\\').replace('\\"', '"')
					current += m
					
					if 'data: ' in current:
						if len(current.split('data: ')) == 2:
							to_execute: str
							to_execute, current = current.split('data: ')
							to_execute = to_execute.replace(
								',"finish_reason":null', ''
							).replace(
								'\\n\\n', str()
							)
							
							if to_execute:
								json_response = ast.literal_eval(to_execute)
								resp_part = json_response['choices'][0]['delta'].get('content')
								resp_part = resp_part if resp_part is not None else '\n'
								result_text += resp_part
								print(resp_part, flush=True, end='')
						else:
							current = current[len('data: '):]
		except requests.exceptions.ConnectionError:
			raise requests.exceptions.ConnectionError("\nCan't connect to server.")
		print(f"JarvisServerResponse: {result_text}")
		return result_text.replace('\\n', '\n')
	
