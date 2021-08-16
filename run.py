from scrapy.crawler import CrawlerProcess
from gtr.spiders import gtr_projects, gtr_project_organisations, gtr_project_people, gtr_organisations, gtr_people, gtr_funds
from scrapy.utils.project import get_project_settings
import argparse
import pandas as pd
from selenium import webdriver 
from time import sleep
import shutil
import glob

from api_scrapers import collaborations_api_scraper, lead_department_api_scraper, identifier_project_lookup_api_scraper
from api_scrapers import participant_values_api_scraper, research_subjects_api_scraper, publications_api_scraper
from api_scrapers import organisation_addresses_api_scraper, projects_and_topics_api_scraper
from api_scrapers import organisations_consolidated_api_scraper, studentships_api_scraper
from api_scrapers import projects_and_funds_api_scraper, combined_text_api_scraper

# import os
# import re
# from os import listdir, path

def main(args):
    
    research_subjects_api_scraper.run()
    organisation_addresses_api_scraper.run()
    lead_department_api_scraper.run()
    projects_and_topics_api_scraper.run()
    publications_api_scraper.run()
    identifier_project_lookup_api_scraper.run()
    participant_values_api_scraper.run()
    collaborations_api_scraper.run()
    projects_and_topics_api_scraper.run()
    organisations_consolidated_api_scraper.run()
    studentships_api_scraper.run()
    projects_and_funds_api_scraper.run()
    combined_text_api_scraper.run()
    
    # settings = get_project_settings()
    # settings.set('FEED_FORMAT', args.outtype)
    # process = CrawlerProcess(settings)

    # if "projects" in args.run_scrapers:        
    #     process.crawl(gtr_projects.GtRProjectsSpider)

    # if "project_organisations" in args.run_scrapers:        
    #     process.crawl(gtr_project_organisations.GtRProjectOrganisationsSpider)

    # if "project_people" in args.run_scrapers:        
    #     process.crawl(gtr_project_people.GtRProjectPeopleSpider)

    # if "organisations" in args.run_scrapers:
    #     process.crawl(gtr_organisations.GtrOrganisationsSpider)

    # if "people" in args.run_scrapers:
    #     process.crawl(gtr_people.GtrPeopleSpider)

    # if "funds" in args.run_scrapers:
    #     process.crawl(gtr_funds.GtRFundsSpider)

    # process.start()

    # if args.check and "projects" in args.run_scrapers:
    #     get_project_csv()
    #     check_project_scrape()

    # if args.check and "organisations" in args.run_scrapers:
    #     get_organisation_csv()
    #     check_organisation_scrape()

def get_project_csv():
    browser = webdriver.Chrome()
    browser.get("https://gtr.ukri.org/search/project?term=*#/csvConfirm")

    sleep(5)
    download_button = browser.find_elements_by_id("toCSV")
    sleep(5)
    download_button[0].click()
    sleep(5)    
    download_button = browser.find_elements_by_xpath("//button[contains(@onclick, 'javascript')]")
    sleep(5)
    download_button[0].click()

    while True:
    
        download = glob.glob("C:/Users/Aaron.Knight/Downloads/projectsearch-*.csv")
    
        if len(download) > 0:
            shutil.move(download[0], "./projectsearch.csv")
            break
    
def check_project_scrape():
    
    df_1 = pd.read_csv(args.output_projects)
    df_2 = pd.read_csv("projectsearch.csv")
    
    if not len(df_1) == len(df_2):
        print("# Scrapping incomplete...")
        print("# %s projects scrapped out of %s" % (len(df_1), len(df_2)))
    else:
        print("# All projects scrapped")

def get_organisation_csv():
    browser = webdriver.Chrome()
    browser.get("https://gtr.ukri.org/search/organisation?term=*#/csvConfirm")

    sleep(5)
    download_button = browser.find_elements_by_id("toCSV")
    sleep(5)
    download_button[0].click()
    sleep(5)    
    download_button = browser.find_elements_by_xpath("//button[contains(@onclick, 'javascript')]")
    sleep(5)
    download_button[0].click()

    while True:
    
        download = glob.glob("/home/aaron/Downloads/organisationsearch-*.csv")
    
        if len(download) > 0:
            shutil.move(download[0], "./organisationsearch.csv")
            break

def check_organisation_scrape():
    
    df_1 = pd.read_csv(args.output_projects)
    df_2 = pd.read_csv("organisationsearch.csv")
    
    if not len(df_1) == len(df_2):
        print("# Scrapping incomplete...")
        print("# %s organisations scrapped out of %s" % (len(df_1), len(df_2)))
    else:
        print("# All organisations scrapped")

def check_arguments():
    
    parse = argparse.ArgumentParser(description="Check arguments for GtR scrapper")
    
    parse.add_argument("--run_scrapers","-r",nargs="*",type=str,help="Run specific scrappers",
                       default=["projects","project_organisations","project_people",
                                "organisations","people"])#,"funds"])

    parse.add_argument("--output_projects","-oproj",type=str,help="Output file",default='./gtr_projects.csv')
    parse.add_argument("--output_organisations","-oorg",type=str,help="Output file",default='./gtr_organisaitons.csv')
    parse.add_argument("--output_people","-opeop",type=str,help="Output file",default='./gtr_people.csv')
    parse.add_argument("--outtype","-t",type=str,help="Type of output file",default="csv")

    parse.add_argument("--check","-c",action="store_true",help="Check all projects have been scrapped")

    args = parse.parse_args()
    return args
    
if __name__ == "__main__":
    args = check_arguments()
    main(args)
