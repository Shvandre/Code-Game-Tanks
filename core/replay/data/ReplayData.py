from core.replay.data.FrameData import FrameData
from core.replay.data.MatchData import MatchData
from core.replay.data.PlayerResultData import PlayerResultData
from core.replay.data.WorldData import WorldData


class ReplayData:

    def __init__(self, replay_dict):
        self.__world = WorldData(replay_dict['world'])
        self.__match = MatchData(replay_dict['match'])
        self.__result_score_table = [PlayerResultData(data) for data in replay_dict['resultScoreTable']]
        self.__frames = [FrameData(frame) for frame in replay_dict['frames']]

    @property
    def world(self):
        return self.__world

    @property
    def match(self) -> MatchData:
        return self.__match

    @property
    def winner(self) -> PlayerResultData:
        return [p for p in self.__result_score_table if p.is_winner][0]

    @property
    def result_score_table(self) -> [PlayerResultData]:
        return sorted(self.__result_score_table, key=lambda p: p.sort_key, reverse=True)

    @property
    def frames_count(self) -> int:
        return len(self.__frames)

    def frame(self, index) -> FrameData:
        return self.__frames[index]

