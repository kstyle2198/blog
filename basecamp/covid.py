from django.shortcuts import render, redirect
# import plotly.graph_objs.scatter.Line as go
import plotly.graph_objects as go
import pandas as pd
from urllib.request import urlopen
import dash
from dash import dash_table
# import dash_table
from dash import html
# import dash_html_components as html
from dash import dcc
# import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash_extensions as de  # pip install dash-extensions


## add Lotties##
url = "https://assets6.lottiefiles.com/private_files/lf30_1KyL2Q.json"
options = dict(loop=True, autoplay=True, rendererSettings=dict(preserveAspectRatio='xMidYMid slice'))

## create DataFrame
sources = urlopen('https://covid19.who.int/WHO-COVID-19-global-data.csv').readlines()
deco_source = [x.decode('utf-8').rstrip('\n').split(',') for x in sources[1:]]
columns = ["date", "country_code", 'country', 'region', 'new_case', 'accum_case', 'new_death', 'accum_death', "None"]
df = pd.DataFrame(deco_source, columns = columns)
df = df.drop(columns='None')

app = dash.Dash(__name__)
# server = app.server

app.layout = html.Div([
    html.Div(de.Lottie(options=options, width="30%", height="30%", url=url)),
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[
                {'label': 'Korea', 'value': 'Republic of Korea'},
                {'label': 'Japan', 'value': 'Japan'},
                {'label': 'China', 'value': 'China'},
                {'label': 'India', 'value': 'India'},
                {'label': 'France', 'value': 'France'},
                {'label': 'Germany', 'value': 'Germany'},
                {'label': 'Italy', 'value': 'Italy'},
                {'label': 'Spain', 'value': 'Spain'},
                {'label': 'Sweden', 'value': 'Sweden'},
                {'label': 'UK', 'value': 'The United Kingdom'},
                {'label': 'USA', 'value': 'United States of America'},
                {'label': 'Brazil', 'value': 'Brazil'},
                {'label': 'Russia', 'value': 'Russian Federation'},
            ],
            value=['Republic of Korea'],
            multi=True,
        ),

        html.Br(),
        dcc.RadioItems(
            id='info-dropdown',
            options=[
                {'label': 'New Case', 'value': 'new_case'},
                {'label': 'New Death', 'value': 'new_death'},
                {'label': 'Cumul_Case', 'value': 'accum_case'},
                {'label': 'Cumul_Death', 'value': 'accum_death'},
            ],
            value='new_case',
            labelStyle={'display': 'inline-block'}
        ),

        html.Br(),
        html.Button(id='submit-button', n_clicks=0, children="Submit")
    ]),
    html.Div([
        dcc.Graph(
            id='graph-output', figure={}
        )
    ]),
    html.Div([
        dash_table.DataTable(
            id="my-datatable",
            columns = [
                {"name":i, "id":i, "deletable":True, "selectable":True, "hideable":True}
                if i == "country_code" or i == "None"
                else {"name":i, "id":i, "deletable":True, "selectable":True}
                for i in df.columns
            ],
            # data = df.to_dict('records'),
            editable=True,              # allow editing of data inside all cells
            filter_action="native",     # allow filtering of data by user ('native') or not ('none')
            sort_action="native",       # enables data to be sorted per-column by user or not ('none')
            sort_mode="single",         # sort across 'multi' or 'single' columns
            column_selectable="multi",  # allow users to select 'multi' or 'single' columns
            row_selectable="multi",     # allow users to select 'multi' or 'single' rows
            row_deletable=True,         # choose if user can delete a row (True) or not (False)
            selected_columns=[],        # ids of columns that user selects
            selected_rows=[],           # indices of rows that user selects
            page_action="native",       # all data is passed to the table up-front or not ('none')
            page_current=0,             # page number that user is on
            page_size=10,                # number of rows visible per page
            style_cell={                # ensure adequate header width when text is shorter than cell's text
                'minWidth': 95, 'maxWidth': 95, 'width': 95
            },
            style_cell_conditional=[  # align text columns to left. By default they are aligned to right
                {
                    'if': {'column_id': c},
                    'textAlign': 'center'
                } for c in ['date','country_code','country', 'region']
            ],
            style_data={  # overflow cells' content into multiple lines
                'whiteSpace': 'normal',
                'height': 'auto'
            },
        )
    ])
])

@app.callback(Output("graph-output", "figure"),
            [Input("submit-button", "n_clicks")],
            [State("country-dropdown", "value"),State("info-dropdown", "value")],
            prevent_initial_call=False)

def update_fig(n_clicks, input_value, input_info):
    data = []
    for value in input_value:
        dff = df[df['country'] == value]

        trace_line = go.Line(
            x=dff.date,
            y=dff["{}".format(input_info)],
            mode='line',
            name = value
        )
        data.append(trace_line)

    data = data

    layout = dict(
        title="Covid19 Visualization",
        height = 500,
        xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                            label="1m",
                            step="month",
                            stepmode="backward"),
                        dict(count=6,
                            label="6m",
                            step="month",
                            stepmode="backward"),
                        dict(count=1,
                            label="YTD",
                            step="year",
                            stepmode="todate"),
                        dict(count=1,
                            label="1y",
                            step="year",
                            stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
            )
    )
    return {
        "data": data,
        "layout": layout
    }

@app.callback(
    Output('my-datatable', 'data'),
    Input("submit-button", "n_clicks"),
    State("country-dropdown", "value"),
    prevent_initial_call=False)

def update_table(n_clicks, input_country):
    df2 = df.loc[df.country.isin(input_country)].sort_values('date', ascending=False)
    return df2.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=False)
