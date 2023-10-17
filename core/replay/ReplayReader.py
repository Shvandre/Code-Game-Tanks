import json

from core.replay.data.ReplayData import ReplayData


class ReplayReader:

    @staticmethod
    def read(replay_file) -> ReplayData:
        with open(replay_file) as file:
            replay_data = ReplayData(json.load(file))
            return replay_data
