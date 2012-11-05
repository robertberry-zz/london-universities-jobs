"""Scraper for City University London job site.
"""

import igrasp

class City(igrasp.IGrasp):
    root_url = "http://www2.i-grasp.com/fe/"

    listing_page = "tpl_cityuniversity01.asp"

    field_map = {
        "Reference Number": "uid",
        "Location": "location",
        "Contract Duration": "type",
        "Hours": "hours",
        u"Salary Range (\u00A3)": "salary",
        }

    def extract_job(self, soup):
        details = super(City, self).extract_job(soup)

        if "salary" not in details:
            # in some of them the salary is encoded as part of the description
            # todo: add logic for extracting that if so here
            pass
        
        return details
