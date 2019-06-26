import sys
import urlparse
from mod_python import apache
sys.path.append('/home/rmiller/Projects/pystocks/lib')
PyStocks = apache.import_module('/home/rmiller/Projects/pystocks/lib/PyStocks/PyStocks.py')
BarChart = apache.import_module('/home/rmiller/Projects/pystocks/lib/Barchart/Barchart.py')


def index(req):
    p = PyStocks.PyStocks()
    return p.ui()


def get_current_opinion(req,sym):
    bc = BarChart.Barchart()
    txt = bc.get_current_opinion(sym)
    apache.log_error('reg = %s' % txt, apache.APLOG_ERR)
    req.content_type = "text/plain"
    req.write(txt)


