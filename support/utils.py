from datetime import datetime as dt
import sys, json, os, socket, glob
from datetime import timedelta
from pytz import timezone
import pytz
from pywinauto import keyboard as k
from selenium import webdriver
import time, pandas as pd, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

import support.paths
from support import vars, report_columns as rc, time_zones as tz
from win32api import *


chromedriver_path = "C:\\chromedriver.exe"
ffdriver_path = "C:\\geckodriver.exe"

#browser = webdriver.Chromechromedriver_path)


def br():
    global br
    br = webdriver.Chrome(chromedriver_path)
    return br


def sleep(t):
    time.sleep(t)


def get_time():
    time_now = float(datetime.utcnow().strftime('%H%M%S.%f'))
    return time_now


def wait(t): # use if en element is not being found in time, it will wait t amount of seconds
    br.implicity_wait(t)
    #WebDriverWait(br, 10).until(t.presence_of_element_located((By.ID, "waitCreate")))


def scroll(elem):
    actions = ActionChains(br)
    actions.move_to_element(elem).perform()


def by_xpath(xp):
    br.find_element(By.XPATH, xp)


def by_ID(id):
    br.find_element(By.ID, id)


def ifid_exists(id):
    try:
        webdriver.find_element('id', id)
    except NoSuchElementException:
        return False
    return True


def ifxpath_exists(xp):
    try:
        webdriver.find_element_by_xpath(xp)
    except NoSuchElementException:
        return False
    return True


def key_tab():
    k.send_keys("{TAB}")


def send_keys(ks):
    k.send_keys(ks)


def close_app():
    k.send_keys("%{F4}")


def open_app(app):
    send_keys("{VK_LWIN down}r{VK_LWIN up}")  # Windows Key + R
    k.send_keys(app, pause=0)
    k.send_keys('{ENTER}')
    time.sleep(5)


def kill_all_apps():
    # kill apps in case they linger
    k.send_keys("{VK_LWIN down}r{VK_LWIN up}")  # Windows Key + R
    k.send_keys("cmd", pause=0)
    k.send_keys('{ENTER}')
    time.sleep(2)  # wait for command prompt to open
    all_desktop_apps_to_close = support.paths.close_app_paths
    for app in all_desktop_apps_to_close:
        k.send_keys(f'taskkill /im {app} /t /f', with_spaces=True, pause=0)
        k.send_keys('{ENTER}')
        time.sleep(0.3)

    k.send_keys('exit', pause=0)  # close command prompt now
    k.send_keys('{ENTER}')


def ping_pro_server(pro, timeout=2):
    port = 9091  # pro server default
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((pro, port))
    except:
        print(f'{pro}:{port} is not responsive')
        return False
    else:
        sock.close()
        print(f'{pro}:{port} is up')
        return True


def switch_core_server(giga):
    if giga == 'JP' or giga == 'Jupiter':
        core_swap_abbrev = 'GC'
        core_swap_name = 'BeachHouse'
    elif giga == 'GC' or giga == 'BeachHouse':
        core_swap_abbrev = 'JP'
        core_swap_name = 'Jupiter'
    elif giga == 'Sa' or giga == 'Saturn':
        core_swap_abbrev = 'JP'
        core_swap_name = 'Jupiter'
    elif giga == 'KC' or giga == 'HomeBase':
        core_swap_abbrev = 'JP'
        core_swap_name = 'Jupiter'

    return core_swap_abbrev, core_swap_name


def switch_pro_server(pro):
    pro_swap_name = ''
    pro_list = vars.pro_host_ip_dict
    if pro in pro_list:
        match pro:
            case 'Skynet Biggie':
                pro_swap_name = 'The Bad Batch Biggie'
            case 'Lance Biggie':
                pro_swap_name = 'Skynet Biggie'
            case 'Groot Biggie':
                pro_swap_name = 'Skynet Biggie'
            case 'The Bad Batch Biggie':
                pro_swap_name = 'Skynet Biggie'

        return pro_swap_name
    elif pro not in pro_list:
        print('No pro system defined')



