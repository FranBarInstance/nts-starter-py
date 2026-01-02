"""
    Hello component routes module.

    Si no necesitamos un dispatch para ejecutar código python, simplemente se puede usar el catch_all con el dispatcher generico.

    Aquí ilustramos los dos casos
"""

from flask import Response, request

from core.dispatcher import Dispatcher  # pylint: disable=import-error

from . import bp  # pylint: disable=no-name-in-module
from .dispatcher_hellocomp import DispatcherHelloComp  # pylint: disable=import-error


@bp.route('/test1', defaults={'route': f'{bp.url_prefix}/test1'}, methods=['GET'])
def test1(route) -> Response:
    """Handle test1 requests."""
    dispatch = DispatcherHelloComp(request, route, bp.current_template_route)
    dispatch.schema_data['dispatch_result'] = "True"
    return dispatch.view.render()


@bp.route("/", defaults={"relative_route": ""}, methods=["GET"])
@bp.route("/<path:relative_route>", methods=["GET"])
def hellocomponent_catch_all(relative_route) -> Response:
    """Handle undefined urls."""
    route = f"{bp.url_prefix}/{relative_route}"
    dispatch = Dispatcher(request, route)
    dispatch.schema_data["dispatch_result"] = True
    dispatch.schema_data["current"]["template"]["route"] = bp.current_template_route
    return dispatch.view.render()
