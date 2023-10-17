from core.objects.GameObject import GameObject

import core.config


class Bonus(GameObject):
    def __init__(self, x, y, lifetime, spawned_at, skin, is_ui, oid=None):
        GameObject.__init__(self, x, y, core.config.default_bonus_radius, 0, 0, skin, is_ui, oid)
        self.lifetime = lifetime
        self.spawned_at = spawned_at

    def is_expired(self, time):
        return time - self.spawned_at > self.lifetime
