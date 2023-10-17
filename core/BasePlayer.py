from pygame import Vector2

from core.objects.Blast import Blast
from core.objects.BonusRepair import BonusRepair
from core.objects.Bullet import Bullet
from core.objects.Tank import Tank
from core.utils import cleanup_angle
from interface.Bonus import Bonus
from interface.IPlayer import IPlayer
from interface.NPC import NPC
from interface.Projectile import Projectile
import core.config


class BasePlayer(IPlayer):
    __angle_delta_by_tick = 2

    def __init__(self, name):
        self.__name = name

        self.__last_bullet_shot = 0
        self.__last_blast_shot = 0
        self.__tick = 0
        self.__last_speed_up_time = None
        self.__current_requested_angle_delta = None

        self.__is_ui = False
        self.__game = None
        self.__world_size = None
        self.__tank = None

    def setup(self, game, x, y, angle, speed, skin, is_ui, tank_id=None):
        self.__is_ui = is_ui
        self.__game = game
        self.__world_size = (game.world_bounds.width, game.world_bounds.height)
        self.__tank = Tank(self.__name,
                           x,
                           self.flip_y(y),
                           angle,
                           speed,
                           skin,
                           is_ui,
                           oid=tank_id)
        self.__game.tanks.append(self.__tank)

    @property
    def id(self):
        return self.__tank.id

    @property
    def name(self):
        return self.__tank.name

    @property
    def x(self):
        return self.__tank.x

    @property
    def y(self):
        return self.__tank.y

    @property
    def angle(self):
        return self.__tank.angle

    @property
    def speed(self):
        return self.__tank.speed

    @property
    def enemies(self):
        return list(map(lambda tank: NPC(tank.x, self.flip_y(tank.y), tank.angle, tank.speed, tank.health),
                        [t for t in self.__game.tanks if t != self.__tank]))

    @property
    def projectiles(self):
        return list(map(lambda projectile: Projectile(projectile.x,
                                                      self.flip_y(projectile.y),
                                                      projectile.angle,
                                                      projectile.speed,
                                                      Projectile.type_bullet if isinstance(projectile, Bullet)
                                                      else Projectile.type_blast,
                                                      projectile.damage),
                        [p for p in self.__game.projectiles]))

    @property
    def bonuses(self):
        return list(map(lambda bonus: Bonus(bonus.x,
                                            self.flip_y(bonus.y),
                                            bonus.angle,
                                            bonus.speed,
                                            Bonus.type_repair if isinstance(bonus, BonusRepair)
                                            else Bonus.type_blast
                                            ),
                        [b for b in self.__game.bonuses]))

    def shoot_bullet(self):
        if self.is_dead:
            return

        if self.__tick - self.__last_bullet_shot >= 500:
            projectile_position = self.__tank.position + (self.__tank.direction * self.__tank.radius)
            new_projectile = Bullet(projectile_position.x,
                                    projectile_position.y,
                                    self.__tank.angle,
                                    self.__tank,
                                    self.__is_ui)
            self.__game.projectiles.append(new_projectile)
            self.__last_bullet_shot = self.__tick

    def shoot_blast(self):
        if self.is_dead:
            return

        if self.__tick - self.__last_blast_shot >= 2000:
            projectile_position = self.__tank.position + (self.__tank.direction * self.__tank.radius)
            new_projectile = Blast(projectile_position.x,
                                   projectile_position.y,
                                   self.__tank.angle,
                                   self.__tank,
                                   self.__is_ui)
            self.__game.projectiles.append(new_projectile)
            self.__last_blast_shot = self.__tick
            self.__tank.has_blast = False

    @property
    def health(self):
        return self.__tank.health

    @property
    def score(self):
        return self.__tank.score

    @property
    def is_dead(self):
        return self.__tank.is_dead

    @property
    def has_blast(self):
        return self.__tank.has_blast

    @property
    def world_size(self):
        return self.__world_size

    def kill(self):
        self.__tank.destroy()

    def distance_to_object(self, obj):
        obj_x = obj.x
        obj_y = self.flip_y(obj.y)
        return self.__tank.distance_to_point_xy(obj_x, obj_y)

    def angle_to_object(self, obj):
        obj_x = obj.x
        obj_y = self.flip_y(obj.y)
        obj_position = Vector2(obj_x, obj_y)
        if self.__tank.position == obj_position:
            return 0

        vector_between_objs = obj_position - self.__tank.position
        return cleanup_angle(vector_between_objs.angle_to(self.__tank.direction))

    def speed_up(self):
        if self.__tank.is_dead:
            return

        if self.__last_speed_up_time is None or self.__tick - self.__last_speed_up_time >= 800:
            self.__tank.speed = core.config.max_tank_speed
            self.__last_speed_up_time = self.__tick

    def rotate_left(self):
        if self.is_dead:
            return

        self.__tank.angle += BasePlayer.__angle_delta_by_tick

    def rotate_right(self):
        if self.is_dead:
            return

        self.__tank.angle -= BasePlayer.__angle_delta_by_tick

    def rotate_by_angle(self, angle_delta):
        if self.is_dead:
            return

        self.__current_requested_angle_delta = cleanup_angle(angle_delta)

    def update_internal(self, dt):
        if not self.__tank.is_dead:
            if not (self.__current_requested_angle_delta is None):
                angle_delta = self.__current_requested_angle_delta
                if abs(angle_delta) < 0.0001:
                    self.__current_requested_angle_delta = None
                else:
                    angle_change = BasePlayer.__angle_delta_by_tick * (angle_delta / abs(angle_delta))
                    self.__tank.angle += angle_change
                    self.__current_requested_angle_delta -= angle_change
            try:
                self.update(self.__tick)
            except:
                print('player %s crashed internally' % self.name)
                self.kill()

        self.__tick += dt

    def update(self, tick):
        pass

    def flip_y(self, y):
        return (self.world_size[1] - 1) - y
