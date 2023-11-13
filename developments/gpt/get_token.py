def gpt_token():
	with open("token.txt", "r") as f:
		return f.read().split('\n')[0]


def google_token():
	with open("token.txt", "r") as f:
		return f.read().split('\n')[1]
