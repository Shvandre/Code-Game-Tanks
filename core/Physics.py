from core import physics_math

from core.objects.Bonus import Bonus
from core.objects.Tank import Tank
from core.objects.Projectile import Projectile
from core.config import *
from pygame.math import Vector2


class Physics:
    normals = dict(
        left=Vector2(1, 0),
        top=Vector2(0, 1),
        right=Vector2(-1, 0),
        bottom=Vector2(0, -1)
    )

    def __init__(self, world_bounds, projectile_manager, bonus_manager):
        self.world_bounds = world_bounds
        self.projectile_manager = projectile_manager
        self.bonus_manager = bonus_manager

    def update(self, game_objects):
        tanks = [t for t in game_objects if isinstance(t, Tank)]
        projectiles = [p for p in game_objects if isinstance(p, Projectile)]
        bonuses = [b for b in game_objects if isinstance(b, Bonus)]

        collided_pairs = dict()

        for tank in tanks:
            if tank.is_dead:
                continue

            '''collisions with other tanks'''

            for other_tank in tanks:
                if not (other_tank is tank or
                        (tank, other_tank) in collided_pairs or
                        (other_tank, tank) in collided_pairs or
                        other_tank.is_dead):
                    if tank.collides(other_tank):
                        physics_math.manage_obj_collision(tank, other_tank)
                        collided_pairs[(tank, other_tank)] = 1

            '''collision with projectiles'''

            for projectile in projectiles:
                if projectile.collides(tank):
                    self.projectile_manager.handle_tank_hit(tank, projectile)

            '''collision with bonuses'''
            for bonus in bonuses:
                if bonus.collides(tank):
                    self.bonus_manager.handle_pickup(tank, bonus)

            '''ground friction'''
            if tank.velocity.length() > 0.00001:
                tank.velocity = tank.velocity * (1 - ground_friction_ratio)
            else:
                tank.velocity = Vector2(0, 0)

            ''' collisions with world bounds '''

            # координата (0, 0) отсчитывается от left-top

            cross_left = tank.left < 0
            cross_top = tank.top < 0
            cross_right = tank.right > self.world_bounds.width
            cross_bottom = tank.bottom > self.world_bounds.height

            print(tank.velocity)
            print(tank.velocity.length())

            if cross_left:
                tank.velocity = tank.velocity.reflect(Physics.normals['left'])
                tank.x = tank.radius + 1

            if cross_top:
                tank.velocity = tank.velocity.reflect(Physics.normals['top'])
                tank.y = tank.radius + 1

            if cross_right:
                tank.velocity = tank.velocity.reflect(Physics.normals['right'])
                tank.x = self.world_bounds.width - tank.radius - 1

            if cross_bottom:
                tank.velocity = tank.velocity.reflect(Physics.normals['bottom'])
                tank.y = self.world_bounds.height - tank.radius - 1

        self.projectile_manager.handle_world_bounds(self.world_bounds)
