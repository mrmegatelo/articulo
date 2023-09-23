class NoHTMLException(Exception):
    pass

class HTTPErrorException(Exception):
    
    def __init__(self, message: str, http_code: int) -> None:
        self.message = message
        self.http_code = http_code
        super().__init__(message)

class MaxIterations(Exception):
    pass

class NoSuchElementException(Exception):
    pass

class NoTitleException(Exception):
    def __init__(self, url: str) -> None:
        super().__init__(f'Document {url} has no apropriate TITLE tag in html.')
