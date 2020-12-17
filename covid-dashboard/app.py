# -*- coding: utf-8 -*-
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
import copy
import dash_table.FormatTemplate as FormatTemplate
from flask import send_from_directory
import os
from pytz import timezone
import functools


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
    {
        'http-equiv': 'Content-Type',
        'content': 'text/html; charset=ISO-8859-1'
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
RAPID_API_KEY=""
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,update_title='Loading...',meta_tags=meta_tags)
app.config['suppress_callback_exceptions'] = True
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.head = [

    html.Link(
        href='/static/styles.css',
        rel='stylesheet'
    ),
    html.Title("COVID-19 DASHBOARD"),
    html.Meta(charSet='ISO-8859-1'),
    html.Meta(httpEquiv='Content-Type',content="text/html; charset=ISO-8859-1")
]
app.title="COVID-19 DASHBOARD"

server = app.server
today = datetime.today()

about_me = "I am a strong programmer, skilled in data analytics, with knowledge in data storage structures, data mining " \
           "and data cleansing. A recent graduate from Boston University, with proficient knowledge in statistics, " \
           "mathematics, and programming. My focus is on solving problems through efficient computing and visualizing" \
           " data through beautiful design. I am also a quick learner and able problem solver with excellent work ethic, " \
           "communication and time management skills, able to work well in groups as well as independently."


github_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/github-logo.jpg?raw=true"
linkedin_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/linkedin-logo.jpg?raw=true"
email_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/@email.jpg?raw=true"
website_logo="https://raw.githubusercontent.com/raypoci/raypoci.github.io/master/static/images/rp-website-logo.png?raw=true"
linkedin_site = "https://www.linkedin.com/in/ray-poci/"
github_site = "https://github.com/raypoci/raypoci.github.io"
website_url = "https://raypoci.herokuapp.com/"
email_url = "mailto:raypoci18@gmail.com"
PLOTLY_LOGO = website_logo

ACTIVE_COLOR = "#506AAF"
ACTIVE_FONT_COLOR = "darkblue"
DEATHS_COLOR= "#bd425c"
DEATHS_FONT_COLOR = "#430028"
CASES_COLOR= 'lightgray'
CASES_FONT_COLOR = "#474747"
RECOVERED_COLOR= "palegreen"
RECOVERED_FONT_COLOR = "darkgreen"
PAGE_COLOR = "#ffd28f"
SEARCH_BACK_COLOR = "lightgray"
CRITICAL_FONT_COLOR='#644F00'
CRITICAL_COLOR='#C4AA3B'
FAT_FONT_COLOR='#392D00'
FAT_COLOR='#ab6634'
EMPTY_CELL_COLOR ='#FFF5D0'

BANNER_HEIGHT='128px'
BANNER_WIDTH ='95%'
BANNER_CLASS = 'col-lg-2 col-md-4 col-sm-6 col-12 '


ACTIVE_TITLE_STYLE = style={"font-weight":"bold","color":ACTIVE_FONT_COLOR,'text-align':'center'}
DEATHS_TITLE_STYLE = style={"font-weight":"bold","color":DEATHS_FONT_COLOR,'text-align':'center'}
CASES_TITLE_STYLE = style={"font-weight":"bold","color":CASES_FONT_COLOR,'text-align':'center'}
RECOVERED_TITLE_STYLE = style={"font-weight":"bold","color":RECOVERED_FONT_COLOR,'text-align':'center'}
CRITICAL_TITLE_STYLE=style={"font-weight":"bold","color":CRITICAL_FONT_COLOR,'text-align':'center'}
FAT_TITLE_STYLE=style={"font-weight":"bold","color":FAT_FONT_COLOR,'text-align':'center'}

cases_bucket = [(1,5000),(5001,50000),(50001,500000),(500001,1000000),(1000000,2000000)]
cases_new_bucket = [(1,10),(11,100),(101,1000),(1001,10000),(10000,100000)]
cases_mil_bucket = [(0.1,100),(100.1,1000),(1000.1,10000),(10000.1,30000),(30000.1,50000)]


deaths_bucket = [(1,50),(51,500),(501,5000),(5001,50000),(50001,200000)]
deaths_new_bucket = [(1,10),(11,50),(51,200),(201,500),(501,1000)]
deaths_mil_bucket = [(0.1,10),(10.1,50),(50.1,100),(100.1,500),(500.1,1000)]

SHOW = {'display':'block'}
HIDE = {'display':'none'}

footer_style = {"text-decoration": "none","color":"darkblue",}
footer =dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.P("About Me:", style={"font-weight":"bold"}),
                    html.P(about_me),
                    html.Br(),
                    html.Br(),
                ]),
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


                ])
            ],justify="center",)

footer = dbc.Card(dbc.CardBody(footer,style={'background-color':PAGE_COLOR}))
FLAGS={}
df = pd.read_csv('assets/flags.csv').to_dict('list')
FLAGS=(dict(zip(df['Country'],df['Flags'])))

