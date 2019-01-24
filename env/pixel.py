class Pixel(object):

    BLANK = 0
    WALL  = 1
    APPLE = 2
    SNAKE_HEAD = 3
    SNAKE_BODY = 4

    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Pixel(self.x + other.x, self.y + other.y)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return Pixel(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items)))

    def __str__(self):
        return str(self.__dict__.items())