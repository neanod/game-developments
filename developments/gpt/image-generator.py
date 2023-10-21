import openai
import gpt_token


openai.api_key = gpt_token.token()

messages = []

while True:
	content = input("User: ")
	match content:
		case '':
			continue
		case _:
			try:
				response = openai.Image.create(
					prompt=content,
					n=1,
					size="1024x1024",
				)
			except openai.error.RateLimitError:
				print("Rate limit exceeded.")
				continue
			except openai.error.InvalidRequestError:
				print("Иди нахер")
				continue
			url = response['data'][0]['url']
			for data in response['data']:
				print(data['url'])
				
