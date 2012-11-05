#!/usr/bin/env python

from london_jobs.jobs import Job
from london_jobs.scrapers import *

from mechanize import Browser
from bs4 import BeautifulSoup

sites = (birkbeck.Birkbeck(),
         cssd.CSSD(),
         city.City(),
         east_london.EastLondon(),
         west_london.WestLondon(),
         )

def main():
    browser = Browser()
    
    for site in sites:
        for job_url in site.job_urls(browser):
            browser.open(job_url)
            html = browser.response().read()
            soup = BeautifulSoup(html)

            job_details = site.extract_job(soup)

            if "uid" not in job_details:
                # No unique ID, just use the URL:
                job_details["uid"] = job_url
            
            job = Job(site, job_url, **job_details)
            print job
            if hasattr(job, "salary"):
                print job.salary

if __name__ == '__main__':
    main()

