from core.replay.data.GameObjectState import GameObjectState
from core.replay.data.PlayerState import PlayerState


class FrameData:
    def __init__(self, frame_dict):
        self.__id = frame_dict['frameId']

        self.__players = self.__associate_by_id(
            [PlayerState(player_dict) for player_dict in frame_dict['players']]
        )
        self.__projectiles = self.__associate_by_id(
            [GameObjectState(projectile_dict) for projectile_dict in frame_dict['projectiles']]
        )
        self.__bonuses = self.__associate_by_id(
            [GameObjectState(bonuses_dict) for bonuses_dict in frame_dict['bonuses']]
        )

        all_objects = dict(self.__projectiles)
        all_objects.update(self.__bonuses)
        self.__all_objects = all_objects

    @staticmethod
    def __associate_by_id(objects):
        return {obj.id: obj for obj in objects}

    @property
    def id(self):
        return self.__id

    @property
    def players(self) -> dict[str, PlayerState]:
        return self.__players

    @property
    def projectiles(self) -> dict[str, GameObjectState]:
        return self.__projectiles

    @property
    def bonuses(self) -> dict[str, GameObjectState]:
        return self.__bonuses

    @property
    def all_objects(self) -> dict[str, GameObjectState]:
        return self.__all_objects
