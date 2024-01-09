import uuid
from flask import render_template, request
from . import forms
from web import settings
from scenes import circle
from scenes import slidingblock


def index_view():
    return render_template("animations/index.html")


def circle_view():
    form = forms.CreateCircleForm()
    file_path = "media/default/Circle.mp4"
    if request.method == "POST":
        if form.validate_on_submit():
            params = circle.Params(
                radius=request.form["radius"],
            )
            scene = circle.DynamicScene(params=params)
            file_name = f"{uuid.uuid4().hex}.mp4"
            scene.renderer.file_writer.movie_file_path = settings.DYNAMIC_VIDEO_DIR / file_name
            scene.render()
            file_path = f"media/dynamic/{file_name}"
    return render_template("animations/circle.html", file_path=file_path, form=form)


def sliding_block_view():
    form = forms.SlidingBlockForm()
    file_path = "media/default/SlidingBlock.mp4"
    if request.method == "POST":
        if form.validate_on_submit():
            params = slidingblock.Params(
                slider_size=request.form["slider_size"],
            )
            scene = slidingblock.DynamicScene(params=params)
            file_name = f"{uuid.uuid4().hex}.mp4"
            scene.renderer.file_writer.movie_file_path = settings.DYNAMIC_VIDEO_DIR / file_name
            scene.render()
            file_path = f"media/dynamic/{file_name}"
    return render_template("animations/sliding_block.html", file_path=file_path, form=form)

def rotating_square_view():
    form: forms.RotatingSquareForm()
    file_path = "media/default/RotatingSquare.mp4"
    if request.method == "POST":
        if form.validate_on_submit():
            params = rotating_square.Params(
                rotation_radian=request.form["rotation_radian"],
            )
            scene = rotating_square.DynamicScene(params=params)
            file_name = f"{uuid.uuid4().hex}.mp4"
            scene.renderer.file_writer.movie_file_path = settings.DYNAMIC_VIDEO_DIR / file_name
            scene.render()
            file_path = f"media/dynamic/{file_name}"
    return render_template("animations/rotating_square.html", file_path=file_path, form=form)