def change_region(lang):
    pc_name = socket.gethostname()
    if 'FXR347' in pc_name:
        pshell = 'pwsh'
    else:
        pshell = 'powershell'
    k.send_keys("{VK_LWIN down}r{VK_LWIN up}")  # Windows Key + R
    time.sleep(0.5)
    k.send_keys(pshell, pause=0)
    time.sleep(0.2)
    k.send_keys('{ENTER}')
    time.sleep(2)
    k.send_keys(f'Set-Culture {lang}', with_spaces=True, pause=0)
    k.send_keys('{ENTER}')
    time.sleep(1)
    k.send_keys('exit', pause=0)  # close powershell window now
    k.send_keys('{ENTER}')


def win_screenshot():
    k.send_keys("{VK_LWIN down}{PRTSC}{VK_LWIN up}")  # Windows Key + PRINT SCREEN


def print_stdout(*a):
    print(*a, file=sys.stdout)


def format_datetime(date_time):
    date_time2 = date_time.replace('T', ' ').split('.')[0]
    output_datetime = datetime.strptime(date_time2, "%Y-%m-%d %H:%M:%S")
    output_datetime2 = output_datetime.strftime('%Y-%b-%d %H:%M:%S')
    return output_datetime2


def format_time_oc(timestamp):
    saved_time_formatted = dt.strptime(timestamp, "%H:%M:%S").strftime('%#I:%M:%S %p')
    return saved_time_formatted


def format_elapsed_time(t):
    t_int = float(t)
    if t_int < 1:
        t_int = t_int + 1
    else:
        t_int = t_int
    return t_int


def write_file_contents(file_name, contents):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'a') as f:
        json.dump(contents, f, indent=0)


def append_file_contents(file_name, contents):
    with open(file_name, 'a') as f:
        f.write(f'\r{contents}')


def append_file_contents_json(file_name, contents):
    with open(file_name, 'a') as f:
        json.dump(contents, f, indent=0)


def get_binscope_html_files():
    html_files = glob.glob('C:/projects/py_automation/binscope/*')
    return html_files


def convert_bytes(size):
    if 1000 <= size < 999999:
        size = round(size/1024, 2)
        size_name = 'KB'
    elif 1000000 <= size < 999999999:
        size = round(size/1024000, 2)
        size_name = 'MB'
    elif size >= 1000000000:
        size = round(size/1024000000, 2)
        size_name = 'GB'
    return size, size_name


def get_oc_time():
    # same format as shown in OC Event Viewer
    timenow = dt.now()
    todays_datetime = timenow.strftime("%#m/%d/%Y %#I:%M:%S %p")  # 3/25/2023 2:11:23 PM format
    return todays_datetime


def get_time_readable():
    timenow = dt.now()
    datetime_readable = timenow.strftime("%Y-%b-%d %H%M%S")  # YYYY-Mon-DD HHMMSS
    return datetime_readable


def get_time_hrs_ago(hrs):
    if hrs == 'rn':
        hrs = 0
        hours_ago = datetime.now() - timedelta(hours=int(hrs))
        hours_ago_formatted = hours_ago.strftime('%#I:%M %p')
    else:
        hours_ago = datetime.now() - timedelta(hours=int(hrs))
        hours_ago_formatted = hours_ago.strftime('%#I:00 %p')
    return hours_ago_formatted


def get_report_time_offset(min_added):
    timenow = dt.now()
    now_plus = timenow + timedelta(minutes=int(min_added))
    time_plus = now_plus.strftime("%#I:%M %p")
    return time_plus


def get_date_from_string(string):
    match string:
        case 'TODAY':
            return_date = vars.calendar_date_today
        case 'YESTERDAY':
            return_date = vars.calendar_date_yesterday
        case 'TOMORROW':
            return_date = vars.calendar_date_tomorrow
    return return_date


def get_timezone_from_text(text):
    text = str(text).title()
    tzones = [t for t in tz.time_zones if re.search(text, t)]
    if not tzones:
        tzones = 'timezone not found'
    return tzones


