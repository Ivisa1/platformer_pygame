import pygame
import sys

import cfg
from game import Game

pygame.init()

game = Game()

ui_font = pygame.font.Font(size=44)

window = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
pygame.display.set_caption("study_with_deepseek")

clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            break

    keys_pressed = pygame.key.get_pressed()
    keys_just_pressed = pygame.key.get_just_pressed()

    game.update(keys_pressed, keys_just_pressed)

    window.fill(cfg.BG_COLOR)
    game.draw(window)
    ui_counter = ui_font.render(str(game.score), True, pygame.Color(0, 0, 0))
    ui_counter_rect = ui_counter.get_rect()
    ui_counter_rect.topright = window.get_rect().topright
    window.blit(ui_counter, dest=ui_counter_rect)
    pygame.display.flip()

    clock.tick(cfg.FPS)

pygame.quit()
sys.exit()
