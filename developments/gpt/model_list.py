import openai
from get_token import gpt_token


client = openai.OpenAI(api_key=gpt_token())

for model in client.models.list():
	print(model)
