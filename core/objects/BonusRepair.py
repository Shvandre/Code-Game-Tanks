import pygame
from core.objects.Bonus import Bonus
import core.config


class BonusRepair(Bonus):
    def __init__(self, x, y, spawned_at, is_ui, oid=None):
        skin = None
        if is_ui:
            skin = pygame.image.load(core.config.bonus_repair_skin)
        Bonus.__init__(self, x, y, core.config.bonus_repair_lifetime, spawned_at, skin, is_ui, oid)

    @property
    def repair_amount(self):
        return core.config.bonus_repair_amount
