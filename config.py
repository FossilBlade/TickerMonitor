ticker_2_monitor = 'ZUO'

monitor_url = "file:///home/raush/vsts_git/PyCharmProjects/TickerMonitor_Mich/test_files/test_table.html"

monitor_interval = 0.0

username = 'raushan.xxxxx@example.com'
password = 'xyz@1234'

# Change below to False if you dont want to close the chrome bowser after the script has completed.
# This might be handy to troubleshoot any issues.

close_chrome_after_complete = True

# time out for the page to load
page_load_timeout = 45



### TRADING APP CONFIG
## variable to control the interaction with trading app. if this is False, no trading app actions will be taken.
enable_trading_app_actions = True

ticker_input_text_box_coordinates = (39, 229)

# Pres enter automatically after the ticker has been put in teh text box
post_paste_actions_or_txt = ['enter','add']

# DEBUG OPTION

# See mouse moving so that the script execution can be verified for various clicks.
# PLEASE NOTE THAT THIS WILL DELAY THE EXECUTION SO IT SHOULD ONLY BE USED FOR TESTING AND VERIFICATION
track_mouse_movements = True


