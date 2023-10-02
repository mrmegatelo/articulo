import pytest
import re
from articulo import Articulo
from articulo.exceptions import NoTitleException
from requests_mock import MockerCore

from .utils.helpers import read_html


@pytest.fixture
def url() -> str:
    return "https://info.cern.ch/"


@pytest.fixture
def initial_html() -> str:
    return read_html("article_simple.html")


class TestEmptyBody:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch"

    @pytest.fixture
    def html(self):
        return read_html("article_with_empty_body.html")


class TestTagH1:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html):
        return initial_html


class TestTagH2:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>(.+)</h1>", "<h2>\\1</h2>", initial_html)


class TestTagH3:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>(.+)</h1>", "<h3>\\1</h3>", initial_html)


class TestTagH4:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>(.+)</h1>", "<h4>\\1</h4>", initial_html)


class TestTagH5:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>(.+)</h1>", "<h5>\\1</h5>", initial_html)


class TestTagH6:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>(.+)</h1>", "<h6>\\1</h6>", initial_html)


class TestTagP:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>(.+)</h1>", "<p>\\1</p>", initial_html)


class TestSeveralTags:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(
            r"<h1>(.+)</h1>",
            "<h1>\\1</h1>\n<h2>\\1 - h2</h2>\n<h3>\\1 - h3</h3>\n",
            initial_html,
        )


class TestTitleFromMeta:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title != "This title should not be returned"
        assert article.title == "http://info.cern.ch - home of the first website"

    @pytest.fixture
    def html(self):
        return read_html("article_with_og_title_meta.html")


class TestUnexpectedTitleTag:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>(.+)</h1>", "<span>\\1</span>", initial_html)


class TestTagTitle:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>.+</h1>", "", initial_html)


class TestTitleNotExist:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        with pytest.raises(NoTitleException) as excetion:
            article.title is None
        assert excetion.match(re.compile(url))

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<(h1|title)>.+</\1>", "", initial_html)


class TestTitleEmpty:
    def test_retrieves_title(self, requests_mock: MockerCore, url, html):
        requests_mock.get(url, text=html)
        article = Articulo(url)
        assert article.title == "http://info.cern.ch"

    @pytest.fixture
    def html(self, initial_html: str) -> str:
        return re.sub(r"<h1>.+</h1>", "<h1></h1>", initial_html)