def get_table(df, option='World'):
    df = copy.deepcopy(df)
    cols = []
    if option not in continents:
        df = df.loc[:, (df != 0).any(axis=0)]
        for i in list(df.columns):
            if i not in ["State/Province", '(Deaths/Cases)%']:
                cols.append({"name": i, "id": i, 'selectable': True, 'deletable': True, 'type': 'numeric',
                             'format': {'specifier': '.4s'}})

            elif i in ['(Deaths/Cases)%']:

                cols.append({"name": i, "id": i, 'type': 'numeric', 'format': FormatTemplate.percentage(2),
                             'selectable': True, })
            else:
                cols.append({'name': i, "id": i, 'selectable': True,
                             'type': 'text', })

    else:

        df = df[['Country', 'Total Cases', 'Total Deaths', 'Active Cases',
                 'Critical Cases', "Cases (24hrs)", 'Deaths (24hrs)','Total Recovered', 'Tests', '(Deaths/Cases)%']]
        df = df[~df['Country'].isin(['Africa', 'Asia', 'Europe', 'North America',
                                     'South America', 'Oceania'])]
        df = df[df['Total Cases'] > 628]
        country_cols = {'name': 'Country',
                        'id': 'Country',
                        'selectable': True,
                        'type': 'text', }
        cols.append(country_cols)

        for i in ['Total Cases', 'Total Deaths', 'Active Cases',
                  'Critical Cases', "Cases (24hrs)", 'Deaths (24hrs)','Total Recovered', 'Tests', ]:
            data_cols = {
                'name': '{}'.format(i),
                'id': '{}'.format(i),
                'deletable': True,
                'selectable': True,
                'type': 'numeric',
                'format': {'specifier': '.4s'},
            }
            cols.append(data_cols)
        mortality_cols = {"name": "(Deaths / Cases)%", "id": "(Deaths/Cases)%", 'type': 'numeric',
                          'format': FormatTemplate.percentage(2), 'selectable': True, }

        cols.append(mortality_cols)
    return dash_table.DataTable(
        style_table={'overflow-x':'scroll'},
        cell_selectable=True,
        page_action="native",
        page_current=0,
        page_size=60,
        style_cell={'textAlign': 'center'},
        style_as_list_view=True,
        filter_action="native",
        sort_action="native",
        style_data_conditional=
        [
            {
                'if': {
                    'column_id': ['Country', "State/Province"],
                },
                'backgroundColor': PAGE_COLOR,
                'font-weight': 'bold',
            },

            {
                'if': {
                    'column_id': "(Deaths/Cases)%"
                },
                'backgroundColor': FAT_COLOR,
                'color': FAT_FONT_COLOR
            },

            {
                'if': {
                    'column_id': ['Total Cases', "Cases (24hrs)", ],
                },
                'backgroundColor': CASES_COLOR,
                'color': CASES_FONT_COLOR
            },
            {
                'if': {
                    'column_id': ['Country', "State/Province"],
                },
                'text-align': 'left'
            },

            {
                'if': {
                    'column_id': ['Total Deaths', "Deaths (24hrs)"],
                },
                'backgroundColor': DEATHS_COLOR,
                'color': DEATHS_FONT_COLOR
            },
            {
                'if': {
                    'column_id': ['Active Cases', 'Total Active', 'Active (24hrs)', "Cases (24hrs)"]
                },
                'backgroundColor': ACTIVE_COLOR,
                'color': ACTIVE_FONT_COLOR
            },
            {
                'if': {
                    'column_id': "Critical Cases",
                },
                'backgroundColor': CRITICAL_COLOR,
                'color': CRITICAL_FONT_COLOR
            },

            {
                'if': {
                    'column_id': ['Total Recovered', 'Recovered (24hrs)'],
                },
                'backgroundColor': RECOVERED_COLOR,
                'color': RECOVERED_FONT_COLOR,
            },
            {
                'if': {
                    'column_id': "Tests"
                },
                'backgroundColor': PAGE_COLOR,
                'color': 'black',
            },
        ]
        +
        [
            {
                'if': {
                    'filter_query': '{{{}}} = 0'.format(i),
                    'column_id': i,
                },
                'backgroundColor': EMPTY_CELL_COLOR,
                'color': "black",
            } for i in ['Total Cases', 'Cases (24hrs)', 'Total Deaths', 'Deaths (24hrs)', 'Active Cases',
                        'Critical Cases', 'Total Recovered', 'Recovered (24hrs)', 'Tests', "Cases (24hrs)"]
        ]

        +
        [
            {
                'if': {
                    'filter_query': '{{{}}} = ""'.format(col),
                    'column_id': col
                },
                'backgroundColor': EMPTY_CELL_COLOR,

            } for col in ['Total Cases', 'Total Deaths', 'Active Cases',
                          'Critical Cases', 'Total Recovered', 'Tests', "Cases (24hrs)"]]
        ,

        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_header_conditional=[
            {
                'if': {
                    'column_id': ['Country', 'State/Province']
                },
                'text-align': 'left'
            }
        ],

        columns=cols,
        data=df.to_dict('records'),)

def get_request(args):
    url = args[0]
    try:
        headers = args[1]
    except:
        headers = None
    try:
        querystring = args[2]
    except:
        querystring = None
    req = requests.request("GET", url, headers=headers, params=querystring)
    return req.json()

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

