import pytest
import re
from articulo import Articulo
from articulo.exceptions import NoHTMLException
from requests_mock import MockerCore
from bs4 import BeautifulSoup

@pytest.fixture
def url():
    return 'https://info.cern.ch/'

@pytest.fixture
def initial_html() -> str:
    return """
<html><head></head><body><header>
<title>http://info.cern.ch</title>
</header>

<h1>http://info.cern.ch - home of the first website</h1>
<p>From here you can:</p>
<ul>
<li><a href="http://info.cern.ch/hypertext/WWW/TheProject.html">Browse the first website</a></li>
<li><a href="http://line-mode.cern.ch/www/hypertext/WWW/TheProject.html">Browse the first website using the line-mode browser simulator</a></li>
<li><a href="http://home.web.cern.ch/topics/birth-web">Learn about the birth of the web</a></li>
<li><a href="http://home.web.cern.ch/about">Learn about CERN, the physics laboratory where the web was born</a></li>
</ul>

</body></html>
"""

class TestArticleInsideBODY:
    def test_parses_article_content(self, requests_mock: MockerCore, url, initial_html, expected_html):
        requests_mock.get(url, text=initial_html)
        article = Articulo(url)
        assert article.markup == expected_html

    @pytest.fixture    
    def expected_html(self, initial_html):
        soup = BeautifulSoup(initial_html, features='lxml')
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
        return ''