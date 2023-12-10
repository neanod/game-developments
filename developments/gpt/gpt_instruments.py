import openai
import get_token

openai.api_key = get_token.gpt_token()


class GPT3:
	def __init__(self, assist=None, model=None):
		"""
		:type assist: str
		:type model: str
		"""
		if assist is None:
			self.system_prompt = "You are helpful bot"
		else:
			self.system_prompt = assist
		if model is None:
			self.model = 'gpt-3.5-turbo'
		else:
			self.model = model
		self.message_history = [
			{
				"role": "system",
				"content": self.system_prompt
			}
		]
		
	def clear_history(self):
		self.message_history = [
			{
				"role": "system",
				"content": self.system_prompt
			}
		]
	
	def get_response(self, user_prompt: str) -> str:
		self.message_history.append(
			{
				"role": "user",
				"content": user_prompt,
			}
		)
		
		completion = openai.chat.completions.create(
			model=self.model,
			messages=self.message_history,
		)
		
		self.message_history.append(
			{
				"role": "assistant",
				"content": completion.choices[0].message.content,
			}
		)
		return completion.choices[0].message.content


if __name__ == '__main__':
	bot = GPT3()
	try:
		print(bot.get_response("Hello!"))
	except openai.PermissionDeniedError as e:
		with open("error.html", 'w') as f:
			f.write(e.message)
			