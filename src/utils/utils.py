# Copyright (C) 2025 https://github.com/FranBarInstance/neutral-pwa-py (See LICENCE)

import json

from flask import request


def get_ip():
    """Get the IP address of the client, cloudflare ip or remote addr."""
    return request.headers.get("CF-Connecting-IP", request.remote_addr)


def format_ua(ua):
    """Format user agent information into a readable string."""
    return f"{ua['name']} - {ua['os']} - {ua['category']}"


def merge_dict(a, b):
    """Merge dictionary b recursively into dictionary a.

    Args:
        a: Target dictionary to merge into (modified in place)
        b: Source dictionary (or JSON string) to merge from

    Note:
        Modifies dictionary 'a' directly. For JSON strings in 'b',
        they are automatically parsed before merging.
    """
    if isinstance(b, str):
        b = json.loads(b)

    def recursive_merge(target, source):
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                recursive_merge(target[key], value)
            else:
                target[key] = value
        return target

    recursive_merge(a, b)
