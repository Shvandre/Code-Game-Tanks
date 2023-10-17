class PlayerState:
    def __init__(self, player_dict):
        self.__id = player_dict['id']
        self.__x = float(player_dict['x'])
        self.__y = float(player_dict['y'])
        self.__name = player_dict['name']
        self.__angle = float(player_dict['angle'])
        self.__score = player_dict['score']
        self.__hp = player_dict['hp']
        self.__has_blast = player_dict['hasBlast']
        self.__is_dead = player_dict['isDead']

    @property
    def id(self):
        return self.__id

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def name(self) -> str:
        return self.__name

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def score(self) -> int:
        return self.__score

    @property
    def health(self) -> int:
        return self.__hp

    @property
    def has_blast(self) -> bool:
        return self.__has_blast

    @property
    def is_dead(self) -> bool:
        return self.__is_dead
