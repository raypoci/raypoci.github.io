import dash
import dash_table
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import pandas as pd
import ast
import functools
import multiprocessing as mp
import copy
meta_tags=[
    # A description of the app, used by e.g.
    # search engines when displaying search results.
    {
        'name': 'description',
        'content': 'My description'
    },
    # A tag that tells Internet Explorer (IE)
    # to use the latest renderer version available
    # to that browser (e.g. Edge)
    {
        'http-equiv': 'X-UA-Compatible',
        'content': 'IE=edge'
    },
    # A tag that tells the browser not to scale
    # desktop widths to fit mobile screens.
    # Sets the width of the viewport (browser)
    # to the width of the device, and the zoom level
    # (initial scale) to 1.
    #
    # Necessary for "true" mobile support.
    {
      'name': 'viewport',
      'content': 'width=device-width, initial-scale=1.0'
    }
]

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets, suppress_callback_exceptions=True,meta_tags=meta_tags)
app.title="STOCK DASHBOARD"
server = app.server
today = datetime.today()

MAX_CORES = mp.cpu_count()

about_me = "I am a strong programmer, skilled in data analytics, with knowledge in data storage structures, data mining " \
           "and data cleansing. A recent graduate from Boston University, with proficient knowledge in statistics, " \
           "mathematics, and programming. My focus is on solving problems through efficient computing and visualizing" \
           " data through beautiful design. I am also a quick learner and able problem solver with excellent work ethic, " \
           "communication and time management skills, able to work well in groups as well as independently."


ALPHA_VANTAGE_KEY = ""
FINNHUB_KEY = ''
RAPID_API_KEY_SUMMARY = ""
RAPID_API_KEY= ""

navbar_color = "#212529"
now_plot = "#e9ecef"
daily_plot = "#999999"
daily_plot =navbar_color
eps_plot = "#999999"
eps_plot =navbar_color
rev_plot = "#999999"
rev_plot = navbar_color
historic_plot = "#e9ecef"
news_plot = "#e9ecef"
about_plot = "#999999"
about_plot = navbar_color

github_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/github-logo.jpg?raw=true"
linkedin_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/linkedin-logo.jpg?raw=true"
email_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/@email.jpg?raw=true"
website_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/rp-website-logo.png?raw=true"
linkedin_site = "https://www.linkedin.com/in/ray-poci/"
github_site = "https://github.com/raypoci/raypoci.github.io"
website_url = "https://raypoci.herokuapp.com/"
email_url = "mailto:raypoci18@gmail.com"
PLOTLY_LOGO = website_logo

FINANCIALS_OPT = {
    'overview': "OVERVIEW",
    "income": "INCOME_STATEMENT",
    "balance": "BALANCE_SHEET",
    "cash_flow": "CASH_FLOW",
}


REQS={}

global TICKERS
TICKERS = pd.read_csv("assets/Tickers.csv")
del TICKERS['Unnamed: 0']

def get_request(args,REQUESTS):
    url = args[0]
    querystring = args[1]
    headers = args[2]
    id = args[3]
    if querystring is not None:
        req = requests.request("GET", url, headers=headers, params=querystring).json()
    else:
        req = requests.request("GET", url, headers=headers,).json()
    REQUESTS[id]=req

def worker(input_queue,REQUESTS):
    while True:
        url = input_queue.get()
        if url is None:
            break
        get_request(url,REQUESTS)

def get_request_summary(args,REQUESTS):
    url = args[0]
    querystring = args[1]
    headers = args[2]
    if querystring is not None:
        req = requests.request("GET", url, headers=headers, params=querystring).json()
    else:
        req = requests.request("GET", url, headers=headers,).json()
    try:
        REQUESTS[querystring["scrIds"]]=req

    except :
        REQUESTS['summary']=req

def worker_summary(input_queue,REQUESTS):
    while True:
        url = input_queue.get()
        if url is None:
            break
        get_request_summary(url,REQUESTS)


search_bar = dbc.Row(
    [
        dbc.Col([
            dbc.Input(id='tick_search', type="search", placeholder="Enter symbol for a stock", list="list-of-options",
                      autoComplete=True, ),
            html.Datalist(id='list-of-options', children=[
                html.Option(TICKERS[option], value=option)
                for option in TICKERS.columns
            ])
        ]),
        dbc.Col(
            dbc.Button("Search", id="button1", color="dark", className="ml-2", n_clicks=0,active=True),
            width="auto",
        ),
    ],
    no_gutters=True,
    className="ml-auto mr-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("Stock Dashboard Project", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            ),
            href="/",
        ),
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
    ],
    color="dark",
    dark=True,
)

