import pygame
import random
import sys
import numpy as np
import os
from pygame.locals import *

def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу, работает и для .exe и для .py"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

pygame.init()
pygame.mixer.init()

# Начальные размеры окна
BASE_SCREEN_WIDTH = 1280
BASE_SCREEN_HEIGHT = 720
SCREEN_WIDTH = BASE_SCREEN_WIDTH
SCREEN_HEIGHT = BASE_SCREEN_HEIGHT

# Создаём окно с возможностью изменения размера
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Игровой проект - Ташевский, Каравашкин, Бехнуд, Алексеев")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 165, 0)

# Функция для масштабирования значений
def scale_value(value, base_size, current_size):
    return int(value * (current_size / base_size))

# Шрифты
def get_scaled_fonts():
    return (
        pygame.font.SysFont('comicsansms', scale_value(60, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)),
        pygame.font.SysFont('comicsansms', scale_value(40, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)),
        pygame.font.SysFont('comicsansms', scale_value(25, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT))
    )

font_large, font_medium, font_small = get_scaled_fonts()

FPS = 60
clock = pygame.time.Clock()

# Загрузка звуков
music_enabled = True
volume = 0.3  # Громкость по умолчанию
background_music = None
button_sound = None
hover_sound = None
try:
    background_music = pygame.mixer.Sound(resource_path("background_music.wav"))
    background_music.set_volume(volume)
    background_music.play(-1)
except Exception as e:
    print("Не удалось загрузить background_music.wav:", e)

try:
    button_sound = pygame.mixer.Sound(resource_path("click.wav"))
    button_sound.set_volume(0.6)
except Exception as e:
    print("Не удалось загрузить button_click.wav:", e)

try:
    hover_sound = pygame.mixer.Sound(resource_path("button_hover.wav"))
    hover_sound.set_volume(0.5)
except Exception as e:
    print("Не удалось загрузить button_hover.wav:", e)

class Star:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size = random.randint(1, 3)
        self.speed = random.randint(1, 3)
    
    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (self.x, self.y), self.size)

stars = [Star() for _ in range(100)]

class Button:
    def __init__(self, center_x_ratio, center_y_ratio, text, color, hover_color, dynamic_text=False):
        self.center_x_ratio = center_x_ratio
        self.center_y_ratio = center_y_ratio
        self.base_text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.was_hovered = False  # Новое поле
        self.dynamic_text = dynamic_text
        self.padding_x = scale_value(20, BASE_SCREEN_WIDTH, SCREEN_WIDTH)
        self.padding_y = scale_value(10, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)
        self.update_rect()
    
    def update_rect(self):
        self.center_x = int(self.center_x_ratio * SCREEN_WIDTH)
        self.center_y = int(self.center_y_ratio * SCREEN_HEIGHT)
        text_surf = font_medium.render(self.base_text if not self.dynamic_text else f"Музыка: {'Вкл' if music_enabled else 'Выкл'}", True, WHITE)
        width = text_surf.get_width() + self.padding_x * 2
        height = text_surf.get_height() + self.padding_y * 2
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = (self.center_x, self.center_y)
        self.text_surf = text_surf
        self.text_rect = text_surf.get_rect(center=self.rect.center)
    
    def draw(self, surface):
        if self.dynamic_text:
            self.update_rect()
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        surface.blit(self.text_surf, self.text_rect)
    
    def check_hover(self, pos):
        hovered = self.rect.collidepoint(pos)
        if hovered and not self.was_hovered:
            if hover_sound:
                hover_sound.play()
        self.was_hovered = hovered
        self.is_hovered = hovered
        return self.is_hovered

    def is_clicked(self, pos, event):
        return event.type == MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(pos)

