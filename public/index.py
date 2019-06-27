import sys
import urlparse
from mod_python import apache
sys.path.append('/home/rmiller/Projects/pystocks/lib')
sys.path.append('/home/rmiller/.local/lib/python2.7/site-packages')
PyStocks = apache.import_module('/home/rmiller/Projects/pystocks/lib/PyStocks/PyStocks.py')
BarChart = apache.import_module('/home/rmiller/Projects/pystocks/lib/Barchart/Barchart.py')
StockCharts = apache.import_module('/home/rmiller/Projects/pystocks/lib/Stockcharts/Stockcharts.py')


def index(req):
    p = PyStocks.PyStocks()
    return p.ui()


def get_current_opinion(req,sym):
    bc = BarChart.Barchart()
    txt = bc.get_current_opinion(sym)
    req.content_type = "text/plain"
    req.write(txt)


def get_sector_perf_chart(req):
    bc = BarChart.Barchart()
    txt = bc.get_sector_perf_chart()
    req.content_type = "text/plain"
    req.write(txt)

