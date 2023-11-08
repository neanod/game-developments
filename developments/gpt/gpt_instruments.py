import time
import openai
import gpt_token

openai.api_key = gpt_token.token()


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
	
	def get_response(self, _text, retry=True, limit=None):
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
					)
					break
				except openai.RateLimitError:
					time.sleep(5)
					# print("Rate Limit exhausted. Retrying")
		else:
			try:
				completion = openai.chat.completions.create(
					model=self.model,
					messages=self.message_history,
				)
			except openai.RateLimitError:
				self.message_history.pop(-1)
				return None
		response = completion.choices[0].message.content
		self.message_history.append(
			{
				"role": "assistant",
				"content": response,
			}
		)
		return response