footer_style = {"text-decoration": "none","color":"darkblue"}
footer = html.Div(dbc.Container(dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.P("About Me:", style={"font-weight":"bold"}),
                    html.P(about_me),
                    html.Br(),
                    html.Br(),
                ],width=6),
                dbc.Col([
                    html.Br(),
                    html.A([

                        html.Span([
                            html.Img(src=linkedin_logo, style={"height":"30px","display":"inline"}),
                            html.P("Visit my LinkedIn",style={"display":"inline","color":"black"})],style={"display":"inline","white-space": "nowrap","overflow-x": "auto"}),

                    ],href=linkedin_site, style=footer_style),
                    html.Br(),
                    html.Br(),
                    html.A([

                        html.Span([
                            html.Img(
                                src=github_logo,
                                style={"height": "30px", "display": "inline"}),
                            html.P("Visit my Github", style={"display": "inline","color":"black"})],
                            style={"display": "inline", "white-space": "nowrap", "overflow-x": "auto"}),

                    ], href=github_site, style=footer_style),
                    html.Br(),
                    html.Br(),
                    html.A([

                        html.Span([
                            html.Img(
                                src=website_logo,
                                style={"height": "30px", "display": "inline"}),
                            html.P("Visit my website", style={"display": "inline","color":"black"})],
                            style={"display": "inline", "white-space": "nowrap", "overflow-x": "auto"}),

                    ], href=website_url, style=footer_style),
                    html.Br(),
                    html.Br(),
                    html.A([

                        html.Span([
                            html.Img(
                                src=email_logo,
                                style={"height": "30px", "display": "inline"}),
                            html.P("Email me", style={"display": "inline","color":"black"})],
                            style={"display": "inline", "white-space": "nowrap", "overflow-x": "auto"}),

                    ], href=email_url, style=footer_style)


                ],width=4)
            ],justify="center",), style={"background-color":"#20c997", "color":"black", },fluid=True),style={"background-color":"#20c997", "color":"black", })

def generate_table(df, name, max_rows=20):
    df.drop_duplicates(subset="headline", keep="first", inplace=True)

    return html.Div(dbc.Table(
                    # Header
                    [html.Tr([html.Th(html.H3("News related to {0}".format(name)), style={'text-align': 'center',"color":"black"})])]
                    +
                    # Body
                    [
                        html.Tr(
                            [
                                html.Td(
                                    html.A(
                                    [

                                        dbc.Row([
                                        dbc.Col(html.Img(src=df.iloc[i]["image"],height="50px"),width=2),

                                        dbc.Col([df.iloc[i]["headline"],
                                         html.Br(),

                                         html.P(
                                             [
                                                 dbc.Row(
                                                     [
                                                         dbc.Col([
                                                             "Posted on {0} by {1}".format(df.iloc[i]['datetime'],df.iloc[i]['source']),
                                                             ], )
                                                     ])
                                             ], style={"font-size": "x-small","color":"silver"})
                                         ])], style={"color":"silver"})
                                    ],
                                        href=df.iloc[i]["url"],
                                        target="_blank"
                                    )
                                )
                            ]
                        , style={"background-color":daily_plot,"color":"silver"} )
                        for i in range(min(len(df), max_rows))
                    ]
    ,bordered=True),style={"height": "400px", "color":"silver","overflowY": "scroll"})

def normalize_num(num):
    num = str(num)
    try:
        temp = ast.literal_eval(num)
        if type(temp).__name__ == "int":
            return "{:,}".format(temp)
        else:
            return '{:,}'.format((round(temp, 2)))

    except:
        return "-"

def plot_movers(df):
    return dash_table.DataTable(
        style_cell={'textAlign': 'left'},
        style_as_list_view=True,
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {
                    'filter_query': '{Change} > 0',
                    'column_id': 'Change'
                },
                'backgroundColor': '#669900',
                'color': 'black'
            },
            {
                'if': {
                    'filter_query': '{%Change} > 0',
                    'column_id': '%Change'
                },
                'backgroundColor': '#669900',
                'color': 'black'
            },
            {
                'if': {
                    'filter_query': '{Change} < 0',
                    'column_id': 'Change'
                },
                'backgroundColor': '#dc143c',
                'color': 'black'
            },
            {
                'if': {
                    'filter_query': '{%Change} <0',
                    'column_id': '%Change'
                },
                'backgroundColor': '#dc143c',
                'color': 'black'
            },
            {
                'if': {
                    'column_id': 'Symbol'
                },
                "font-weight": "bold"
            },
            {
                'if': {
                    'column_id': 'Last'
                },
                "font-weight": "darkblue"
            },
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },

        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
    )

def get_summary(req):

    response = req
    temp = copy.deepcopy(response["marketSummaryAndSparkResponse"]['result'])
    temp = temp[0:3] + [temp[7]] + [temp[9]] + [temp[11]]
    lst = []
    for stock in temp:

        tmp= {}
        if str(stock["symbol"]) == "BTC-USD":
            tmp["shortName"] = "BTC"
        else:
            tmp["shortName"] = stock["shortName"]

        tmp["fullExchangeName"]=stock["fullExchangeName"]
        tmp["symbol"] = stock["symbol"]
        tmp["regularMarketTime"] = stock["regularMarketTime"]["fmt"]
        tmp["regularMarketPreviousClose"] = stock["spark"]["previousClose"]
        try:
            tmp["close"] = float(stock["spark"]["close"][-1])
        except :
            tmp["close"] = float(stock["spark"]["close"][-2])
        tmp["change"] = str(round((float(tmp["close"])-float(tmp["regularMarketPreviousClose"])),2))
        tmp["prc_change"] = str(round(((float(tmp["change"])*100)/float(tmp["close"])),2))
        tmp["sign"] = "+" if float(tmp["change"])>0 else ""
        lst.append(tmp)

    df_market = pd.DataFrame(lst)

    snp_date = temp[0]['spark']['timestamp']
    snp_close = temp[0]['spark']['close']
    snp_dct = {"date":snp_date,"close":snp_close}
    df_snp = pd.DataFrame(snp_dct)
    df_snp.date = df_snp["date"].apply(lambda x: datetime.fromtimestamp(x))

    dji_date = temp[1]['spark']['timestamp']
    dji_close = temp[1]['spark']['close']
    dji_dct = {"date": dji_date, "close": dji_close}
    df_dji = pd.DataFrame(dji_dct)
    df_dji.date = df_dji["date"].apply(lambda x: datetime.fromtimestamp(x))

    nasdaq_date = temp[2]['spark']['timestamp']
    nasdaq_close = temp[2]['spark']['close']
    nasdaq_dct = {"date": nasdaq_date, "close": nasdaq_close}
    df_nasdaq = pd.DataFrame(nasdaq_dct)
    df_nasdaq.date = df_nasdaq["date"].apply(lambda x: datetime.fromtimestamp(x))

    return df_market, df_snp, df_dji, df_nasdaq

