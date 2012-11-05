"""Screen scraper for University of East London job site.
"""

from common import *

SALARY_RE = re.compile(u'''
    \u00A3          # Pound sign
    ([\d,]+)        # digits and commas (the min salary)
    \s+             # at least one space
    to              # the word 'to'
    \s+             # at least one space
    \u00A3          # Pound sign
    ([\d,]+)        # digits and commas (the max salary)
''', re.VERBOSE)

def extract_fields(soup):
    """The job listing does not have the fields in very easily navigable
    HTML. It is one p tag with the headers in strong tags followed by the
    values in plain text. This, given the p tag soup, returns the fields in a
    dictionary.
    """
    # initial strong is just the job title; skip over it
    soup = soup.find("strong")
    headers = soup.find_next_siblings("strong")

    def header_text(header):
        return header.replace(u': \xa0', u'')

    return dict((header_text(header.next), header.next.next) \
                    for header in headers)

class EastLondon(object):
    ROOT_URL = "http://jobs.uel.ac.uk"

    LISTING_PAGE = "vacancies.aspx?cat=-1"

    def job_urls(self, browser):
        browser.open(urljoin(EastLondon.ROOT_URL, EastLondon.LISTING_PAGE))
        soup = BeautifulSoup(browser.response().read())

        def is_vacancy_href(href):
            return starts_with(href, "Vacancy.aspx")

        return [urljoin(EastLondon.ROOT_URL, link.get("href")) for link in \
                    soup.find(id="ctl00_mainContentPlaceHolder_pnlAllCats").\
                    find_all_next("a", href=is_vacancy_href)]

    def extract_job(self, soup):
        title = unicode(string.strip(soup.find("h1").string))

        fields = extract_fields(soup.find("h1").find_next_sibling("p"))

        job = dict(title=title, uid=fields.get("Reference", None).strip())

        try:
            salary = fields["Salary"]
            m = SALARY_RE.match(salary)
            if m:
                job["salary"] = tuple(parse_salary(s) for s in m.groups())
        except KeyError:
            salary = None

        return job
