"""Base scraper class for East and West Universities of London. Much of how
both the sites work is very similar, so the code for dealing with that is
encapsulated here.
"""

from abc import ABCMeta, abstractproperty, abstractmethod

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

def header_text(header):
    return header.replace(u': \xa0', u'')

class EastWest(object):
    """Base class for East London and West London scrapers.
    """
    __metaclass__ = ABCMeta
    
    @abstractproperty
    def root_url(self):
        """Root url of the jobs site.
        """
        pass

    @abstractproperty
    def listings_page(self):
        """URL of the listings page.
        """
        pass

    @abstractmethod
    def extract_fields(self, soup):
        pass

    def job_urls(self, browser):
        browser.open(urljoin(self.root_url, self.listings_page))
        soup = BeautifulSoup(browser.response().read())

        def is_vacancy_href(href):
            return starts_with(href, "Vacancy.aspx")

        return [urljoin(self.root_url, link.get("href")) for link in \
                    soup.find("h2").\
                    find_all_next("a", href=is_vacancy_href)]

    def extract_job(self, soup):
        title = unicode(string.strip(soup.find("h1").string))

        fields = self.extract_fields(soup)

        job = dict(title=title, uid=fields.get("Reference", None).strip())

        try:
            salary = fields["Salary"]
            m = SALARY_RE.search(salary)
            if m:
                job["salary"] = tuple(parse_salary(s) for s in m.groups())
        except KeyError:
            salary = None

        return job
