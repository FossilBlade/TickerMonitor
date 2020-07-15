from selenium import webdriver

from time import sleep
from bs4 import BeautifulSoup
from traceback import print_exc
import pyautogui

import logging

LOG = logging.getLogger(__name__)

from config import LOGGING_LVL, monitor_url, username, password, monitor_interval, close_chrome_after_complete, \
    page_load_timeout, ticker_input_text_box_coordinates, ticker_input_text_box_coordinates2, \
    ticker_input_text_box_coordinates3, ticker_input_text_box_coordinates4, ticker_input_text_box_coordinates5, \
    track_mouse_movements, \
    post_paste_actions_or_txt, post_paste_actions_or_txt2, post_paste_actions_or_txt3, post_paste_actions_or_txt4, \
    enable_trading_app_actions

import pyperclip

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
    # driver.get(LOGIN_URL)
    try:
        username_input = driver.find_element_by_xpath('//li[@id="loginEmailUsername"]//input')
    except:
        LOG.info('Login not required')
    else:
        LOG.info('Login Required. Performing automated login')
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


def get_url_source(url):
    LOG.debug('Opening URL to get source: {}'.format(url))
    driver.get(url)
    return driver.page_source


def get_first_update_title_and_ticker(soup):
    LOG.debug('Getting first article title and ticker')
    LOG.debug('Finding div with id "recent-articles"')
    update_div = soup.find("div", {"id": "recent-articles"})
    if update_div:
        LOG.debug('Finding ul in div')
        updates_ul = update_div.find('ul')
        if updates_ul:
            LOG.debug('Find first li in ul')
            update_li = updates_ul.find('li')
            if update_li:
                ticker_text = None
                LOG.debug('Getting title text of h3 in li')
                title_txt = update_li.find('h3').text.strip()
                LOG.debug('Finding ticker span in li')
                ticker_span = update_li.find('span', {'class': "content-tickers"})
                if ticker_span:
                    LOG.debug('Getting ticker text')
                    ticker_text = ticker_span.text.strip()
                    if not ticker_text or ticker_text == '' or ',' in ticker_text:
                        LOG.debug('Ticker text empty or multiple')
                        ticker_text = None

                return title_txt, ticker_text

    raise Exception('ERROR: "News and Updates" section could not be parsed to get the latest article')


def monitor_ticker():
    setup_driver()
    LOG.info('Opening URL: {}'.format(monitor_url))
    driver.get(monitor_url)
    login()
    source_html = driver.page_source
    if source_html:
        soup = BeautifulSoup(source_html, "html.parser")
    else:
        raise Exception('ERROR: Page could not be loaded by the url: {}'.format(monitor_url))

    base_title, base_ticker = get_first_update_title_and_ticker(soup)

    LOG.info('Base title which will be monitored for change: [{}]'.format(base_title))

    while True:
        source_html = get_url_source(monitor_url)
        soup = BeautifulSoup(source_html, "html.parser")

        new_title, new_ticker = get_first_update_title_and_ticker(soup)

        if new_title != base_title:

            LOG.debug('New post detected. Title:[{}], Ticker: [{}]'.format(new_title, new_ticker))

            if not new_ticker:
                raise Exception('ERROR: New post has no or multiple ticker')

            pyperclip.copy(new_ticker)
            LOG.debug('NOTIFING: Title changed from [{}] to [{}]'.format(base_title, new_title))
            LOG.debug('NEW TICKER [{}] COPIED TO CLIPBOARD'.format(new_ticker))
            break

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
