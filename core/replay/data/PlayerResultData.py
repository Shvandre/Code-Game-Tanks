class PlayerResultData:
    def __init__(self, data):
        self.__name = data['name']
        self.__score = data['score']
        self.__hp = data['hp']
        self.__is_winner = data['isWinner']

    @property
    def name(self) -> str:
        return self.__name

    @property
    def score(self) -> int:
        return self.__score

    @property
    def health(self) -> int:
        return self.__hp

    @property
    def is_winner(self) -> bool:
        return self.__is_winner

    @property
    def sort_key(self):
        return self.__score, self.__hp
