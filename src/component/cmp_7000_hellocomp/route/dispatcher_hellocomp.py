# Copyright (C) 2025 https://github.com/FranBarInstance/neutral-pwa-py (See LICENCE)

"""rrss"""

from core.dispatcher import Dispatcher  # pylint: disable=import-error


class DispatcherHelloComp(Dispatcher):
    """Read RSS."""

    def __init__(self, request, route, current_template_route):
        super().__init__(request, route)
        self.schema_data['current']['template']['route'] = current_template_route
