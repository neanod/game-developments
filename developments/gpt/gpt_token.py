def token():
	with open("token.txt", "r") as f:
		return f.read().split('\n')[0]
