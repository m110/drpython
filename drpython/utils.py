
class Pos(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return Pos(self.x + other.x, self.y + other.y)
        elif isinstance(other, (tuple, list)):
            return Pos(self.x + other[0], self.y + other[1])
        else:
            raise TypeError('Unknown object in Pos __add__')

    __radd__ = __add__
    __iadd__ = __add__

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, (tuple, list)):
            return self.x == other[0] and self.y == other[1]
        else:
            raise TypeError('Unknown object in Pos __eq__')

    def __ne__(self, other):
        return not self.__eq__(other)
