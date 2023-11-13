import time
import openai
import get_token

openai.api_key = get_token.gpt_token()


class GPT:
	def __init__(self, assist=None, model=None):
		if assist is None:
			self.assist_text = "You are helpful bot"
		else:
			self.assist_text = assist
		if model is None:
			self.model = 'gpt-3.5-turbo'
		else:
			self.model = model
		self.message_history = [
			{
				"role": "system",
				"content": self.assist_text
			}
		]
		
	def clear_history(self) -> None:
		self.message_history = [
			{
				"role": "system",
				"content": self.assist_text
			}
		]
	
	def get_response(self, _text, retry=True, limit=None, timeout=60) -> str:
		# enter the message
		self.message_history.append(
			{
				"role": "user",
				"content": _text,
			}
		)
		# get response
		if retry:
			while True:
				try:
					completion = openai.chat.completions.create(
						model=self.model,
						messages=self.message_history,
						max_tokens=limit,
						timeout=timeout,
					)
					break
				except openai.RateLimitError as e:
					time.sleep(20)
					print("\tRate Limit exhausted. Retrying")
					if "Request too large" in str(e):
						completion = {
							"role": "system",
							"content": "NO_INFORMATION - too long request",
						}
						break
						
				except openai.BadRequestError:
					completion = {
						"role": "system",
						"content": "NO_INFORMATION - too long request",
					}
					break
		else:
			try:
				completion = openai.chat.completions.create(
					model=self.model,
					messages=self.message_history,
				)
			except openai.RateLimitError:
				self.message_history.pop(-1)
				return None
		try:
			response: str = completion.choices[0].message.content
		except AttributeError:
			response = completion['content']
		self.message_history.append(
			{
				"role": "assistant",
				"content": response,
			}
		)
		return response
