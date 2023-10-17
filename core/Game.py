from typing import List

import pygame
import sys

from pygame.rect import Rect

from core.BonusManager import BonusManager
from core.Physics import Physics
from core.ProjectileManager import ProjectileManager

from collections import defaultdict

from core.ScoreTable import ScoreTable
from core.objects.TextObject import TextObject

from core.config import *
from core.BasePlayer import BasePlayer
from core.replay.EmptyPlayer import EmptyPlayer
from core.replay.ReplayFrameRunner import ReplayFrameRunner
from core.replay.data.ReplayData import ReplayData
from core.replay.ReplayReader import ReplayReader
from core.utils import final_score_sort_key
from screen_resolution import screen_width, screen_height

default_durations = {'intro': 5000, 'match': match_duration, 'outro': 5000}


class Game:
    def __init__(self, caption, width, height, back_image_filename, frame_rate_, handle_continue_button, fullscreen):
        self.reset()

        self.__handle_continue_button = handle_continue_button
        self.__continue_pressed = False

        self.background_image = pygame.image.load(back_image_filename)
        self.blank_background = pygame.Surface((width, height))
        self.blank_background.fill((0, 0, 0))

        self.frame_rate = frame_rate_

        self.blank_duration = 1500

        pygame.init()
        pygame.font.init()

        world_bounds = Rect(0, 0, width, height)
        self.world_bounds = world_bounds

        self.info_title_text = TextObject("",
                                          pygame.font.SysFont("Arial Black", 72),
                                          (255, 255, 255),
                                          center=(width / 2, height / 4))
        self.intro_players_texts = [
            TextObject("",
                       pygame.font.SysFont("Arial Black", 56),
                       (255, 255, 255),
                       center=(width / 2, height / 3 - i * 60)) for i in range(4)]

        self.match_over_text = TextObject("БОЙ ЗАВЕРШЁН",
                                          pygame.font.SysFont("Arial Black", 64),
                                          (255, 255, 255),
                                          center=(width / 2, height / 2))
        self.winner_text = TextObject("winner",
                                      pygame.font.SysFont("Arial Black", 56),
                                      (255, 255, 255),
                                      center=(width / 2, height / 2 + 80))

        self.tick_countdown_text = TextObject("-",
                                              pygame.font.SysFont("Arial Black", 28),
                                              (255, 255, 255),
                                              center=(40, 20))

        mode = pygame.FULLSCREEN if fullscreen else pygame.DOUBLEBUF
        self.surface = pygame.display.set_mode((width, height), mode, 32)
        pygame.display.set_caption(caption)

        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []

    @classmethod
    def create(cls, handle_continue_button=False, fullscreen=False):
        return cls("Tankovod", screen_width, screen_height, background_image, frame_rate, handle_continue_button, fullscreen)

    def reset(self):
        self.ticks = 0
        self.stage_state = 'blank'
        self.running = False
        self.match_over = False
        self.__continue_pressed = False

        self.replay_mode = False
        self.replay_runner = None

        self.battle_name = None
        self.tanks = []
        self.projectiles = []
        self.bonuses = []
        self.players = []
        self.score_table = None
        self.bonus_manager = None
        self.physics = None

    def __reset_continue_button(self):
        if self.__handle_continue_button and self.__continue_pressed:
            self.__continue_pressed = False

    def setup_new_battle(self, battle_name, players, durations=None):
        self.running = True
        self.match_over = False
        self.battle_name = battle_name

        self.__setup_stages(durations)

        projectile_manager = ProjectileManager(self.tanks, self.projectiles, self.bonuses)
        bonus_manager = BonusManager(self.world_bounds, self.tanks, self.projectiles, self.bonuses, is_ui=True)

        self.score_table = ScoreTable(20, screen_width - 120)
        self.bonus_manager = bonus_manager
        self.physics = Physics(self.world_bounds, projectile_manager, bonus_manager)
        self.__setup_players_list(players)

        self.clock = pygame.time.Clock()

    def setup_new_single_replay(self, replay_file, durations=None):
        try:
            replay_data = ReplayReader.read(replay_file)
        except Exception as e:
            print(f'Error during reading replay file {replay_file}: {e}')
            return

        self.running = True
        self.replay_mode = True
        self.match_over = False
        self.battle_name = replay_data.match.name
        self.replay_runner = ReplayFrameRunner(replay_data, self.tanks, self.projectiles, self.bonuses)

        self.__setup_stages(durations)

        self.score_table = ScoreTable(20, screen_width - 120)
        self.__setup_players_for_replay(replay_data)

        self.clock = pygame.time.Clock()

    def __setup_players_for_replay(self, replay_data: ReplayData):
        for i, player_state in enumerate(replay_data.match.players_initial):
            player = EmptyPlayer(player_state.name)
            skin = tank_skins[player_colors[i]]
            player.setup(self, player_state.x, player_state.y, player_state.angle, 0, skin,
                         is_ui=True, tank_id=player_state.id)
            self.players.append(player)

    def __setup_stages(self, durations=None):
        if durations is None:
            durations = default_durations

        self.intro_duration = durations['intro']
        self.match_duration = durations['match']
        self.outro_duration = durations['outro']
        self.stage_state = 'blank'

    def __setup_players_list(self, players: List[BasePlayer]):
        for i, player in enumerate(players):
            (x_mult, y_mult) = player_init_locations_multipliers[i]
            skin = tank_skins[player_colors[i]]
            angle = player_init_angles[i]
            x = x_mult * self.world_bounds.width / 4
            y = y_mult * self.world_bounds.height / 4
            player.setup(self, x, y, angle, 0, skin, is_ui=True)

        self.set_players(players)

    def set_players(self, players):
        self.players = players

    def get_objects(self, sort_for_drawing=False):
        tanks = self.tanks if not sort_for_drawing else sorted(self.tanks, key=lambda t: not t.is_dead)
        return tanks + self.projectiles + self.bonuses

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif self.__handle_continue_button and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__continue_pressed = True

    def update_game(self, dt):
        for p in self.players:
            p.update_internal(dt)

        for o in self.get_objects():
            o.update(dt)

        self.bonus_manager.update(dt)
        self.physics.update(self.get_objects())
        self.update_ui()

    def update_replay(self):
        self.replay_runner.update()
        self.update_ui()

    def update_ui(self):
        self.score_table.update(self.tanks)

        ticks_left = int(
            (self.match_duration - (self.ticks - self.blank_duration - self.intro_duration)) / 10)
        self.tick_countdown_text.text = str(ticks_left)
        if ticks_left < 500:
            rem_of_20 = ticks_left % 50
            if rem_of_20 >= 25:
                self.tick_countdown_text.color = (255, 50, 50)
            else:
                self.tick_countdown_text.color = (255, 255, 200)

    def draw(self):
        width = self.world_bounds.width
        height = self.world_bounds.height

        if self.stage_state == 'blank':
            pass
        elif self.stage_state == 'intro':
            self.info_title_text.update(self.battle_name, center=(width / 2, height / 4))
            self.info_title_text.draw(self.surface)
            for i, player in enumerate(self.players):
                self.intro_players_texts[i].update(player.name, center=(width / 2, height / 3 + (i + 1) * 60))
                self.intro_players_texts[i].draw(self.surface)
            pass
        else:
            for o in self.get_objects(sort_for_drawing=True):
                o.draw(self.surface)

            self.score_table.draw(self.surface)

            if self.stage_state == 'outro':
                self.match_over_text.draw(self.surface)
                alive_players = filter(lambda p: not p.is_dead, self.players)
                winner = sorted(alive_players, key=lambda p: final_score_sort_key(p), reverse=True)[0]
                self.winner_text.update("Победитель: %s" % winner.name,
                                        center=(self.world_bounds.width / 2, self.world_bounds.height / 2 + 80))
                self.winner_text.draw(self.surface)
            elif self.stage_state == 'match':
                self.tick_countdown_text.draw(self.surface)

    def run(self):
        while self.running:

            self.handle_events()

            if self.stage_state == 'blank':
                self.surface.blit(self.blank_background, (0, 0))
                pass
            elif self.stage_state == 'intro':
                self.surface.blit(self.blank_background, (0, 0))
                pass
            elif self.stage_state == 'match':
                if self.__handle_continue_button and not self.__continue_pressed:
                    self.clock.tick(self.frame_rate)
                    continue

                self.surface.blit(self.background_image, (0, 0))
                if self.replay_mode:
                    self.update_replay()
                else:
                    self.update_game(self.clock.get_time())

            elif self.stage_state == 'outro':
                self.surface.blit(self.background_image, (0, 0))

            self.draw()
            pygame.display.update()

            self.ticks += self.clock.tick(self.frame_rate)
            state = self.stage_state

            if state == 'outro' and self.ticks > self.blank_duration + self.intro_duration + self.match_duration + self.outro_duration:
                ## КОСТЫЛЬ
                while self.__handle_continue_button and not self.__continue_pressed:
                    self.clock.tick(self.frame_rate)
                    self.handle_events()

                self.running = False
            elif state == 'match' and ((self.replay_mode and not self.replay_runner.has_next_frame()) or
                                       self.ticks > self.blank_duration + self.intro_duration + self.match_duration):
                print('-> outro')
                self.stage_state = 'outro'
                self.__reset_continue_button()
            elif state == 'intro' and self.ticks > self.blank_duration + self.intro_duration:
                print('-> match')
                self.stage_state = 'match'
                self.__reset_continue_button()
            elif state == 'blank' and self.ticks > self.blank_duration:
                print('-> intro')
                self.stage_state = 'intro'
