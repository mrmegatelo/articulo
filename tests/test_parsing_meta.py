import pytest
from articulo import Articulo
from requests_mock import MockerCore
from bs4 import BeautifulSoup

@pytest.fixture
def url() -> str:
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
class TestParsingIcons:
    def test_returns_none_if_no_icon_found(self, requests_mock: MockerCore, url, initial_html):
        requests_mock.get(url, text=initial_html)
        article = Articulo(url)

        assert article.icon is None

    def test_retrieves_default_icon(self, requests_mock: MockerCore, url, html_with_default_icon, icon_href_default):
        requests_mock.get(url, text=html_with_default_icon)
        article = Articulo(url)

        assert article.icon == icon_href_default

    def test_retrieves_biggest_icon(self, requests_mock: MockerCore, url, html_with_several_icons, icon_href_big):
        requests_mock.get(url, text=html_with_several_icons)
        article = Articulo(url)

        assert article.icon == icon_href_big
        
    @pytest.fixture
    def icon_href_default(self):
        return '/icon.png'
    
    @pytest.fixture
    def html_with_default_icon(self, initial_html, icon_href_default):
        soup = BeautifulSoup(initial_html, features='lxml')
        icon_without_size_tag = soup.new_tag('link', rel='icon', href=icon_href_default)
        soup.head.append(icon_without_size_tag)

        return str(soup)
    
    @pytest.fixture
    def icon_href_small(self):
        return '/icon_small.png'
    
    @pytest.fixture
    def icon_href_big(self):
        return '/icon_big.png'

    @pytest.fixture
    def html_with_several_icons(self, initial_html, icon_href_big, icon_href_small):
        soup = BeautifulSoup(initial_html, features='lxml')
        icon_small = soup.new_tag('link', rel='icon', href=icon_href_small, sizes='16x16')
        icon_big = soup.new_tag('link', rel='icon', href=icon_href_big, sizes='32x32')
        soup.head.append(icon_big)
        soup.head.append(icon_small)

        return str(soup)
    
class TestParsingKeywords:
    def test_retrieves_empty_list(self, requests_mock: MockerCore, url, initial_html):
        requests_mock.get(url, text=initial_html)
        article = Articulo(url)
        assert not article.keywords is None
        assert len(article.keywords) == 0

    def test_retrieves_keywords_list(self, requests_mock: MockerCore, url, html_with_keywords, expected_keywords):
        requests_mock.get(url, text=html_with_keywords)
        article = Articulo(url)
        assert not article.keywords is None
        assert article.keywords == expected_keywords

    @pytest.fixture
    def expected_keywords(self):
        return ['lorem', 'ipsum']
    
    @pytest.fixture
    def html_with_keywords(self, initial_html, expected_keywords):
        soup = BeautifulSoup(initial_html, features='lxml')
        keywords_meta = soup.new_tag('meta', attrs={ 'name': 'keywords', 'content': ', '.join(expected_keywords) })
        soup.head.append(keywords_meta)
        return str(soup)
    
class TestParsingDescription:
    def test_retrieves_none(self, requests_mock: MockerCore, url, initial_html):
        requests_mock.get(url, text=initial_html)
        article = Articulo(url)
        assert article.description is None

    def test_retrieves_description_from_meta(self, requests_mock: MockerCore, url, html_with_meta_description, expected_description):
        requests_mock.get(url, text=html_with_meta_description)
        article = Articulo(url)
        assert article.description == expected_description
    
    @pytest.fixture
    def expected_description(self):
        return 'Lorem ipsum'
    
    @pytest.fixture
    def html_with_meta_description(self, initial_html, expected_description):
        soup = BeautifulSoup(initial_html, features='lxml')
        description_meta = soup.new_tag('meta', attrs={ 'name': 'description', 'content': expected_description })
        soup.head.append(description_meta)
        return str(soup)
    
class TestParsingPreview:
    def test_retrieves_none(self, requests_mock: MockerCore, url, initial_html):
        requests_mock.get(url, text=initial_html)
        article = Articulo(url)
        assert article.preview is None

    def test_retrieves_preview_from_meta(self, requests_mock: MockerCore, url, html_with_meta_preview, expected_preview):
        requests_mock.get(url, text=html_with_meta_preview)
        article = Articulo(url)
        assert article.preview == expected_preview

    @pytest.fixture
    def expected_preview(self):
        return '/preview.png'
    
    @pytest.fixture
    def html_with_meta_preview(self, initial_html, expected_preview):
        soup = BeautifulSoup(initial_html, features='lxml')
        preview_meta = soup.new_tag('meta', attrs={ 'property': 'og:image', 'content': expected_preview })
        soup.head.append(preview_meta)
        return str(soup)