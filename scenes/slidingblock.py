import math
from manim import *
from manim.utils.file_ops import open_file as open_media_file 

try:
    from scenes.base import BaseScene
except ModuleNotFoundError:
    from base import BaseScene

from pydantic import BaseModel


class Params(BaseModel):
    slider_size: float = 1.0


class DynamicScene(BaseScene):
    def construct(self):
        # Color Palette
        PEACHY = '#ffbe98'
        YELLOWY = '#fed992'
        BLUEY = '#b5ccda'
        PERRY = '#5c7ca3'
        ROSEY = '#d44934'

        ACC_G = 9.8
        DENSITY = 0.2

        # Ramp paramaterized
        RAMP_HEIGHT = 5
        RAMP_BASE = 8
        RAMP_HYP = math.sqrt(RAMP_HEIGHT ** 2 + RAMP_BASE ** 2)
        # Angles Start at 90 and go ccw
        RAMP_ANGLES = [(PI / 2), (math.acos(RAMP_BASE / RAMP_HYP)), (math.acos(RAMP_HEIGHT / RAMP_HYP))]
        RAMP_CORNER = [-6, -3, 0]

        # Slider paramaterized
        SLIDER = self.params.slider_size
        SLIDER_REF = [RAMP_CORNER[0], RAMP_CORNER[1] + RAMP_HEIGHT, 0]
        sliderMass = SLIDER ** 2 * DENSITY
        slider = Square(side_length=SLIDER, fill_opacity=0.5, color=YELLOWY)
        sliderFGy = ACC_G * sliderMass
        sliderDispMag = -(ACC_G * sliderMass) * math.sin(RAMP_ANGLES[1])
        sliderNormMag = -(ACC_G * sliderMass) * math.cos(RAMP_ANGLES[1])

        # Ramp consturcted from height and base length with 90 degree
        RAMP_COORD = [RAMP_CORNER,
                      [RAMP_CORNER[0] + RAMP_BASE, RAMP_CORNER[1], 0],
                      [RAMP_CORNER[0], RAMP_CORNER[1] + RAMP_HEIGHT, 0]]
        ramp = Polygon(*RAMP_COORD, fill_opacity=0.5, color=PEACHY)

        # Background Plane
        planeBG = NumberPlane(
            background_line_style={
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        self.add(planeBG)

        # DIRECTION VECTORS
        lengthVector = SLIDER
        vctX = Vector([lengthVector, 0])
        # Force of Gravity Vector, in negative Y direction
        vctY = Vector([0, -(ACC_G * sliderMass)], color=PERRY)
        # Displacement Vector, and its copy to use for reference
        vctD = Vector([0, -(ACC_G * sliderMass) * math.sin(RAMP_ANGLES[1]), 0],
                      color=ROSEY
                      ).rotate(about_point=(slider.get_critical_point((0, 0, 0))),
                               angle=(RAMP_ANGLES[2]))
        vctD2 = vctD.copy().set_color(color=ROSEY)
        # Normal vector of slider on ramp
        vctN = Vector([0, -(ACC_G * sliderMass) * math.cos(RAMP_ANGLES[1]), 0],
                      color=YELLOWY
                      ).rotate(about_point=(slider.get_critical_point((0, 0, 0))),
                               angle=-RAMP_ANGLES[1])

        # TEXT FORMULAE
        thetaText = MathTex(r'\theta').move_to([RAMP_COORD[1][0] - RAMP_BASE / 4 - 0.2, RAMP_COORD[1][1] + 0.2, 0])

        sliderFGVar = Variable(sliderFGy,
                               MathTex(r'F_g (mg)'),
                               num_decimal_places=1
                               ).move_to([4, 3, 0])
        sliderFGVar.label.set_color(WHITE)
        sliderFGVar.value.set_color(PERRY)

        normalVar = Variable(-sliderNormMag,
                             MathTex(r'F_N (mg*cos\theta)'),
                             num_decimal_places=1,
                             ).next_to(sliderFGVar, DOWN, aligned_edge=RIGHT)
        normalVar.label.set_color(WHITE)
        normalVar.value.set_color(YELLOWY)

        displacementVar = Variable(-sliderDispMag,
                                   MathTex(r'F_D (mg*sin\theta)'),
                                   num_decimal_places=1
                                   ).next_to(normalVar, DOWN, aligned_edge=RIGHT)
        displacementVar.label.set_color(WHITE)
        displacementVar.value.set_color(ROSEY)

        # DIMENSIONS of Ramp dispayed
        rampHeightText = Integer(number=RAMP_HEIGHT).move_to(ramp.get_critical_point(LEFT), aligned_edge=RIGHT).shift(
            [-0.2, 0, 0])
        rampBaseText = Integer(number=RAMP_BASE).move_to(ramp.get_critical_point(DOWN), aligned_edge=UP).shift(
            [0, -0.2, 0])

        # RAMP INCLINE ANGLE
        line1 = Line(start=RAMP_COORD[1], end=RAMP_COORD[2])
        line2 = Line(start=RAMP_COORD[1], end=RAMP_COORD[0])
        thetaArc = Angle(line1, line2, radius=(RAMP_BASE / 4))
        rampGroup = Group(ramp, thetaArc)

        textGroup = Group(rampBaseText, rampHeightText, thetaText)

        # Place the slider to the far left ontop of ramp
        slider.move_to(SLIDER_REF, aligned_edge=DL)

        # Display the Ramp and the slider on the scene
        self.play(
            Create(slider),
            Create(ramp),
            Write(rampHeightText),
            Write(rampBaseText),
        )
        self.wait(1)

        # Rotate the slider into the correct angle
        self.play(
            Rotate(
                slider,
                angle=-RAMP_ANGLES[1],
                about_point=[*SLIDER_REF]
            ),
            Create(thetaArc),
            Write(thetaText)
        )
        # self.add(theta)
        self.wait(1)

        # Align each vector to the start at the center of the slider
        vctX.move_to(slider.get_critical_point((0, 0, 0)), aligned_edge=(LEFT))
        vctD.move_to(slider.get_critical_point((0, 0, 0)), aligned_edge=(LEFT + UP))
        vctD2.move_to(slider.get_critical_point((0, 0, 0)), aligned_edge=(LEFT + UP))
        vctY.move_to(slider.get_critical_point((0, 0, 0)), aligned_edge=((0, 0, 0) + UP))
        vctN.move_to(slider.get_critical_point((0, 0, 0)), aligned_edge=(RIGHT + UP))
        vctGroup = Group(vctD, vctD2, vctY, vctN)

        # Add Directional vectors and formula in sequence with pauses
        self.play(Create(vctY), Write(sliderFGVar))
        self.wait(2)
        self.play(Create(vctN), Write(normalVar))
        self.wait(2)
        self.play(Create(vctD), Write(displacementVar))
        self.wait(2)
        self.play(Create(vctD2))

        # Shift D2 to Tail of N vector
        self.play(
            vctD2.animate.shift(vctN.get_vector())
        )
        self.wait(2)

        # Slider proceeds to bottom of ramp
        sliderGroup = Group(slider, vctD)
        self.play(
            sliderGroup.animate.shift([(RAMP_HYP - SLIDER) * math.cos(RAMP_ANGLES[1]),
                                       (RAMP_HYP - SLIDER) * -math.sin(RAMP_ANGLES[1]), 0])
        )
        self.wait(2)

        # Slider returns to original postion
        self.play(
            sliderGroup.animate.shift([-(RAMP_HYP - SLIDER) * math.cos(RAMP_ANGLES[1]),
                                       (RAMP_HYP - SLIDER) * math.sin(RAMP_ANGLES[1]), 0])
        )
        self.wait(2)

        # Rotate entire slider and ramp group to level and center ramp
        systemGroup = Group(slider, rampGroup, vctGroup, textGroup)
        newCorner = [RAMP_HEIGHT * math.sin(RAMP_ANGLES[1]), RAMP_CORNER[1], 0]
        self.play(
            Rotate(systemGroup,
                   RAMP_ANGLES[1],
                   about_point=[*RAMP_CORNER])
        )
        self.play(
            systemGroup.animate.shift([newCorner[0], 0, 0]),
        )
        self.play(
            Rotate(rampBaseText, -RAMP_ANGLES[1], about_point=rampBaseText.get_center()),
            Rotate(rampHeightText, -RAMP_ANGLES[1], about_point=rampHeightText.get_center()),
            Rotate(thetaText, -RAMP_ANGLES[1], about_point=thetaText.get_center())
        )
        self.wait(2)

if __name__ == '__main__':
    scene = DynamicScene(params=Params())
    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)