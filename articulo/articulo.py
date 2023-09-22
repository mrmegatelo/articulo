import requests
from typing import Union
from requests import RequestException
from functools import cached_property
from bs4 import BeautifulSoup, NavigableString
from .exceptions import HTTPErrorException

MAX_CONTENT_LOSS = 0.7

class Articulo:

    def __init__(self, link: str, threshold: float = MAX_CONTENT_LOSS, verbose: bool = False) -> None:
        """
        Article object

        Parameters:
        @link: Link to article, that should be processed.
        @threshold (optional): Max information loss coefficient, that affects article content parsing.
        @verbose (optional): Verbose mode. If enabled than all the operations will be logged.
        """
        self.__link = link
        self.__threshold = threshold
        self.__verbose = verbose
    
    @property
    def title(self):
        """
        Parsed article title
        """
        return self.__title_element.text
    
    @property
    def text(self):
        """
        Parsed article main content text.
        """
        return self.__content_markup.text
    
    @property
    def markup(self):
        """
        Article main content html markup.
        """
        return str(self.__content_markup)

    @cached_property
    def __content_markup(self):
        """
        Parses article html and returns main artice content markup.
        """
        content = None
        soup = BeautifulSoup(self.__html, features="lxml")

        best_parent_found = False
        best_parent = soup.find('body')
        test_counter = 0

        while not best_parent_found:
            self.__log(f'Looking for an element containing "{self.__title_element.text}" title inside {best_parent.name.upper()} tag...')
            for child in best_parent.children:
                if (isinstance(child, NavigableString)):
                    self.__log(f'Skipping the "{child}" string...')
                    continue
                if (child.find(self.__title_element.name, string=self.__title_element.text)):
                    self.__log(f'Found a {child.name.upper()} child tag with "{self.__title_element.text} inside."')
                    best_parent_content_length = len(best_parent.find_all('p'))
                    child_content_length = len(child.find_all('p'))

                    if (child_content_length == 0):
                        self.__log(f"Child element {child.name.upper()} is has no nested P elements. The best possible parent is {best_parent.name.upper()}.")
                        best_parent_found = True
                        break

                    content_loss_coeff = 1.0 - (child_content_length / best_parent_content_length)

                    if (child == self.__title_element.parent):
                        self.__log(f"Child element {child.name.upper()} is equal to title's parent element. Best possible parent is found.")
                        best_parent_found = True
                    elif (content_loss_coeff > self.__threshold):
                        self.__log(f"Content loss coefficient: {content_loss_coeff}. The best possible parent is {best_parent.name.upper()}.")
                        best_parent_found = True
                    else:
                        self.__log(f"Content loss coefficient: {content_loss_coeff}. Going down the document tree.")
                        best_parent = child
                    test_counter += 1
                    break
                else:
                    self.__log(f'Not found "{self.__title_element.text}" inside {child.name.upper()} tag. Skipping...')
        content = best_parent
        return content

    @cached_property
    def __title_element(self):
        """
        Parses article html and returns article title.
        """

        title = None
        soup = BeautifulSoup(self.__html, features="lxml")

        for tag in ['h1', 'h2']:
            result = soup.find(tag)
            if result is not None:
                title = result
                break

        return title

    @cached_property
    def __html(self) -> Union[str, None]:
        """
        Loads article html from link provided at the moment of an Articulo object instantiation.
        Returns full page html or None if request was not successful.
        """
        self.__log(f'Start loading article from {self.__link}...')
        response = requests.get(self.__link)
        try:
            response.raise_for_status()
        except RequestException:
            self.__log('Error loading an article.')
            raise HTTPErrorException(f"Http error: {response.reason}", response.status_code)
        self.__log(f'Article loaded.')
        return response.text
    
    def __log(self, message: str) -> None:
        """
        Logs message if object instantiated with verbose mode.
        Params:
        @message: message to log
        """
        if (self.__verbose):
            print(message)