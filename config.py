import logging
# When running for troubleshooting
# LOGGING_LVL = logging.DEBUG
# When for actual
LOGGING_LVL = logging.INFO

monitor_url = "https://www.fool.com/premium/rule-breakers/"
# FOR MY TESTING --  monitor_url = "http://www.faucetsandshowerheads.com/recommendation.htm"

monitor_interval = 0.005

username = 'mike@bbdstores.com'
password = '*******'

# Change below to False if you dont want to close the chrome bowser after the script has completed.
# This might be handy to troubleshoot any issues.

close_chrome_after_complete = False

# time out for the page to load
page_load_timeout = 45

### TRADING APP CONFIG
## variable to control the interaction with trading app. if this is False, no trading app actions will be taken.

enable_trading_app_actions = True

ticker_input_text_box_coordinates = (2675, 125)
ticker_input_text_box_coordinates2 = (3700, 270)
ticker_input_text_box_coordinates3 = (3710, 440)
ticker_input_text_box_coordinates4 = (2820, 95)
ticker_input_text_box_coordinates5 = (60, 100)

# Presses enter automatically after the ticker has been pasted in the text box

post_paste_actions_or_txt = ['enter']
post_paste_actions_or_txt2 = ['prtsc']
post_paste_actions_or_txt3 = ['enter']
post_paste_actions_or_txt4 = ['enter']

# DEBUG OPTION

# See mouse moving so that the script execution can be verified for various clicks.
# PLEASE NOTE THAT THIS WILL DELAY THE EXECUTION SO IT SHOULD ONLY BE USED FOR TESTING AND VERIFICATION
track_mouse_movements = False