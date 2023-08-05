#!/usr/bin/env python
# cardinal_pythonlib/wsgi/constants.py

"""
===============================================================================
    Copyright (C) 2009-2017 Rudolf Cardinal (rudolf@pobox.com).

    This file is part of cardinal_pythonlib.

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
===============================================================================

Miscellany to help with WSGI work.

"""

from typing import Callable, Dict, Iterable, List, Tuple

# =============================================================================
# Type hints for WSGI
# =============================================================================

# https://www.python.org/dev/peps/pep-0333/
TYPE_WSGI_ENVIRON = Dict[str, str]
TYPE_WSGI_STATUS = str
TYPE_WSGI_RESPONSE_HEADERS = List[Tuple[str, str]]
TYPE_WSGI_START_RESP_RESULT = Callable[[str], None]  # call with e.g. write(body_data)  # noqa
TYPE_WSGI_START_RESPONSE = Callable[[TYPE_WSGI_STATUS,
                                     TYPE_WSGI_RESPONSE_HEADERS],
                                    TYPE_WSGI_START_RESP_RESULT]
# There is an optional third parameter to start_response()
TYPE_WSGI_APP_RESULT = Iterable[str]
TYPE_WSGI_APP = Callable[[TYPE_WSGI_ENVIRON, TYPE_WSGI_START_RESPONSE],
                         TYPE_WSGI_APP_RESULT]


# =============================================================================
# Constants
# =============================================================================

class WsgiEnvVar(object):
    """
    WSGI environment variable names.

    For core ones, see http://wsgi.readthedocs.io/en/latest/definitions.html
    """
    HTTP_HOST = "HTTP_HOST"  # [2]
    HTTP_X_FORWARDED_FOR = "HTTP_X_FORWARDED_FOR"  # [2]
    HTTP_X_REAL_IP = "HTTP_X_REAL_IP"  # [7]
    HTTP_X_FORWARDED_HTTPS = "HTTP_X_FORWARDED_HTTPS"  # [7]
    HTTP_X_FORWARDED_HOST = "HTTP_X_FORWARDED_HOST"  # [4]
    HTTP_X_FORWARDED_SCRIPT_NAME = "HTTP_X_FORWARDED_SCRIPT_NAME"  # [7]
    HTTP_X_FORWARDED_SERVER = "HTTP_X_FORWARDED_SERVER"  # [4]
    HTTP_X_FORWARDED_PORT = "HTTP_X_FORWARDED_PORT"  # [7]
    HTTP_X_FORWARDED_PROTO = "HTTP_X_FORWARDED_PROTO"  # [6]
    HTTP_X_FORWARDED_PROTOCOL = "HTTP_X_FORWARDED_PROTOCOL"  # [6]
    HTTP_X_FORWARDED_SCHEME = "HTTP_X_FORWARDED_SCHEME"  # [7]
    HTTP_X_FORWARDED_SSL = "HTTP_X_FORWARDED_SSL"  # [7]
    HTTP_X_HOST = "HTTP_X_HOST"  # [7]
    HTTP_X_HTTPS = "HTTP_X_HTTPS"  # [7]
    HTTP_X_SCHEME = "HTTP_X_SCHEME"  # [5]
    HTTP_X_SCRIPT_NAME = "HTTP_X_SCRIPT_NAME"  # [5]
    PATH_INFO = "PATH_INFO"  # [1]
    REMOTE_ADDR = "REMOTE_ADDR"  # [1]
    SCRIPT_NAME = "SCRIPT_NAME"  # [1]
    SERVER_NAME = "SERVER_NAME"  # [1]
    SERVER_PORT = "SERVER_PORT"  # [1]
    URL_SCHEME = "wsgi.url_scheme"  # [3]

    # [1] Standard WSGI and standard CGI; must always be present;
    #     http://wsgi.readthedocs.io/en/latest/definitions.html
    #     https://www.python.org/dev/peps/pep-0333/
    #     https://en.wikipedia.org/wiki/Common_Gateway_Interface
    # [2] Standard WSGI as copies of standard HTTP request fields (thus,
    #     optional); http://wsgi.readthedocs.io/en/latest/definitions.html
    # [3] Also standard WSGI, but not CGI; must always be present.
    # [4] From non-standard but common HTTP request fields;
    #     https://en.wikipedia.org/wiki/List_of_HTTP_header_fields#Common_non-standard_request_fields  # noqa
    #     https://github.com/omnigroup/Apache/blob/master/httpd/modules/proxy/mod_proxy_http.c  # noqa
    # [5] Non-standard; Nginx-specific? Nonetheless, all "HTTP_" variables in
    #     WSGI should follow the HTTP request headers.
    # [6] Protocols (i.e. http versus https):
    #     https://stackoverflow.com/questions/16042647/whats-the-de-facto-standard-for-a-reverse-proxy-to-tell-the-backend-ssl-is-used  # noqa
    # [7] http://modwsgi.readthedocs.io/en/develop/release-notes/version-4.4.9.html  # noqa