@functools.lru_cache()
def get_timeseries(country):
    given_cts = ["USA", 'UK', 'UAE', 'Palestine', 'S Korea', 'DRC', 'Congo', 'CAR', "Diamond Princess ",
         'Faeroe Islands', 'St Barth', 'MS Zaandam ', 'All']
    new_cts = ["United States", 'United Kingdom', 'United Arab Emirates', 'Palestinian Territories',
         'South Korea', 'Congo (Kinshasa)', 'Congo (Brazzaville)', "Central African Republic",
         'Diamond Princess', 'Faroe Islands', 'St Barthoulemy', 'MS Zaandam', 'World']

    for i, ct in enumerate(new_cts):
        if country==ct:
            country=given_cts[i]
    url = "https://covid-193.p.rapidapi.com/history"

    headers = {
        'x-rapidapi-key': RAPID_API_KEY,
        'x-rapidapi-host': "covid-193.p.rapidapi.com"
    }
    querystring = {"country": country}

    args = [url, headers,querystring]
    request = get_request(args)['response']


    for req in request:

        try:
            req['new_cases'] = int(req['cases']['new'])
        except:
            req['new_cases'] = ""
        try:
            req['active_cases'] = int(req['cases']['active'])
        except:
            req['active_cases'] = ""
        try:
            req['critical_cases'] = int(req['cases']['critical'])
        except:
            req['critical_cases'] = ""
        try:
            req['recovered'] = int(req['cases']['recovered'])
        except:
            req['recovered'] = ""
        try:
            req['total_cases'] = int(req['cases']['total'])
        except:
            req['total_cases'] = ""
        try:
            req['new_deaths'] = int(req['deaths']['new'])
        except:
            req['new_deaths'] = ""
        try:
            req['total_deaths'] = int(req['deaths']['total'])
        except:
            req['total_deaths'] = ""
        try:
            req['total_tests'] = int(req['tests']['total'])
        except:
            req['total_tests'] = ""
        try:
            req['fatality_rate'] = float(req['total_deaths']) / float(req['total_cases'])
        except:
            req['fatality_rate'] = ""

        try:
            req['Deaths/1M'] = float(req['deaths']['1M_pop'])
        except :
            req['Deaths/1M'] = ""

        try:
            req['Cases/1M'] = float(req['cases']['1M_pop'])
        except :
            req['Cases/1M'] = ""

        try:
            req['Tests/1M'] = float(req['tests']['1M_pop'])
        except :
            req['Tests/1M'] = ""

        req['date'] = datetime.fromisoformat(req['time']).date()

        del req["cases"]
        del req["deaths"]
        del req["tests"]

    cols = {
        "country": "Country",
        "total_cases": "Total Cases",
        "new_cases": "Cases (24hrs)",
        "total_deaths": "Total Deaths",
        "new_deaths": "Deaths (24hrs)",
        "recovered": "Total Recovered",
        "critical_cases": "Critical Cases",
        "active_cases": "Active Cases",
        "total_tests": "Tests",
        "fatality_rate": "(Deaths/Cases)%"
    }
    df = pd.DataFrame(request)
    df = df.groupby('date',as_index=True).first().reset_index(drop=False)
    df.rename(columns=cols, inplace=True)

    df['Country'] = df['Country'].apply(lambda x: str(x).replace("-", " "))
    df['continent'] = df['continent'].apply(lambda x: str(x).replace("-", " "))
    df['Country'] = df['Country'].replace(
        ["USA", 'UK', 'UAE', 'Palestine', 'S Korea', 'DRC', 'Congo', 'CAR', "Diamond Princess ",
         'Faeroe Islands', 'St Barth', 'MS Zaandam ', 'All'],
        ["United States", 'United Kingdom', 'United Arab Emirates', 'Palestinian Territories',
         'South Korea', 'Congo (Kinshasa)', 'Congo (Brazzaville)', "Central African Republic",
         'Diamond Princess', 'Faroe Islands', 'St Barthoulemy', 'MS Zaandam', 'World'])
    df = df[~df['Country'].isin(['R&eacute;union', 'Cura&ccedil;ao', 'Channel Islands'])]
    df = df[~df['Country'].isna()]
    df.sort_values(by='Total Cases', inplace=True, ascending=False)
    return df

def get_today_df():
    url = "https://covid-193.p.rapidapi.com/statistics"

    headers = {
        'x-rapidapi-key': RAPID_API_KEY,
        'x-rapidapi-host': "covid-193.p.rapidapi.com"
    }
    args = [url, headers, ]
    request = get_request(args)['response']

    for req in request:

        try:
            req['new_cases'] = int(req['cases']['new'])
        except:
            req['new_cases'] = ""
        try:
            req['active_cases'] = int(req['cases']['active'])
        except:
            req['active_cases'] = ""
        try:
            req['critical_cases'] = int(req['cases']['critical'])
        except:
            req['critical_cases'] = ""
        try:
            req['recovered'] = int(req['cases']['recovered'])
        except:
            req['recovered'] = ""
        try:
            req['total_cases'] = int(req['cases']['total'])
        except:
            req['total_cases'] = ""
        try:
            req['new_deaths'] = int(req['deaths']['new'])
        except:
            req['new_deaths'] = ""
        try:
            req['total_deaths'] = int(req['deaths']['total'])
        except:
            req['total_deaths'] = ""
        try:
            req['total_tests'] = int(req['tests']['total'])
        except:
            req['total_tests'] = ""
        try:
            req['fatality_rate'] = float(req['total_deaths']) / float(req['total_cases'])
        except:
            req['fatality_rate'] = ""
        try:
            req['Deaths/1M'] = float(req['deaths']['1M_pop'])
        except :
            req['Deaths/1M'] = ""

        try:
            req['Cases/1M'] = float(req['cases']['1M_pop'])
        except :
            req['Cases/1M'] = ""

        try:
            req['Tests/1M'] = float(req['tests']['1M_pop'])
        except :
            req['Tests/1M'] = ""
        del req["cases"]
        del req["deaths"]
        del req["tests"]

    cols = {
        "country": "Country",
        "total_cases": "Total Cases",
        "new_cases": "Cases (24hrs)",
        "total_deaths": "Total Deaths",
        "new_deaths": "Deaths (24hrs)",
        "recovered": "Total Recovered",
        "critical_cases": "Critical Cases",
        "active_cases": "Active Cases",
        "total_tests": "Tests",
        "fatality_rate": "(Deaths/Cases)%"
    }
    df = pd.DataFrame(request)
    df.rename(columns=cols, inplace=True)
    df['Country'] = df['Country'].apply(lambda x: str(x).replace("-", " "))
    df['continent'] = df['continent'].apply(lambda x: str(x).replace("-", " "))
    df['Country'] = df['Country'].replace(
        ["USA", 'UK', 'UAE', 'Palestine', 'S Korea', 'DRC', 'Congo', 'CAR', "Diamond Princess ",
         'Faeroe Islands', 'St Barth', 'MS Zaandam ', 'All'],
        ["United States", 'United Kingdom', 'United Arab Emirates', 'Palestinian Territories',
         'South Korea', 'Congo (Kinshasa)', 'Congo (Brazzaville)', "Central African Republic",
         'Diamond Princess', 'Faroe Islands', 'St Barthoulemy', 'MS Zaandam', 'World'])
    df = df[~df['Country'].isin(['R&eacute;union', 'Cura&ccedil;ao', 'Channel Islands'])]
    df = df[~df['Country'].isna()]
    df.sort_values(by='Total Cases', inplace=True, ascending=False)
    return df, df[df['continent'] == 'All']
countries_df, globals_df = get_today_df()

