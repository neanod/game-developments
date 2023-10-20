import openai
import gpt_token


openai.api_key = gpt_token.token()

messages = []

while True:
	content = input("User: ")
	match content:
		case '/clear':
			messages = []
			continue
		case '':
			continue
		case _:
			messages.append({"role": "user", "content": content})
			
			completion = openai.ChatCompletion.create(
				model="gpt-3.5-turbo",
				messages=messages,
			)
			
			chat_response = completion.choices[0].message.content
			print(f'ChatGPT: {chat_response}')
			# print(f"{messages=}")
			messages.append({"role": "assistant", "content": chat_response})