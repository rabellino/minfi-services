"""Module to run a web server that handles REST calls to support minfi"""
import logging
import json
import os
from argparse import ArgumentParser, Namespace
from http import HTTPStatus

from dateutil.parser import parse as dt_parse
from flask import Flask, Response, request, current_app
from flask_cors import CORS

logger = logging.getLogger(__name__)

# URLs that webserver will tell browsers to allow requests from (CORS setting)
ALLOWED_ORIGINS = [
    'http://localhost:5173',  # local UI
    'http://minfi:5173',  # Dockerized UI
    'https://minfi.com',  # k8s dev/staging environments
]

def create_response(body: dict | str,
                    status: int | str | HTTPStatus = 200,
                    content_type = 'application/json') -> Response:
    """Create a Flask Response object

    Args:
        body (dict | str): content of response message, which must be valid JSON/JSON string.
            Will be converted to string before returning
        status (int | str | HTTPStatus): the http response status, such as 404 or '200 OK'.
            Default is 200.
        content_type (optional, str): the http response Content-Type header.
            Default is application/json.
    """
    json_body = body if isinstance(body, str) else json.dumps(body)
    return Response(response=json_body, status=status, content_type=content_type)

class APIServices:
    """Handles HTTP access to api endpoints."""

    # ---------------------
    # Initialize
    def __init__(self):
        """Handles service initialization."""
        pass

    # ---------------------
    # GET request for all example service endpoint
    def foo(self) -> Response:
        """Handles api requests"""
        logging.debug('Entering APIService#foo')
        response = {}
        try:
            response = 'bar'
        except Exception as exc:  # pylint: disable=broad-exception-caught
            logger.error('Could not build response? : %s', str(exc))
            return create_response({'error': str(exc)}, 500)

        return create_response(response)

class AppWrapper:
    """Web server class wrapping Flask app operations"""
    # pylint: disable=too-few-public-methods
    def __init__(self):
        """Build web app instance, mapping handler to endpoint"""
        self.app: Flask = Flask(__name__)

        # set CORS policy to allow specific origins on all endpoints
        CORS(self.app, methods=['OPTIONS', 'GET', 'POST'], origins=ALLOWED_ORIGINS)
        # set a CORS HEADER policy in order for browsers to allow POST requests 
        # with a JSON content type, the following header must be set
        self.app.config['CORS_HEADERS'] = 'Content-Type'

        self._api = APIServices()

        # register endpoints
        self.app.add_url_rule('/foo', 'foo', methods=['GET'], view_func=self._api.foo)

    def run(self, **kwargs):
        """Start up web server"""
        self.app.run(**kwargs)

def create_app(args: Namespace | None = None) -> tuple[Flask, int]:
    """Entry point for the Flask web server to start"""
    # initialize new AppWrapper with any config arguments
    wrapper = AppWrapper()

    return wrapper.app, args.port

if __name__ == '__main__':  # pragma: no cover
    # pylint: disable=duplicate-code

    # handle command line arguments required to run the service
    parser = ArgumentParser()
    parser.add_argument('--port', dest='port', default=8080, type=int,
                        help='The port the API web server will listen on.')

    _args = parser.parse_args()

    app, port = create_app(_args)
    app.run(host='0.0.0.0', port=port, debug=False)

# set up container run time with gunicorn (which doesn't support ArgumentParser)
elif 'gunicorn' in os.getenv('SERVER_SOFTWARE', default=''):  # pragma: no cover
    app = Flask(__name__)

    app_wrapper = AppWrapper()
    app = app_wrapper.app