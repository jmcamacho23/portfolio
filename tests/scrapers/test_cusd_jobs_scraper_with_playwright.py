"""
Author: Jose Camacho
a beautifulsoup scraper integrated with Playwright to bypass a javascript-loaded page
this gets the list of jobs marked as 'Classified' (based on url vars) and lists them out
before running, in terminal you must install Playwright, and BeautifulSoup through pip ('pip install playwright', etc.)
then run the command 'playwright install' in terminal
"""

import pytest
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
from support import vars


@pytest.mark.asyncio
@pytest.mark.playwright
async def test_scrape_cusd_jobs_pw():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=800, args=["--start-maximized"]) # needs to be slowed because of their animation delays
        page =  await browser.new_page(no_viewport=True)
        await page.set_extra_http_headers(vars.CHROME_USER_AGENT)

        print(f'Going to CUSD EdJoin now...')
        await page.goto(vars.CUSD_URL, wait_until="networkidle")

        html_content_for_bs4 = await page.content()
        await page.close()

    cusd_soup = BeautifulSoup(html_content_for_bs4, 'html.parser')
    cusd_job_tiles = cusd_soup.find_all('a', attrs={"data-postingid": True})
    sorted_tiles = sorted(cusd_job_tiles, key=lambda tag: tag.text.strip())
    print('Central Unified jobs list: ')
    if not cusd_job_tiles:
        print("No jobs found")
        return

    for job in sorted_tiles:
        title = job.text.strip()
        link = job.get('href')

        if link and not link.startswith('http'):
            link = f'https://edjoin.org{link}'

        print(f'{title}')
        print(f'-- {link}')
