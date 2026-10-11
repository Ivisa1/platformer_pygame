import pygame
from os import listdir
from os.path import join
from typing import TYPE_CHECKING

import cfg

if TYPE_CHECKING:
    from level import Tile
    from camera import Camera


class Player(pygame.sprite.Sprite):
    """
    Класс игрового персонажа
    """

    def __init__(
            self,
            start_pos: tuple[int, int],
            size: tuple[int, int],
            collide_size: tuple[int, int],
            color: tuple[int, int, int]
    ) -> None:
        super().__init__()
        self.start_pos: tuple[int, int] = start_pos
        self.draw_rect: pygame.Rect | pygame.FRect = pygame.Rect(start_pos, size)
        self.rect: pygame.Rect | pygame.FRect = pygame.Rect(start_pos, collide_size)
        self.rect.midbottom = self.draw_rect.midbottom
        self.color: pygame.Color = pygame.Color(color)
        self.image: pygame.Surface = pygame.Surface(self.draw_rect.size, pygame.SRCALPHA)
        self.image.fill(self.color)
        self.current_speed: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
        self.last_direction_x: int = 1
        self.on_ground: bool = False
        self.animations: dict[str, list[pygame.Surface]] = self.load_animations(join("assets", "player"))
        self.last_animation: str = 'idle'
        self.current_animation: str = 'idle'
        self.current_animation_frame: int = 0

    def load_animations(self, folder: str) -> dict[str, list[pygame.Surface]]:
        """
        Загружает все анимации в данные персонажа
        """
        animations: dict[str, list[pygame.Surface]] = {}
        for file in listdir(folder):
            animation_name = file.split('.')[0]
            animations[animation_name] = []
            full_animation: pygame.Surface = pygame.image.load(join(folder, file)).convert_alpha()
            rows_cols = list(
                map(
                    int, [full_animation.size[i] / cfg.PLAYER_SIZE[i] for i in range(len(full_animation.size)-1, -1, -1)]
                )
            )
            for row in range(rows_cols[0]):
                for col in range(rows_cols[1]):
                    animations[animation_name].append(
                        full_animation.subsurface(
                            col*cfg.PLAYER_SIZE[0],
                            row*cfg.PLAYER_SIZE[1],
                            cfg.PLAYER_SIZE[0],
                            cfg.PLAYER_SIZE[1]
                        )
                    )
        print(animations)
        return animations

    def set_player_to_start_pos(self) -> None:
        """
        Устанавливает rect и collide_rect пользователя в стартовую позицию
        """
        self.draw_rect = self.draw_rect.move_to(topleft=self.start_pos)
        self.rect.midbottom = self.draw_rect.midbottom

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

    def _update_current_and_last_animations(self):
        """
        Обновляет параметр анимации, проигрываемой на предыдущем тике.
        Обновляет номер текущего кадра анимации
        """
        if self.current_animation == self.last_animation:
            self.current_animation_frame = (
                self.current_animation_frame + 1
                if self.current_animation_frame + 1 < len(self.animations[self.current_animation]) else
                0
            )
        else:
            self.last_animation = self.current_animation
            self.current_animation_frame = 0

    def set_last_direction(self):
        """
        Записывает последнее направление, в котором двигался персонаж
        """
        if self.current_speed.x > 0:
            self.last_direction_x = 1
        elif self.current_speed.x < 0:
            self.last_direction_x = -1

    def set_animation_image(self):
        """
        Устанавливает поверхность, которая будет отображаться при рисовании героя
        """
        if self.last_direction_x == 1:
            self.image = self.animations[self.current_animation][self.current_animation_frame]
        elif self.last_direction_x == -1:
            self.image = pygame.transform.flip(
                self.animations[self.current_animation][self.current_animation_frame],
                flip_x=True,
                flip_y=False
            )

    def update_animation(self):
        """
        Обновляет текущую анимацию
        """
        if self.on_ground == True:
            if self.current_speed.x:
                self.current_animation = 'run'
                self._update_current_and_last_animations()
            elif not self.current_speed.x:
                self.current_animation = 'idle'
                self._update_current_and_last_animations()
        else:
            if self.current_speed.y <= 0:
                self.current_animation = 'jump'
                self._update_current_and_last_animations()
            if self.current_speed.y > 0:
                self.current_animation = 'fall'
                self._update_current_and_last_animations()
        self.set_animation_image()
        self.set_last_direction()

    def update(self, bounds: pygame.Rect, platforms: pygame.sprite.Group) -> None:
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
        self.draw_rect.midbottom = self.rect.midbottom
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
        self.draw_rect.midbottom = self.rect.midbottom
        self.last_direction_x = (
            1 if self.current_speed.x > 0 else
            -1 if self.current_speed.x < 0 else
            self.last_direction_x
        )
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.current_speed.x > 0:
                    self.rect.right = platform.rect.left
                    self.draw_rect.midbottom = self.rect.midbottom
                elif self.current_speed.x < 0:
                    self.rect.left = platform.rect.right
                    self.draw_rect.midbottom = self.rect.midbottom
                break

        self.update_animation()

        self.current_speed.x = 0
        self.rect.clamp_ip(bounds)
        self.draw_rect.midbottom = self.rect.midbottom

    def draw(self, surface: pygame.Surface, camera: 'Camera'):
        """
        Метод отрисовки персонажа
        """
        surface.blit(self.image, camera.apply(self.draw_rect).topleft)
