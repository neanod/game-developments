import pygame
import sys

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Размер окна
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# Создание окна
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ваша игра")

# Создание поверхности для текста
text_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
text_surface.fill(WHITE)

# Инициализация шрифта
font = pygame.font.Font(None, 36)

# Текст о создателях
creators_text = [
    "Создатели:",
    "Neanod - программист",
    "Kotsem - дизайнер",
    "Mregorian - художник",
    "Мы с друзьями с радостью создали эту игру!",
]

# Определение параметров для текста
text_color = BLACK
text_y = WINDOW_HEIGHT // 2 - (len(creators_text) * 36) // 2
scroll_speed = 1  # Увеличим скорость прокрутки

# Функция для отображения текста
def display_text():
    text_surface.fill(WHITE)
    y = text_y
    for line in creators_text:
        text = font.render(line, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y))
        text_surface.blit(text, text_rect)
        y += 36

# Функция для прокрутки текста
def scroll_text(text_lines, scroll_position):
    text_surface.fill(WHITE)
    y = text_y
    for i, line in enumerate(text_lines):
        if y > scroll_position - WINDOW_HEIGHT and y < scroll_position:
            text = font.render(line, True, BLACK)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y - scroll_position + WINDOW_HEIGHT))
            text_surface.blit(text, text_rect)
        #y += 36
        ...

# Функция для обработки действий в меню
def handle_menu_click(action):
    if action == "Играть":
        # Здесь вы можете добавить код для вашей игры
        pass
    elif action == "Настройки":
        clear_screen()
        create_volume_slider()
    elif action == "Выход":
        pygame.quit()
        sys.exit()
    elif action == "Создатели":
        display_creators()

# Функция для создания ползунка громкости
def create_volume_slider():
    # Ваш код для создания ползунка громкости здесь
    pass

# Функция для очистки экрана
def clear_screen():
    screen.fill(WHITE)

# Функция для отображения информации о создателях
def display_creators():
    clear_screen()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    handle_menu_click(check_button_click(event.pos))

        # Очистка экрана
        clear_screen()

        display_text()  # Отображаем текст о создателях

        screen.blit(text_surface, (0, 0))
        pygame.display.update()

# Функция для отображения меню
def display_menu():
    clear_screen()
    menu_items = ["Играть", "Настройки", "Выход", "Создатели"]
    text_y = 175
    for item in menu_items:
        text = font.render(item, True, text_color)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, text_y))
        text_surface.blit(text, text_rect)
        text_y += 50

    screen.blit(text_surface, (0, 0))
    pygame.display.update()

# Функция для определения, на какую кнопку было нажато
def check_button_click(pos):
    if 150 <= pos[0] <= 450 and 175 <= pos[1] <= 225:
        return "Играть"
    elif 150 <= pos[0] <= 450 and 225 <= pos[1] <= 275:
        return "Настройки"
    elif 150 <= pos[0] <= 450 and 275 <= pos[1] <= 325:
        return "Выход"
    elif 150 <= pos[0] <= 450 and 325 <= pos[1] <= 375:
        return "Создатели"

if __name__ == "__main__":
    display_menu()  # Отображение меню при старте
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    action = check_button_click(event.pos)
                    handle_menu_click(action)

    pygame.quit()
    sys.exit()
