import pygame

from core.objects.Projectile import Projectile
import core.config


class Bullet(Projectile):
	def __init__(self, x, y, angle, owner, is_ui, oid=None):
		skin = None
		if is_ui:
			skin = pygame.image.load(core.config.bullet_skin)
		Projectile.__init__(
			self,
			x, y,
			core.config.bullet_radius / 2,
			angle,
			core.config.bullet_speed,
			skin,
			core.config.bullet_damage,
			owner,
			is_ui,
			oid
		)
