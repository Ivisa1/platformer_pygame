import pygame
from typing import TYPE_CHECKING

import cfg

if TYPE_CHECKING:
    from level import Tile
    from camera import Camera


class Player(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple[int, int], size: tuple[int, int], color: tuple[int, int, int]) -> None:
        super().__init__()
        self.start_pos: tuple[int, int] = start_pos
        self.rect: pygame.Rect | pygame.FRect = pygame.Rect(start_pos, size)
        self.color: pygame.Color = pygame.Color(color)
        self.image: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(self.color)
        self.current_speed: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.on_ground: bool = False

    def set_player_to_start_pos(self) -> None:
        """
        Устанавливает rect пользователя в стартовую позицию
        """
        self.rect = self.rect.move_to(topleft=self.start_pos)

    def set_speed_to_zero(self) -> None:
        """
        Делает вектор скорости игрока нулевым
        """
        self.current_speed: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

    def handle_input(
            self,
            keys_pressed: pygame.key.ScancodeWrapper,
            keys_just_pressed: pygame.key.ScancodeWrapper
    ) -> None:
        """
        Обработка ввода от пользователя для управления персонажем
        """
        if keys_just_pressed[pygame.K_SPACE] and self.on_ground:
            self.current_speed.y = cfg.JUMP_POWER
            self.on_ground = False
        if keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]:
            self.current_speed.x -= cfg.PLAYER_VELOCITY_X
        if keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]:
            self.current_speed.x += cfg.PLAYER_VELOCITY_X

    def update(self, bounds: pygame.Rect, platforms: list['Tile']) -> None:
        """
        Обработка физики персонажа
        """
        self.on_ground = False

        ### ДВИЖЕНИЕ И ОБРАБОТКА СТОЛКНОВЕНИЙ ПО Y ###
        self.current_speed.y += cfg.GRAVITY
        if self.current_speed.y > 0:
            self.current_speed.y = min(int(self.current_speed.y), int(cfg.MAX_FALL_SPEED))
        elif self.current_speed.y < 0:
            self.current_speed.y = max(int(self.current_speed.y), int(-cfg.MAX_FALL_SPEED))
        self.rect.y += self.current_speed.y
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.current_speed.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.current_speed.y = 0
                elif self.current_speed.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.current_speed.y = 0
                break
        if self.rect.bottom >= bounds.bottom:
            self.current_speed.y = 0
            self.on_ground = True

        ### ДВИЖЕНИЕ И ОБРАБОТКА СТОЛКНОВЕНИЙ ПО X ###
        self.rect.x += int(self.current_speed.x)
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.current_speed.x > 0:
                    self.rect.right = platform.rect.left
                elif self.current_speed.x < 0:
                    self.rect.left = platform.rect.right
                break
        self.current_speed.x = 0

        self.rect.clamp_ip(bounds)

    def draw(self, surface: pygame.Surface, camera: 'Camera'):
        surface.blit(self.image, camera.apply(self.rect).topleft)
