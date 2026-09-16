"""
*** Variables, constants, etc ***
 """
from datetime import date
from datetime import datetime as dt
from datetime import timedelta

####################
# Date/time strings
####################

today = date.today()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)
timenow = dt.now()
todays_date = today.strftime("%Y-%m-%d")  # YYYY-MM-DD format
todays_date_day = today.strftime("%A, %B %d, %Y")  # Saturday, January 01, 2022
todays_dayofweek = today.strftime("%A")  # current day of the week, example: Monday
todays_date_short_month = today.strftime("%b-%d-%Y")  # Mon-DD-YYYY
todays_datetime = timenow.strftime("%Y-%m-%d %H:%M:%S")
date_hour_now = timenow.strftime("%Y-%m-%d %H:")
hour_now = timenow.strftime("%H")
datetime_alpha = timenow.strftime("%Y%m%d%H%M%S")
date_alpha = timenow.strftime("%Y%m%d")
date_alpha_format = "%Y%m%d"
date_alpha_yesterday = yesterday.strftime(date_alpha_format)  # 20230730 format
datetime_readable_format = "%Y-%b-%d %H%M%S"
datetime_readable = timenow.strftime(datetime_readable_format)  # YYYY-Mon-DD HHMMSS
timepicker_now = timenow.strftime("%#I:%M %p")  # H:MM:XX e.g. 4:05 PM
calendar_date_today = today.strftime("%#m/%d/%Y")  # 3/14/2023
calendar_date_yesterday = yesterday.strftime("%#m/%d/%Y")  # 3/13/2023 format
calendar_date_tomorrow = tomorrow.strftime("%#m/%d/%Y")  # 3/13/2023 format

# BROWSER VARS

CHROME_USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip',
    'DNT': '1',
    'Connection': 'close'
}
ICIMS_USER_AGENT = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,es-US;q=0.8,es;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'DNT': '1',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Site': 'same-origin'
}


# URLS

AMAZON_BASE_URL = 'https://amazon.com'
CCSEARCHPAGEURL = 'https://calcareers.ca.gov/CalHRPublic/Search/JobSearchResults.aspx#empty'
# location for Fresno County is 85, but can lose the url var if an update is made in the search
CCFRESNO_URL = 'https://calcareers.ca.gov/CalHRPublic/Search/JobSearchResults.aspx#locid=85'
CUSD_URL = 'https://www.edjoin.org/CENTRALusd?rows=100&page=1&catID=3&districtID=118'
FUSD_URL = 'https://www.edjoin.org/FresnoUnified?rows=10&page=1&catID=3&districtID=134'
UHC_URL = 'https://nonprovider-unitedhealthcenters.icims.com/jobs/search'