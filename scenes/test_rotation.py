import math
from manim import *

def distance_rotated(object, angle):
    radius = object.side_length / 2
    return angle * radius

def distance_vector(object, angle, compliment):
    radius = object.side_length / 2
    displacement = compliment * radius
    d_x = displacement * math.cos(angle)
    d_y = displacement * math.sin(angle)
    return Vector([d_x, -d_y, 0])

class RotatingSquare:
    def __init__(self, side_length, starting_postion):
        self.side_length = side_length
        self.starting_postion = starting_postion
        self.ending_postion = [0,0,0]
    
    def displacement_magnitude(self):
        displacement = math.sqrt(
            (self.starting_postion[0] - self.ending_postion[0]) ** 2
            +
            (self.starting_postion[1] - self.ending_postion[1]) ** 2
        )
        return displacement
    
    def displacement_x(self):
        displacement = math.sqrt(abs(self.starting_postion[0] - self.ending_postion[0] ** 2))
        return displacement
    
    def displacement_y(self):
        displacement = math.sqrt(abs(self.starting_postion[1] - self.ending_postion[1] ** 2))
        return displacement
    
class RotateSquare(Scene):
    def construct(self):

        short_wait = 1
        reg_wait = 2
        long_wait = 3

        theta = PI/3
        phy = PI - theta

        # Our test square
        square = Square(side_length=2, fill_opacity=0.5)
        square_object = RotatingSquare(side_length=2, starting_postion=[0,0,0])
        # Its starting center of mass
        cm_start = Dot(point=square.get_center())

        self.play(
            Create(square),
            Create(cm_start)
        )
        self.wait(reg_wait)

        # Rotate square
        self.play(
            Rotate(square,
                   about_point=(square.get_critical_point(DL)),
                   angle=-theta)
        )
        self.wait(reg_wait)
        square_object.ending_postion = square.get_center()

        cm_next = Dot(point=square.get_center())
        self.play(
            Create(cm_next)
        )

        dist_displaced = square_object.displacement_magnitude()
        displacement_cm = Variable(dist_displaced,
                                   MathTex(r'CM displacement'),
                                   num_decimal_places=2
        ).move_to([4,3,0])

        displacement_vector = Arrow(
            start=square_object.starting_postion,
            end=square_object.ending_postion,
            color=YELLOW,
            buff=0
        )

        ending_x = square_object.displacement_x()
        displacement_x_vector = Arrow(
            start=square_object.starting_postion,
            end=[square_object.starting_postion[0] + ending_x,
                 square_object.starting_postion[1],
                 0],
            buff=0,
            color=RED
        )

        ending_y = square_object.displacement_y()
        displacement_y_vector = Arrow(
            start = square_object.starting_postion,
            end=[square_object.starting_postion[0],
                 square_object.starting_postion[1] - ending_y,
                 0],
            buff=0,
            color=BLUE
        )

        self.play(Write(displacement_cm),
                  Create(displacement_vector),
                  Create(displacement_x_vector),
                  Create(displacement_y_vector))

        self.wait(long_wait)