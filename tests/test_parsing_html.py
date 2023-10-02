import pytest
import re
from articulo import Articulo
from articulo.exceptions import NoHTMLException
from requests_mock import MockerCore
from bs4 import BeautifulSoup

from .utils.helpers import read_html


@pytest.fixture
def url():
    return "https://info.cern.ch/"


@pytest.fixture
def initial_html() -> str:
    return read_html("article_simple.html")


class TestEmptyBody:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.markup is None
        assert article.text is None

    @pytest.fixture
    def html(self):
        return read_html("article_with_empty_body.html")


class TestArticleInsideBODY:
    def test_parses_article_content(
        self, requests_mock: MockerCore, url, initial_html, expected_html
    ):
        requests_mock.get(url, text=initial_html)
        article = Articulo(url, verbose=True)
        assert article.markup == expected_html

    @pytest.fixture
    def expected_html(self, initial_html):
        soup = BeautifulSoup(initial_html, features="lxml")
        return str(soup.body)


class TestNoHtmlException:
    def test_throwing_no_html_exception(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        with pytest.raises(NoHTMLException) as excetion:
            assert article.title is None
        assert excetion.match(re.compile(url))

    @pytest.fixture
    def html(self):
        return ""


class TestFindHtmlWithSiblings:
    def test_parses_article(self, requests_mock: MockerCore, url, html, expected_html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.markup == expected_html

    @pytest.fixture
    def expected_html(self, html):
        soup = BeautifulSoup(html, features="lxml")
        return str(soup.find("article"))

    @pytest.fixture
    def html(self) -> str:
        return read_html("article_with_content_siblings.html")


class TestFindHtmlWithNestedHeader:
    def test_parses_article(self, requests_mock: MockerCore, url, html, expected_html):
        requests_mock.get(url, text=html)
        article = Articulo(url, verbose=True)
        assert article.markup == expected_html

    @pytest.fixture
    def expected_html(self, html):
        soup = BeautifulSoup(html, features="lxml")
        return str(soup.find("article"))

    @pytest.fixture
    def html(self) -> str:
        return read_html("article_with_nested_heading.html")


class TestFindHtmlWithDeeplyNestedHeader:
    def test_parses_article(self, requests_mock: MockerCore, url, html, expected_html):
        requests_mock.get(url, text=html)
        article = Articulo(url, verbose=True)
        assert article.markup == expected_html

    @pytest.fixture
    def expected_html(self, html):
        soup = BeautifulSoup(html, features="lxml")
        return str(soup.find("article"))

    @pytest.fixture
    def html(self) -> str:
        return read_html("article_with_deeply_nested_heading.html")

    class TestFindHtmlWithDeeplyNestedHeader:
        def test_parses_article(
            self, requests_mock: MockerCore, url, html, expected_html
        ):
            requests_mock.get(url, text=html)
            article = Articulo(url, verbose=True)
            assert article.markup == expected_html

        @pytest.fixture
        def expected_html(self, html):
            soup = BeautifulSoup(html, features="lxml")
            return str(soup.find("article"))

        @pytest.fixture
        def html(self) -> str:
            return read_html("article_with_deeply_nested_content.html")
