import json

from pygame import Rect

from core.BonusManager import BonusManager
from core.Physics import Physics
from core.ProjectileManager import ProjectileManager
from core.utils import final_score_sort_key


def pf(number):
    return "%.2f" % number


class GamePrinter:

    def __init__(self, width, height, match_name, match_duration, out_file):
        self.match_duration = match_duration
        self.match_name = match_name
        self.out_file = out_file

        self.tanks = []
        self.projectiles = []
        self.bonuses = []
        self.players = []

        self.initial_player_states = []
        self.frame_states = []
        self.frame_time_ms = 17

        self.world_bounds = Rect(0, 0, width, height)
        self.projectile_manager = ProjectileManager(self.tanks, self.projectiles, self.bonuses)
        self.bonus_manager = BonusManager(self.world_bounds, self.tanks, self.projectiles, self.bonuses, is_ui=False)
        self.physics = Physics(self.world_bounds, self.projectile_manager, self.bonus_manager)

        self.match_over = False

    def set_players(self, players):
        self.players = players

    def get_objects(self):
        return self.tanks + self.projectiles + self.bonuses

    def update(self, dt, tick):
        for p in self.players:
            p.update_internal(dt)

        for o in self.get_objects():
            o.update(dt)

        self.physics.update(self.get_objects())
        self.bonus_manager.update(dt)

    def get_frame_state(self, tick):
        return {
            'frameId': tick,
            'players': self.__get_players_state(),
            'projectiles': [{
                'id': projectile.id,
                'type': projectile.__class__.__name__,
                'x': pf(projectile.x),
                'y': pf(projectile.y),
                'angle': pf(projectile.angle)
            } for projectile in self.projectiles],
            'bonuses': [{
                'id': bonus.id,
                'type': bonus.__class__.__name__,
                'x': pf(bonus.x),
                'y': pf(bonus.y)
            } for bonus in self.bonuses]
        }

    def __get_players_state(self):
        return [{
            'id': player.id,
            'name': player.name,
            'x': pf(player.x),
            'y': pf(player.y),
            'angle': pf(player.angle),
            'hp': player.health,
            'hasBlast': player.has_blast,
            'score': player.score,
            'isDead': player.is_dead
        } for player in self.players]

    def print_state_to_file(self):
        alive_players = list(filter(lambda p: not p.is_dead, self.players))

        if len(alive_players) == 0:
            scored_players = self.players
        else:
            scored_players = alive_players

        winner = sorted(scored_players, key=lambda p: final_score_sort_key(p), reverse=True)[0]
        with open(self.out_file, 'w') as file:
            json.dump({
                'world': {
                    'width': self.world_bounds.width,
                    'height': self.world_bounds.height
                },
                'match': {
                    'name': self.match_name,
                    'duration': self.match_duration,
                    'playersInitial': self.initial_player_states,
                },
                'resultScoreTable': [{
                    'name': player.name,
                    'score': player.score,
                    'hp': player.health,
                    'isWinner': player.id is winner.id
                } for player in sorted(self.players, key=lambda p: final_score_sort_key(p), reverse=True)],
                'frames': self.frame_states
            }, file, ensure_ascii=False, indent=2)

    def run(self):
        self.initial_player_states = self.__get_players_state()

        tick = 0
        while not self.match_over:
            self.update(self.frame_time_ms, tick)
            self.frame_states.append(self.get_frame_state(tick))
            tick = tick + 1
            if tick >= self.match_duration:
                self.match_over = True

        self.print_state_to_file()