def get_timezone_offset(tzo):
    tz_offset = dt.now(pytz.timezone(tzo)).strftime('%z')
    return tz_offset


def convert_local_time_to_other_timezone(time_zone):
    time_zone_find_name = get_timezone_from_text(time_zone)[0]
    time_zone_conversion = dt.now(timezone(time_zone_find_name))
    time_zone_date_clean = f'{str(time_zone_conversion)[0:10]}'  # cut it down to the hour
    time_zone_hour_clean = f'{str(time_zone_conversion)[11:13]}'

    return time_zone_date_clean, time_zone_hour_clean


def check_between_time(saved_time, event_time, inter):
    # saved_time is the time when the context.log_time was recorded as a part of the saving process
    # event_time is the time in Event Viewer as an example
    # inter is the interval in seconds that it is checking against, such as within 3 seconds of the event_time
    saved_time_formatted = dt.strptime(saved_time, "%m/%d/%Y %I:%M:%S %p")
    event_time_formatted = dt.strptime(event_time, "%m/%d/%Y %I:%M:%S %p")

    saved_time_unix = int(dt.timestamp(saved_time_formatted))
    event_time_unix = int(dt.timestamp(event_time_formatted))

    minustime = int(saved_time_unix) - int(inter)
    plustime = int(saved_time_unix) + int(inter)

    print(f'Minus {inter}: {minustime} | PLUS {inter}: {plustime}')
    print(f'Saved time Unix: {saved_time_unix} ({saved_time_formatted}) | Event time unix: {event_time_unix} ({event_time_formatted})')
    if (event_time_unix >= minustime) and (event_time_unix <= plustime):
        print(f'{event_time} is within {inter} seconds of event creation time')
        return True
    else:
        print(f'{event_time} is out of bounds of the {inter} second allowance')
        return False


def find_csv_data(file_path, search_item, column_name, row_skip):
    """
    :param file_path: the full path for the file to be examined
    :param search_item: the search term (string) to query
    :param column_name: the name of the column in the csv to be search with search_item
    :param row_skip: the amount of rows to be skipped from the csv, where the next is the header, then the data
    :return: boolean; True if search_item was found in the column_name for the csv
    """
    csv_data = pd.read_csv(file_path, sep=',', skiprows=row_skip)
    item_search = csv_data[csv_data[column_name] == search_item]
    if not item_search.empty:
        print(f'Search of {search_item} present in {column_name} for file {file_path}\n Results: {item_search.values}')
        return True
    elif item_search.empty:
        print(f'{search_item} not found! in {file_path}')
        return False


def find_sql_data(file_path, search_item):
    """
    :param file_path: the full path for the file to be queried
    :param search_item: the word/phrase to be searched in the file
    :return: boolean; True if the search_item was found in the sql file
    """
    with open(file_path, 'r') as q:
        sql_list = q.read()
    item_found = sql_list.find(search_item)
    return item_found


def verify_report_columns(file_path, report_type):
    """
    :param file_path: the path of the csv to analyze
    :param report_type: type of report selected that executes
    :return: boolean, True if there are columns present and they match to the predetermined set
    """
    report_columns = rc.columns[report_type]
    csv_data = pd.read_csv(file_path, sep=',', skiprows=rc.report_type_row_skip[report_type], usecols=report_columns)
    if not csv_data.empty:
        print(f'columns from {file_path} match expected columns for {report_type} report \r{csv_data.columns}')
        return True
    else:
        print(f'no columns found in {file_path}')
        return False


def get_version_number(file_path):
    file_info = GetFileVersionInfo(file_path, "\\")

    ms_file_version = file_info['FileVersionMS']
    ls_file_version = file_info['FileVersionLS']

    version2 = [str(HIWORD(ms_file_version)), str(LOWORD(ms_file_version)), str(HIWORD(ls_file_version)), str(LOWORD(ls_file_version))]
    version = ".".join(version2)
    return version

