"""
Author: Jose Camacho
a beautifulsoup scraper integrated with Playwright to bypass a javascript-loaded page
before running, in terminal you must install Playwright, and BeautifulSoup through pip ('pip install playwright', etc.)
then run the command 'playwright install' in terminal
this is a single-file approach to searching a page with multiple results and paging through them to get
them all using Playwright, and then BeautifulSoup to parse
"""
import re
import time

import pytest
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, expect
from support import vars
from playwright_stealth import Stealth

@pytest.mark.asyncio
@pytest.mark.scraper
async def test_uhc_jobs_scraper_paging():

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True, slow_mo=800, args=["--start-maximized"])
        uhcpage =  await browser.new_page(no_viewport=True)

        print(f'Going to UHC now...')
        await uhcpage.goto(vars.UHC_URL, wait_until="networkidle")

        iframe = uhcpage.frame_locator('iframe#icims_content_iframe')
        sort_by = iframe.locator('#iCIMS_SortSelect')
        await sort_by.select_option(index=6)
        iframe_content = uhcpage.frame(name="icims_content_iframe").content()


        job_listings = [await iframe_content]
        #print(f'JOB LISTINGS BEFORE: \n\n\n {job_listings}')

        paging_present = iframe.locator('div[class="iCIMS_PagingBatch "]')
        await paging_present.click()
        page_count = (await iframe.locator('div[class="iCIMS_PagingBatch "]').locator('a').count()+1)
        for page in range(1, page_count):
            next_button = iframe.locator('span[class="halflings halflings-menu-right"]')
            await next_button.click()
            job_listings.append(await uhcpage.frame(name="icims_content_iframe").content())

        all_one_job_td = "|||".join(job_listings)
        #print(f'JOB LISTINGS AFTER (ALL): \n\n\n {all_one_job_td}')
        await browser.close()

        print('Done getting job info from UHC jobs page')

    # now that all pages are joined, parse the results of all those pages
    uhc_soup = BeautifulSoup(all_one_job_td, 'html.parser')

    uhc_job_tiles = uhc_soup.find_all('li', class_=re.compile('iCIMS_JobCardItem'))
    #sorted_jobs = sorted(uhc_job_tiles, key=lambda tag: tag.text.strip())
    print(f'UHC jobs list ({len(uhc_job_tiles)}) (paging): ')
    if not uhc_job_tiles:
        print("No jobs found")
        return
    time.sleep(1)
    for job in uhc_job_tiles:
        title = job.find('div', class_=re.compile('col-xs-12 title')).find('h3').text.strip()
        days_ago = job.find('div', class_=re.compile('col-xs-6 header right')).find_all('span')[1].find_all('span')[0].get_text()
        link = job.find('div', class_=re.compile('col-xs-12 title')).find('a').get('href').strip()
        work_place = job.find('div', class_=re.compile('col-xs-6 header left')).select_one('span:nth-of-type(2)').text.strip()
        schedule = job.find('div', class_=re.compile('col-xs-12 additionalFields')).find_all('div', class_="iCIMS_JobHeaderTag")[1].find('dd').text.strip()


        if link and not link.startswith('http'):
            link = f'https://nonprovider-unitedhealthcenters.icims.com/{link}'

        print(f'{title} | {schedule} | {work_place} - {days_ago}')
        print(f'-- {link}')
