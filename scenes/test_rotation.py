from manim import *

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
                   about_point=(square.get_critical_point(UR)),
                   angle=-theta)
        )
        self.wait(reg_wait)

        cm_next = Dot(point=square.get_center())
        self.play(
            Create(cm_next)
        )

        self.wait(long_wait)