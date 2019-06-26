import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
f = open(os.path.join(__location__, "account.txt"), "r")
lines = f.readlines()
username = lines[0]
password = lines[1]
f.close()

configuration = {
    'username': username,
    'password': password,
    'top_links': {
        'S&P 500': 'http://www.barchart.com/stocks/sp500.php',
        'SectorMovement': 'http://stockcharts.com/freecharts/sectorsummary.html#&S=PD&O=4',
        'Zacks': 'https://www.zacks.com'
    }
}
