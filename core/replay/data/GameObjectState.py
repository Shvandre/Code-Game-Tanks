class GameObjectState:
    def __init__(self, object_dict):
        self.__id = object_dict['id']
        self.__x = float(object_dict['x'])
        self.__y = float(object_dict['y'])
        self.__obj_type = object_dict['type']
        if 'angle' in object_dict:
            self.__angle = float(object_dict['angle'])
        else:
            self.__angle = 0.0

    @property
    def id(self) -> str:
        return self.__id

    @property
    def x(self) -> float:
        return self.__x

    @property
    def y(self) -> float:
        return self.__y

    @property
    def obj_type(self):
        return self.__obj_type

    @property
    def angle(self) -> float:
        return self.__angle

    @property
    def is_bullet(self) -> bool:
        return self.__obj_type == 'Bullet'

    @property
    def is_blast(self) -> bool:
        return self.__obj_type == 'Blast'

    @property
    def is_bonus_repair(self) -> bool:
        return self.__obj_type == 'BonusRepair'

    @property
    def is_bonus_blast(self) -> bool:
        return self.__obj_type == 'BonusBlast'
