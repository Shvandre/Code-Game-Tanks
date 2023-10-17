import random

from core.objects.BonusBlast import BonusBlast
from core.objects.BonusRepair import BonusRepair
import core.config


class BonusManager:
    def __init__(self, world_bounds, tanks, projectiles, bonuses, is_ui):
        self.is_ui = is_ui
        self.tanks = tanks
        self.bonuses = bonuses
        self.projectiles = projectiles
        self.world_bounds = world_bounds
        self.tick = 0

    def update(self, dt):
        for bonus in self.bonuses:
            if bonus.is_expired(self.tick) and bonus in self.bonuses:
                self.bonuses.remove(bonus)

        if random.random() < 0.02:
            is_repair = random.random() > 0.5
            radius = core.config.default_bonus_radius
            while True:
                x = random.uniform(100, self.world_bounds.width)
                y = random.uniform(100, self.world_bounds.height)
                if self.precheck_collision(x, y, radius):
                    self.spawn_bonus(x, y, is_repair)
                    break

        self.tick += dt

    def handle_pickup(self, tank, bonus):
        if isinstance(bonus, BonusBlast):
            tank.has_blast = True
        elif isinstance(bonus, BonusRepair):
            tank.health += bonus.repair_amount

        if bonus in self.bonuses:
            self.bonuses.remove(bonus)

    def spawn_bonus(self, x, y, is_repair):
        bonus = BonusRepair(x, y, self.tick, self.is_ui) if is_repair else BonusBlast(x, y, self.tick, self.is_ui)
        self.bonuses.append(bonus)

    def precheck_collision(self, x, y, radius):
        objs = self.tanks + self.projectiles + self.bonuses
        for o in objs:
            if o.collides_by_params(x, y, radius):
                return False

        return True
