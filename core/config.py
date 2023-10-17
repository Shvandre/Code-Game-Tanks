background_image = 'images/background-large.jpg'
frame_rate = 60
match_duration = 60000

tank_skins = dict(
    green='images/ship_green.png',
    yellow='images/ship_yellow.png',
    blue='images/ship_blue.png',
    red='images/ship_red.png'
)

player_init_locations_multipliers = [
    (1, 1),
    (3, 1),
    (1, 3),
    (3, 3)
]

player_colors = ['red', 'green', 'yellow', 'blue']
player_init_angles = [30, 150, 330, 210]

blast_skin = 'images/blast.png'
blast_radius = 100
blast_speed = 0.25
blast_damage = 25

bullet_skin = 'images/bullet_new.png'
bullet_radius = 30
bullet_speed = 0.5
bullet_damage = 5

tank_radius = 60
tank_speed = 0.08
max_tank_speed = 0.3

default_bonus_radius = 24

bonus_blast_skin = 'images/bonus_blast.png'
bonus_blast_lifetime = 8000

bonus_repair_skin = 'images/bonus_repair.png'
bonus_repair_lifetime = 8000
bonus_repair_amount = 10

ground_friction_ratio = 0.02

debug_mode = False