def get_movers(gainers, losers, active):


    df_gainers = pd.DataFrame(gainers['finance']['result'][0]['quotes'])
    df_gainers['Symbol'] = df_gainers["symbol"]
    df_gainers["Last"] = df_gainers["regularMarketPrice"].apply(lambda x : normalize_num(x))
    df_gainers["Change"] = df_gainers["regularMarketChange"].apply(lambda x: normalize_num(x))
    df_gainers["%Change"] = df_gainers["regularMarketChangePercent"].apply(lambda x: normalize_num(x))
    df_gainers = df_gainers[['Symbol','Last','Change','%Change']]

    df_losers = pd.DataFrame(losers['finance']['result'][0]['quotes'])
    df_losers['Symbol'] = df_losers["symbol"]
    df_losers["Last"] = df_losers["regularMarketPrice"].apply(lambda x : normalize_num(x))
    df_losers["Change"] = df_losers["regularMarketChange"].apply(lambda x: normalize_num(x))
    df_losers["%Change"] = df_losers["regularMarketChangePercent"].apply(lambda x: normalize_num(x))
    df_losers = df_losers[['Symbol', 'Last', 'Change', '%Change']]


    df_active = pd.DataFrame(active['finance']['result'][0]['quotes'])
    df_active['Symbol'] = df_active["symbol"]
    df_active["Last"] = df_active["regularMarketPrice"].apply(lambda x : normalize_num(x))
    df_active["Change"] = df_active["regularMarketChange"].apply(lambda x: normalize_num(x))
    df_active["%Change"] = df_active["regularMarketChangePercent"].apply(lambda x: normalize_num(x))
    df_active = df_active[['Symbol', 'Last', 'Change', '%Change']]


    return df_gainers, df_losers, df_active

def get_intraday_prices(req):

    response = req['chart']['result'][0]
    date = response['timestamp']
    date_df = pd.DataFrame(date, columns=["date"])
    date_df.date = date_df["date"].apply(lambda x: datetime.fromtimestamp(x))
    rest_data = response['indicators']['quote'][0]
    rest_df = pd.DataFrame(rest_data)[["high", "close", "low", "open"]]
    df = pd.concat([date_df, rest_df], axis=1).set_index("date",drop=False)
    return df

def get_earnings(req):
    earnings = req['earningsChart']['quarterly']
    for item in earnings:
        item['actual']=item['actual']['raw']
        item['estimate'] = item['estimate']['raw']
    df_e = pd.DataFrame(earnings)

    financials =req['financialsChart']['yearly']
    for item in financials:
        item['revenue']=item['revenue']['raw']
        item['earnings'] = item['earnings']['raw']

    df_f = pd.DataFrame(financials)
    return df_e, df_f

def get_about(response):

    temp = response["assetProfile"]
    empl = temp["companyOfficers"]
    for emp in empl:
        try:
            del emp['exercisedValue']
        except :
            pass
        try:
            del emp['unexercisedValue']
        except:
            pass
        try:
            del emp["totalPay"]
        except:
            pass
    df_empl = pd.DataFrame(empl)[['name','title']]

    del temp["companyOfficers"]
    df = pd.DataFrame(temp,index=[0])[['zip',
       'longBusinessSummary', 'city', 'phone', 'state',
       'country', 'address1', 'industry']]

    return df, df_empl

