from selenium import webdriver

from time import sleep
from bs4 import BeautifulSoup
from traceback import print_exc
import pyautogui

from config import LOGGING_LVL, monitor_url, username, password, ticker_2_monitor, monitor_interval, \
    close_chrome_after_complete, \
    page_load_timeout, ticker_input_text_box_coordinates, ticker_input_text_box_coordinates2, \
    ticker_input_text_box_coordinates3, ticker_input_text_box_coordinates4, ticker_input_text_box_coordinates5, \
    track_mouse_movements, \
    post_paste_actions_or_txt, post_paste_actions_or_txt2, post_paste_actions_or_txt3, post_paste_actions_or_txt4, \
    enable_trading_app_actions

import pyperclip

import logging

LOG = logging.getLogger(__name__)

############### DO NOT REMOVE BELOW ####################################
import chromedriver_binary  # Adds chromedriver binary to path

if not page_load_timeout:
    page_load_timeout = 45

if not monitor_interval:
    monitor_interval = 0.005

LOGIN_URL = 'https://www.fool.com/secure/Login.aspx'

txt_coor = ticker_input_text_box_coordinates
txt_coor2 = ticker_input_text_box_coordinates2
txt_coor3 = ticker_input_text_box_coordinates3
txt_coor4 = ticker_input_text_box_coordinates4
txt_coor5 = ticker_input_text_box_coordinates5

driver = None


def setup_driver(headless=False):
    options = webdriver.ChromeOptions()

    options.add_argument('--profile-directory=Default')
    options.add_argument("--user-data-dir=chrome-profile/profile")

    options.add_argument("disable-infobars")
    options.add_argument("disable-extensions")
    options.add_argument("disable-cache")
    options.add_argument("disk-cache-size=1")

    options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    options.add_experimental_option('useAutomationExtension', False)

    options.headless = headless

    prefs = {'profile.default_content_setting_values': {'cookies': 1, 'images': 2, 'javascript': 2,
                                                        'plugins': 2, 'popups': 2, 'geolocation': 2,
                                                        'notifications': 2, 'auto_select_certificate': 1,
                                                        'fullscreen': 2,
                                                        'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                                        'media_stream_mic': 2, 'media_stream_camera': 2,
                                                        'protocol_handlers': 2,
                                                        'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                                        'push_messaging': 2, 'ssl_cert_decisions': 2,
                                                        'metro_switch_to_desktop': 2,
                                                        'protected_media_identifier': 2, 'app_banner': 2,
                                                        'site_engagement': 2,
                                                        'durable_storage': 2}}

    options.add_experimental_option("prefs", prefs)

    global driver
    driver = webdriver.Chrome(options=options, desired_capabilities=None)
    # driver.set_page_load_timeout(page_load_timeout)
    #
    # # driver.maximize_window()
    # size = driver.get_window_size()
    # driver.set_window_size(size.get('width')/4, size.get('height'))
    # driver.set_window_position(size.get('width')+1, 0)


def login():
    # print('Login to site using url: {}'.format(LOGIN_URL))
    # driver.get(LOGIN_URL)
    try:
        username_input = driver.find_element_by_xpath('//li[@id="loginEmailUsername"]//input')
    except:
        print('Login not required')
    else:
        print('Login Required. Performing automated login')
        password_input = driver.find_element_by_xpath('//li[@id="loginPassword"]//input')

        username_input.clear()
        username_input.send_keys(username)
        sleep(.3)
        password_input.clear()
        password_input.send_keys(password)
        sleep(.3)

        login_btn = driver.find_element_by_xpath('//div[@class="signInRow"]//input')

        login_btn.click()
        sleep(3)


def get_tickers_set(soup):
    tickers = []
    LOG.debug('Finding section with id: main-content')
    table_div = soup.find("section", {"id": "main-content"})
    if table_div:
        LOG.debug('Finding table in section')
        table_2_mon = table_div.find('table')
        if table_2_mon:
            LOG.debug('Getting ticker from table')
            for ticker in table_2_mon.find_all('td', {'class': "ticker"}):
                tickers.append(ticker.text.strip())

    return set(tickers)


def get_soup_from_source(url):
    LOG.info('Opening URL: {}'.format(url))
    driver.get(url)
    source_html = driver.page_source
    if source_html:
        LOG.debug('Creating Soup')
        return BeautifulSoup(source_html, "html.parser")

    raise Exception('ERROR: Page could not be loaded by the url: {}'.format(monitor_url))


def monitor_ticker():
    setup_driver()
    soup = get_soup_from_source(monitor_url)
    login()

    LOG.info('Finding Ticker: {}'.format(ticker_2_monitor))
    orig_tickers = get_tickers_set(soup)

    LOG.info('Tickers Found: {}'.format(orig_tickers))

    if len(orig_tickers) == 0 or ticker_2_monitor not in orig_tickers:
        raise Exception('ERROR: No Ticker found "{}"'.format(ticker_2_monitor))

    if len(orig_tickers) == 3:
        raise Exception('ERROR: Not expecting 3 tickers at start of script. It should be 2')

    while True:
        soup = get_soup_from_source(monitor_url)
        tickers = get_tickers_set(soup)
        if tickers != orig_tickers:
            LOG.debug('Difference is ticker detected: New {}, Orig {}'.format(tickers, orig_tickers))
            diff_ticker = tickers - orig_tickers
            if len(diff_ticker) == 1:
                new_ticker = list(diff_ticker)[0]
                pyperclip.copy(new_ticker)
                LOG.debug('NOTIFYING: New Ticker {}'.format(new_ticker))
                break
            else:
                raise Exception('ERROR: Detected change not as expected. More than 1 ticker updated or added.')

        sleep(float(monitor_interval))
        LOG.info('Retrying after {} Sec'.format(monitor_interval))


def open_trading_app():
    if track_mouse_movements:
        pyautogui.moveTo(txt_coor, duration=0.0)

    pyautogui.click(txt_coor)

    pyautogui.hotkey('ctrl', 'v')

    if len(post_paste_actions_or_txt) > 0:
        for action in post_paste_actions_or_txt:
            pyautogui.press(action)

    if track_mouse_movements:
        pyautogui.moveTo(txt_coor5, duration=0.0)

    pyautogui.click(txt_coor5)

    pyautogui.hotkey('ctrl', 'v')

    if len(post_paste_actions_or_txt4) > 0:
        for action in post_paste_actions_or_txt4:
            pyautogui.press(action)

    if track_mouse_movements:
        pyautogui.moveTo(txt_coor2, duration=0.1)

    pyautogui.click(txt_coor2)

    if track_mouse_movements:
        pyautogui.moveTo(txt_coor3, duration=0.0)

    pyautogui.click(txt_coor3)

    if len(post_paste_actions_or_txt2) > 0:
        for action in post_paste_actions_or_txt2:
            pyautogui.press(action)

    if track_mouse_movements:
        pyautogui.moveTo(txt_coor4, duration=0.0)

    pyautogui.click(txt_coor4)

    if len(post_paste_actions_or_txt3) > 0:
        for action in post_paste_actions_or_txt3:
            pyautogui.press(action)


def run():
    try:
        monitor_ticker()

        if enable_trading_app_actions:
            open_trading_app()

    except:
        print_exc()
    finally:
        if close_chrome_after_complete:
            global driver
            if driver:
                driver.quit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.ERROR, format='%(levelname)s: %(asctime)s (%(name)s) --> %(message)s')
    LOG = logging.getLogger(__name__)
    LOG.setLevel(LOGGING_LVL)
    run()
