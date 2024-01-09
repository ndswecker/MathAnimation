import math
from manim import *
from manim.utils.file_ops import open_file as open_media_file
from custom_objects.square_rotatable import RotatingSquare

try:
    from scenes.base import BaseScene
except ModuleNotFoundError:
    from base import BaseScene

from pydantic import BaseModel

class Params(BaseModel):
    rotation_radian: float= PI / 2
    
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