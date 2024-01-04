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
        ramp_height = 4
        ramp_base = 10
        ramp_calc_hypotenuse = math.sqrt(ramp_height ** 2 + ramp_base ** 2)
        # Angles Start at 90 and go ccw
        ramp_angles_array = [(PI / 2), (math.acos(ramp_base / ramp_calc_hypotenuse)), (math.acos(ramp_height / ramp_calc_hypotenuse))]
        theta = ramp_angles_array[1]
        phy = ramp_angles_array[2]
        ramp_reference_corner = [-6, -3, 0]

        # Slider paramaterized
        slider_size = self.params.slider_size
        SLIDER_REF = [ramp_reference_corner[0], ramp_reference_corner[1] + ramp_height, 0]
        slider_mass = slider_size ** 2 * DENSITY
        slider_weight = slider_mass * ACC_G
        slider = Square(side_length=slider_size, fill_opacity=0.5, color=YELLOWY)
        slider_FG_mag = ACC_G * slider_mass
        slider_FD_mag = -(ACC_G * slider_mass) * math.sin(ramp_angles_array[1])
        slider_FN_mag = -(ACC_G * slider_mass) * math.cos(ramp_angles_array[1])

        

        # Ramp consturcted from height and base length with 90 degree
        RAMP_COORD = [ramp_reference_corner,
                      [ramp_reference_corner[0] + ramp_base, ramp_reference_corner[1], 0],
                      [ramp_reference_corner[0], ramp_reference_corner[1] + ramp_height, 0]]
        ramp_corner_theta = RAMP_COORD[1]
        ramp_corner_phy = RAMP_COORD[2]
        ramp = Polygon(*RAMP_COORD, fill_opacity=0.5, color=PEACHY)
        
        # Reflection Force Triangle
        force_triangle_FG = Vector([-slider_FG_mag, 0, 0]).move_to(RAMP_COORD[1], aligned_edge=RIGHT).rotate(-ramp_angles_array[1], about_point=(RAMP_COORD[1]))
        force_triangle_FN = Vector([slider_FN_mag, 0, 0]).move_to(RAMP_COORD[1], aligned_edge=RIGHT)
        force_triangle_FD = Vector([0, -slider_FD_mag, 0]).move_to([ramp_corner_theta[0]+slider_FN_mag, ramp_corner_theta[1], ramp_corner_theta[2]], aligned_edge=DOWN)
        force_triangle_prime_group = VGroup(force_triangle_FD, force_triangle_FG, force_triangle_FN)
        #self.add(force_triangle_FG, force_triangle_FN, force_triangle_FD)

        # Background Plane
        planeBG = NumberPlane(
            background_line_style={
                "stroke_width": 2,
                "stroke_opacity": 0.3
            }
        )
        self.add(planeBG)

        #### DIRECTION VECTORS ####

        # Force of Gravity Vector, in negative Y direction
        vctY = Vector(
            direction=[0, -slider_weight, 0],
            color=PERRY)
        # Displacement Vector, and its copy to use for reference
        vctD = Vector(
            direction= [0, -slider_weight * math.sin(theta), 0],
            color=ROSEY
            ).rotate(angle=(phy))
        vctD2 = vctD.copy().set_color(color=ROSEY)
        # Normal vector of slider on ramp
        vctN = Vector(
            direction=[0, -slider_weight * math.cos(theta), 0],
            color=YELLOWY
            ).rotate(angle=-theta)

        # TEXT FORMULAE
        thetaText = MathTex(
            r'\theta'
            ).move_to([
                RAMP_COORD[1][0] - ramp_base / 4 - 0.2,
                RAMP_COORD[1][1] + 0.2,
                0]
            )

        sliderFGVar = Variable(
            var=slider_FG_mag,
            label=MathTex(r'F_G (mg)', color=WHITE),
            num_decimal_places=1,
            ).move_to([4, 3, 0])
        sliderFGVar.value.set_color(PERRY)

        normalVar = Variable(
            var=-slider_FN_mag,
            label=MathTex(r'F_N (mg*cos\theta)', color=WHITE),
            num_decimal_places=1,
            ).next_to(sliderFGVar, DOWN, aligned_edge=RIGHT)
        normalVar.value.set_color(YELLOWY)

        displacementVar = Variable(
            var=-slider_FD_mag,
            label=MathTex(r'F_D (mg*sin\theta)', color=WHITE),
            num_decimal_places=1,
            ).next_to(normalVar, DOWN, aligned_edge=RIGHT)
        displacementVar.value.set_color(ROSEY)

        # DIMENSIONS of Ramp dispayed
        rampHeightText = Integer(number=ramp_height).move_to(ramp.get_critical_point(LEFT), aligned_edge=RIGHT).shift(
            [-0.2, 0, 0])
        rampBaseText = Integer(number=ramp_base).move_to(ramp.get_critical_point(DOWN), aligned_edge=UP).shift(
            [0, -0.2, 0])

        # RAMP INCLINE ANGLE
        line1 = Line(start=RAMP_COORD[1], end=RAMP_COORD[2])
        line2 = Line(start=RAMP_COORD[1], end=RAMP_COORD[0])
        thetaArc = Angle(line1, line2, radius=(ramp_base / 4))
        rampGroup = Group(ramp, thetaArc)

        textGroup = Group(rampBaseText, rampHeightText, thetaText)

        # Place the slider to the far left ontop of ramp
        slider.move_to(SLIDER_REF, aligned_edge=DL)

        ##### ANIMATIONS #####

        # Display the Ramp and Slider
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
                angle=-ramp_angles_array[1],
                about_point=[*SLIDER_REF]
            ),
            Create(thetaArc),
            Write(thetaText)
        )
        # self.add(theta)
        self.wait(1)

        # Align each vector to the start at the center of the slider
        vctD.move_to(slider.get_center(), aligned_edge=(LEFT + UP))
        vctD2.move_to(slider.get_center(), aligned_edge=(LEFT + UP))
        vctY.move_to(slider.get_center(), aligned_edge=((0, 0, 0) + UP))
        vctN.move_to(slider.get_center(), aligned_edge=(RIGHT + UP))
        vct_force_group = VGroup(vctD, vctD2, vctY, vctN)

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

        # Transform the ghost vector group into the prime theta triangle
        self.play(
            Create(force_triangle_prime_group),
            FadeTransform(vct_force_group, force_triangle_prime_group)
        )

        # Rotate and flip the Vector Triangle theta into the Ramp Triangle theta
        # self.play(
        #     Rotate(vctGroup, angle=RAMP_ANGLES[1] + (PI/2), about_point=[*vctY.get_end()]),
        # )
        # self.play(
        #     vctGroup.animate.flip().move_to(RAMP_COORD[1], aligned_edge=(DR)).shift([0, -0.2, 0]),
        # )

        

        # Slider proceeds to bottom of ramp
        sliderGroup = Group(slider, vctD)
        self.play(
            sliderGroup.animate.shift([(ramp_calc_hypotenuse - slider_size) * math.cos(ramp_angles_array[1]),
                                       (ramp_calc_hypotenuse - slider_size) * -math.sin(ramp_angles_array[1]), 0])
        )
        self.wait(2)

        # Slider returns to original postion
        self.play(
            sliderGroup.animate.shift([-(ramp_calc_hypotenuse - slider_size) * math.cos(ramp_angles_array[1]),
                                       (ramp_calc_hypotenuse - slider_size) * math.sin(ramp_angles_array[1]), 0])
        )
        self.wait(2)

        # Rotate entire slider and ramp group to level and center ramp
        systemGroup = Group(slider, rampGroup, vct_force_group, textGroup)
        newCorner = [ramp_height * math.sin(ramp_angles_array[1]), ramp_reference_corner[1], 0]
        self.play(
            Rotate(systemGroup,
                   ramp_angles_array[1],
                   about_point=[*ramp_reference_corner])
        )
        self.play(
            systemGroup.animate.shift([newCorner[0], 0, 0]),
        )
        self.play(
            Rotate(rampBaseText, -ramp_angles_array[1], about_point=rampBaseText.get_center()),
            Rotate(rampHeightText, -ramp_angles_array[1], about_point=rampHeightText.get_center()),
            Rotate(thetaText, -ramp_angles_array[1], about_point=thetaText.get_center())
        )
        self.wait(2)

if __name__ == '__main__':
    scene = DynamicScene(params=Params())
    scene.render()
    open_media_file(scene.renderer.file_writer.movie_file_path)