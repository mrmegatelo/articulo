import pytest
from requests_mock import MockerCore

from articulo import Articulo
from tests.utils.helpers import read_html_text


@pytest.fixture
def url() -> str:
    return "https://info.cern.ch/"


class TestEmptyBody:
    def test_does_not_have_paywall(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.has_paywall == False

    @pytest.fixture
    def html(self):
        return read_html_text("article_with_empty_body.html")


class TestJsonLdPaywall:
    def test_does_has_paywall(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.has_paywall == True

    @pytest.fixture
    def html(self):
        return read_html_text("article_with_json_ld_paywall.html")
