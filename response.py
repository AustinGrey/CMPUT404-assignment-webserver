class HTTPResponse():

    response_codes = {
        200: 'OK',
        301: 'Moved Permanently',
        404: 'Path Not Found',
        405: 'Method Not Allowed'
    }

    def __init__(self):
        """
        Hardcoded to support HTTP/1.1 right now
        """
        self.protocol = 'HTTP'
        self.version = '1.1'

        # By default, we assume the path is not found
        self.code = 404

        # Allow a dictionary of headers
        self.headers = {}

        # Response contents
        self.contents = ""

    def add_header(self, header_name, header_contents):
        self.headers[header_name] = header_contents



    def resolve(self):
        """
        Resolves the current request into a byte array appropriate for sending as a response
        :return: byte array
        """
        output = f"{self.protocol}/{self.version} {self.code} {self.response_codes[self.code]}\r\n"

        # Calculate the content length
        self.add_header('Content-Length', str(len(bytearray(self.contents, 'utf-8'))))

        for header in self.headers:
            output += f"{header}: {self.headers[header]}\r\n"

        output += f"\r\n{self.contents}"

        return bytearray(output, 'utf-8')
