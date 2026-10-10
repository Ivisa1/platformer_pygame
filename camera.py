import pygame

from help_funcs import clamp


class Camera:
    def __init__(self):
        self.offset: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

    def update(self, target_rect: pygame.Rect, level_bounds: pygame.Rect, screen_size: tuple[int, int]):
        desired_x = target_rect.centerx - screen_size[0] / 2
        desired_y = target_rect.centery - screen_size[1] / 2
        self.offset.x = clamp(desired_x, 0, level_bounds.width-screen_size[0])
        self.offset.y = clamp(desired_y, 0, level_bounds.height-screen_size[1])

    def apply(self, rect: pygame.Rect) -> pygame.Rect:
        new_rect = pygame.Rect(
            (rect.x-self.offset.x, rect.y-self.offset.y),
            rect.size
        )
        return new_rect

    def draw_sprite_group(self, surface: pygame. Surface, sprite_group: pygame.sprite.Group):
        for sprite in sprite_group.sprites():
            surface.blit(sprite.image, self.apply(sprite.rect).topleft)