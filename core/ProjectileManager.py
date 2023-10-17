class ProjectileManager:
    def __init__(self, tanks, projectiles, bonuses):
        self.tanks = tanks
        self.projectiles = projectiles
        self.bonuses = bonuses

    def handle_tank_hit(self, tank, projectile):
        damage = projectile.damage_applied(tank)
        if damage > 0:
            tank.health -= damage
            projectile.owner.score += damage
            if projectile in self.projectiles:
                self.projectiles.remove(projectile)

    def handle_bonus_hit(self, bonus, projectile):
        if projectile in self.projectiles:
            self.projectiles.remove(projectile)

        if bonus in self.bonuses:
            self.bonuses.remove(bonus)

    def handle_world_bounds(self, bounds):
        for p in self.projectiles:
            if not bounds.collidepoint(p.center) and p in self.projectiles:
                self.projectiles.remove(p)
