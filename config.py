ticker_2_monitor = 'ZUO'

monitor_url = "file:///home/raush/vsts_git/PyCharmProjects/TickerMonitor_Mich/test_files/test_table.html"

monitor_interval = 0.5

username = 'raushan.trade@gmail.com'
password = 'Fool@1234'

# Change below to False if you dont want to close the chrome bowser after the script has completed.
# This might be handy to troubleshoot any issues.

close_chrome_after_complete = True

# time out for the page to load
page_load_timeout = 45

### Trading App Config

app_minimized_taskbar_icon_coordinates = (397, 862)  # (X,Y)
ticker_input_text_box_coordinates = (20, 194)

# DEBUG OPTION

# See mouse moving so that the script execution can be verified for various clicks.
# PLEASE NOTE THAT THIS WILL DELAY THE EXECUTION SO IT SHOULD ONLY BE USED FOR TESTING AND VERIFICATION
track_mouse_movements = False

# Pres enter automatically after the ticker has been put in teh text box
auto_press_enter_to_initiate_trade = True
