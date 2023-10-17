from interface.GameObject import GameObject


class NPC(GameObject):

    # Соперник, его свойства

    def __init__(self, x, y, angle, speed, health):
        GameObject.__init__(self, x, y, angle, speed)
        self._health = health

    # Текущее здоровье в HP
    @property
    def health(self) -> int:
        return self._health

    # Является ли данный соперник уже подбитым
    @property
    def is_dead(self) -> bool:
        return self._health == 0
