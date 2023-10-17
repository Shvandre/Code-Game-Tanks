from interface.GameObject import GameObject


class Projectile(GameObject):

    type_bullet = "bullet"
    type_blast = "blast"

    # Свойства летящего снаряда

    def __init__(self, x, y, angle, speed, projectile_type, damage):
        GameObject.__init__(self, x, y, angle, speed)
        self._projectile_type = projectile_type
        self._damage = damage

    # Является ли снаряд пулей
    @property
    def is_bullet(self) -> bool:
        return self._projectile_type == Projectile.type_bullet

    # Является ли снаряд лучом
    @property
    def is_blast(self) -> bool:
        return self._projectile_type == Projectile.type_blast

    # Урон снаряда в HP
    @property
    def damage(self) -> int:
        return self._damage