def get_states_df():
    args = ["https://covid-api.com/api/reports/"]
    req = get_request(args)['data']
    for r in req:
        r['name'] = r['region']['name']
        r['province'] = r['region']['province']
        del r['region']
    cols = {
        "province": "State/Province",
        "confirmed": "Total Cases",
        "confirmed_diff": "Cases (24hrs)",
        "deaths": "Total Deaths",
        "deaths_diff": "Deaths (24hrs)",
        "recovered": "Total Recovered",
        "recovered_diff": "Recovered (24hrs)",
        "active": "Total Active",
        "active_diff": "Active (24hrs)",
        "fatality_rate": "(Deaths/Cases)%"

    }
    df = pd.DataFrame(req)
    is_state = df['province'] != ""
    df_states = df[is_state]
    df_states = df_states.set_index("name", drop=False)
    df_states['name'] = df_states['name'].replace(['US'], 'United States')
    states_list = list(df_states['name'].unique())
    df_states.drop(['date', 'last_update'], axis=1, inplace=True)
    df_states.rename(columns=cols, inplace=True)

    df_states.sort_values(by='Total Cases', inplace=True, ascending=False)

    return df_states, states_list
states_df, states_list = get_states_df()

def get_country_codes():
    df = pd.read_csv("assets/countries.csv")
    return df
country_codes = get_country_codes()
continents = list(countries_df['continent'].unique())
continents.remove("All")
continents.remove('None')
continents.sort()
continents.insert(0, "World")
country_list = list(countries_df['Country'].unique())
country_codes = country_codes.loc[country_codes['Country'].isin(country_list)]

def get_graph_df():
    df = copy.deepcopy(countries_df)
    list_coded_countries = [x for x in country_list if x in country_codes['Country'].unique()]
    df = df[df['Country'].isin(list_coded_countries)]
    df['Code'] = df['Country'].values
    df['Code'] = df.Code.apply(
        lambda x: country_codes[country_codes['Country'] == x]['alpha-3'].values[0])

    return df

graph_df = get_graph_df()

def get_summary_menu():

    last_update = globals_df['time'].values[0]
    last_update = datetime.fromisoformat(last_update).astimezone(timezone('US/Eastern')).strftime("%Y-%m-%d %H:%M:%S")
    confirmed = int(globals_df['Total Cases'].values[0])
    confirmed_diff =int(globals_df['Cases (24hrs)'].values[0])
    confirmed_prc = float(confirmed_diff/(confirmed-confirmed_diff))*100

    deaths = int(globals_df['Total Deaths'].values[0])
    deaths_diff = int(globals_df['Deaths (24hrs)'].values[0])
    deaths_prc = float(deaths_diff / (deaths - deaths_diff))*100

    recovered = int(globals_df['Total Recovered'].values[0])

    active = int(globals_df['Active Cases'].values[0])
    critical = int(globals_df['Critical Cases'].values[0])

    confirmed = normalize_num(confirmed)
    confirmed_diff =normalize_num(confirmed_diff)
    confirmed_prc = normalize_num(confirmed_prc)

    deaths = normalize_num(deaths)
    deaths_diff =normalize_num(deaths_diff)
    deaths_prc = normalize_num(deaths_prc)

    recovered = normalize_num(recovered)
    active =normalize_num(active)
    critical = normalize_num(critical)
    fatality_rate = normalize_num(globals_df['(Deaths/Cases)%'].values[0]*100)

    cases_totals = [
            html.H4("{0}".format(confirmed),className="card-title", style={"color":CASES_FONT_COLOR,'text-align':'center'}),
            html.H6("+{0} (+{1}%)".format(confirmed_diff, confirmed_prc),className='card-subtitle',style={'text-align':'center'})]


    deaths_totals = [
            html.H4("{0}".format(deaths),className="card-title", style={"color":DEATHS_FONT_COLOR,'text-align':'center'}),
            html.H6("+{0} (+{1}%)".format(deaths_diff, deaths_prc),className='card-subtitle',style={'text-align':'center'})]

    recovered_totals = [
            html.H4("{0}".format(recovered),className="card-title", style={"color":RECOVERED_FONT_COLOR,'text-align':'center'},),
        ]

    active_totals = [
            html.H4("{0}".format(active),className="card-title", style={"color":ACTIVE_FONT_COLOR,'text-align':'center'}),
            ]

    critical_totals = [
            html.H4("{0}".format(critical),className="card-title", style={"color":CRITICAL_FONT_COLOR,'text-align':'center'}),
            ]
    fatality = [
            html.H4("{0}%".format(fatality_rate),className="card-title", style={"color":FAT_FONT_COLOR,'text-align':'center'}),
            ]

    search_div = dbc.Form(dbc.FormGroup(
        [

            dbc.RadioItems(
                options=(

                        [{"label": "{0} {1}".format(FLAGS[continents[i]],continents[i]), "value": continents[i]}
                         for i in range(len(continents))]
                +
                [
                    {"label": "{0} {1}".format(FLAGS[states_list[i]],states_list[i]), "value": states_list[i]}
                    for i in range(len(states_list) )
                ] ),
                value="World",
                id="radioitems",
                inline=True,
                labelClassName="btn btn-block btn-outline-secondary ",
                labelCheckedClassName="active",
                labelStyle={'margin': '0px 10px 10px 0px','color':'black','font-weight':'bold'}
            ),
        ]
    ))

    summary_menu_card= dbc.Card(
    dbc.CardBody(
        [
            html.H4("Coronavirus | COVID-19", className="card-title"),
            html.H6("Data is updated periodically. Last Updated at {0} (US/Eastern)".format(last_update), className="card-subtitle",
                    style={'font-size':'small','font-style':'italic'}),
            html.Br(),
            dbc.Container(
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H5("Total Cases",style=CASES_TITLE_STYLE,),
                    html.Div(children=cases_totals,id='total_cases')
                ],style={'background-color':CASES_COLOR,'height':BANNER_HEIGHT,"width":BANNER_WIDTH},className=BANNER_CLASS),
                dbc.Col([
                    html.Br(),
                    html.H5("Total Deaths", style=DEATHS_TITLE_STYLE,),
                    html.Div(children=deaths_totals,id='total_deaths')

                ],style={'background-color':DEATHS_COLOR,'height':BANNER_HEIGHT,"width":BANNER_WIDTH},className=BANNER_CLASS),
                dbc.Col([
                    html.Br(),
                    html.H5("Total Recovered", style=RECOVERED_TITLE_STYLE),
                    html.Div(children=recovered_totals,id='total_recovered')

                ],style={'background-color':RECOVERED_COLOR,'height':BANNER_HEIGHT,"width":BANNER_WIDTH},className=BANNER_CLASS),
                dbc.Col([
                    html.Br(),
                    html.H5("Total Active", style=ACTIVE_TITLE_STYLE,),
                    html.Div(children=active_totals,id='total_active')

                ],style={'background-color':ACTIVE_COLOR,'height':BANNER_HEIGHT,"width":BANNER_WIDTH},className=BANNER_CLASS),



            dbc.Col([
                    html.Br(),
                    html.H5("Critical Cases", style=CRITICAL_TITLE_STYLE, className="card-title"),
                    html.Div(children=critical_totals, id='crital_cases')
                ], style={'background-color': CRITICAL_COLOR,'height':BANNER_HEIGHT,"width":BANNER_WIDTH},className=BANNER_CLASS ),

                dbc.Col([
                    html.Br(),
                    html.H5("(Deaths/Cases)%", style=FAT_TITLE_STYLE, className="card-title"),
                    html.Div(children=fatality, id='mortality')
                ], style={'background-color': FAT_COLOR,'height':BANNER_HEIGHT,"width":BANNER_WIDTH},className=BANNER_CLASS)],justify='around',no_gutters=False),fluid=True),
            html.Br(),
            dbc.Row([
               dbc.Col(
                [
                    dbc.Button(
                        "Filter Table: Pick a Region to display its countries or a Country to display its State/Province",
                        id="collapse-search",
                        color="secondary",
                        block=True,
                        n_clicks=0,
                        style={'display':'block'}

                    ),
                ]
            ,)])
                    ,

                    dbc.Row(dbc.Col(dbc.Collapse(dbc.Card([
                        search_div
                    ], body=True,style={"background-color":"lightgray"}),id='collapse'),)),]
    ),style={'background-color':PAGE_COLOR})

    return html.Div(summary_menu_card)

