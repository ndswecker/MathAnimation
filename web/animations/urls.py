from flask import Blueprint

from . import views

router = Blueprint(
    name="animations",
    import_name=__name__,
    url_prefix="/animations",
)

router.add_url_rule(
    rule="/",
    endpoint="index",
    view_func=views.index_view,
)

router.add_url_rule(
    rule="/circle",
    endpoint="circle",
    view_func=views.circle_view,
    methods=["GET", "POST"],
)

router.add_url_rule(
    rule="/sliding_block",
    endpoint="sliding_block",
    view_func=views.sliding_block_view,
    methods=["GET", "POST"],
)

router.add_url_rule(
    rule="/rotating_square",
    endpoint="rotating_square"
    view_func=views.rotating_square_view,
    methods=["GET", "POST"]
)
