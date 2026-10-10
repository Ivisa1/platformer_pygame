import pygame
from enum import Enum

import cfg
from camera import Camera
from enemy import Enemy, Directions
from  player import Player


class Form(Enum):
    """
    Перечисление возможных форм объектов
    """
    RECT = 'rect'
    CIRCLE = 'circle'

class Tile(pygame.sprite.Sprite):
    """
    Класс для платформ на уровне
    """
    def __init__(
            self,
            color: tuple[int, int, int],
            position: tuple[int, int],
            size: tuple[int, int],
    ):
        super().__init__()
        self.color: pygame.Color = pygame.Color(color)
        self.rect: pygame.Rect = pygame.Rect(position, size)
        self.image: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill(self.color)

class Object(pygame.sprite.Sprite):
    """
    Класс для игровых объектов на уровне
    """
    def __init__(
            self,
            form: Form,
            color: tuple[int, int, int],
            position: tuple[int, int],
            size: tuple[int, int],
            radius: int
    ):
        super().__init__()
        self.form: Form = form
        self.color: pygame.Color = pygame.Color(color)
        self.rect: pygame.Rect = pygame.Rect(position, size)
        self.radius = radius
        self.image: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        if self.form == Form.RECT:
            self.image.fill(self.color)
        elif self.form == Form.CIRCLE:
            pygame.draw.circle(self.image, self.color, self.image.get_rect().center, radius)


class Level:
    def __init__(self, path: str) -> None:
        self.platforms: pygame.sprite.Group = pygame.sprite.Group()
        self.objects: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.start_pos = (0, 0)
        self.width = 0
        self.height = 0
        self.level_bounds = pygame.Rect(
            (0, 0),
            (self.width, self.height)
        )
        self.finish: Object | None = None
        self.load_level(path)
        self.complete = False

    def clear_level(self):
        """
        Очистка данных уровня перед загрузкой следующего
        """
        self.platforms: pygame.sprite.Group = pygame.sprite.Group()
        self.objects: pygame.sprite.Group = pygame.sprite.Group()
        self.enemies: pygame.sprite.Group = pygame.sprite.Group()
        self.start_pos = (0, 0)
        self.width = 0
        self.height = 0
        self.level_bounds = pygame.Rect(
            (0, 0),
            (0, 0)
        )
        self.finish: Object | None = None
        self.complete = False

    def load_level(self, path: str) -> None:
        """
        Загрузка уровня
        """
        self.clear_level()
        with open(path, 'r', encoding='utf-8') as file:
            for i, row in enumerate(file):
                self.height = (i+1) * cfg.PLATFORM_SIZE[1]
                row = row.strip()
                row = row.split(',')
                for y, field in enumerate(row):
                    if self.width < (y+1) * cfg.PLATFORM_SIZE[0]:
                        self.width = (y+1) * cfg.PLATFORM_SIZE[0]
                    if field != cfg.PLATFORM_EMPTY:
                        if field == cfg.START_POS_PLATFORM:
                            self.start_pos = (y*cfg.PLATFORM_SIZE[0], i*cfg.PLATFORM_SIZE[1])
                        elif field in cfg.PLATFORM_PARAMS:
                            self.platforms.add(
                                Tile(
                                    position=(y * cfg.PLATFORM_SIZE[0], i * cfg.PLATFORM_SIZE[1]),
                                    size=cfg.PLATFORM_SIZE,
                                    color=cfg.PLATFORM_PARAMS.get(field, {}).get('color', pygame.Color(0, 0, 0))
                                )
                            )
                        elif field in cfg.OBJECTS_PARAMS:
                            object_info = cfg.OBJECTS_PARAMS.get(field, {})
                            if field == '8':
                                self.finish = Object(
                                    form=Form(object_info.get('form', 'rect')),
                                    color=object_info.get('color', pygame.Color(0, 0, 0)),
                                    position=(y * cfg.PLATFORM_SIZE[0], i * cfg.PLATFORM_SIZE[1]),
                                    size=cfg.PLATFORM_SIZE,
                                    radius=object_info.get('radius', 0)
                                )
                                continue
                            self.objects.add(
                                Object(
                                    form=Form(object_info.get('form', 'rect')),
                                    color=object_info.get('color', pygame.Color(0, 0, 0)),
                                    position=(y * cfg.PLATFORM_SIZE[0], i * cfg.PLATFORM_SIZE[1]),
                                    size=cfg.PLATFORM_SIZE,
                                    radius=object_info.get('radius', 0)
                                )
                            )
                        elif field in cfg.ENEMIES_PARAMS:
                            enemy_info = cfg.ENEMIES_PARAMS.get(field, {})
                            self.enemies.add(
                                Enemy(
                                    (y * cfg.PLATFORM_SIZE[0], i * cfg.PLATFORM_SIZE[1]),
                                    cfg.PLATFORM_SIZE,
                                    pygame.Color(enemy_info.get('color', (255, 255, 255))),
                                    enemy_info.get('speed_x', 3),
                                    Directions(enemy_info.get('direction', 0))
                                )
                            )
        self.level_bounds = pygame.Rect(
            (0, 0),
            (self.width, self.height)
        )

    def interact_objects(self, player: 'Player') -> int:
        """
        Обработка взаимодействий с объектами уровня
        """
        collected = len(pygame.sprite.spritecollide(player, self.objects, dokill=True))

        if self.finish and self.finish.rect.colliderect(player.rect):
            self.complete = True
        return collected

    def draw(self, surface: pygame.Surface, camera: Camera):
        """
        Отрисовка всех объектов уровня
        """
        camera.draw_sprite_group(surface, self.platforms)
        camera.draw_sprite_group(surface, self.objects)
        camera.draw_sprite_group(surface, self.enemies)
        if self.finish:
            surface.blit(self.finish.image, camera.apply(self.finish.rect).topleft)
