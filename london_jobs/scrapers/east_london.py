"""Screen scraper for University of East London job site.
"""

from east_west import EastWest, header_text

def extract(soup):
    """The job listing does not have the fields in very easily navigable
    HTML. It is one p tag with the headers in strong tags followed by the
    values in plain text. This, given the p tag soup, returns the fields in a
    dictionary.
    """
    # initial strong is just the job title; skip over it
    soup = soup.find("strong")
    headers = soup.find_next_siblings("strong")

    return dict((header_text(header.next), header.next.next) \
                    for header in headers)

class EastLondon(EastWest):
    root_url = "http://jobs.uel.ac.uk"

    listings_page = "vacancies.aspx?cat=-1"

    def extract_fields(self, soup):
        return extract(soup.find("h1").find_next_sibling("p"))
