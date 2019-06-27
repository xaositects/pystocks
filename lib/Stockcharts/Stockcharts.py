import requests
from bs4 import BeautifulSoup
from mod_python import apache
import sys


class Stockcharts:
    def __init__(self):
        self.sector_perf_chart_url = 'https://stockcharts.com/freecharts/sectorsummary.html?O=4'
        self.sector_perf_chart_container = 'pagecontents'

    def get_sector_perf_chart_page(self):
        try:

            user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            headers = {'User-Agent': user_agent}
            response = requests.get(self.sector_perf_chart_url,headers=headers)
            html = response.content
            apache.log_error('%s' % html, apache.APLOG_ERR)
            return str(html)
        except:
            apache.log_error('%s' % sys.exc_info()[0], apache.APLOG_ERR)


    def get_sector_perf_chart(self):
        html = self.get_sector_perf_chart_page()
        apache.log_error('%s' % html, apache.APLOG_ERR)
        soup = BeautifulSoup(html, 'html.parser')
        box = soup.find('div', id=self.sector_perf_chart_container)
        if box is not None:
            return str(box)
        else:
            return str(html)
