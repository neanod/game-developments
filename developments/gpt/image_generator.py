import openai
import get_token

openai.api_key = get_token.gpt_token()

messages = []


def generate(prompt: str) -> list[str, str]:
	client = openai.Client(api_key=get_token.gpt_token())
	try:
		response = client.images.generate(
			prompt=prompt,
			model="dall-e-3",
			size="1792x1024",
			response_format="url",
			style="vivid",
		)
	except openai.RateLimitError:
		print("Image-gen rate limit exceeded.")
		return ["IMAGE-GEN: Can't generate images", "Because Rate-limit"]
	except openai.BadRequestError as e:
		print("Bad request")
		return ["IMAGE-GEN: Can't generate images", f"Because Bad request\n{e}"]
	except Exception as e:
		if '<title>Attention Required! | Cloudflare</title>' in e:
			return ["IMAGE-GEN: Can't generate images", "Because IP banned"]
		else:
			return ["IMAGE-GEN: Can't generate images", f"Because... ХЗ BLYAT ЛОВИ ЧЕПОЛАХ!\n{e}"]
	
	return [response.data[0].url, response.data[0].revised_prompt]


def main():
	while True:
		content = input("User: ")
		res = generate(content)
		print(res[0])
		print(res[1])


if __name__ == '__main__':
	main()
