import pygame
from pygame.rect import Rect


class HealthBar:

    background_color = (240, 0, 0)
    line_color = (0, 0, 0)
    health_color = (0, 220, 0)
    rect = Rect(0, 0, 70, 10)
    line_thickness = 2

    health_max = 100

    def __init__(self, initial_health, center):
        self._health = initial_health
        self._rect = HealthBar.rect.copy()
        self._rect.center = center

    def update(self, health, center):
        self._health = health
        self._rect.center = center

    def draw(self, surface):
        pygame.draw.rect(surface, HealthBar.background_color, self._rect)
        pygame.draw.rect(surface, HealthBar.line_color, self._rect, 2)

        if self._health > 0:
            health_rect = self._rect.copy()
            health_rect.width = health_rect.width * (self._health / HealthBar.health_max) - HealthBar.line_thickness * 2 + 1
            health_rect.height = health_rect.height - HealthBar.line_thickness * 2 + 1
            health_rect.x += HealthBar.line_thickness
            health_rect.y += HealthBar.line_thickness
            pygame.draw.rect(surface, HealthBar.health_color, health_rect)