# Общая функция для обработки событий
def handle_common_events(event, buttons, game_functions):
    global SCREEN_WIDTH, SCREEN_HEIGHT, font_large, font_medium, font_small, screen, stars, volume
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    if event.type == VIDEORESIZE:
        SCREEN_WIDTH, SCREEN_HEIGHT = event.size
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
        font_large, font_medium, font_small = get_scaled_fonts()
        stars.clear()
        stars.extend([Star() for _ in range(100)])
    if event.type == KEYDOWN:
        if event.key == K_1:
            if button_sound: button_sound.play()
            game_functions.get(0, lambda: None)()
        elif event.key == K_2:
            if button_sound: button_sound.play()
            game_functions.get(1, lambda: None)()
        elif event.key == K_0:
            if button_sound: button_sound.play()
            pygame.quit()
            sys.exit()
    for i, button in enumerate(buttons):
        if button.is_clicked(pygame.mouse.get_pos(), event):
            if button_sound: button_sound.play()
            if i == len(buttons) - 1:  # Кнопка выхода
                pygame.quit()
                sys.exit()
            elif i == len(buttons) - 2:  # Кнопка музыки
                global music_enabled
                music_enabled = not music_enabled
                if background_music:
                    if music_enabled:
                        background_music.play(-1)
                    else:
                        background_music.stop()
            else:
                game_functions.get(i, lambda: None)()
    # Обработка ползунка громкости
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        mx, my = pygame.mouse.get_pos()
        slider_x = SCREEN_WIDTH - 160
        slider_y = 20
        slider_w = 120
        slider_h = 16
        if slider_x <= mx <= slider_x + slider_w and slider_y <= my <= slider_y + slider_h:
            volume = (mx - slider_x) / slider_w
            if background_music:
                background_music.set_volume(volume)
            if button_sound:
                button_sound.set_volume(volume)
            if hover_sound:
                hover_sound.set_volume(volume * 0.8)

def draw_volume_slider():
    slider_x = SCREEN_WIDTH - 160
    slider_y = 20
    slider_w = 120
    slider_h = 16
    # Фон
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_w, slider_h), border_radius=8)
    # Заполненная часть
    pygame.draw.rect(screen, CYAN, (slider_x, slider_y, int(slider_w * volume), slider_h), border_radius=8)
    # Обводка
    pygame.draw.rect(screen, WHITE, (slider_x, slider_y, slider_w, slider_h), 2, border_radius=8)
    # Эмодзи динамика слева от полоски через шрифт Segoe UI Emoji
    emoji_font = pygame.font.SysFont('Segoe UI Emoji', scale_value(25, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT))
    vol_icon = emoji_font.render("🔊", True, WHITE)
    icon_rect = vol_icon.get_rect()
    icon_rect.centery = slider_y + slider_h // 2
    icon_rect.right = slider_x - 8
    screen.blit(vol_icon, icon_rect)

def draw_animated_background():
    for star in stars:
        star.update()
        star.draw(screen)

