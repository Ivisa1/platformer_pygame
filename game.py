import pygame
from os.path import join, isfile

import cfg
from camera import Camera
from level import Level
from player import Player

class Game:
    def __init__(self) -> None:
        self.score = 0
        self.camera = Camera()
        self.level_index = 0
        self.level = Level(join("levels", f"level_{int(self.level_index)}.csv"))
        self.player = Player(self.level.start_pos, cfg.PLAYER_SIZE, cfg.PLAYER_COLOR)

    def next_level(self, path: str) -> None:
        self.level.clear_level()
        self.level.load_level(path)

    def update(self, key_pressed, key_just_pressed) -> None:
        self.player.handle_input(key_pressed, key_just_pressed)
        self.player.update(self.level.level_bounds, self.level.platforms)
        for enemy in self.level.enemies:
            enemy.update(self.level.level_bounds, self.level.platforms)
        for enemy in self.level.enemies:
            if enemy.rect.colliderect(self.player.rect):
                self.player.set_player_to_start_pos()
                self.player.set_speed_to_zero()
                self.player.on_ground = False
                break
        self.score += self.level.interact_objects(self.player)
        if self.level.complete:
            self.level_index += 1
            level_path = join("levels", f"level_{int(self.level_index)}.csv")
            if isfile(level_path):
                self.next_level(level_path)
            else:
                self.level_index = 0
                self.score = 0
                level_path = join("levels", f"level_{int(self.level_index)}.csv")
                self.next_level(level_path)
            self.player.start_pos = self.level.start_pos
            self.player.set_player_to_start_pos()
            self.player.set_speed_to_zero()
        self.camera.update(self.player.rect, self.level.level_bounds, (cfg.WIDTH, cfg.HEIGHT))

    def draw(self, surface: pygame.Surface) -> None:
        self.level.draw(surface, self.camera)
        self.player.draw(surface, self.camera)