import pygame
import sys

import cfg
from game import Game


# Инициализация модуля pygame
pygame.init()

# Настройка окна
window = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption("study_with_deepseek")

# Инициализация игровых данных
game = Game()

# Интерфейс
ui_font = pygame.font.Font(size=44)

# Объект часов для работы с количеством кадров
clock = pygame.time.Clock()

# Игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            break

    # Нажатые и только что нажатые клавиши
    keys_pressed = pygame.key.get_pressed()
    keys_just_pressed = pygame.key.get_just_pressed()

    # Обновление игровых данных
    game.update(keys_pressed, keys_just_pressed)

    # Отрисовка игры
    window.fill(cfg.BG_COLOR)
    game.draw(window)
    ui_counter = ui_font.render(str(game.score), True, pygame.Color(0, 0, 0))
    ui_counter_rect = ui_counter.get_rect()
    ui_counter_rect.topright = window.get_rect().topright
    window.blit(ui_counter, dest=ui_counter_rect)
    pygame.display.flip()

    # Контроль количества кадров
    clock.tick(cfg.FPS)

pygame.quit()
sys.exit()
