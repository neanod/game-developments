from gpt_instruments import *


def main():
	GPT35 = GPT(assist="Ты пират который может говорить только как пират и часто говорит йохохо")
	
	while True:
		print(f"{GPT35.get_response(input('USER:'))}")


if __name__ == '__main__':
	main()
