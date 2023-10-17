from core.BasePlayer import BasePlayer
import random

class MyBot(BasePlayer):
    def __init__(self, name):
        super(MyBot, self).__init__(name)
        seed = random.randint(1, 999999) % random.randint(1, 999999)
        self.__random = random.Random(seed)
    def update(self, tick):
        try:
            cnt = 0
            sdist = 300000
            mode = "Passive"
            for el in self.enemies:
                if not el.is_dead:
                    cnt += 1
            for e in self.enemies:
                if e.is_dead:
                    continue
                distance = self.distance_to_object(e)
                if distance < sdist:
                    sdist = distance
            if sdist <= 200:
                mode = "Aggressive"
            if cnt == 1 or mode == "Aggressive":
                enemy = None
                min_distance = 300000
                for e in self.enemies:
                    if e.is_dead:
                        continue
                    distance = self.distance_to_object(e)
                    if distance < min_distance:
                        min_distance = distance
                        enemy = e

                if enemy is not None:
                    enemy_angle = self.angle_to_object(enemy)
                    my_angle = self.angle
                    side = "Null"
                    if 0 <= my_angle <= 180 and 0 <= enemy_angle <= 180:
                        side = "right" if enemy_angle > my_angle else "left"
                    elif 90 <= my_angle <= 270 and 90 <= enemy_angle <= 270:
                        side = "right" if enemy_angle > my_angle else "left"
                    elif 180 <= my_angle <= 359 and 180 <= enemy_angle <= 359:
                        side = "right" if enemy_angle > my_angle else "left"
                    elif 0 <= min(my_angle, enemy_angle) <= 90 and 270 <= max(my_angle, enemy_angle) <= 359:
                        side = "left" if enemy_angle > my_angle else "right"
                    else:
                        side = "Null"
                    if side == "Null":
                        self.rotate_by_angle(self.angle_to_object(enemy))
                    elif side == "left":
                        self.rotate_by_angle((self.angle_to_object(enemy) + 350) % 360)
                    else:
                        self.rotate_by_angle((self.angle_to_object(enemy) + 370) % 360)
                    if self.has_blast and abs(self.angle_to_object(enemy)) <= 15:
                        self.shoot_blast()
                    else:
                        self.shoot_bullet()
                self.speed_up()
            else:
                # Second strategy
                # Уверачиваемся от пуль
                bullets = self.projectiles
                min_dist_to_blast = 30000000
                bullet = None
                for b in bullets:
                    if b.is_blast:
                        min_dist_to_blast = self.distance_to_object(b)
                        bullet = b
                if bullet is not None and min_dist_to_blast <= 400:
                    self.rotate_by_angle((bullet.angle + 90) % 360)
                    self.speed_up()
                else:
                    cur_choice = random.random()
                    if self.has_blast or cur_choice <= 0.50:
                        # Стреляем по ближайшему
                        min_dist_to_enemy = 30000000
                        enemy = None
                        for e in self.enemies:
                            if e.is_dead:
                                continue
                            distance = self.distance_to_object(e)
                            if distance < min_dist_to_enemy:
                                min_dist_to_enemy = distance
                                enemy = e
                        if (self.has_blast and min_dist_to_enemy < 500) or random.random() < 0.5:
                            if enemy is not None:
                                enemy_angle = self.angle_to_object(enemy)
                                my_angle = self.angle
                                side = "Null"
                                if 0 <= my_angle <= 180 and 0 <= enemy_angle <= 180:
                                    side = "right" if enemy_angle > my_angle else "left"
                                elif 90 <= my_angle <= 270 and 90 <= enemy_angle <= 270:
                                    side = "right" if enemy_angle > my_angle else "left"
                                elif 180 <= my_angle <= 359 and 180 <= enemy_angle <= 359:
                                    side = "right" if enemy_angle > my_angle else "left"
                                elif 0 <= min(my_angle, enemy_angle) <= 90 and 270 <= max(my_angle, enemy_angle) <= 359:
                                    side = "left" if enemy_angle > my_angle else "right"
                                else:
                                    side = "Null"
                                if side == "Null":
                                    self.rotate_by_angle(self.angle_to_object(enemy))
                                elif side == "left":
                                    self.rotate_by_angle((self.angle_to_object(enemy) + 350) % 360)
                                else:
                                    self.rotate_by_angle((self.angle_to_object(enemy) + 370) % 360)
                                if self.has_blast and min_dist_to_enemy < 400 and abs(self.angle_to_object(enemy)) <= 15:
                                    self.shoot_blast()
                                else:
                                    self.shoot_bullet()
                                self.speed_up()
                    else:
                        if self.health <= 70:
                            priority = "Health"
                        else:
                            priority = "Blast"
                        bonus_lst = self.bonuses
                        min_dist_to_bonus = 3000000
                        cur_bonus = None
                        for bon in bonus_lst:
                            if bon.is_repair and priority == "Health" and self.distance_to_object(bon) < min_dist_to_bonus:
                                min_dist_to_bonus = self.distance_to_object(bon)
                                cur_bonus = bon
                            elif bon.is_blast and priority == "Blast" and self.distance_to_object(bon) < min_dist_to_bonus:
                                min_dist_to_bonus = self.distance_to_object(bon)
                                cur_bonus = bon
                        if cur_bonus is not None:
                            self.rotate_by_angle(self.angle_to_object(cur_bonus))
                            self.speed_up()
        except Exception as error:
            print(error)


