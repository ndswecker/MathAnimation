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

class RotateSquare(Scene):
    def construct(self):

        short_wait = 1
        reg_wait = 2
        long_wait = 3

        theta = PI/6
        phy = PI/3

        # Our test square
        square = Square(side_length=2, fill_opacity=0.5)
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

        cm_next = Dot(point=square.get_center())
        self.play(
            Create(cm_next)
        )

        dist_displaced = distance_rotated(square, theta)
        displacement_cm = Variable(dist_displaced,
                                   MathTex(r'CM displacement'),
                                   num_decimal_places=2
        ).move_to([4,3,0])
        displacement_vector = Arrow(start=[0,0,0], end=square.get_center(), buff=0)


        self.play(Write(displacement_cm),
                  Create(displacement_vector))

        self.wait(long_wait)