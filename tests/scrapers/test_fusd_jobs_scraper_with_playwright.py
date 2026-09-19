"""
Author: Jose Camacho
a beautifulsoup scraper integrated with Playwright to bypass a javascript-loaded page
this gets the list of jobs marked as 'Classified' (based on url vars) and lists them out
before running, in terminal you must install Playwright, and BeautifulSoup through pip ('pip install playwright', etc.)
then run the command 'playwright install' in terminal
this is a single-file approach
"""

from bs4 import BeautifulSoup
import pytest
from support import vars
from playwright.async_api import async_playwright


@pytest.mark.asyncio
@pytest.mark.playwright
async def test_scrape_fusd_jobs_pw():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, slow_mo=800, args=["--start-maximized"]) # needs to be slowed because of their animation delays
        page =  await browser.new_page(no_viewport=True)
        await page.set_extra_http_headers(vars.CHROME_USER_AGENT)

        print(f'Going to FUSD EdJoin now...')
        await page.goto(vars.FUSD_URL, wait_until="networkidle")

        html_content_for_bs4 = await page.content()
        await page.close()

    fusd_soup = BeautifulSoup(html_content_for_bs4, 'html.parser')

    fusd_job_tiles = fusd_soup.find_all('a', attrs={"data-postingid": True})
    sorted_tiles = sorted(fusd_job_tiles, key=lambda tag: tag.text.strip())
    print('FRESNO Unified jobs list: ')
    if not fusd_job_tiles:
        print("No jobs found")
        return

    for job in sorted_tiles:
        title = job.text.strip()
        link = job.get('href')

        if link and not link.startswith('http'):
            link = f'https://edjoin.org{link}'

        print(f'{title}')
        print(f'-- {link}')
