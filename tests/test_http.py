import pytest
from articulo import Articulo
from articulo.exceptions import HTTPErrorException
from requests_mock import MockerCore


@pytest.fixture
def url() -> str:
    return 'https://info.cern.ch/'

@pytest.fixture
def html() -> str:
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
