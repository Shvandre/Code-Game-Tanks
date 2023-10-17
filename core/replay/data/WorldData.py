class WorldData:
    def __init__(self, data):
        self.__width = data['width']
        self.__height = data['height']
        self.__terrain = 0

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def terrain(self) -> int:
        return self.__terrain
