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

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)
server = app.server
today = datetime.today()


about_me = "I am a strong programmer, skilled in data analytics, with knowledge in data storage structures, data mining " \
           "and data cleansing. A recent graduate from Boston University, with proficient knowledge in statistics, " \
           "mathematics, and programming. My focus is on solving problems through efficient computing and visualizing" \
           " data through beautiful design. I am also a quick learner and able problem solver with excellent work ethic, " \
           "communication and time management skills, able to work well in groups as well as independently."

TIINGO_KEY = ""
ALPHA_VANTAGE_KEY = ""
FINNHUB_KEY = ""
RAPID_API_KEY = ""

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

HISTORIC_OPTS = {
    'm': 'TIME_SERIES_MONTHLY',
    'w': "TIME_SERIES_WEEKLY",
    'd': 'TIME_SERIES_DAILY',
    'i': 'TIME_SERIES_INTRADAY',
    'ix': 'TIME_SERIES_INTRADAY_EXTENDED'
}

FINANCIALS_OPT = {
    'overview': "OVERVIEW",
    "income": "INCOME_STATEMENT",
    "balance": "BALANCE_SHEET",
    "cash_flow": "CASH_FLOW",
}

global TICKERS
TICKERS = pd.read_csv("assets/Tickers.csv")
del TICKERS['Unnamed: 0']

def get_request(args,REQUESTS):
    url = args[0]
    querystring = args[1]
    headers = args[2]
    if querystring is not None:
        req = requests.request("GET", url, headers=headers, params=querystring).json()
    else:
        req = requests.request("GET", url, headers=headers,).json()
    REQUESTS[url]=req

def worker(input_queue,REQUESTS):
    while True:
        url = input_queue.get()
        if url is None:
            break
        get_request(url,REQUESTS)


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

def get_summary():
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-summary"

    querystring = {"region": "US"}

    headers = {
        'x-rapidapi-key': RAPID_API_KEY,
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()
    temp = response["marketSummaryAndSparkResponse"]['result']
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
        tmp["regularMarketPreviousClose"] = stock["regularMarketPreviousClose"]["raw"]
        tmp["close"] = stock["spark"]["close"][-1]
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

def get_movers():

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-movers"

    querystring = {"region": "US", "start": "0", "lang": "en-US", "count": "6"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }

    response = requests.request("GET", url, headers=headers, params=querystring).json()['finance']['result']
    df_gainers = pd.DataFrame(response[0]['quotes'])['symbol']
    df_losers = pd.DataFrame(response[1]['quotes'])['symbol']
    df_active = pd.DataFrame(response[2]['quotes'])['symbol']  # most volume

    return df_gainers, df_losers, df_active

def get_overview(tick):
    fun = FINANCIALS_OPT['overview']
    base_url = "https://www.alphavantage.co/query?function={0}&symbol={1}&apikey={2}&datatype=pandas".format(fun, tick,
                                                                                                             ALPHA_VANTAGE_KEY)
    header = {
        'Content-Type': 'application/json'
    }
    df = requests.get(url=base_url, headers=header).json()

    df = pd.DataFrame(df, index=[0])

    base_url = "https://finnhub.io/api/v1/stock/profile2?symbol={0}&token={1}".format(tick, FINNHUB_KEY)
    df2 = requests.get(url=base_url, headers=header).json()
    df2 = pd.DataFrame(df2, index=[0])

    return df, df2

def get_quotes_movers():
    gainers, losers, active = get_movers()

    syms = ""

    for y in (gainers,losers,active):
        syms += ",".join(y.values)
        syms +=","



    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
    querystring = {"symbols": syms, "region": "US"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }

    req = requests.request("GET", url, headers=headers, params=querystring).json()['quoteResponse']['result']
    dfs=[]

    for lst in req:
        tmp={}
        #tmp["Name"] = lst['shortName']
        tmp["Symbol"] = lst['symbol']
        tmp["Last"] = lst['regularMarketPrice']
        #tmp["Day's Range"] = lst['regularMarketDayRange']
        tmp["Change"] = lst['regularMarketChange']
        tmp["%Change"] = lst['regularMarketChangePercent']
        dfs.append(tmp)

    df = pd.DataFrame(dfs)
    df["Last"] = df["Last"].apply(lambda x : normalize_num(x))
    df["Change"] = df["Change"].apply(lambda x: normalize_num(x))
    df["%Change"] = df["%Change"].apply(lambda x: normalize_num(x))

    df.set_index("Symbol", inplace=True,drop=False)

    return df, gainers, losers, active

def get_tick_data(ticks):

    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes"
    querystring = {"symbols": ticks, "region": "US"}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
    }

    df = requests.request("GET", url, headers=headers, params=querystring).json()['quoteResponse']['result'][0]


    try:
        del df['components']

        earnings = df['quoteSummary']['earnings']['earningsChart']['quarterly']
        df_e = pd.DataFrame(earnings)

        financials = df['quoteSummary']['earnings']['financialsChart']['quarterly']
        df_f = pd.DataFrame(financials)

        del df['quoteSummary']

        return pd.DataFrame(df, index=[0]), df_e, df_f
    except:
        df_e=[]
        df_f=[]

        return pd.DataFrame(df, index=[0])