def game_over_screen(score, game_name):
    back_button = Button(0.5, 0.75, "Назад", ORANGE, YELLOW)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)
        draw_animated_background()
        
        game_over_text = font_large.render("Игра окончена!", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//3))
        
        score_text = font_medium.render(f"Ваш счет в {game_name}: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2))
        
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            handle_common_events(event, [back_button], {})
            if event.type == KEYDOWN or back_button.is_clicked(mouse_pos, event):
                return

def snake_game():
    CELL_SIZE = scale_value(20, BASE_SCREEN_WIDTH, SCREEN_WIDTH)
    GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
    GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE
    
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (1, 0)
    pending_direction = direction
    food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
    bonuses = []
    obstacles = [(random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)) for _ in range(5) 
                 if (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)) not in snake and 
                 (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)) != food]
    score = 0
    speed = 10
    last_move_time = 0
    paused = False
    dragon_mode = False
    dragon_timer = 0
    secret_input = ""
    
    back_button = Button(0.9, 0.92, "Назад", ORANGE, YELLOW)
    pause_button = Button(0.7, 0.92, "Пауза", PURPLE, CYAN)
    
    while True:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            handle_common_events(event, [back_button, pause_button], {})
            if event.type == KEYDOWN:
                if event.key == K_UP and direction != (0, 1):
                    pending_direction = (0, -1)
                elif event.key == K_DOWN and direction != (0, -1):
                    pending_direction = (0, 1)
                elif event.key == K_LEFT and direction != (1, 0):
                    pending_direction = (-1, 0)
                elif event.key == K_RIGHT and direction != (-1, 0):
                    pending_direction = (1, 0)
                elif event.key == K_ESCAPE:
                    return
                elif event.key == K_p:
                    paused = not paused
                else:
                    # Проверяем, является ли клавиша буквенно-цифровой
                    if event.unicode and event.unicode.isalnum():
                        secret_input += event.unicode.upper()
                        if "SNAKE" in secret_input:
                            dragon_mode = True
                            dragon_timer = current_time + 10000
                            secret_input = ""
            if back_button.is_clicked(mouse_pos, event):
                return
            if pause_button.is_clicked(mouse_pos, event):
                paused = not paused
        
        if not paused and current_time - last_move_time > 1000 // speed:
            last_move_time = current_time
            direction = pending_direction
            if dragon_mode and current_time > dragon_timer:
                dragon_mode = False
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or 
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in obstacles or new_head in snake):
                game_over_screen(score, "Змейка")
                return
            
            snake.insert(0, new_head)
            if new_head == food:
                score += 10
                food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                while food in snake or food in obstacles:
                    food = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                if random.random() < 0.3:
                    bonus = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                    while bonus in snake or bonus == food or bonus in obstacles:
                        bonus = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                    bonuses.append((bonus, current_time + 5000))
            else:
                snake.pop()
            
            for bonus in bonuses[:]:
                pos, timer = bonus
                if current_time > timer:
                    bonuses.remove(bonus)
                    continue
                if new_head == pos:
                    bonuses.remove(bonus)
                    bonus_type = random.choice(["speed_up", "speed_down", "score"])
                    if bonus_type == "speed_up":
                        speed += 2
                    elif bonus_type == "speed_down":
                        speed = max(5, speed - 2)
                    elif bonus_type == "score":
                        score += 50
            
            if random.random() < 0.05:
                obstacle = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                while obstacle in snake or obstacle == food or obstacle in bonuses or obstacle in obstacles:
                    obstacle = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
                obstacles.append(obstacle)
        
        screen.fill(BLACK)
        draw_animated_background()
        
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))
        
        for i, segment in enumerate(snake):
            color = ORANGE if dragon_mode else GREEN
            if dragon_mode and i == 0:
                pygame.draw.rect(screen, RED, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.circle(screen, YELLOW, (segment[0]*CELL_SIZE + CELL_SIZE//2, segment[1]*CELL_SIZE), CELL_SIZE//2)
            else:
                pygame.draw.rect(screen, color, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        pygame.draw.rect(screen, RED, (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        for bonus, _ in bonuses:
            pygame.draw.circle(screen, CYAN, (bonus[0]*CELL_SIZE + CELL_SIZE//2, bonus[1]*CELL_SIZE + CELL_SIZE//2), CELL_SIZE//2)
        
        for obstacle in obstacles:
            pygame.draw.rect(screen, GRAY, (obstacle[0]*CELL_SIZE, obstacle[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        score_text = font_small.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        pause_button.check_hover(mouse_pos)
        pause_button.draw(screen)
        
        draw_volume_slider()
        
        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            pause_text = font_large.render("Пауза", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - pause_text.get_height()//2))
        
        pygame.display.update()
        clock.tick(FPS)

def game_2048():
    CELL_SIZE = scale_value(100, BASE_SCREEN_WIDTH, SCREEN_WIDTH)
    GRID_SIZE = 4
    GRID_PADDING = scale_value(10, BASE_SCREEN_WIDTH, SCREEN_WIDTH)
    GRID_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GRID_PADDING
    GRID_HEIGHT = GRID_WIDTH
    GRID_X = (SCREEN_WIDTH - GRID_WIDTH) // 2
    GRID_Y = (SCREEN_HEIGHT - GRID_HEIGHT) // 2
    
    TILE_COLORS = {0: (204, 192, 179), 2: (238, 228, 218), 4: (237, 224, 200), 8: (242, 177, 121),
                   16: (245, 149, 99), 32: (246, 124, 95), 64: (246, 94, 59), 128: (237, 207, 114),
                   256: (237, 204, 97), 512: (237, 200, 80), 1024: (237, 197, 63), 2048: (237, 194, 46)}

    def add_random_tile(grid):
        empty_cells = [(y, x) for y in range(4) for x in range(4) if grid[y][x] == 0]
        if empty_cells:
            y, x = random.choice(empty_cells)
            grid[y][x] = 2 if random.random() < 0.9 else 4
    
    def merge_tiles(line):
        new_line = [0] * 4
        index = score_change = 0
        for i in range(4):
            if line[i] != 0:
                if new_line[index] == 0:
                    new_line[index] = line[i]
                elif new_line[index] == line[i]:
                    new_line[index] *= 2
                    score_change += new_line[index]
                    index += 1
                else:
                    index += 1
                    new_line[index] = line[i]
        return np.array(new_line), score_change
    
    def move_grid(grid, direction_func):
        moved = False
        score_change = 0
        for i in range(4):
            line = direction_func(grid, i)
            new_line, sc = merge_tiles(line)
            if not np.array_equal(line, new_line):
                direction_func(grid, i, new_line)
                moved = True
                score_change += sc
        return moved, score_change
    
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    add_random_tile(grid)
    add_random_tile(grid)
    score = 0
    game_over = False
    paused = False
    
    back_button = Button(0.9, 0.92, "Назад", ORANGE, YELLOW)
    pause_button = Button(0.7, 0.92, "Пауза", PURPLE, CYAN)
    
    while True:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            handle_common_events(event, [back_button, pause_button], {})
            if event.type == KEYDOWN:
                if not game_over and not paused:
                    moved = False
                    sc = 0
                    if event.key == K_UP:
                        moved, sc = move_grid(grid, lambda g, i, v=None: g[:, i] if v is None else g.__setitem__((slice(None), i), v))
                    elif event.key == K_DOWN:
                        moved, sc = move_grid(grid, lambda g, i, v=None: g[:, i][::-1] if v is None else g.__setitem__((slice(None), i), v[::-1]))
                    elif event.key == K_LEFT:
                        moved, sc = move_grid(grid, lambda g, i, v=None: g[i, :] if v is None else g.__setitem__((i, slice(None)), v))
                    elif event.key == K_RIGHT:
                        moved, sc = move_grid(grid, lambda g, i, v=None: g[i, :][::-1] if v is None else g.__setitem__((i, slice(None)), v[::-1]))
                    if moved:
                        score += sc
                        add_random_tile(grid)
                        if not (0 in grid or any(grid[y][x] == grid[y][x+1] for y in range(4) for x in range(3)) or 
                                any(grid[y][x] == grid[y+1][x] for y in range(3) for x in range(4))):
                            game_over = True
                if event.key == K_ESCAPE:
                    return
                elif event.key == K_r:
                    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
                    add_random_tile(grid)
                    add_random_tile(grid)
                    score = 0
                    game_over = False
                elif event.key == K_p:
                    paused = not paused
            if back_button.is_clicked(mouse_pos, event):
                return
            if pause_button.is_clicked(mouse_pos, event):
                paused = not paused
        
        screen.fill(BLACK)
        draw_animated_background()
        
        score_text = font_medium.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, scale_value(30, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)))
        
        pygame.draw.rect(screen, (187, 173, 160), (GRID_X, GRID_Y, GRID_WIDTH, GRID_HEIGHT))
        
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                value = grid[y][x]
                tile_x = GRID_X + GRID_PADDING + x * (CELL_SIZE + GRID_PADDING)
                tile_y = GRID_Y + GRID_PADDING + y * (CELL_SIZE + GRID_PADDING)
                pygame.draw.rect(screen, TILE_COLORS.get(value, (60, 58, 50)), (tile_x, tile_y, CELL_SIZE, CELL_SIZE))
                if value:
                    text = (font_medium if value < 1000 else font_small).render(str(value), True, (119, 110, 101) if value < 8 else (249, 246, 242))
                    screen.blit(text, text.get_rect(center=(tile_x + CELL_SIZE//2, tile_y + CELL_SIZE//2)))
        
        back_button.check_hover(mouse_pos)
        back_button.draw(screen)
        pause_button.check_hover(mouse_pos)
        pause_button.draw(screen)
        
        draw_volume_slider()
        
        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            game_over_text = font_large.render("Игра окончена!", True, WHITE)
            restart_text = font_medium.render("Нажмите R для рестарта", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - game_over_text.get_height()//2 - scale_value(30, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 - restart_text.get_height()//2 + scale_value(30, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)))
        
        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))
            pause_text = font_large.render("Пауза", True, WHITE)
            screen.blit(pause_text, (SCREEN_WIDTH//2 - pause_text.get_width()//2, SCREEN_HEIGHT//2 - pause_text.get_height()//2))
        
        pygame.display.update()
        clock.tick(FPS)

def main_menu():
    button_configs = [
        ("1. Змейка", BLUE, (100, 150, 255), False, 0.35),
        ("2. Игра 2048", GREEN, (100, 255, 100), False, 0.48),
        ("Музыка: Вкл", CYAN, (150, 255, 255), True, 0.61),
        ("0. Выход", PURPLE, (200, 100, 200), False, 0.74)
    ]
    
    buttons = [Button(0.5, y_ratio, text, color, hover_color, dynamic_text)
               for text, color, hover_color, dynamic_text, y_ratio in button_configs]
    
    game_functions = {0: snake_game, 1: game_2048}
    
    while True:
        for button in buttons:
            button.update_rect()
        
        screen.fill(BLACK)
        draw_animated_background()
        draw_volume_slider()
        
        title = font_large.render("Игровой проект", True, YELLOW)
        title_y = scale_value(50, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, title_y))
        
        developers = font_small.render("Разработчики: Ташевский, Каравашкин, Бехнуд, Алексеев", True, CYAN)
        dev_y = title_y + scale_value(80, BASE_SCREEN_HEIGHT, SCREEN_HEIGHT)
        screen.blit(developers, (SCREEN_WIDTH // 2 - developers.get_width() // 2, dev_y))
        
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            handle_common_events(event, buttons, game_functions)
        
        clock.tick(FPS)

if __name__ == "__main__":
    main_menu()