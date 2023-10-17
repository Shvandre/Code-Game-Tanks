from core.replay.data.PlayerState import PlayerState


class MatchData:
    def __init__(self, match_dict):
        self.__name = match_dict['name']
        self.__duration = match_dict['duration']
        self.__players_initial = [PlayerState(player) for player in match_dict['playersInitial']]

    @property
    def name(self) -> str:
        return self.__name

    @property
    def duration(self) -> int:
        return self.__duration

    @property
    def players_initial(self) -> [PlayerState]:
        return self.__players_initial
