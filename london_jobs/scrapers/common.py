# Common imports

import string
import re

from urlparse import urljoin

from bs4 import BeautifulSoup

def starts_with(haystack, needle):
    """Whether haystack begins with substring needle.
    """
    return string.find(haystack, needle) == 0

def parse_salary(salary):
    salary = string.replace(salary, ",", "")
    return int(salary)