def display_now(df_more,finhub_req):


    df_profile = pd.DataFrame(finhub_req, index=[0])

    boolean = df_profile.empty
    if not boolean:
        logo = df_profile['logo'].values[0]
        url = df_profile['weburl'].values[0]
        sector = df_profile['finnhubIndustry'].values[0]
    else:
        logo = "https://github.com/raypoci/raypoci.github.io/blob/master/static/images/no_logo.png?raw=true"
        url = "#"
        sector = "-"

    try:
        symbol = df_more['symbol'].values[0]
    except :
        symbol = "-"
    try:
        name = df_more['displayName'].values[0]
    except :
        name = df_more['shortName'].values[0]

    try:
        exchange = df_more['fullExchangeName'].values[0]
    except :
        exchange = "-"
    try:
        curr = df_more['currency'].values[0]
    except:
        curr = "-"
    try:
        market_open = normalize_num(df_more["regularMarketOpen"].values[0])
    except :
        market_open="-"

    try:
        market_cap = normalize_num(df_more['marketCap'].values[0])
    except:
        market_cap= "-"

    try:
        price = normalize_num(df_more['regularMarketPrice'].values[0])
    except:
        price = "-"

    try:
        change = normalize_num(df_more['regularMarketChange'].values[0])
    except:
        change = "-"


    try:
        prc_change = normalize_num(df_more['regularMarketChangePercent'].values[0])
    except:
        prc_change= "-"

    if float(change) > 0:
        color = "green"
        sign = "+"
    elif float(change) < 0:
        color = "red"
        sign = ""
    else:
        color = "black"
        sign = ""
    try:
        low = normalize_num(df_more['regularMarketDayLow'].values[0])
    except:
        low=""
    try:
        high = normalize_num(df_more['regularMarketDayHigh'].values[0])
    except:
        high = ""
    try:
        prev_close = normalize_num(df_more['regularMarketPreviousClose'].values[0])
    except :
        prev_close="-"

    try:
        low_52 = normalize_num(df_more['fiftyTwoWeekLow'].values[0])
    except:
        low_52=""
    try:
        high_52 = normalize_num(df_more['fiftyTwoWeekHigh'].values[0])
    except:
        high_52 = ""

    try:
        today_vol = normalize_num(df_more['regularMarketVolume'].values[0])
    except:
        today_vol = "-"

    try:
        forward_eps = normalize_num(df_more['epsForward'].values[0])
    except:
        forward_eps = "-"

    try:
        trailing_pe = normalize_num(df_more['trailingPE'].values[0])
    except:
        trailing_pe = "-"
    try:
        shares_out = normalize_num(df_more['sharesOutstanding'].values[0])
    except :
        shares_out = "-"
    try:
        trailing_eps = normalize_num(df_more['epsTrailingTwelveMonths'].values[0])
    except:
        trailing_eps = "-"

    try:
        vol_10d = normalize_num(df_more['averageDailyVolume10Day'].values[0])
    except:
        vol_10d = "-"
    try:
        vol_3M = normalize_num(df_more['averageDailyVolume3Month'].values[0])
    except:
        vol_3M = "-"

    try:
        price_book = normalize_num(df_more['priceToBook'].values[0])
    except:
        price_book = "-"
    try:
        book_value = normalize_num(df_more['bookValue'].values[0])
    except:
        book_value = "-"
    try:
        forward_pe = normalize_num(df_more['forwardPE'].values[0])
    except:
        forward_pe = "-"

    lay = dbc.Container(dbc.Jumbotron(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    html.A(html.Img(src=logo, height="30px"), href=url
                                           ),
                                    html.H3(name)
                                ]),
                            dbc.Row(html.P("{0} : {1}".format(exchange, symbol))),
                            dbc.Row(
                                [
                                    html.H4(
                                        [
                                            price,
                                            html.Span(curr, style={'font-size': 'small'}),
                                            html.Span('               {0}{1} ({2}%)'.format(sign, change, prc_change),
                                                      style={ 'color': color})
                                        ]),
                                ]),
                        ]),
                    dbc.Col([

                        dbc.Row(
                            [
                                dbc.Col("Exchange:    {0}".format(exchange)),
                                dbc.Col("52 Week Range: {0} - {1}".format(low_52, high_52)),
                                dbc.Col("Trailing P/E:   {0}".format(trailing_pe))

                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Sector:   {0}".format(sector)),
                                dbc.Col("Today's Volume:     {0}".format(today_vol)),
                                dbc.Col("Forward P/E:   {0}".format(forward_pe))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Market Open:  {0}".format(market_open)),
                                dbc.Col("Avg 10D Volume :  {0}".format(vol_10d)),
                                dbc.Col("Trailing EPS:   {0}".format(trailing_eps))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Last Close: {0}".format(prev_close)),
                                dbc.Col("Avg 3M Volume: {0}".format(vol_3M)),
                                dbc.Col("Forward EPS:   {0}".format(forward_eps))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Today's Range:  {0} - {1}".format(low, high)),
                                dbc.Col("Market Cap: {0}".format(market_cap)),
                                dbc.Col("P/B:   {0}".format(price_book))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Prev Close:   {0}".format(prev_close)),
                                dbc.Col("Free Float :    {0}".format(shares_out)),
                                dbc.Col("Book Value:   {0}".format(book_value))
                            ])

                    ], width=8)
                ],style={"background-color":now_plot}),
        ],style={"background-color":now_plot,"height": "248px",}), style={"height": "248px","background-color":now_plot},fluid=True)

    return lay

