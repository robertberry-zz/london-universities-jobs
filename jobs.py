#!/usr/bin/env python

from london_jobs.jobs import Job
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
            job = Job(site, job_url, **site.extract_job(soup))
            print job
            if hasattr(job, "salary"):
                print job.salary

if __name__ == '__main__':
    main()