def get_map_menu():
    map_type = dbc.Form(dbc.FormGroup(
        [

            dbc.RadioItems(
                options=(

                        [{"label": "{0} Chloropleth".format(FLAGS['Map']), "value": 'map'},
                         {"label": "{0} Bubble".format(FLAGS['Bubble']), "value": 'bubble'}
                         ]),

                value="map",
                id="select-map-type",
                inline=True,
                labelClassName="btn btn-block btn-outline-secondary ",
                labelCheckedClassName="active",
                labelStyle={'margin': '0px 10px 10px 0px', 'color': 'black', 'font-weight': 'bold'}
            ),
        ]
    ))
    map_condition=dbc.Form(dbc.FormGroup(
        [

            dbc.RadioItems(
                options=(

                        [{"label": "Cases", "value": 'cases'},
                         {"label": "Deaths", "value": 'deaths'}
                         ]),

                value="cases",
                id="select-map-condition",
                inline=True,
                labelClassName="btn btn-block btn-outline-secondary ",
                labelCheckedClassName="active",
                labelStyle={'margin': '0px 10px 10px 0px', 'color': 'black', 'font-weight': 'bold'}
            ),
        ]
    ))
    map_option=dbc.Select(id='select-map-option',
                                    options=[
                                        {'label':"Total",'value':'total'},
                                        {'label':"Total per 1 million population",'value':'per_mil'},
                                        {'label': "Newly reported in last 24 hours", 'value': 'new'}
                                    ],
                                    value='total'
            )
    map_menu_card=dbc.Card(dbc.CardBody(dbc.Row([dbc.Col(

        [
        html.Hr(),
        html.Small('Chose a map type'),
        (map_type),
        html.Small('Toggle between Cases or Deaths'),
        (map_condition),
        html.Small('Select a category of Cases or Deaths'),
        (map_option),
        html.Hr(),
    ],className='col-lg-2 col-md-2 col-sm-12 col-12 '),

        dbc.Col(id="map-content",className='col-lg-10 col-md-10 col-sm-12 col-12 ')
    ])),style={'background-color':PAGE_COLOR})
    return (map_menu_card)

def get_graph_menu():
    graph_menu_card=dbc.Row([
        dbc.Col(dbc.Card(
        [
            dbc.CardHeader('Pick a Country'),
            dbc.CardBody(dbc.Select(id='select-country',
                                    options=[
                                        {'label':"{0} {1}".format(c,FLAGS[c]),'value':c}
                                        for c in country_list
                                    ],
                                    value='World'
            ),style={'background-color':PAGE_COLOR})
        ],style={'background-color':PAGE_COLOR})),
        dbc.Col(dbc.Card(
            [
                dbc.CardHeader('Pick a Scale'),
                dbc.CardBody(dbc.Select(id='select-scale',
                                        options=[
                                            {'label': "Logarithmic", 'value': 'log'},
                                            {'label': "Linear", 'value': 'linear'}

                                        ],
                                        value='log'

                                        ),style={'background-color':PAGE_COLOR})
            ],style={'background-color':PAGE_COLOR}))
    ])
    return (graph_menu_card)

def get_summary(option):
    if option == "World":
        filtered_df = copy.deepcopy(countries_df)

    elif option in continents:

        filtered_df = copy.deepcopy(countries_df)
        filtered_df = filtered_df[filtered_df['continent']==option]
    else:

        filtered_df = copy.deepcopy(states_df[states_df["name"] == option])
        filtered_df = filtered_df[["State/Province", "Total Cases", "Cases (24hrs)", "Total Deaths", "Deaths (24hrs)",
                        "Total Active", "Active (24hrs)", "Total Recovered", "Recovered (24hrs)",
                        "(Deaths/Cases)%"]]
        filtered_df = filtered_df[~filtered_df['State/Province'].isin(['Unknown', 'Recovered'])]
        filtered_df['(Deaths/Cases)%']=filtered_df['Total Deaths']/filtered_df['Total Cases']

    table = get_table(filtered_df,option=option)
    return dbc.Card(dbc.CardBody(table,style={'background-color':PAGE_COLOR}))

