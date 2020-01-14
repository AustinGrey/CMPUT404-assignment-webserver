from request import HTTPRequest
from response import HTTPResponse
import pathlib
import os

class HTTPWebHandler():

    default_contents = {
        301: '<h1>301 - Moved Permanently</h1>',
        404: '<h1>404 - Path Not Found</h1>',
        405: '<h1>405 - Method Not Allowed</h1>'
    }

    web_root = str(pathlib.Path("www").resolve()) + os.sep

    def __init__(self, request: HTTPRequest):
        self.request = request
        self.response = HTTPResponse()

        # Go ahead and handle the request
        self.handle_request()

    def handle_request(self):
        """
        Handles the request and prepares the response
        :return:
        """
        if self.request.method != 'GET':
            self.response.code = 405
            return

        self.get_path()

    def get_path(self):
        """
        Gets the path requested and places in the response, setting the appropriate headers
        :return:
        """
        # Since the Path class always removes trailing slashes, we need to store the slash
        trailing_slash = os.sep if self.request.uri[-1] == '/' else ''

        request_path = pathlib.Path(self.request.uri)
        # Normalize this path relative to the web root
        norm_path = pathlib.Path(self.web_root + str(request_path)).resolve()

        # Then check if the path is within the web root
        try:
            norm_path.relative_to(pathlib.Path(self.web_root))
        except:
            # We do not authorize paths outside of web root
            # But a 403 Forbidden should state why the request was not authorized
            # and I don't want to encourage whoever is trying to hack my root
            # So we do a 404 instead
            self.response.code = 404
            return

        if norm_path.exists() and norm_path.is_file():
            with norm_path.open() as f:
                self.response.contents = f.read()
            self.response.code = 200

            # Information about this header was gathered from
            # MDN Web Docs
            # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
            # Any copyright is dedicated to the Public Domain. http://creativecommons.org/publicdomain/zero/1.0/
            self.response.add_header('Content-Type', f'text/{norm_path.suffix[1:]}; charset=UTF-8')

        elif (norm_path / 'index.html').exists() and norm_path.is_dir():
            if trailing_slash == os.sep:
                # Serve the index.html file for this directory
                with (norm_path / 'index.html').open() as f:
                    self.response.contents = f.read()
                self.response.code = 200

                # Information about this header was gathered from
                # MDN Web Docs
                # https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Type
                # Any copyright is dedicated to the Public Domain. http://creativecommons.org/publicdomain/zero/1.0/
                self.response.add_header('Content-Type', 'text/html; charset=UTF-8')
            else:
                # The path is wrong, they are attempting to access the directory without a slash
                self.response.code = 301
                self.response.add_header('Location', self.request.uri + '/')

        else:
            self.response.code = 404



    # def result(self):
    #     """
    #     Return the HTTPResponse object we would like to have sent
    #     :return: None
    #     """
    #     return self.response
