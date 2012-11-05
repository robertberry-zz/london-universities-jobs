"""Screen scraper for Birkbeck College job site.
"""

import igrasp

class Birkbeck(igrasp.IGrasp):
    root_url = "http://jobs.bbk.ac.uk/fe/"

    listing_page = "tpl_birkbeckcollege01.asp?newms=se"

    field_map = {
        "Reference Number": "uid",
        "Location": "location",
        "Position Type": "type",
        "Salary from/to": "salary",
        "Hours": "hours"
        }