def graph_chloro(option):
    df = copy.deepcopy(graph_df)

    fig = go.Figure(data=go.Choropleth(
        locations=df['Code'],
        z=df[option],
        text=df['Country'],
        colorscale='Earth',
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title=option,
    ))

    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    graph= dcc.Graph(figure=fig, )
    return graph

def graph_bubble(option):
    if option=='Total Cases':
        limit = cases_bucket
    elif option=='Cases (24hrs)':
        limit = cases_new_bucket
    elif option=='Cases/1M':
        limit = cases_mil_bucket
    elif option=='Total Deaths':
        limit = deaths_bucket
    elif option=='Deaths (24hrs)':
        limit = deaths_new_bucket
    else:
        limit = deaths_mil_bucket
    bubble_size = [1,5,10,15,20,30]
    df = copy.deepcopy(graph_df)

    fig = go.Figure()

    def get_text(x):
        try:
            return '{:,}'.format(x)
        except :
            return ''


    df['text'] = df[option].apply(lambda x: get_text(x) )

    df_sub = df.loc[df[option] == ""]
    fig.add_trace(go.Scattergeo(
        locations=df_sub['Code'],
        text=df_sub['Country'] + "<br>{0} ".format(option) + df_sub['text'],
        marker=dict(
            size=1,
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area',

        ),
        name='No Data Reported',hoverinfo='text'))

    df_sub = df.loc[df[option] == 0]
    fig.add_trace(go.Scattergeo(
        locations=df_sub['Code'],
        text=df_sub['Country'] + "<br>{0} ".format(option) + df_sub['text'],
        marker=dict(
            size=1,
            line_color='rgb(40,40,40)',
            line_width=0.5,
            sizemode='area',

        ),
        name='0',hoverinfo='text'))

    for i in range(6):
        df_sub = df.loc[~((df[option]=="") | (df[option]==0))]
        if i!=5:
            lim = limit[i]
            df_sub = df_sub.loc[(df_sub[option] >= lim[0]) & (df_sub[option] <= lim[1])]

            fig.add_trace(go.Scattergeo(
                locations=df_sub['Code'],
                text=df_sub['Country'] + "<br>{0} ".format(option) + df_sub['text'],
                marker = dict(
                    size=bubble_size[i],
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode = 'area',

                ),
                name='{:,} - {:,}'.format(lim[0], lim[1]),hoverinfo='text'))
        elif i==5:
            lim = limit[i-1]
            df_sub = df_sub.loc[(df_sub[option] >= lim[1])]
            fig.add_trace(go.Scattergeo(
                locations=df_sub['Code'],
                text=df_sub['Country'] + "<br>{0} ".format(option) + df_sub['text'],
                marker=dict(
                    size=bubble_size[i],
                    line_color='rgb(40,40,40)',
                    line_width=0.5,
                    sizemode='area',

                ),
                name='>{:,}'.format(lim[1]),hoverinfo='text'))


    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular',
            scope='world',
            landcolor='rgb(217, 217, 217)'
        ),
        margin=dict(l=0, r=0, t=0, b=0),
    )
    graph = dcc.Graph(figure=fig, )
    return graph

def get_map(map_type='map',map_condition='cases',map_option='total'):
    if map_type=='map':
        if map_condition=="cases":
            if map_option=='total':
                content = graph_chloro('Total Cases')
            elif map_option == 'new':
                content = graph_chloro('Cases (24hrs)')
            else:
                content = graph_chloro('Cases/1M')

        else:
            if map_option=='total':
                content = graph_chloro('Total Deaths')
            elif map_option == 'new':
                content = graph_chloro('Deaths (24hrs)')
            else:
                content = graph_chloro('Deaths/1M')
    else:
        if map_condition == "cases":
            if map_option == 'total':
                content = graph_bubble('Total Cases')
            elif map_option == 'new':
                content = graph_bubble('Cases (24hrs)')
            else:
                content = graph_bubble('Cases/1M')

        else:
            if map_option == 'total':
                content = graph_bubble('Total Deaths')
            elif map_option == 'new':
                content = graph_bubble('Deaths (24hrs)')
            else:
                content = graph_bubble('Deaths/1M')
    map_card=html.Div(content)
    return (map_card)

