from rembg import remove as remove_bg
from PIL import Image


def remove_background(inp_path: str = 'input.png', out_path: str = 'output.png') -> None:
	img = Image.open(inp_path)
	result = remove_bg(img)
	result.save(out_path)


if __name__ == '__main__':
	remove_background()
