from manim import Scene
from pydantic import BaseModel


class BaseScene(Scene):
    def __init__(self, params: BaseModel, **kwargs):
        super().__init__(**kwargs)
        self.params = params
