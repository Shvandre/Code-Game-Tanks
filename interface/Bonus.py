from interface.GameObject import GameObject


class Bonus(GameObject):

    type_repair = "repair"
    type_blast = "blast"

    # Свойства бонуса

    def __init__(self, x, y, angle, speed, bonus_type):
        GameObject.__init__(self, x, y, angle, speed)
        self._bonus_type = bonus_type

    # Это бонус ремонта?
    @property
    def is_repair(self) -> bool:
        return self._bonus_type == Bonus.type_repair

    # Это бонус заряд луча?
    @property
    def is_blast(self) -> bool:
        return self._bonus_type == Bonus.type_blast