def get_intraday_prices(req):

    response = req['chart']['result'][0]
    date = response['timestamp']
    date_df = pd.DataFrame(date, columns=["date"])
    date_df.date = date_df["date"].apply(lambda x: datetime.fromtimestamp(x))
    rest_data = response['indicators']['quote'][0]
    rest_df = pd.DataFrame(rest_data)[["high", "close", "low", "open"]]
    df = pd.concat([date_df, rest_df], axis=1).set_index("date",drop=False).resample("2T").pad()

    return df

start = datetime.today() - timedelta(weeks=52 * 5)
def get_historic_prices(req):

    df = req
    df = pd.DataFrame(df)
    df['date'] = pd.to_datetime(df['date']).apply(lambda x: datetime.date(x))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    return df

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

def display_now(tick, df_more):
    df_describe, df_profile = get_overview(tick)

    boolean = df_profile.empty
    logo = df_profile['logo'].values[
        0] if not boolean else "https://github.com/raypoci/raypoci.github.io/blob/master/static/images/no_logo.png?raw=true"
    url = df_profile['weburl'].values[0] if not boolean else "#"

    symbol = df_describe['Symbol'].values[0]
    name = df_describe['Name'].values[0]
    exchange = df_describe['Exchange'].values[0]
    curr = df_describe['Currency'].values[0]

    sector = df_describe['Sector'].values[0]
    try:
        pre_market = normalize_num(df_more["preMarketPrice"].values[0])
    except :
        pre_market="-"

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
        prev_close = normalize_num(df_more['regularMarketPreviousClose'].values[0])
    except :
        prev_close="-"

    try:
        low = normalize_num(df_more['regularMarketDayLow'].values[0])
    except:
        low=""
    try:
        high = normalize_num(df_more['regularMarketDayHigh'].values[0])
    except:
        high = ""
    try:
        low_target = normalize_num(df_more['targetPriceLow'].values[0])
    except :
        low_target=""
    try:
        high_target = normalize_num(df_more['targetPriceHigh'].values[0])
    except:
        high_target= ""
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
        pe_ratio = normalize_num(df_describe['PERatio'].values[0])
    except:
        pe_ratio = "-"

    try:
        peg_ratio = normalize_num(df_describe['PEGRatio'].values[0])
    except:
        peg_ratio = "-"
    try:
        forward_pe = normalize_num(df_describe['ForwardPE'].values[0])
    except :
        forward_pe = "-"
    try:
        eps = normalize_num(df_describe['EPS'].values[0])
    except:
        eps = "-"

    try:
        vol_10d = normalize_num(df_more['averageDailyVolume10Day'].values[0])
    except:
        vol_10d = "-"
    try:
        vol_3M = normalize_num(df_more['averageDailyVolume3Month'].values[0])
    except:
        vol_3M = "-"

    try:
        beta = normalize_num(df_describe['Beta'].values[0])
    except:
        beta = "-"
    try:
        book_value = normalize_num(df_more['bookValue'].values[0])
    except:
        book_value = "-"
    try:
        div_share = normalize_num(df_more['dividendsPerShare'].values[0])
    except:
        div_share = "-"

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
                                dbc.Col("P/E Ratio:   {0}".format(pe_ratio))

                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Sector:   {0}".format(sector)),
                                dbc.Col("Today's Volume:     {0}".format(today_vol)),
                                dbc.Col("Forward P/E:   {0}".format(forward_pe))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Pre Market Price:  {0}".format(pre_market)),
                                dbc.Col("Avg 10D Volume :  {0}".format(vol_10d)),
                                dbc.Col("EPS:   {0}".format(eps))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Price Target Range:  {0} - {1}".format(low_target, high_target)),
                                dbc.Col("Avg 3M Volume: {0}".format(vol_3M)),
                                dbc.Col("PEG Ratio:   {0}".format(peg_ratio))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Today's Range:  {0} - {1}".format(low, high)),
                                dbc.Col("Market Cap: {0}".format(market_cap)),
                                dbc.Col("Beta:   {0}".format(beta))
                            ]),
                        dbc.Row(
                            [
                                dbc.Col("Prev Close:   {0}".format(prev_close)),
                                dbc.Col("Divident Per Share:    {0}".format(div_share)),
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
                        showlegend=False)

    trace_candle = go.Candlestick(x=df.index,
                                  open=df['open'],
                                  high=df['high'],
                                  low=df['low'],
                                  close=df['close'],
                                  visible=False,
                                  showlegend=False)

    trace_line = go.Scatter(x=df.date, y=df['close'], showlegend=False,line=dict(color="silver"))

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
    title = "Chart of Intraday Data for {0}".format(name)
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
    xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1D", step="day", stepmode="backward"),
                    dict(count=1, label="3D", step="day", stepmode="backward"),
                    dict(count=5, label="5D", step="day", stepmode="backward"),
                    dict(count=10, label="10D", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(step="all")
                ]))

        ),
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
                        open=df['adjOpen'],
                        high=df['adjHigh'],
                        low=df['adjLow'],
                        close=df['adjClose'],
                        visible=False,
                        showlegend=False)

    trace_candle = go.Candlestick(x=df.index,
                                  open=df['adjOpen'],
                                  high=df['adjHigh'],
                                  low=df['adjLow'],
                                  close=df['adjClose'],
                                  visible=False,
                                  showlegend=False)

    trace_line = go.Scatter(x=df.index, y=df['adjClose'], showlegend=False, line=dict(color="#20c997"))

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
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=3, label="3m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=3, label="3y", step="year", stepmode="backward"),
                    dict(step="all")
                ]))

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
            dbc.Col(graph1),
            dbc.Col(graph2)
        ],style={"background-color":eps_plot,"color":"silver"})

    return lay

