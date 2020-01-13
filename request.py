import re


class HTTPRequest():

    def __init__(self, request_string):
        """
        Parses the request string into an object for easy access. If there is an error in processing it
        will return None
        :param request_string:
        """
        # Parse the request string and store the values
        # Determine the type of request
        request_line = re.match(r'^([A-Z]+) ([^ ]+) HTTP/([0-9.]+)', request_string)
        self.method = request_line.group(0)
        self.uri = request_line.group(1)
        self.version = request_line.group(2)

        # if self. != 'GET':
        #     # @todo invalid request error
        #     print("INVALID REQUEST")
        #
        #     self.request.sendall(bytearray("""HTTP/1.1 200 OK
        # Date: Mon, 13 Jan 2020 14:59:18 GMT
        # Expires: -1
        # Cache-Control: private, max-age=0
        # Content-Type: text/html; charset=ISO-8859-1""", 'utf-8'))
