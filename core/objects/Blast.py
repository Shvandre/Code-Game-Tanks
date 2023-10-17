import pygame

from core.objects.Projectile import Projectile
import core.config


class Blast(Projectile):

	size = 100
	speed = 0.25
	damage = 47

	def __init__(self, x, y, angle, owner, is_ui, oid=None):
		skin = None
		if is_ui:
			skin = pygame.image.load(core.config.blast_skin)
		Projectile.__init__(
			self,
			x, y,
			core.config.blast_radius / 2,
			angle,
			core.config.blast_speed,
			skin,
			core.config.blast_damage,
			owner,
			is_ui,
			oid
		)
