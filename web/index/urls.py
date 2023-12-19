from flask import Blueprint

from . import views

router = Blueprint(
    name="index",
    import_name=__name__,
)

router.add_url_rule(
    rule="/",
    endpoint="index",
    view_func=views.index,
)
