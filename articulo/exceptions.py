class NoHTMLException(Exception):
    pass

class HTTPErrorException(Exception):
    
    def __init__(self, message: str, http_code: int) -> None:
        self.message = message
        self.http_code = http_code
        super().__init__(message)

class NoSuchElementException(Exception):
    pass

