import pygame

from core import config
from core.objects.GameObject import GameObject
from core.HealthBar import HealthBar
from core.TankExplosion import TankExplosion
from core.objects.TextObject import TextObject
import core.config
from core.replay.data.PlayerState import PlayerState
from core.utils import rotate_center


class Tank(GameObject):
    health_bar_margin = 15
    label_margin = 20
    label_color = (255, 255, 255)

    def __init__(self, name, x, y, angle, speed, skin_ref, is_ui, oid=None):
        skin = None
        if is_ui:
            skin = pygame.image.load(skin_ref)
            self.blast_skin = pygame.image.load(config.blast_skin)

        GameObject.__init__(self, x, y, core.config.tank_radius / 2, angle, speed, skin, is_ui, oid)
        self.name = name

        self._health = 100
        self._score = 0
        self._has_blast = False

        if is_ui:
            self.health_bar = HealthBar(self.health, self.health_bar_center())
            self.font = pygame.font.SysFont("Arial", 18)
            self.label = TextObject(self.name, self.font, Tank.label_color, self.label_center())
            self.pending_explosion = TankExplosion(self.center)

    @property
    def health(self):
        return self._health

    @property
    def score(self):
        return self._score

    @property
    def has_blast(self):
        return self._has_blast

    @property
    def is_dead(self):
        return self.health == 0

    @has_blast.setter
    def has_blast(self, has_blast):
        self._has_blast = has_blast

    @health.setter
    def health(self, health):
        self._health = max(0, min(100, health))

    @score.setter
    def score(self, score):
        self._score = score

    def destroy(self):
        self.health = 0

    def health_bar_center(self):
        return self.x, self.y - self.radius - Tank.health_bar_margin

    def label_center(self):
        return self.x, self.y - self.radius - Tank.health_bar_margin - Tank.label_margin

    def explosion_center(self):
        return self.x - self.radius * 2, self.y - self.radius * 2

    def update(self, dt):
        super().update(dt)
        self.update_ui()
        if self.is_dead:
            self.velocity *= 0

    def update_ui(self):
        if not self.is_ui:
            return

        self.health_bar.update(self.health, self.health_bar_center())
        self.label.update(self.name, self.label_center())
        if self.is_dead:
            self.pending_explosion.launch(self.explosion_center())

    def update_tank_from_replay_frame(self,
                                      x: float, y: float, angle: float,
                                      score: int, health: int,
                                      has_blast: bool):
        super().update_object_from_replay_frame(x, y, angle)
        self.score = score
        self.health = health
        self.has_blast = has_blast

    def draw(self, surface):
        if not self.is_ui:
            return

        if not (self.is_dead and self.pending_explosion.completed):
            if self.has_blast:
                self.draw_attached_blast(surface)
            super().draw(surface)

        self.health_bar.draw(surface)
        self.label.draw(surface)
        if self.is_dead:
            self.pending_explosion.draw(surface)

    def draw_attached_blast(self, surface):
        if not self.is_ui:
            return

        rotated_skin = rotate_center(self.blast_skin, self.angle + 90)
        surface.blit(rotated_skin, (self.x - rotated_skin.get_width() / 2, self.y - rotated_skin.get_height() / 2))