def display_intra_chart(df, name):
    trace_bar = go.Ohlc(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'],
                        visible=False,
                        showlegend=False,
                        name = "Bar")

    trace_candle = go.Candlestick(x=df.index,
                                  open=df['open'],
                                  high=df['high'],
                                  low=df['low'],
                                  close=df['close'],
                                  visible=False,
                                  showlegend=False,
                                  name = "Candlestick")

    trace_line = go.Scatter(x=df.date, y=df['close'], showlegend=False,line=dict(color="silver"),connectgaps=True, name="Line", line_shape='spline')

    data = [trace_bar, trace_candle, trace_line]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [False, False, True]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False]}],
                    label='Candle',
                    method='update'
                ),
                dict(
                    args=[{'visible': [True, False, False]}],
                    label='Bar',
                    method='update'
                ),
            ]),
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0,
            xanchor='left',
            y=1.05,
            yanchor='top'
        ),
    ])
    title = "Daily Chart for {0}".format(name)
    layout = go.Layout(

        title={
            'text': title,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',},
        updatemenus=updatemenus,
        plot_bgcolor = "rgba(42, 42, 46, 1)",
        paper_bgcolor=daily_plot,
        autosize=True,
        xaxis=dict(rangeslider=dict(
            visible=False
        )),
        yaxis=dict(autorange=True)

    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        font_color="#20c997",
        font_family="Courier New",
        title_font_family="Times New Roman",
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    return dcc.Graph(figure=fig, style={"background-color":daily_plot,"color":"silver"})

def display_chart(df, name):
    trace_bar = go.Ohlc(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'],
                        visible=False,
                        showlegend=False)

    trace_candle = go.Candlestick(x=df.index,
                                  open=df['open'],
                                  high=df['high'],
                                  low=df['low'],
                                  close=df['close'],
                                  visible=False,
                                  showlegend=False)

    trace_line = go.Scatter(x=df.index, y=df['close'], showlegend=False, line=dict(color="#20c997"), line_shape='spline')

    data = [trace_bar, trace_candle, trace_line]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [False, False, True]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, True, False]}],
                    label='Candle',
                    method='update'
                ),
                dict(
                    args=[{'visible': [True, False, False]}],
                    label='Bar',
                    method='update'
                ),
            ]),
            direction='down',
            pad={'r': 10, 't': 10},
            showactive=True,
            x=0,
            xanchor='left',
            y=1.05,
            yanchor='top'
        ),
    ])

    layout = go.Layout(

        title={
            'text': "Chart of Historic Data for {0}".format(name),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',},
        updatemenus=updatemenus,
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=7, label="7d", step="day", stepmode="backward"),
                    dict(count=14, label="2w", step="day", stepmode="backward"),
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(step="all")
                ])),
            rangebreaks=[dict(bounds=[16, 9], pattern="hour"),
                         dict(bounds=["sat", "mon"]),
                         dict(values=["2020-12-25", "2020-01-01"])],

            rangeslider=dict(
                visible=True

        ),

        )

    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        font_family="Courier New",
        title_font_family="Times New Roman",
        plot_bgcolor = "rgba(42, 42, 46, 1)",
        paper_bgcolor=historic_plot,

    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    return dcc.Graph(figure=fig, style={"background-color":historic_plot})

