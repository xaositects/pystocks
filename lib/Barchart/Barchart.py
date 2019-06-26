import requests
from bs4 import BeautifulSoup
from mod_python import apache
import sys

class Barchart:
    def __init__(self):
        pass

    @staticmethod
    def get_opinion_page(sym):
        try:
            response = requests.get('https://www.barchart.com/stocks/quotes/' + sym + '/analyst-ratings')
            return response.content
        except:
            apache.log_error('%s' % sys.exc_info()[0], apache.APLOG_ERR)

    def get_current_opinion(self, sym):
        soup = BeautifulSoup(self.get_opinion_page(sym), 'html.parser')
        ana_box = soup.find('span', string='Current')
        cur_box = 'No Rating'
        if ana_box is not None:
            if ana_box.find_parent('div') is not None:
                if ana_box.find_parent('div').find_parent() is not None:
                    cur_box = ana_box.find_parent('div').find_parent()
        if cur_box is not None:
            return str(cur_box)
        else:
            return 'No Rating'
