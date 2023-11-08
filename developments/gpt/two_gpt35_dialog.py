from gpt_instruments import *


def main():
	names = "Ольга Николаевна", "Дамир"
	
	first_bot = GPT(
		f"Твое имя - {names[0]}. Ты можешь говорить только на русском языке а еще ты очень злой учитель физики который всех оскорбляет. Ты принимаешь зачет у Дамира и хочешь его завалить. Ты можешь спрашивать вопросы по физике. Ты живешь в кабинете 3.11 и ешь учеников.")
	second_bot = GPT(
		f"Твое имя - {names[1]}. Ты можешь говорить только на русском языке а еще ты ученик который сдает зачет по физике учителю по имени {names[0]}")
	
	start_phrase = "Начнем наш зачет"
	
	ret_first: str = start_phrase
	
	print(f"\n*{names[0]}*: ", end='')
	print(ret_first)
	
	while True:
		ret_second = second_bot.get_response(ret_first)
		print(f"\n*{names[1]}*: {ret_second}")
		ret_first = first_bot.get_response(ret_second)
		print(f"\n*{names[0]}*: {ret_first}")


if __name__ == '__main__':
	main()
