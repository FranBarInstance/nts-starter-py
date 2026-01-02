"""Info routes module."""

from flask import Response, request

from core.dispatcher import Dispatcher  # pylint: disable=import-error

from . import bp  # pylint: disable=no-name-in-module


@bp.route("/<path:relative_route>", methods=["GET"])
def info_catch_all(relative_route) -> Response:
    """Handle undefined urls."""
    route = f"{bp.url_prefix}/{relative_route}"
    dispatch = Dispatcher(request, route)
    dispatch.schema_data["dispatch_result"] = True
    dispatch.schema_data["current"]["template"]["route"] = bp.current_neutral_route
    return dispatch.view.render()
