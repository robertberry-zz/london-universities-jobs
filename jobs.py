#!/usr/bin/env python

from london_jobs.scrapers import *

from mechanize import Browser
from bs4 import BeautifulSoup

sites = (
    birkbeck.Birkbeck(),
    )

def main():
    browser = Browser()
    
    for site in sites:
        for job_url in site.job_urls(browser):
            browser.open(job_url)
            html = browser.response().read()
            soup = BeautifulSoup(html)
            print site.extract_job(soup)

if __name__ == '__main__':
    main()

