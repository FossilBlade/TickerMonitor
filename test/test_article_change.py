import logging

from bs4 import BeautifulSoup

from ticker_home import get_first_update_title_and_ticker
logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

if __name__ == "__main__":
    soup = BeautifulSoup(open("/home/raush/git/TickerMonitor/html_src_files/inspect_source_fool.com_premium.xml"),
                         "html.parser")

    LOG.info(get_first_update_title_and_ticker(soup))
