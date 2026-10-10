import pygame
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from level import Tile
    from camera import Camera


class Directions(Enum):
    LEFT = -1
    RIGHT = 1
    STOP = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(
            self,
            position: tuple[int, int],
            size: tuple[int, int],
            color: pygame.Color,
            speed_x: int,
            direction: Directions
    ):
        super().__init__()
        self.start_position = position
        self.rect: pygame.Rect = pygame.Rect(position, size)
        self.color: pygame.Color = color
        self.image: pygame.Surface = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.image.fill(self.color)
        self.speed_x: int = speed_x
        self.direction: Directions = direction

    def update(self, bounds: pygame.Rect, platforms: list['Tile']):
        """
        Обработка физики противников
        """
        if self.direction != Directions.STOP:
            self.rect.x += self.speed_x * self.direction.value
            if not bounds.contains(self.rect):
                self.rect.clamp_ip(bounds)
                self.direction = Directions(self.direction.value*-1)
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    if self.direction == Directions.LEFT:
                        self.rect.left = platform.rect.right
                        self.direction = Directions.RIGHT
                        break
                    elif self.direction == Directions.RIGHT:
                        self.rect.right = platform.rect.left
                        self.direction = Directions.LEFT
                        break


    def draw(self, surface: pygame.Surface, camera: 'Camera'):
        pygame.draw.rect(surface, self.color, camera.apply(self.rect))