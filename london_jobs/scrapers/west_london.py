"""Screen scraper for University of West London job site.
"""

from east_west import EastWest, extract_from_headers

class WestLondon(EastWest):
    root_url = "http://jobs.uwl.ac.uk"

    listings_page = "vacancies.aspx?cat=-1&type=5"

    def extract_fields(self, soup):
        headers = soup.find("h4").find_next_siblings("b")
        return extract_from_headers(headers)

