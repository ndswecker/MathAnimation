from manim import *
from scenes.base import BaseScene
from pydantic import BaseModel


class Params(BaseModel):
    radius: float = 1.0


class DynamicScene(BaseScene):
    def construct(self):
        circle = Circle(radius=self.params.radius)
        circle.set_fill(PINK, opacity=0.5)
        self.play(Create(circle))


if __name__ == "__main__":
    DynamicScene(params=Params()).render()