def display_earnings(df_e, df_f, name):

    e_trace1 = go.Bar(x = df_e['date'], y=df_e['estimate'], name="Estimate")
    e_trace2 = go.Bar(x=df_e['date'], y=df_e['actual'], name="Actual")

    e_data = [e_trace1, e_trace2]
    fig1 = go.Figure(data=e_data)
    fig1.update_layout(
        font_color="silver",
        plot_bgcolor="lightsalmon",
        paper_bgcolor = eps_plot,
        barmode="group",
        font_family="Courier New",
        title_font_family="Times New Roman",
        title={
            'text': "EPS".format(name),
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}
    )
    fig1.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    fig1.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    graph1 =  dcc.Graph(figure=fig1, style={"background-color":eps_plot,"color":"silver"})

    f_trace1 = go.Bar(x=df_f['date'], y=df_f['revenue'], name="Revenue")
    f_trace2 = go.Bar(x=df_f['date'], y=df_f['earnings'], name="Earnings")

    f_data = [f_trace1, f_trace2]
    fig2 = go.Figure(data=f_data)
    fig2.update_layout(
        font_color="silver",
        plot_bgcolor="lightskyblue",
        paper_bgcolor=rev_plot,
        barmode="group",
        font_family="Courier New",
        title_font_family="Times New Roman",
        title={
            'text': "Revenue",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',}
    )
    fig2.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    fig2.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    graph2 = dcc.Graph(figure=fig2, style={"background-color":rev_plot,"color":"silver"},)
    lay = dbc.Row([
            dbc.Col(graph1,className="col-lg-6 col-md-12 col-sm-12 col-12"),
            dbc.Col(graph2,className="col-lg-6 col-md-12 col-sm-12 col-12")
        ],style={"background-color":eps_plot,"color":"silver"})

    return lay

def display_news(req, name):
    df = req
    df = pd.DataFrame(df)

    try:
        df['datetime'] = df['datetime'].apply(lambda x: datetime.fromtimestamp(x))
        df = df[['datetime', 'headline', 'source', 'summary', 'url', "image"]]
        return generate_table(df, name)
    except:
        return []

def display_about(df_about, df_empl, name, max_rows = 9):
    name = str(name)
    try:
        street = df_about['address1'].values[0]
    except:
        street = " "
    try:
        city = df_about['city'].values[0]
    except:
        city = " "
    try:
        state = df_about['state'].values[0]
    except:
        state = " "
    try:
        zip_code = df_about['zip'].values[0]
    except:
        zip_code = " "
    try:
        country = df_about['country'].values[0]
    except:
        country = " "
    try:
        phone = df_about['phone'].values[0]
    except:
        phone = " "
    try:
        sector = df_about['sector'].values[0]
    except:
        sector = " "
    try:
        industry = df_about['industry'].values[0]
    except:
        industry = " "
    try:
        description = df_about['longBusinessSummary'].values[0]
    except:
        description = " "
    lay = dbc.Container(dbc.Jumbotron([

    dbc.Row([
        dbc.Col([
            html.Hr(),
            dbc.Col([
            dbc.Row([
                html.H3(html.B("About {0}".format(name)))
            ]),
            dbc.Row("{0}, {1}, {2}, {3} ".format(street,city,state,zip_code)),
            dbc.Row("{0}".format(country)),
            dbc.Row("{0}".format(phone)),
            dbc.Row("{0}".format(industry)),
            html.Hr(),
            dbc.Row(html.H4(html.B("Key Executives")))]),
            html.Hr(),
            dbc.Row([
                dbc.Col(html.H6(html.B("NAME"),style={"color":"silver"} )),
                dbc.Col(html.H6(html.B("TITLE"),style={"color":"silver"}))
            ]),
            html.Hr(),
            html.Div([
                dbc.Row([
                    dbc.Col("{0}".format(df_empl.iloc[i]['name'])),
                    dbc.Col(html.B("{0}".format(df_empl.iloc[i]['title'])))
                ])
                for i in range(min(len(df_empl),max_rows))
            ]),
            html.Hr()
        ]),
        dbc.Col([
            html.Hr(),
            html.P(description),
            html.Hr()

        ], align="center")
    ], style={"background-color":about_plot,"color":"silver"},justify="between")],style={"background-color":about_plot,"color":"silver"}),fluid=True,style={"background-color":about_plot,"color":"silver"})

    return lay

def display_summary(df_snp, df_dji, df_nasdaq):
    trace_line_snp = go.Scatter(x=df_snp.date, y=df_snp['close'], showlegend=False, line=dict(color="#fd7e14"),name="S&P", line_shape='spline')
    trace_line_dji = go.Scatter(x=df_dji.date, y=df_dji['close'], showlegend=False, line=dict(color="red"),name="DJI", line_shape='spline')
    trace_line_nasdaq = go.Scatter(x=df_nasdaq.date, y=df_nasdaq['close'], showlegend=False, line=dict(color="blue"),name="NASDAQ", line_shape='spline')

    layout = go.Layout(

        title={
            'text': "S&P 500",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},

    )
    fig = go.Figure(data=trace_line_snp, layout=layout)
    fig.update_layout(
        font_family="Courier New",
        title_font_family="Times New Roman",
        plot_bgcolor = "rgba(42, 42, 46, 1)",
        paper_bgcolor=historic_plot,

    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True,showgrid=False, zeroline=False)

    g1 = dcc.Graph(figure=fig, style={"background-color":historic_plot},)

    fig2 = go.Figure(data=trace_line_dji, layout=layout)
    fig2.update_layout(
        title={
            'text': "Dow Jones Industrial",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
        },
        font_family="Courier New",
        title_font_family="Times New Roman",
        plot_bgcolor="rgba(42, 42, 46, 1)",
        paper_bgcolor=historic_plot,

    )
    fig2.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, showgrid=False, zeroline=False)
    fig2.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, showgrid=False, zeroline=False)

    g2 = dcc.Graph(figure=fig2, style={"background-color": historic_plot}, )

    fig3 = go.Figure(data=trace_line_nasdaq, layout=layout)
    fig3.update_layout(
        title={
            'text': "Nasdaq",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        font_family="Courier New",
        title_font_family="Times New Roman",
        plot_bgcolor="rgba(42, 42, 46, 1)",
        paper_bgcolor=historic_plot,

    )
    fig3.update_xaxes(showline=True, linewidth=2, linecolor='black', mirror=True, showgrid=False, zeroline=False)
    fig3.update_yaxes(showline=True, linewidth=2, linecolor='black', mirror=True, showgrid=False, zeroline=False)

    g3 = dcc.Graph(figure=fig3, style={"background-color": historic_plot}, )

    return dbc.Row([
        dbc.Col(g1,className="col-lg-4 col-md-4 col-sm-12 col-12"),
        dbc.Col(g2,className="col-lg-4 col-md-4 col-sm-12 col-12"),
        dbc.Col(g3,className="col-lg-4 col-md-4 col-sm-12 col-12")
    ],no_gutters=True,justify='around')

def make_home_page(df_market, df_snp, df_dji, df_nasdaq, df_gainers, df_losers, df_active):


    graph = display_summary(df_snp, df_dji, df_nasdaq)
    lay = html.Div([

        html.Div([
            dbc.Row([
                dbc.Col([

                    dbc.Card([
                        dbc.CardHeader(

                            [
                                html.Div([
                                html.P("{0}".format(df_market.iloc[i]["symbol"]), style={"color": "white",'display':'inline','float':'left'}),
                                html.P("{0}".format(normalize_num(df_market.iloc[i]["close"])),
                                        style={"color": "green",'display':'inline','float':'right'} if float(df_market.iloc[i]["prc_change"]) > 0 else {
                                            "color": "red",'display':'inline','float':'right'})], style={'overflow':'hidden'})
                            ],

                        ),
                        dbc.CardBody(

                            [

                                html.H5("{0}".format(df_market.iloc[i]["shortName"]), className="card-title",
                                        style={"color": "white"}),
                                html.H4(
                                    "{0}{1}  ({2})".format(df_market.iloc[i]["sign"], df_market.iloc[i]["change"],
                                                           df_market.iloc[i]["prc_change"]),
                                    className="card-text",
                                    style={"color": "green"} if float(df_market.iloc[i]["prc_change"]) > 0 else {
                                        "color": "red"}
                                ),
                            ]
                        ),
                    ], color="dark")

                ], className="col-lg-2 col-md-2 col-sm-4 col-6")
                for i in range(min(len(df_market), 6))
            ], no_gutters=True)
        ], style={"background-color": navbar_color}),

        html.Br(),
        html.H2("Today's Market Summary", style={"text-align": "center"}),


        dbc.Container(graph,fluid=True),

        dbc.Container([
            dbc.Row([
                dbc.Col([

                    html.H3("Today's Top Gainers", style={"text-align": 'center'}),
                    plot_movers(df_gainers)

                ], className="col-lg-3 col-md-3 col-sm-12 col-12"),
                dbc.Col([

                    html.H3("Today's Worse Losers", style={"text-align": 'center'}),
                    plot_movers(df_losers)

                ], className="col-lg-3 col-md-3 col-sm-12 col-12"),
                dbc.Col([

                    html.H3("Today's Most Active", style={"text-align": 'center'}),
                    plot_movers(df_active)

                ], className="col-lg-3 col-md-3 col-sm-12 col-12")
            ], justify="around")
        ], fluid=True),
        html.Br(),

    ],id="home-layout" )

    return lay

def make_home():
    REQS['summary'] = {
        'summary_url': "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-summary",
        'summary_query': {"region": "US"},
        'summary_header': {
            'x-rapidapi-key': RAPID_API_KEY_SUMMARY,
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        },
    }

    REQS['movers'] = {
        'day_gainers_url': "https://yahoo-finance-low-latency.p.rapidapi.com/ws/screeners/v1/finance/screener/predefined/saved",
        'most_actives_url': "https://yahoo-finance-low-latency.p.rapidapi.com/ws/screeners/v1/finance/screener/predefined/saved",
        'day_losers_url': "https://yahoo-finance-low-latency.p.rapidapi.com/ws/screeners/v1/finance/screener/predefined/saved",

        'day_gainers_query': {"scrIds": "day_gainers", "count": "6"},
        'most_actives_query': {"scrIds": "most_actives", "count": "6"},
        'day_losers_query': {"scrIds": "day_losers", "count": "6"},

        'day_gainers_header': {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
        },
        'most_actives_header': {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
        },
        'day_losers_header': {
            'x-rapidapi-key': RAPID_API_KEY,
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
        }

    }
    urls = [REQS['summary']['summary_url'], REQS['movers']['day_gainers_url'], REQS['movers']['most_actives_url'],
            REQS['movers']['day_losers_url']]

    query = [REQS['summary']['summary_query'], REQS['movers']['day_gainers_query'],
             REQS['movers']['most_actives_query'],
             REQS['movers']['day_losers_query']]

    headers = [REQS['summary']['summary_header'], REQS['movers']['day_gainers_header'],
               REQS['movers']['most_actives_header'],
               REQS['movers']['day_losers_header']]

    assert len(urls) == len(query)

    REQUESTS = mp.Manager().dict()
    arguments = zip(urls, query, headers)

    input_queue = mp.Queue()
    workers = []

    for i in range(min(4, MAX_CORES)):
        p = mp.Process(target=worker_summary, args=(input_queue, REQUESTS,))
        workers.append(p)
        p.start()
    for arg in arguments:
        input_queue.put(arg)

    for _ in workers:
        input_queue.put(None)

    for w in workers:
        w.join()

    summary_req = REQUESTS['summary']
    gainer_req = REQUESTS[REQS['movers']['day_gainers_query']["scrIds"]]
    losers_req = REQUESTS[REQS['movers']['day_losers_query']["scrIds"]]
    actives_req = REQUESTS[REQS['movers']['most_actives_query']["scrIds"]]

    df_market, df_snp, df_dji, df_nasdaq = get_summary(summary_req)
    df_gainers, df_losers, df_active = get_movers(gainer_req, losers_req, actives_req)

    home = make_home_page(df_market, df_snp, df_dji, df_nasdaq, df_gainers, df_losers, df_active)
    return home

home = make_home()
app.layout = html.Div([navbar, home, html.Div(id="search-output"), footer])

# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@functools.lru_cache()
@app.callback(
    [Output("search-output", "children"),Output("home-layout", "style")],
    [Input('button1', 'n_clicks')],
    [State("tick_search", "value")],
    prevent_initial_call=True

)
def search(n_clicks, value):
    if not n_clicks and not value:
        return [],{"display":"block"}
    else:
        try:

            today = datetime.today().date()
            last_month = today - timedelta(days=30)
            REQS['tick'] = {
                'chart_url': "https://yahoo-finance-low-latency.p.rapidapi.com/v8/finance/chart/{0}".format(value),
                'historic_url': "https://yahoo-finance-low-latency.p.rapidapi.com/v8/finance/chart/{0}".format(value),
                'profile_url': "https://yahoo-finance-low-latency.p.rapidapi.com/v11/finance/quoteSummary/{0}".format(value),
                'news_url': "https://finnhub.io/api/v1/company-news?symbol={0}&from={1}&to={2}&token={3}".format(value.upper(),
                                                                                                    last_month, today,
                                                                                                    FINNHUB_KEY),
                'quotes_url':"https://yahoo-finance-low-latency.p.rapidapi.com/v6/finance/quote",
                'finhub_url':"https://finnhub.io/api/v1/stock/profile2?symbol={0}&token={1}".format(value, FINNHUB_KEY),


                'chart_query': {"range": "1d", "interval": "1m"},
                'historic_query': {"range": "1y", "interval": "1d"},
                'profile_query': {"modules":"assetProfile,earnings"},
                'news_query': None,
                'quotes_query': {"symbols":value},
                'finhub_query':None,

                'chart_header':{
    'x-rapidapi-key': RAPID_API_KEY,
    'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
    },
                'historic_header': {
                    'x-rapidapi-key': RAPID_API_KEY,
                    'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"

                },
                'quotes_header': {
                    'x-rapidapi-key': RAPID_API_KEY,
                    'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
                },
                'news_header': {
        'Content-Type': 'application/json'
    },
                'profile_header': {
                    'x-rapidapi-key': RAPID_API_KEY,
                    'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com"
                },
                'finhub_header':  {
                'Content-Type': 'application/json'
            },
                'chart_id':'daily_chart',
                'historic_id':'historic_chart',
                'quotes_id':'quotes_chart',
                'news_id':'news_chart',
                'profile_id':'profile_chart',
                'finhub_id':'finhub_chart'
            }

            REQS['insights'] = {
                'insights_url': "https://yahoo-finance-low-latency.p.rapidapi.com/ws/insights/v1/finance/insights",
                'insights_query': {"symbol": value}
            }

            urls = [REQS['tick']['chart_url'],REQS['tick']['historic_url'],REQS['tick']['quotes_url'],
                    REQS['tick']['news_url'],REQS['tick']['profile_url'],REQS['tick']['finhub_url']]

            query = [REQS['tick']['chart_query'],REQS['tick']['historic_query'],REQS['tick']['quotes_query'],
                     REQS['tick']['news_query'],REQS['tick']['profile_query'], REQS['tick']['finhub_query']]

            headers = [REQS['tick']['chart_header'], REQS['tick']['historic_header'], REQS['tick']['quotes_header'],
                     REQS['tick']['news_header'], REQS['tick']['profile_header'],REQS['tick']['finhub_header']]

            ids = [REQS['tick']['chart_id'], REQS['tick']['historic_id'], REQS['tick']['quotes_id'],
                     REQS['tick']['news_id'], REQS['tick']['profile_id'],REQS['tick']['finhub_id']]

            assert len(urls)==len(query)
            REQUESTS = mp.Manager().dict()
            arguments = zip(urls, query,headers,ids)

            input_queue = mp.Queue()
            workers = []

            for i in range(min(MAX_CORES,6)):
                p = mp.Process(target=worker, args=(input_queue, REQUESTS,))
                workers.append(p)
                p.start()
            for arg in arguments:
                input_queue.put(arg)

            for _ in workers:
                input_queue.put(None)

            for w in workers:
                w.join()

            profile_req = REQUESTS[REQS['tick']['profile_id']]
            chart_req = REQUESTS[REQS['tick']['chart_id']]
            historic_req = REQUESTS[REQS['tick']['historic_id']]
            news_req = REQUESTS[REQS['tick']['news_id']]
            quote_req = REQUESTS[REQS['tick']['quotes_id']]
            finhub_req = REQUESTS[REQS['tick']['finhub_id']]


            df_more = pd.DataFrame(quote_req['quoteResponse']['result'][0],index=[0])

            try:
                name = df_more['displayName'].values[0]
            except :
                name = df_more['shortName'].values[0]

            now_div = display_now(df_more,finhub_req)

            df_today = get_intraday_prices(chart_req)
            today_chart = display_intra_chart(df_today, name)

            try:

                earnings_req = profile_req["quoteSummary"]["result"][0]['earnings']
                df_e, df_f = get_earnings(earnings_req)
                earnings_div = display_earnings(df_e, df_f, name)
                tab_1 = dbc.Container(dbc.Jumbotron(dbc.Row([
                    dbc.Col(today_chart,className="col-lg-6 col-md-12 col-sm-12 col-12"),
                    dbc.Col(earnings_div,className="col-lg-6 col-md-12 col-sm-12 col-12")
                ]), style={"background-color": daily_plot, "color": "silver"}),
                    style={"background-color": daily_plot, "color": "silver"}, fluid=True)


            except :
                tab_1 = dbc.Container(dbc.Jumbotron([
                    today_chart],style={"background-color":daily_plot,"color":"silver"}),style={"background-color":daily_plot,"color":"silver"})

            df_hist = get_intraday_prices(historic_req)
            chart_div = display_chart(df_hist, name)
            news_div = display_news(news_req, name)
            if news_div:
                tab_2 = dbc.Container(dbc.Jumbotron(dbc.Row([
                    dbc.Col([chart_div],style={"background-color":historic_plot},className="col-lg-6 col-md-12 col-sm-12 col-12"),
                    dbc.Col([news_div],style={"background-color":news_div},className="col-lg-6 col-md-12 col-sm-12 col-12")
                ]),style={"background-color":historic_plot}),style={"background-color":historic_plot},fluid=True)
            else:
                tab_2 = dbc.Container(dbc.Jumbotron(chart_div,style={"background-color":historic_plot}),style={"background-color":historic_plot},fluid=True)

            asset_req = profile_req["quoteSummary"]["result"][0]
            df_about, df_empl = get_about(asset_req)
            tab_3 = display_about(df_about, df_empl, name)

            lay = html.Div([
                now_div,

                dbc.Row(tab_1,style={"background-color":daily_plot,"color":"silver"}),

                dbc.Row(tab_2,style={"background-color":historic_plot}),


                dbc.Row(
                    dbc.Container(dbc.Jumbotron(tab_3,style={"background-color":about_plot,"color":"silver"}), fluid=True, style={"background-color":about_plot,"color":"silver"}),
                ),

            ])

            return lay, {"display":"none"}
        except Exception:
            import traceback
            print(traceback.print_exc(Exception))
            return [], {"display":"block"}