def get_total_graph(df,country,scale):
    n=14
    boolean = True
    not_boolean = False
    if country =='World':
        country = "{0} Worldwide".format(FLAGS[country])
        boolean = False
        not_boolean = True

    else:
        country = "{1} {0}".format(country,FLAGS[country])
    cases_trace = go.Scattergl(x=df["date"], y=df['Total Cases'], showlegend=True,line=dict(color="darkblue"),connectgaps=True,
                             name="Total Cases", mode='lines',text="{0} Total Cases".format(country),hoverinfo='x+y+text')

    deaths_trace = go.Scattergl(x=df["date"], y=df['Total Deaths'], showlegend=True, line=dict(color=DEATHS_COLOR), connectgaps=True,
                             name="Total Deaths", mode='lines',text="{0} Total Deaths".format(country),hoverinfo='x+y+text' )

    recovered_trace = go.Scattergl(x=df["date"], y=df['Total Recovered'], showlegend=True, line=dict(color="#83D12E"), connectgaps=True,
                             name="Total Recovered", mode='lines',text="{0} Total Recovered".format(country),hoverinfo='x+y+text' )

    active_trace = go.Scattergl(x=df["date"], y=df['Active Cases'], showlegend=True, line=dict(color="black"), connectgaps=True,
                             name="Active Cases",  mode='lines',text="{0} Active Cases".format(country),hoverinfo='x+y+text')

    critical_trace = go.Scattergl(x=df["date"], y=df['Critical Cases'], showlegend=True,line=dict(color=CRITICAL_COLOR),connectgaps=True,
                             name="Critical Cases", mode='lines',text="{0} Critical Cases".format(country),hoverinfo='x+y+text')

    tests_trace = go.Scattergl(x=df["date"], y=df['Tests'], showlegend=boolean,line=dict(color="orange"),connectgaps=True,
                             name="Tests", mode='lines',text="{0} Tests".format(country),hoverinfo='x+y+text')

    cases_bar = go.Bar(x=df['date'].iloc[::n], y=df['Total Cases'].iloc[::n], name="Total Cases",text="{0} Total Cases".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': "darkblue"},type='bar')
    deaths_bar = go.Bar(x=df['date'].iloc[::n], y=df['Total Deaths'].iloc[::n], name="Total Deaths",text="{0} Total Deaths".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': DEATHS_COLOR},type='bar')
    recovered_bar = go.Bar(x=df['date'].iloc[::n], y=df['Total Recovered'].iloc[::n], name="Total Recovered",text="{0} Total Recovered".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': "#83D12E"},type='bar')
    active_bar = go.Bar(x=df['date'].iloc[::n], y=df['Active Cases'].iloc[::n], name="Active Cases",text="{0} Active Cases".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': "black"},type='bar')
    critical_bar = go.Bar(x=df['date'].iloc[::n], y=df['Critical Cases'].iloc[::n], name="Critical Cases",text="{0} Critical Cases".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': CRITICAL_COLOR},type='bar')
    tests_bar = go.Bar(x=df['date'].iloc[::n], y=df['Tests'].iloc[::n], name="Tests",text="{0} Tests".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': "orange"},type='bar')

    data = [cases_trace, deaths_trace, recovered_trace, active_trace, critical_trace,tests_trace,cases_bar,deaths_bar,recovered_bar,active_bar,critical_bar,tests_bar]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, True, True,True,True,boolean,False,False,False,False,False,False],
                           'showlegend': [True, True, True,True,True,boolean,False,False,False,False,False,False]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False,False,False,False,True,True, True,True,True,boolean],
                           'showlegend': [False, False, False,False,False,False,True,True, True,True,True,boolean]}],
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

    title = "<b> Total : {0} </b>".format(country)
    layout = go.Layout(
        updatemenus=updatemenus,

        title={
            'text': title,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size':30},
        plot_bgcolor = PAGE_COLOR,
        paper_bgcolor=PAGE_COLOR,
        autosize=True,
        xaxis=dict(rangeslider=dict(
            visible=False
        )),
        yaxis=dict(autorange=True)

    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        barmode="group",
        font_color="black",
        font_family="Courier New",
        title_font_family="Times New Roman",
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',showgrid=False, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',showgrid=False, zeroline=False, type=scale)
    graph= dcc.Graph(figure=fig, style={"background-color":PAGE_COLOR})
    return graph

def get_deaths_graph(df,country,scale):
    n=14
    if country =='World':
        country = "{0} Worldwide".format(FLAGS[country])
    else:
        country = "{1} {0}".format(country,FLAGS[country])

    deaths_trace = go.Scattergl(x=df["date"], y=df['Total Deaths'], showlegend=True, line=dict(color=DEATHS_COLOR), connectgaps=True,
                             name="Total Deaths", mode='lines',text="{0} Total Deaths".format(country),hoverinfo='x+y+text' )

    new_deaths_trace = go.Scattergl(x=df["date"], y=df['Deaths (24hrs)'], showlegend=True, line=dict(color="darkblue"), connectgaps=True,
                             name="New Deaths", mode='lines',text="{0} New Deaths".format(country),hoverinfo='x+y+text' )

    per_mil_trace = go.Scattergl(x=df["date"], y=df['Deaths/1M'], showlegend=True, line=dict(color="black"), connectgaps=True,
                             name="Deaths/1M",  mode='lines',text="{0} Deaths/1M".format(country),hoverinfo='x+y+text')


    deaths_bar = go.Bar(x=df['date'].iloc[::n], y=df['Total Deaths'].iloc[::n], name="Total Deaths",text="{0} Total Deaths".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': DEATHS_COLOR},type='bar')
    new_deaths_bar = go.Bar(x=df['date'].iloc[::n], y=df['Deaths (24hrs)'].iloc[::n], name="New Deaths",text="{0} New Deaths".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': "darkblue"},type='bar')
    per_mil_bar = go.Bar(x=df['date'].iloc[::n], y=df['Deaths/1M'].iloc[::n], name="Deaths/1M",text="{0} Deaths/1M".format(country),hoverinfo='x+y+text',visible=False,
                                  marker={'color': "black"},type='bar')

    data = [deaths_trace, new_deaths_trace, per_mil_trace,deaths_bar,new_deaths_bar,per_mil_bar]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, True, True,False,False,False],
                           'showlegend': [True, True, True,False,False,False]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, True,True,True],
                           'showlegend': [False, False, False,True,True,True]}],
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

    title = "<b> Deaths : {0} </b>".format(country)
    layout = go.Layout(
        updatemenus=updatemenus,

        title={
            'text': title,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size':30},
        plot_bgcolor = PAGE_COLOR,
        paper_bgcolor=PAGE_COLOR,
        autosize=True,
        xaxis=dict(rangeslider=dict(
            visible=False
        )),
        yaxis=dict(autorange=True)

    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        barmode="group",
        font_color="black",
        font_family="Courier New",
        title_font_family="Times New Roman",
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black',showgrid=False, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black',showgrid=False, zeroline=False, type=scale)
    graph= dcc.Graph(figure=fig, style={"background-color":PAGE_COLOR})
    return graph

def get_cases_graph(df, country, scale):

    n = 14
    if country == 'World':
        country = "{0} Worldwide".format(FLAGS[country])
    else:
        country = "{1} {0}".format(country, FLAGS[country])
    cases_trace = go.Scattergl(x=df["date"], y=df['Total Cases'], showlegend=True, line=dict(color=DEATHS_COLOR),
                               connectgaps=True,
                               name="Total Cases", mode='lines', text="{0} Total Cases".format(country),
                               hoverinfo='x+y+text')

    new_trace = go.Scattergl(x=df["date"], y=df['Cases (24hrs)'], showlegend=True, line=dict(color='darkblue'),
                                connectgaps=True,
                                name="New Cases", mode='lines', text="{0} New Cases".format(country),
                                hoverinfo='x+y+text')

    active_trace = go.Scattergl(x=df["date"], y=df['Active Cases'], showlegend=True, line=dict(color="black"),
                                connectgaps=True,
                                name="Active Cases", mode='lines', text="{0} Active Cases".format(country),
                                hoverinfo='x+y+text')

    critical_trace = go.Scattergl(x=df["date"], y=df['Critical Cases'], showlegend=True,
                                  line=dict(color=CRITICAL_COLOR), connectgaps=True,
                                  name="Critical Cases", mode='lines',
                                  text="{0} Critical Cases".format(country), hoverinfo='x+y+text')
    per_mil_trace = go.Scattergl(x=df["date"], y=df['Cases/1M'], showlegend=True,
                                  line=dict(color="#83D12E"), connectgaps=True,
                                  name="Cases/1M", mode='lines',
                                  text="{0} Cases/1M".format(country), hoverinfo='x+y+text')


    cases_bar = go.Bar(x=df['date'].iloc[::n], y=df['Total Cases'].iloc[::n], name="Total Cases",
                       text="{0} Total Cases".format(country), hoverinfo='x+y+text', visible=False,
                       marker={'color': DEATHS_COLOR}, type='bar')
    new_bar = go.Bar(x=df['date'].iloc[::n], y=df['Cases (24hrs)'].iloc[::n], name="New Cases",
                           text="{0} New Cases".format(country), hoverinfo='x+y+text', visible=False,
                           marker={'color': "darkblue"}, type='bar')
    active_bar = go.Bar(x=df['date'].iloc[::n], y=df['Active Cases'].iloc[::n], name="Active Cases",
                        text="{0} Active Cases".format(country), hoverinfo='x+y+text', visible=False,
                        marker={'color': "black"}, type='bar')
    critical_bar = go.Bar(x=df['date'].iloc[::n], y=df['Critical Cases'].iloc[::n], name="Critical Cases",
                          text="{0} Critical Cases".format(country), hoverinfo='x+y+text', visible=False,
                          marker={'color': CRITICAL_COLOR}, type='bar')
    per_mil_bar = go.Bar(x=df['date'].iloc[::n], y=df['Cases/1M'].iloc[::n], name="Cases/1M",
                          text="{0} Cases/1M".format(country), hoverinfo='x+y+text', visible=False,
                          marker={'color': "#83D12E"}, type='bar')

    data = [cases_trace, new_trace, active_trace, critical_trace,per_mil_trace, cases_bar,
            new_bar, active_bar, critical_bar,per_mil_bar]

    updatemenus = list([
        dict(
            buttons=list([
                dict(
                    args=[{'visible': [True, True, True, True,True,False, False, False, False, False],
                           'showlegend': [True, True, True, True,True,False, False, False, False, False]}],
                    label='Line',
                    method='update'
                ),
                dict(
                    args=[{'visible': [False, False, False, False, False,True, True, True, True, True],
                           'showlegend': [False, False, False, False, False,True, True, True, True, True]}],
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

    title = "<b> Cases : {0} </b>".format(country)
    layout = go.Layout(
        updatemenus=updatemenus,

        title={
            'text': title,
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font_size': 30},
        plot_bgcolor=PAGE_COLOR,
        paper_bgcolor=PAGE_COLOR,
        autosize=True,
        xaxis=dict(rangeslider=dict(
            visible=False
        )),
        yaxis=dict(autorange=True)

    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(
        barmode="group",
        font_color="black",
        font_family="Courier New",
        title_font_family="Times New Roman",
    )
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black', showgrid=False, zeroline=False)
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black', showgrid=False, zeroline=False, type=scale)
    graph = dcc.Graph(figure=fig, style={"background-color": PAGE_COLOR})
    return graph

def get_graphs(df, country,scale):
    total_graph= get_total_graph(df,country,scale)
    deaths_graph = get_deaths_graph(df,country,scale)
    cases_graph = get_cases_graph(df, country, scale)
    return  [(dbc.Row(dbc.Col(total_graph,className='col-lg-10 col-md-12 col-sm-12 col-12 '),justify='center')),
             html.Br(),
             dbc.Row([dbc.Col(cases_graph,className='col-lg-6 col-md-12 col-sm-12 col-12 '),
                      dbc.Col(deaths_graph, className='col-lg-6 col-md-12 col-sm-12 col-12 ')],justify='center')]

menu_tabs = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Summary", id='summary', tab_id="summary",),
                dbc.Tab(label="Map", tab_id="map"),
                dbc.Tab(label="Graph", tab_id="graph"),
            ],
            id="menu_tabs",
            active_tab="summary",
        ),
        html.Div(get_summary_menu(), style=SHOW, id='summary_menu'),
        html.Div(get_map_menu(), style=HIDE,id='map_menu'),
        html.Div(get_graph_menu(), style=HIDE, id='graph_menu'),
        html.Br(),
        html.Div(id="content"),
        html.Br(),
        html.Div(footer)
    ]
,fluid=True,style={"margin": "20px 40px 0px 20px"})

app.layout=html.Div([
    menu_tabs])

@app.server.route('/static/<path:path>')
def static_file(path):
    static_folder = os.path.join(os.getcwd(), 'static')
    return send_from_directory(static_folder, path)

@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-search", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@functools.lru_cache()
@app.callback(
    [Output("summary_menu", "style"),
     Output("map_menu", "style"),
     Output("graph_menu", "style"),
     Output("content", "children"),
     Output("map-content", "children")],
    [Input("menu_tabs", "active_tab"),
     Input("radioitems","value"),
     Input("select-country","value"),
     Input("select-scale","value"),
     Input("select-map-type","value"),
     Input("select-map-condition","value"),
     Input("select-map-option","value")
     ])
def switch_tab(at,radio,country,scale,map_type,map_condition,map_option):

    if at == "summary":
        return SHOW,HIDE,HIDE, get_summary(radio),[]
    elif at == "map":
        return HIDE,SHOW,HIDE,[],get_map(map_type,map_condition,map_option)
    elif at == 'graph':
        return HIDE,HIDE,SHOW,get_graphs(get_timeseries(country),country, scale),[]

if __name__=='__main__':
    app.run_server(port=2131)