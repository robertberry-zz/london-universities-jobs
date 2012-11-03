import string

from urlparse import urljoin
from collections import defaultdict

from bs4 import BeautifulSoup

from ..jobs import Job

class Birkbeck(object):
    ROOT_URL = "http://jobs.bbk.ac.uk/fe/"

    LISTING_PAGE = "tpl_birkbeckcollege01.asp?newms=se"

    def job_urls(self, browser):
        browser.open(urljoin(Birkbeck.ROOT_URL, Birkbeck.LISTING_PAGE))
        browser.select_form(name="data")
        browser.submit()

        html = browser.response().read()
        soup = BeautifulSoup(html)
    
        return [urljoin(Birkbeck.ROOT_URL, link.get("href")) for link in \
                    soup.find(id="searchresultslist").find("tbody").find_all("a")]

    def extract_job(self, soup):
        title = soup.find(id="Div1")

        values = soup.find_all(class_="jobcodelists")[0]\
            .find_all(class_="desclabel")

        extract_to = {
            "Reference Number": "uid",
            "Location": "location",
            "Position Type": "type",
            "Salary from/to": "salary",
            "Hours": "hours"
            }

        extracted = defaultdict(lambda: None)

        for value in values:
            label = string.strip(str(value.string))
            if label in extract_to:
                extracted[extract_to[label]] = \
                    str(value.find_next_sibling(class_="descvalue").string)
        
        return Job(title=str(title.string), **extracted)
