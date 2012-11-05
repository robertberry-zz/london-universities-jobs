"""Screen scraper for Central School of Speech & Drama job site.
"""

import string
import re

from urlparse import urljoin

from bs4 import BeautifulSoup

SALARY_RE = re.compile(r'''
    ([\d,]+)            # The salary; a mix of digits and commas
    \s*                 # Any number of spaces
    (?:                 # followed by either per annum or pro rata
      per\sannum|
      pro\srata
    )
''', re.VERBOSE)

class CSSD(object):
    ROOT_URL = "http://www.cssd.ac.uk"

    LISTING_PAGE = "/jobs/"

    def job_urls(self, browser):
        browser.open(urljoin(CSSD.ROOT_URL, CSSD.LISTING_PAGE))

        soup = BeautifulSoup(browser.response().read())

        return [urljoin(CSSD.ROOT_URL, link.get("href")) for link in \
                    soup.find("table", class_="views-table").find_all("a")]

    def extract_job(self, soup):
        title = str(soup.find("h1").string)

        salary_string = soup.select(".content .field .field-items " + \
                                        ".field-item p")[0].string

        m = SALARY_RE.search(salary_string)

        if m:
            salary = string.replace(m.group(1), ",", "")
        else:
            salary = None

        return dict(title=title, salary=salary)
