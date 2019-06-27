
<div class="row">
    <div class="col s2 l1">Equity</div>
    <div class="col s8 l5">Sector Distribution</div>
    <div class="col s8 l6">Sector Performance</div>
</div>
<div class="row">
    <div class="col s2 l1">{{"$%.2f"|format(equity | float)}}</div>
    <div class="col s8 l6"><canvas id="sec_dist" width="400" height="400"></canvas></div>
    <div class="col s8 l6"><div id="sec_perf"></div></div>
</div>
<div class="row">
<div class="col s8 l2">Symbol/Last Price</div>
<div class="col s2 l1">Opinion</div>
<div class="col s12 l1">Purchase Price / Gain/Loss%</div>
<div class="col s4 l1">
    Vol.
</div>
<div class="col s4 l1">Avg. Daily Vol.</div>
<div class="col s4 l1">
    Chg. / Chg. %
</div>
<div class="col s12 l1">
    Chg. from 50/200 Day MA
</div>
<div class="col s12 l4">
    News
</div>

</div>
<div class="divider"></div>
        {% for key, value in portfolio.items() %}
<div class="row">
{% if value %}
<div class="col s8 l2">{{ value.symbol }} / {{ "$%.2f"|format(value.data.last_trade_price | float) }} <br/>{{value.fundamentals.sector}}
</div>

<div class="col s2 l1" id="{{value.symbol}}_opinion">Loading...
</div>
<div class="col s12 l1">{{ "$%.2f"|format(value.position.average_buy_price|float) }} / <span
        class="{% if value.pct_change | float > 0 %} green-text {% endif %}{% if value.pct_change | float < 0 %} red-text {% endif %}">{{ "%.2f"|format(value.pct_change | float) }}%</span>
</div>
<div class="col s4 l1">
    {{ value.fundamentals.volume | float | round }}
</div>
<div class="col s4 l1"> {{ value.fundamentals.average_volume | float | round }}</div>
<div class="col s4 l1">
    <span class="">{{ ((value.data.previous_close | float) - (value.data.last_trade_price | float)) }}</span>
</div>
<div class="col s12 l1">
    <span class="">&nbsp;</span>
    / <span
        class="">&nbsp;</span>
</div>
<div class="col s12 l4">
    <ul class="collection">
        {% for val in value.news.results %}
        <li class="collection-item"><a href="{{ val.url }}" target="new">{{ val.title }}</a></li>
        {% endfor %}
    </ul>
</div>
{% endif %}
</div>
<div class="divider"></div>
        {% endfor %}
