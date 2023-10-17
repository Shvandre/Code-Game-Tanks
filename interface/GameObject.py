class GameObject:

    # Игровой объект и его свойства

    def __init__(self, x, y, angle, speed):
        self._x = x
        self._y = y
        self._angle = angle
        self._speed = speed

    # Координата Х
    @property
    def x(self) -> float:
        return self._x

    # Координата Y
    @property
    def y(self) -> float:
        return self._y

    # Угол относительно вектора (1, 0) - в градусах, против часовой стрелки
    @property
    def angle(self) -> float:
        return self._angle

    # Скорость
    @property
    def speed(self) -> float:
        return self._speed