def display_news(news_req, name):
    df = news_req
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
    trace_line_snp = go.Scatter(x=df_snp.date, y=df_snp['close'], showlegend=False, line=dict(color="#fd7e14"))
    trace_line_dji = go.Scatter(x=df_dji.date, y=df_dji['close'], showlegend=False, line=dict(color="red"))
    trace_line_nasdaq = go.Scatter(x=df_nasdaq.date, y=df_nasdaq['close'], showlegend=False, line=dict(color="blue"))

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
        dbc.Col(g1),
        dbc.Col(g2),
        dbc.Col(g3)
    ],no_gutters=True)

def make_home_page():
    df_market, df_snp, df_dji, df_nasdaq = get_summary()
    df_movers, df_gainers, df_losers, df_active = get_quotes_movers()

    gainers = [df_movers.loc[str(symb)] for symb in df_gainers.values]
    df_gainers = pd.DataFrame(gainers)

    losers = [df_movers.loc[str(symb)] for symb in df_losers.values]
    df_losers = pd.DataFrame(losers)

    active = [df_movers.loc[str(symb)] for symb in df_active.values]
    df_active = pd.DataFrame(active)

    graph = display_summary(df_snp, df_dji, df_nasdaq)
    lay = html.Div([

        html.Div([
            dbc.Row([
                dbc.Col([

                    dbc.Card([
                        dbc.CardHeader(

                            dbc.Row([
                                dbc.Col("{0}".format(df_market.iloc[i]["symbol"]), style={"color": "white"}),
                                dbc.Col("{0}".format(normalize_num(df_market.iloc[i]["close"])),
                                        style={"color": "green"} if float(df_market.iloc[i]["prc_change"]) > 0 else {
                                            "color": "red"})
                            ], justify="between")

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

                ], width=2)
                for i in range(min(len(df_market), 6))
            ], no_gutters=True)
        ], style={"background-color": navbar_color}),

        html.Br(),
        html.H2("Today's Market Summary", style={"text-align": "center"}),

        html.Div([
            graph
        ]),

        dbc.Container([
            dbc.Row([
                dbc.Col([

                    html.H3("Today's Top Gainers", style={"text-align": 'center'}),
                    plot_movers(df_gainers)

                ], width=3),
                dbc.Col([

                    html.H3("Today's Worse Losers", style={"text-align": 'center'}),
                    plot_movers(df_losers)

                ], width=3),
                dbc.Col([

                    html.H3("Today's Most Active", style={"text-align": 'center'}),
                    plot_movers(df_active)

                ], width=3)
            ], justify="around")
        ], fluid=True),
        html.Br(),

    ],id="home-layout" )

    return lay


home = make_home_page()
app.layout=html.Div([navbar,home,html.Div(id="search-output"),footer])


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

)
def search(n_clicks, value):
    if not n_clicks and not value:
        return [],{"display":"block"}
    else:
        try:
            today = datetime.today().date()
            last_month = today - timedelta(days=30)
            headers = [{
                'x-rapidapi-key': RAPID_API_KEY,
                'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
            },
                {
                    'x-rapidapi-key': RAPID_API_KEY,
                    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
                },
                {
                    'Content-Type': 'application/json'
                },
                {
                    'Content-Type': 'application/json'
                }

            ]
            profile_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-profile"
            chart_url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart"
            historic_url = "https://api.tiingo.com/tiingo/daily/{0}/prices?startDate={1}&token={2}".format(value, start, TIINGO_KEY)
            news_url = "https://finnhub.io/api/v1/company-news?symbol={0}&from={1}&to={2}&token={3}".format(
                        value.upper(),
                        last_month, today,
                        FINNHUB_KEY)
            urls = [profile_url,chart_url,historic_url,news_url]

            query = [{"symbol": value, "region": "US"},
                     {"interval": "2m", "symbol": value, "range": "1mo", "region": "US"},
                     None,None]
            REQUESTS = mp.Manager().dict()
            arguments = zip(urls, query,headers)

            input_queue = mp.Queue()
            workers = []

            for i in range(4):
                p = mp.Process(target=worker, args=(input_queue, REQUESTS,))
                workers.append(p)
                p.start()
            for arg in arguments:
                input_queue.put(arg)

            for _ in workers:
                input_queue.put(None)

            for w in workers:
                w.join()

            profile_req = REQUESTS[profile_url]
            chart_req = REQUESTS[chart_url]
            historic_req = REQUESTS[historic_url]
            news_req = REQUESTS[news_url]


            try:
                df_more, df_e, df_f= get_tick_data(value)
            except:
                df_more = get_tick_data(value)
                df_e = []
                df_f = []
            name = df_more['shortName'].values[0]
            now_div = display_now(value, df_more)

            df_today = get_intraday_prices(chart_req)
            today_chart = display_intra_chart(df_today, name)
            try:
                boolean = df_e.empty and df_f.empty
            except :
                boolean= True
            if boolean:
                tab_1 = dbc.Container(dbc.Jumbotron([
                    today_chart],style={"background-color":daily_plot,"color":"silver"}),style={"background-color":daily_plot,"color":"silver"})

            else:
                earnings_div= display_earnings(df_e, df_f, name)
                tab_1 = dbc.Container(dbc.Jumbotron(dbc.Row([
                    dbc.Col(today_chart),
                    dbc.Col(earnings_div)
                    ]),style={"background-color":daily_plot,"color":"silver"}), style={"background-color":daily_plot,"color":"silver"},fluid=True)

            df_hist = get_historic_prices(historic_req)
            chart_div = display_chart(df_hist, name)
            news_div = display_news(news_req, name)
            if news_div:
                tab_2 = dbc.Container(dbc.Jumbotron(dbc.Row([
                    dbc.Col([chart_div],style={"background-color":historic_plot}),
                    dbc.Col([news_div],style={"background-color":news_div})
                ]),style={"background-color":historic_plot}),style={"background-color":historic_plot},fluid=True)
            else:
                tab_2 = dbc.Container(dbc.Jumbotron(chart_div,style={"background-color":historic_plot}),style={"background-color":historic_plot},fluid=True)

            df_about, df_empl = get_about(profile_req)
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
        except :
            return [], {"display":"block"}