<script type="application/javascript">
$(document).ready(function () {
    BC.loadOpinions($.parseJSON('{{syms}}'));
    SC.loadSectorPerformanceChart();
});
</script>
<script>
var data = {
    "datasets":[{
        "data": {{sector_counts}},
        "backgroundColor": {{sector_colors}}
    }],
    "labels": {{sectors}},

}
var ctx = document.getElementById('sec_dist').getContext('2d');
var sectorDistChart = new Chart(ctx, {
    type: 'pie',
    data: data
});
</script>

        <!--
        data: {'symbol': u'ACB', 'data': {u'previous_close': u'7.480000', u'has_traded': True, u'last_trade_price': u'7.450100', u'last_extended_hours_trade_price': None, u'adjusted_previous_close': u'7.480000', u'last_trade_price_source': u'nls', u'updated_at': u'2019-06-20T19:46:28Z', u'ask_price': u'7.440000', u'instrument': u'https://api.robinhood.com/instruments/71d81e7d-783c-4b8c-b574-ee50fcc4ce3a/', u'symbol': u'ACB', u'trading_halted': False, u'ask_size': 26400, u'bid_price': u'7.430000', u'previous_close_date': u'2019-06-19', u'bid_size': 26900}}
        fundamentals: {u'sector': u'Health Technology', u'year_founded': 2006, u'float': u'975173000.000000', u'high': u'7.620000', u'average_volume_2_weeks': u'9006502.100000', u'dividend_yield': u'0.000000', u'open': u'7.540000', u'headquarters_state': u'Alberta', u'instrument': u'https://api.robinhood.com/instruments/71d81e7d-783c-4b8c-b574-ee50fcc4ce3a/', u'pe_ratio': None, u'high_52_weeks': u'12.525000', u'low': u'7.390000', u'low_52_weeks': u'4.047800', u'headquarters_city': u'Edmonton', u'market_cap': u'7590141100.000000', u'description': u'Aurora Cannabis, Inc. is a Canada-based company, which is engaged in the production and distribution of medical cannabis. It also produces and sells indoor cultivation systems and hemp related food products. The company was founded by Terry Booth and Steve Dobler on December 21, 2006 and is headquartered in Edmonton, Canada.', u'num_employees': 967, u'ceo': u'Terry Booth', u'volume': u'8852455.000000', u'shares_outstanding': u'1014724748.000000', u'industry': u'Pharmaceuticals Other', u'average_volume': u'16346992.408000', u'pb_ratio': u'2.311100'}
        positions: {u'shares_held_for_stock_grants': u'0.0000', u'account': u'https://api.robinhood.com/accounts/5QZ82012/', u'pending_average_buy_price': u'6.3000', u'shares_held_for_options_events': u'0.0000', u'intraday_average_buy_price': u'0.0000', u'url': u'https://api.robinhood.com/positions/5QZ82012/e39605bf-9789-41f5-8b50-9bd38fec8f17/', u'shares_held_for_options_collateral': u'0.0000', u'created_at': u'2016-09-14T17:49:51.167722Z', u'updated_at': u'2019-06-05T14:15:09.239521Z', u'shares_held_for_buys': u'0.0000', u'average_buy_price': u'6.3000', u'instrument': u'https://api.robinhood.com/instruments/e39605bf-9789-41f5-8b50-9bd38fec8f17/', u'intraday_quantity': u'0.0000', u'shares_held_for_sells': u'0.0000', u'shares_pending_from_options_events': u'0.0000', u'quantity': u'2.0000'}
        news: {u'relay_url': u'https://news.robinhood.com/8750a233-c362-34dc-8eea-04c5bdb7b4fe/', u'uuid': u'8750a233-c362-34dc-8eea-04c5bdb7b4fe', u'author': u'', u'url': u'https://finance.yahoo.com/news/agilent-announces-receipt-fda-approval-212109130.html', u'title': u'Agilent Announces Receipt of FDA Approval for pharmDX Assay', u'updated_at': u'2019-06-18T23:03:29.891434Z', u'num_clicks': 80, u'summary': u'', u'currency_id': u'None', u'instrument': u'https://api.robinhood.com/instruments/2095bd69-d441-4da8-a014-5af9bcbf5394/', u'published_at': u'2019-06-14T22:21:00Z', u'related_instruments': [u'2095bd69-d441-4da8-a014-5af9bcbf5394'], u'preview_image_url': u'https://images.robinhood.com/rPYm8sKif18KrUOHL8_Vhd3atag/aHR0cHM6Ly9zLnlpbWcuY29tL255L2FwaS9yZXMvMS4yL3FwNzVaQXR3cVdkeFRZTmZjbkhOcXctLS9ZWEJ3YVdROWFHbG5hR3hoYm1SbGNqdDNQVEV5TnpBN2FEMDRNREEtL2h0dHBzOi8vcy55aW1nLmNvbS91dS9hcGkvcmVzLzEuMi9FZFAuRmJpNzhWcHRreGVjNnFiQl9nLS1-Qi9hRDAwTURBN2R6MDJNelU3YzIwOU1UdGhjSEJwWkQxNWRHRmphSGx2YmctLS9odHRwczovL21lZGlhLnplbmZzLmNvbS9lbi11cy96YWNrcy5jb20vMTM4MTAyMzg5OTRjZDQ0Y2MxMDk5N2JmY2QyNzExNjg', u'api_source': u'yahoo_finance', u'source': u'Yahoo Finance'}
        -->
