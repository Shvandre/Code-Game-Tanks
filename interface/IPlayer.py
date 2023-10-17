from abc import ABC, abstractmethod
from typing import List

from interface.Bonus import Bonus
from interface.GameObject import GameObject
from interface.NPC import NPC
from interface.Projectile import Projectile


class IPlayer(ABC):

    # Физические свойства игрового бота

    # Координата X
    @property
    @abstractmethod
    def x(self) -> float:
        pass

    # Координата Y
    @property
    @abstractmethod
    def y(self) -> float:
        pass

    # Угол относительно вектора (1, 0) - в градусах, против часовой стрелки
    @property
    @abstractmethod
    def angle(self) -> float:
        pass

    # Скорость, пикс/кадр
    @property
    @abstractmethod
    def speed(self) -> float:
        pass

    # Свойства игровой арены
    # Размер игровой арены (ширина, высота, в писк.)
    @property
    @abstractmethod
    def world_size(self) -> (int, int):
        pass

    # Массив других игроков на арене
    @property
    @abstractmethod
    def enemies(self) -> List[NPC]:
        pass

    # Массив всех выпущенных снарядов
    @property
    @abstractmethod
    def projectiles(self) -> List[Projectile]:
        pass

    # Массив всех бонусов
    @property
    @abstractmethod
    def bonuses(self) -> List[Bonus]:
        pass

    # Действия
    # Выстрелить пулей
    def shoot_bullet(self):
        pass

    # Выстрелить лучом (если имеется такой заряд)
    def shoot_blast(self):
        pass

    # Нажать на газ
    def speed_up(self):
        pass

    # Повернуть влево (против часовой)
    def rotate_left(self):
        pass

    # Повернуть вправо (по часовой)
    def rotate_right(self):
        pass

    # Запросить поворот на угол относительно текущего направвления (будет исполняться несколько кадров)
    def rotate_by_angle(self, angle_delta: float):
        pass

    # Дополнительные методы игрового бота
    # Имеется ли луч
    @property
    @abstractmethod
    def has_blast(self) -> bool:
        pass

    # Расстояние до объекта в пикс.
    def distance_to_object(self, obj: GameObject):
        pass

    # Угол до объекта (минимальный, в градусах)
    def angle_to_object(self, obj: GameObject):
        pass

    # Метод расчёта логики, выполняемый каждый кадр для игрока
    def update(self, tick):
        pass
