


class GridNode():
    def __init__(self,parent=None,position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self,other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position}"
