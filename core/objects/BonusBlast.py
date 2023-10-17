import pygame
from core.objects.Bonus import Bonus
import core.config


class BonusBlast(Bonus):
    def __init__(self, x, y, spawned_at, is_ui, oid=None):
        skin = None
        if is_ui:
            skin = pygame.image.load(core.config.bonus_blast_skin)
        Bonus.__init__(self, x, y, core.config.bonus_blast_lifetime, spawned_at, skin, is_ui, oid)
