import json
import sys
import random
from mod_python import apache

sys.path.append('/home/rmiller/Projects/pystocks/lib')
from jinja2 import Environment, FileSystemLoader
# Robinhood = apache.import_module('/home/rmiller/Projects/pystocks/lib/Robinhood/Robinhood.py')
# endpoints = apache.import_module('/home/rmiller/Projects/pystocks/lib/Robinhood/endpoints.py')
from Robinhood import Robinhood
from Robinhood import endpoints

pystockconfig = apache.import_module('/home/rmiller/Projects/pystocks/lib/pystockconfig/pystockconfig.py')
BarChart = apache.import_module('/home/rmiller/Projects/pystocks/lib/Barchart/Barchart.py')


class PyStocks:
    tpl_path = '/home/rmiller/Projects/pystocks/templates'
    ui_tpl = 'html.tpl'
    top_links_tpl = 'top_links.tpl'
    portfolio_tpl = 'portfolio.tpl'

    def __init__(self):
        self.config = pystockconfig.configuration
        self.r = Robinhood()
        self.r.login(username=self.config['username'], password=self.config['password'])
        self.ev = 0
        self.file_loader = FileSystemLoader(self.tpl_path)
        self.env = Environment(loader=self.file_loader)

    def ui(self):
        template = self.env.get_template(self.ui_tpl)
        output = template.render(top_links=self.get_top_links(), portfolio=self.get_portfolio())
        return output

    def get_top_links(self):
        template = self.env.get_template(self.top_links_tpl)
        output = template.render(links=self.config['top_links'])
        return output

    @staticmethod
    def get_pct_change(abp, ltp):
        pc = 0
        if float(abp) > 0:
            pc = ((float(ltp) - float(abp)) / float(abp)) * 100
        return float(pc)

    def get_portfolio(self):
        self.ev = self.r.equity()
        db = endpoints.instruments()
        sops = {}
        for sop in self.r.positions()['results']:
            sym = self.get_symbol_from_instrument_url(self.r, sop['instrument'], db)
            try:
                if sym:
                    sops.update({sym: dict(symbol=sym, position=sop)})
            except:
                apache.log_error('%s is invalid' % sym, apache.APLOG_ERR)
                sops.update({sym: 'symbol ' + sym + ' is invalid'})
        sos = {}
        sectors = {}
        sector_colors = {}
        for so in self.r.securities_owned()['results']:
            sym = self.get_symbol_from_instrument_url(self.r, so['instrument'], db)
            if sym in sops.keys():
                pos = sops[sym]
            else:
                apache.log_error('key: %s is invalid' % sym, apache.APLOG_ERR)
                pos = sym
            news = self.r.get_news(sym)
            quote = self.r.get_quote(sym)
            pct_change = self.get_pct_change(pos['position']['average_buy_price'], quote['last_trade_price'])
            fundamentals = self.r.get_fundamentals(sym)
            sector_colors[fundamentals["sector"]] = 'rgb(' + str(random.randint(1, 255)) + ',' + str(random.randint(1, 255)) + ',' + str(random.randint(1, 255)) + ')'
            if fundamentals["sector"] in sectors.keys():
                sectors[fundamentals["sector"]] += 1
            else:
                sectors[fundamentals["sector"]] = 1
            sos.update({sym: dict(symbol=sym, data=quote, fundamentals=fundamentals, position=pos['position'],
                                  pct_change=pct_change, news=news, opinion='None')})
        template = self.env.get_template(self.portfolio_tpl)
        output = template.render(portfolio=sos, syms=json.dumps({k: k for k in sos.keys()}), equity=self.ev,
                                 sector_counts=sectors.values(), sectors=json.dumps(sectors.keys()),
                                 sector_colors=json.dumps(sector_colors.values()))
        return output

    @staticmethod
    def fetch_json_by_url(rb_client, url):
        return rb_client.session.get(url).json()

    def get_symbol_from_instrument_url(self, rb_client, url, db):
        instrument = {}
        if url in db:
            instrument = db[url]
        else:
            dburl = self.fetch_json_by_url(rb_client, url)
            instrument = dburl
        return instrument['symbol']
