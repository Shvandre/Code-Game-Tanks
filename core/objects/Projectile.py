from core.objects.GameObject import GameObject


class Projectile(GameObject):
	def __init__(self, x, y, radius, angle, speed, skin, damage, owner, is_ui, oid=None):
		GameObject.__init__(self, x, y, radius, angle, speed, skin, is_ui, oid)
		self._damage = damage
		self._owner = owner

	@property
	def damage(self):
		return self._damage

	@property
	def owner(self):
		return self._owner

	def damage_applied(self, obj):
		if self.owner is obj:
			return 0
		else:
			return self.damage
