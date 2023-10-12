import pytest
from articulo import Articulo
from articulo.exceptions import HTTPErrorException, DecodingException
from requests_mock import MockerCore

from .utils.helpers import read_html_text, read_html_bytes


@pytest.fixture
def url() -> str:
    return "https://info.cern.ch/"


@pytest.fixture
def html() -> str:
    return read_html_text("article_simple.html")


@pytest.fixture
def html_ru() -> bytes:
    return read_html_bytes("article_simple_ru.html", "cp1251")


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
    article_without_headers = Articulo(url)
    article_without_headers.title
    assert request.last_request.headers.get("Accept") == "*/*"

    article_with_headers = Articulo(url, http_headers={"Accept": "text/html"})
    article_with_headers.title
    assert request.last_request.headers.get("Accept") == "text/html"


def test_throws_http_exception(requests_mock: MockerCore, url):
    requests_mock.get(url, text="Not Found", status_code=404, reason="Not Found")
    article = Articulo(url)

    with pytest.raises(HTTPErrorException) as excetion:
        assert article.title is None
    assert str(excetion.value) == "Http error: Not Found"


def test_handles_default_charset(requests_mock: MockerCore, url, html_ru):
    requests_mock.get(url, content=html_ru)
    article = Articulo(url, def_charset="cp1251")

    assert article.title == "Тестовый заголовок"


def test_throws_decoding_exception(requests_mock: MockerCore, url, html_ru):
    requests_mock.get(url, content=html_ru)
    article = Articulo(url)

    with pytest.raises(DecodingException) as excetion:
        assert article.title is None
    assert str(excetion.value) == "Document https://info.cern.ch/ cannot be decoded with utf-8 charset"
