import math

class RotatingSquare:
    def __init__(self, side_length, starting_postion):
        self.side_length = side_length
        self.starting_postion = starting_postion
        self.ending_postion = [0,0,0]
    
    def displacement_magnitude(self):
        displacement = math.sqrt(
            (self.ending_postion[0] - self.starting_postion[0]) ** 2
            +
            (self.ending_postion[1] - self.starting_postion[1]) ** 2
        )
        return displacement
    
    def displacement_x(self):
        return math.sqrt((self.starting_postion[0] - self.ending_postion[0]) ** 2)
    
    def displacement_y(self):
        return math.sqrt((self.ending_postion[1] - self.starting_postion[1]) ** 2)