"""PytSite HTTP API Package.
"""
# Public API
from ._api import handle, endpoint, url, call, on_pre_request, on_request

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, router, tpl
    from . import _eh, _controllers

    # HTTP entry point route
    router.handle(_controllers.Entry(), '/api/<int:http_api_version>/<path:http_api_endpoint>',
                  'pytsite.http_api@entry', methods='*')

    # JavaScript API
    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**')
    assetman.js_module('pytsite-http-api', __name__ + '@pytsite-http-api')

    # Tpl globals
    tpl.register_global('http_api_endpoint', endpoint)

    # Event listeners
    router.on_response(_eh.router_response)


_init()
