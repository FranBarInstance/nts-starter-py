"""
    Hello component routes module.

    Si no necesitamos un dispatch para ejecutar código python, simplemente se puede usar el catch_all con el dispatcher generico.

    Aquí ilustramos los dos casos
"""

from flask import Response, request

from core.dispatcher import Dispatcher  # pylint: disable=import-error

from . import bp  # pylint: disable=no-name-in-module
from .dispatcher_hellocomp import DispatcherHelloComp  # pylint: disable=import-error


@bp.route('/test1', defaults={'route': 'test1'}, methods=['GET'])
def test1(route) -> Response:
    """Handle test1 requests."""
    dispatch = DispatcherHelloComp(request, route, bp.current_neutral_route)
    dispatch.schema_data['dispatch_result'] = "True"
    return dispatch.view.render()


@bp.route("/", defaults={"route": ""}, methods=["GET"])
@bp.route("/<path:route>", methods=["GET"])
def hellocomp_catch_all(route) -> Response:
    """Handle undefined urls."""
    dispatch = Dispatcher(request, route)
    dispatch.schema_data["dispatch_result"] = True
    dispatch.schema_data["current"]["template"]["route"] = bp.current_neutral_route
    return dispatch.view.render()
