import pygame
from core.objects.TextObject import TextObject
from core.utils import final_score_sort_key


class ScoreTable:

    text_color_normal = (255, 255, 255)
    text_color_dead = (255, 0, 0)
    row_margin = 40

    def __init__(self, top, right):
        self.top = top
        self.right = right

        self.font = pygame.font.SysFont("Arial", 24)
        self.tanks_lines = []

    def update(self, tanks):
        cur_top = 0
        if len(self.tanks_lines) == 0:
            for i, tank in enumerate(tanks):
                line = TextObject(self.tank_str(tank), self.font, ScoreTable.text_color_normal, topright=(self.right, self.top + cur_top))
                self.tanks_lines.append(line)
                cur_top += ScoreTable.row_margin
        else:
            for i, tank in enumerate(sorted(tanks, key=lambda p: final_score_sort_key(p), reverse=True)):
                if tank.is_dead:
                    color = ScoreTable.text_color_dead
                else:
                    color = ScoreTable.text_color_normal
                self.tanks_lines[i].color = color
                self.tanks_lines[i].update(self.tank_str(tank), topright=(self.right, self.top + cur_top))
                cur_top += ScoreTable.row_margin

    def draw(self, surface):
        for line in self.tanks_lines:
            line.draw(surface)

    def tank_str(self, tank):
        return tank.name + ", " + str(tank.health) + " HP, " + "счёт - " + str(tank.score)
