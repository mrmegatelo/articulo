import pytest
from articulo import Articulo
from articulo.exceptions import HTTPErrorException
from requests_mock import MockerCore

from .utils.helpers import read_html


@pytest.fixture
def url() -> str:
    return 'https://info.cern.ch/'

@pytest.fixture
def html() -> str:
    return read_html('article_simple.html')

def test_dont_run_request_on_instatiation(requests_mock: MockerCore, url, html):
    request = requests_mock.get(url, text=html)
    Articulo(url, verbose=True)
    assert not request.called

def test_run_request_only_once(requests_mock: MockerCore, url, html):
    request = requests_mock.get(url, text=html)
    article = Articulo(url)
    article.title
    article.markup
    article.text
    assert request.called_once

def test_provides_headers_for_request(requests_mock: MockerCore, url, html):
    request = requests_mock.get(url, text=html)
    article_without_headers =  Articulo(url)
    article_without_headers.title
    assert request.last_request.headers.get('Accept') == '*/*'

    article_with_headers = Articulo(url, http_headers={ 'Accept': 'text/html' })
    article_with_headers.title
    assert request.last_request.headers.get('Accept') == 'text/html'

def test_throws_http_exception(requests_mock: MockerCore, url):
    requests_mock.get(url, text='Not Found', status_code=404, reason='Not Found')
    article = Articulo(url)
    
    with pytest.raises(HTTPErrorException) as excetion:
        assert article.title is None
    assert str(excetion.value) == 'Http error: Not Found'
