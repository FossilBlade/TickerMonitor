from selenium import webdriver

from time import sleep
from bs4 import BeautifulSoup
from traceback import print_exc
import pyautogui

from config import monitor_url, username, password, ticker_2_monitor, monitor_interval, close_chrome_after_complete, \
    page_load_timeout, ticker_input_text_box_coordinates, track_mouse_movements, \
    post_paste_actions_or_txt,enable_trading_app_actions

import pyperclip

############### DO NOT REMOVE BELOW ####################################
import chromedriver_binary  # Adds chromedriver binary to path



if not page_load_timeout:
    page_load_timeout=45

if not monitor_interval:
    monitor_interval=0.5

LOGIN_URL = 'https://www.fool.com/secure/Login.aspx'

txt_coor = ticker_input_text_box_coordinates

driver = None


def setup_driver(headless=False):
    options = webdriver.ChromeOptions()

    options.add_argument('--profile-directory=Default')
    options.add_argument("--user-data-dir=chrome-profile/profile")

    options.add_argument("disable-infobars")
    options.add_argument("disable-extensions")
    options.add_argument("disable-cache")
    options.add_argument("disk-cache-size=1")

    options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
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
    print('Login to site using url: {}'.format(LOGIN_URL))
    driver.get(LOGIN_URL)
    username_input = driver.find_element_by_xpath('//li[@id="loginEmailUsername"]//input')
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
    print('Opening URL: {}'.format(url))
    driver.get(url)
    print('Returning page source')
    return driver.page_source


def get_table_2_monitor(soup):
    table_div = soup.find("section", {"id": "main-content"})
    if table_div:
        return table_div.find('table')
    else:
        return None



def get_tickers(table_2_mon):
    tickers =[]
    if not table_2_mon:
        return tickers

    for ticker in table_2_mon.find_all('td',{'class':"ticker"}):
        tickers.append(ticker.text.strip())
    return tickers


def monitor_ticker():
    setup_driver()
    login()


    source_html = get_url_source(monitor_url)
    print('Creating Soup')
    if source_html:
        soup = BeautifulSoup(source_html, "html.parser")
    else:
        raise Exception('ERROR: Page could not be loaded by the url: {}'.format(monitor_url) )
    print('Finding Table 2 Monitor')
    table_2_mon = get_table_2_monitor(soup)
    print('Finding Ticker: {}'.format(ticker_2_monitor))
    orig_tickers = get_tickers(table_2_mon)

    if len(orig_tickers) == 0 or ticker_2_monitor not in orig_tickers:
        raise Exception('ERROR: No Ticker found "{}"'.format(ticker_2_monitor))

    print('Ticker Found. Monitoring Ticker for Change')

    while True:
        source_html = get_url_source(monitor_url)
        soup = BeautifulSoup(source_html, "html.parser")
        table_2_mon = get_table_2_monitor(soup)
        tickers = get_tickers(table_2_mon)

        diff_ticker = []
        if ticker_2_monitor not in tickers:
            diff_ticker = set(tickers) - set(orig_tickers)

        if len(diff_ticker) > 0:
            pyperclip.copy(list(diff_ticker)[0])
            # print('NOTIFING: Ticker changed from {} to {}'.format(ticker_2_monitor, list(diff_ticker)[0]))
            # print('NEW TICKER COPIED TO CLIPBOARD')
            break

        sleep(float(monitor_interval))
        print('Retrying after {} Sec'.format(monitor_interval))


def open_trading_app():

    if track_mouse_movements:
        pyautogui.moveTo(txt_coor,duration=3)

    pyautogui.click(txt_coor)

    pyautogui.hotkey('ctrl', 'v')

    if len(post_paste_actions_or_txt)>0:
        for action in post_paste_actions_or_txt:
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


def main():
    run()


if __name__ == '__main__':
    main()
