"""Home routes module."""

from flask import Response, request

from core.dispatcher import Dispatcher  # pylint: disable=import-error

from . import bp  # pylint: disable=no-name-in-module


@bp.route('/', defaults={'route': 'home'}, endpoint='home', methods=['GET'])
def home(route) -> Response:
    """Route handler for the home page."""
    dispatch = Dispatcher(request, route)
    dispatch.schema_data['current']['template']['route'] = bp.current_template_route
    dispatch.schema_data['dispatch_result'] = True
    return dispatch.view.render()
