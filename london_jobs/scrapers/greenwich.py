"""Scraper for University of Greenwich.
"""

from east_west import EastWest, extract_from_headers

class Greenwich(EastWest):
    root_url = "https://jobs.gre.ac.uk"

    listings_page = "vacancies.aspx?cat=-1&type=5"

    def extract_fields(self, soup):
        headers = soup.find("h3").find_next_siblings("b")
        return extract_from_headers(headers)

