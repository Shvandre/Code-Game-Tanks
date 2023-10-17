import secrets

from pygame.math import Vector2
from core.utils import *
from core.config import *


class GameObject:

    unity_vector = Vector2(1, 0)

    def __init__(self, x, y, radius, angle, speed, skin, is_ui, oid=None):

        if oid is None:
            self._id = secrets.token_hex(nbytes=24)
        else:
            self._id = oid

        self._position = Vector2(x, y)

        self._direction = Vector2(1, 0)
        self._direction.rotate_ip(-angle)
        self._speed = speed

        self._radius = radius
        self.skin = skin
        self.is_ui = is_ui

    @property
    def id(self):
        return self._id

    @property
    def center(self):
        return self.x, self.y

    @property
    def x(self):
        return self._position.x

    @x.setter
    def x(self, x):
        self._position = Vector2(x, self._position.y)

    @property
    def y(self):
        return self._position.y

    @y.setter
    def y(self, y):
        self._position = Vector2(self._position.x, y)

    @property
    def left(self):
        return self.x - self.radius

    @property
    def top(self):
        return self.y - self.radius

    @property
    def right(self):
        return self.x + self.radius

    @property
    def bottom(self):
        return self.y + self.radius

    @property
    def top_point(self):
        return self.x, self.y - self.radius
    
    @property
    def bottom_point(self):
        return self.x, self.y + self.radius
    
    @property
    def left_point(self):
        return self.x - self.radius, self.y
    
    @property
    def right_point(self):
        return self.x + self.radius, self.y

    @property
    def radius(self):
        return self._radius
    
    @property
    def angle(self):
        return cleanup_angle(self._direction.angle_to(GameObject.unity_vector))
    
    @property
    def speed(self):
        return self._speed

    @property
    def velocity(self):
        velocity_vector = Vector2(self._direction)
        velocity_vector.scale_to_length(self._speed)
        return velocity_vector

    @angle.setter
    def angle(self, new_angle):
        self._direction = Vector2(1, 0)
        self._direction.rotate_ip(-new_angle)

    @speed.setter
    def speed(self, new_speed):
        self._speed = new_speed

    @velocity.setter
    def velocity(self, new_velocity):
        self._speed = new_velocity.length()
        if new_velocity.length() > 0:
            self._direction = new_velocity.normalize()

    @property
    def position(self):
        return self._position

    @property
    def direction(self):
        return self._direction

    def distance_to_point(self, position):
        return self.position.distance_to(position)

    def distance_to_point_xy(self, x, y):
        return self.distance_to_point(Vector2(x, y))

    def distance_to_obj(self, other_obj):
        return self.distance_to_point(other_obj.position)

    def collides(self, other):
        return self.distance_to_obj(other) <= self.radius + other.radius

    def collides_by_params(self, x, y, radius):
        return self.distance_to_point_xy(x, y) < self.radius + radius

    def drawing_start_point(self):
        return self.x - self.radius, self.y - self.radius

    def draw(self, surface):
        if not self.is_ui:
            return
        rotated_skin = rotate_center(self.skin, 90 + self.angle)
        surface.blit(rotated_skin, (self.x - rotated_skin.get_width() / 2, self.y - rotated_skin.get_height() / 2))
        if debug_mode:
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y)), int(self.radius), 1)
            pygame.draw.circle(surface, (255, 255, 0), (int(self.top_point[0]), int(self.top_point[1])), 3, 0)
            pygame.draw.circle(surface, (255, 255, 0), (int(self.left_point[0]), int(self.left_point[1])), 3, 0)
            pygame.draw.circle(surface, (255, 255, 0), (int(self.right_point[0]), int(self.right_point[1])), 3, 0)
            pygame.draw.circle(surface, (255, 255, 0), (int(self.bottom_point[0]), int(self.bottom_point[1])), 3, 0)

    def update(self, dt):
        if self.speed == 0:
            return

        self._position += self.velocity * dt

    def update_object_from_replay_frame(self, x: float, y: float, angle: float):
        self._position = Vector2(x, y)
        self._direction = Vector2(1, 0)
        self._direction.rotate_ip(-angle)
        self._speed = 0

