from flask_wtf import FlaskForm
from wtforms import FloatField


class CreateCircleForm(FlaskForm):
    radius = FloatField("Radius")


class SlidingBlockForm(FlaskForm):
    slider_size = FloatField("Slider Size")
