"""
Author: Jose Camacho
a jobs scraper using Playwright and BeautifulSoup
using the GovernmentJobs.com site and looping through the direct URLs
"""
import pytest
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from support import vars

urls = {'Fresno County': 'https://www.governmentjobs.com/careers/fresnoca',
        'Kings County': 'https://www.governmentjobs.com/careers/kingscounty',
        'Madera County': 'https://www.governmentjobs.com/careers/maderacountyca',
        'Tulare County': 'https://www.governmentjobs.com/careers/TULARE',
        'Merced County': 'https://www.governmentjobs.com/careers/merced',
        'Mariposa County': 'https://www.governmentjobs.com/careers/mariposacounty',
        'Stanislaus County': 'https://www.governmentjobs.com/careers/stanislaus',
        'Tuolumne County': 'https://www.governmentjobs.com/careers/tuolumnecounty',
        'City of Hanford': 'https://www.governmentjobs.com/careers/hanfordca',
        'City of Selma': 'https://www.governmentjobs.com/careers/cityofselma',
        'City of Clovis': 'https://www.governmentjobs.com/careers/clovisca',
        'City of Fresno': 'https://www.governmentjobs.com/careers/cityoffresno',
        'City of Sanger': 'https://www.governmentjobs.com/careers/sanger',
        'City of Madera': 'https://www.governmentjobs.com/careers/madera',
        'City of Merced': 'https://www.governmentjobs.com/careers/mercedca',
        'City of Visalia': 'https://www.governmentjobs.com/careers/visalia',
        'City of Tulare': 'https://www.governmentjobs.com/careers/tulareca'
        }

@pytest.mark.asyncio
@pytest.mark.scraper
@pytest.mark.playwright
async def test_scrape_govjobs():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=["--start-maximized"]) # needs to be slowed because of their animation delays
        page =  await browser.new_page(no_viewport=True)
        await page.set_extra_http_headers(vars.CHROME_USER_AGENT)
        total_listings = 0
        job_listings = []
        exclude_list = ['police', 'deputy', 'Firefighter', 'Cadet', 'Paralegal', 'Pediatric', 'Psychiatric',
                        'clinician']
        for key, value in urls.items():
            print(f'Going to {key} site now...')
            await page.goto(value, wait_until="networkidle")

            try:
                consent_banner = await page.locator("div[aria-label='Cookie Consent Banner']").is_visible()
                if consent_banner:
                    await page.get_by_role('button', name='Accept').click()
            except AttributeError:
                pass

            await page.locator('#action-grid-view').click()
            # check if there's pagination at the bottom and page through results
            results_found = await page.locator('#number-found-items').inner_text()
            results_found_number = results_found.strip().replace(' jobs found', '')
            print(f'JOBS NUMBER for {key}: {results_found_number}')

            job_listings.append(await page.content())
            total_listings += int(results_found_number)

            if int(results_found_number) > 10:
                page_last_num = await page.locator('div.pager-container-normal').locator('li.PagedList-skipToNext').locator("xpath=preceding-sibling::*[1]").text_content()
                page_num = int(page_last_num)-1
                for p in range(page_num):
                    await page.get_by_role('link', name='Go to Next Page').click()
                    #time.sleep(1)
                    job_listings.append(await page.content())
            else:
                print(f'Only one page of results for {key}')
            #print(f'PAGE CONTENT: {job_listings}')

            all_one_job_td = "".join(job_listings)
        govjobs_soup = BeautifulSoup(all_one_job_td, 'html.parser')
        job_tiles = govjobs_soup.find_all('th', attrs={'class': 'job-table-title', 'scope': 'row'})
        sorted_jobs = sorted(job_tiles, key=lambda tag: tag.text.strip())
        print(f'Total number of all jobs is: {total_listings}')
        for job in sorted_jobs:
            good_jobs = [
                j.find('a', class_='item-details-link').text.strip().lower()
                for j in sorted_jobs
                if not any(exclude in j.find('a', class_='item-details-link').text.strip().lower() for exclude in exclude_list)
            ]
            #print(f'GOOD JOBS:\n{good_jobs}')
            job_title = job.find('a', class_='item-details-link').text.strip()
            job_link = job.find('a', class_='item-details-link').get('href').strip()
            full_url = page.url
            url_index = full_url.find('/careers/')
            base_url = full_url[:url_index]
            main_th = job.find('a', class_='item-details-link').parent.parent
            job_type = main_th.find('td', class_='job-table-type').text.strip()
            job_salary = main_th.find('td', class_='job-table-salary hidden-xs').text.strip()

            print(f'{job_title} | {job_type} | {job_salary}')
            print(f'-- {base_url}{job_link}')
