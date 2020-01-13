from request import HTTPRequest
from response import HTTPResponse
import pathlib

class HTTPWebHandler():

    default_contents = {
        301: '<h1>301 - Moved Permanently</h1>',
        404: '<h1>404 - Path Not Found</h1>',
        405: '<h1>405 - Method Not Allowed</h1>'
    }

    web_root = pathlib.Path("www")

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
        self.get_path()

    def get_path(self):
        """
        Gets the path requested and places in the response
        :return:
        """
        path = pathlib.Path(self.request.uri)
        print("Path:", path)
        print("Relative Path:", path.relative_to("./www"))
        print("Relative Web Path:", self.web_root)
        self.response.contents = "An example contents"

    # def result(self):
    #     """
    #     Return the HTTPResponse object we would like to have sent
    #     :return: None
    #     """
    #     return self.response
