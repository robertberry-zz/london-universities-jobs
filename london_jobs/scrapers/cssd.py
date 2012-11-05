"""Screen scraper for Central School of Speech & Drama job site.
"""

from common import *

SALARY_RE = re.compile(r'''
    ([\d,]+)            # The salary; a mix of digits and commas
    \s*                 # Any number of spaces
    (?:                 # followed by either per annum or pro rata
      per\sannum|
      pro\srata
    )
''', re.VERBOSE)

class CSSD(object):
    root_url = "http://www.cssd.ac.uk"

    listings_page = "/jobs/"

    def job_urls(self, browser):
        browser.open(urljoin(self.root_url, self.listings_page))

        soup = BeautifulSoup(browser.response().read())

        return [urljoin(self.root_url, link.get("href")) for link in \
                    soup.find("table", class_="views-table").find_all("a")]

    def extract_job(self, soup):
        title = unicode(soup.find("h1").string)
        salary_string = soup.select(".content .field .field-items " + \
                                        ".field-item p")[0].string
        m = SALARY_RE.search(salary_string)

        if m:
            salary = parse_salary(m.group(1))
        else:
            salary = None

        return dict(title=title, salary=salary)
