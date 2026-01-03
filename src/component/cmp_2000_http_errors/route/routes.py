"""Test for HTTP errors."""

from flask import abort, current_app, redirect, request, url_for
from werkzeug.exceptions import HTTPException

from core.dispatcher import Dispatcher  # pylint: disable=import-error

from . import bp  # pylint: disable=no-name-in-module


@bp.errorhandler(Exception)
def handle_exception(e):
    """Handle exceptions globally."""
    if isinstance(e, HTTPException):
        code = e.code
        name = e.name
        description = e.description
    else:
        if current_app.debug:
            raise e

        code = 500
        name = "Internal Server Error"
        description = "An internal error occurred in app."

    dispatch = Dispatcher(request, "HTTP_ERROR", bp.neutral_route)
    return dispatch.view.render_error(code, name, description)


@bp.route("/zerodivisionerror")
def error_test_zerodivisionerror():
    """This will raise a ZeroDivisionError, which is caught by the global exception handler."""
    get_error = 0 / 0  # pylint: disable=unused-variable,pointless-statement


@bp.route("/403")
def error_test_403():
    """test abort 403."""
    abort(403)


@bp.route("/404")
def error_test_404():
    """test template error 404."""
    dispatch = Dispatcher(request, "404", bp.neutral_route)
    return dispatch.view.render_error(
        404, "Not Found", "The requested resource was not found."
    )


@bp.route("/302")
def error_test_302():
    """test redirect 302."""

    return redirect(url_for("bp_5100_home.home"))
