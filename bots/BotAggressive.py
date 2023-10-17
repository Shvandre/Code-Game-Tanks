import random

from core.BasePlayer import BasePlayer


class BotAggressive(BasePlayer):

    def __init__(self, name):
        super(BotAggressive, self).__init__(name)
        seed = random.randint(1, 999999) % random.randint(1, 999999)
        self.__random = random.Random(seed)

    def update(self, tick):

        enemy = None
        min_distance = 9000

        if self.__random.random() < 0.2:
            enemy = self.__random.choice(self.enemies)
        else:
            for e in self.enemies:
                if e.is_dead:
                    continue
                distance = self.distance_to_object(e)
                if distance < min_distance:
                    min_distance = distance
                    enemy = e

        if enemy is not None:
            self.rotate_by_angle(self.angle_to_object(enemy))
            if abs(self.angle_to_object(enemy)) < 15:
                if self.has_blast:
                    self.shoot_blast()
                else:
                    self.shoot_bullet()
        else:
            if self.__random.random() < 0.001:
                self.rotate_by_angle(self.__random.randint(-40, 45))

        if self.__random.random() < 0.8:
            self.speed_up()

