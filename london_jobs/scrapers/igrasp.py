"""Scraper for University websites using the iGrasp format.
"""

import string
import re

from abc import ABCMeta, abstractproperty
from urlparse import urljoin
from collections import defaultdict

from bs4 import BeautifulSoup

SALARY_RE = re.compile(r'''
    (\d+)       # From portion of salary
    \s*\-\s*    # hyphen surrounded by any number of spaces
    (\d+)       # To portion of salary
''', re.VERBOSE)

class IGrasp(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def root_url(self):
        """Root url for the site.
        """
        pass

    @abstractproperty
    def listing_page(self):
        """The listing search page (relative from the root url).
        """
        pass

    @abstractproperty
    def field_map(self):
        """Map of fields in the table at the top of the job page to Job
        properties.
        """
        pass
    
    def job_urls(self, browser):
        def extract_page_urls(soup):
            """Given a BeautifulSoup object for a search results page, extract
            all of the urls for jobs.
            """
            return soup.select("td.igsearchresultstitle a")

        def get_next_page_url(soup):
            """Given a BeautifulSoup object for a search results page, return
            the URL of the next search results page if there is one, otherwise
            return None.
            """
            elem = soup.select("a.nextbullet")

            try:
                return elem[0].get("href")
            except IndexError:
                return None

        has_more = get_next_page_url
        
        browser.open(urljoin(self.root_url, self.listing_page))
        browser.select_form(name="data")
        browser.submit()

        html = browser.response().read()
        soup = BeautifulSoup(html)

        urls = extract_page_urls(soup)

        while has_more(soup):
            browser.open(get_next_page_url(soup))
            soup = BeautifulSoup(browser.response().read())
            urls += extract_page_urls(soup)

        return [urljoin(self.root_url, url.get("href")) for url in urls]

    def extract_job(self, soup):
        title = soup.find(id="Div1")

        values = soup.find_all(class_="jobcodelists")[0]\
            .find_all(class_="desclabel")

        extracted = defaultdict(lambda: None)

        for value in values:
            label = string.strip(unicode(value.string))
            if label in self.field_map:
                extracted[self.field_map[label]] = \
                    unicode(value.find_next_sibling(class_="descvalue").string)

        extracted["title"] = str(title.string)

        salary = extracted["salary"]
        del extracted["salary"]

        if salary is not None:
            m = SALARY_RE.match(salary)

            if m:
                extracted["salary"] = m.groups()
        
        return extracted

