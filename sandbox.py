import pandas as pd
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
from getFromDb import getVesselsFromDB, getDFfromDB
from tools.dashboardtools import tanks, vesselspositionScat, vesselspositionMapbox

dfVessels  = getDFfromDB()#'local'
#external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(
    #external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
 )
server = app.server #For Digital ocean
mapOffLine = 'http://localhost/assets/'
#SIDEBAR
sidebar_header = dbc.Row(
    [
        dbc.Col(html.Img(src='/assets/logo.gif', id='brand-logo')),
        dbc.Col(
            html.Button(
                # use the Bootstrap navbar-toggler classes to style the toggle
                html.Span(className="navbar-toggler-icon"),
                className="navbar-toggler",
                # the navbar-toggler classes don't set color, so we do it here
                style={
                    "color": "white",
                    "border-color": "white",
                },
                id="toggle",
            ),
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
    ]
 )

vesselsName = getVesselsFromDB()#'local'
vesselsNameLink = dcc.Dropdown( 
    id="navbar-vessel-name",
    options=[
        {'label': f"{vesselsName[x]['label']}", 'value': f"{vesselsName[x]['value']},{vesselsName[x]['label']}"} for x in range(len(vesselsName))
    ],
    value='',
    placeholder="Select vessel.",
    className='m-0',
    style={'color':'black'}
  )
#veseelsCharterLink = dcc.Dropdown(style={'color':'black'})
#veseelsGroupLink = dcc.Dropdown(style={'color':'black'})
sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "A responsive sidebar layout with collapsible navigation "
                    "links.",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    # html.P('Group filter'),
                    # veseelsGroupLink,
                    # html.P('Charter filter'),
                    # veseelsCharterLink,
                     html.P('Vessel filter'),
                    vesselsNameLink,
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
 )

#CONTENT
vesselNameContent = dbc.Col(
    dbc.Label(
        'FLEET',
         id='vessel-name-content'
    ),
    className='col-sm-12 pl-2 label-background-grey',
    id='vessel-name-content-div'
 )
tankHFO = tanks(180,'HFO','tons','black',110)
tankMGO = tanks(100,'MGO','tons','#ef647c',50)
tankFwater = tanks(150,'Fresh Water','tons','blue',70)
tankSewageBilge = tanks(80,'Sewage','tons','brown',5)
#tempME 
#Vessels MAP-BOX
vesselsPositionMap = dbc.Container(
        dbc.Row(
            dbc.Col(
                html.Div(
                    id="world-map-wrapper-mapbox",
                    children=[
                        dcc.Graph(
                            className="main-wrapper",
                            id="world-map-mapbox",
                            figure=vesselspositionMapbox(dfVessels),
                            config={"displayModeBar": False, "scrollZoom": False},
                            ),  
                        ],
                    ),
                    className = "p-0"
                )
            ),
        fluid=True,
        className = "p-0")
content = html.Div(
    [
        dbc.Row(vesselNameContent),
        dbc.Tabs(
            [
                dbc.Tab(
                    [
                        dbc.Container(
                        [
                            dbc.Row(vesselsPositionMap),
                        ],
                        fluid=True)
                    ],
                    label="Map"),
                dbc.Tab(
                    [
                        dbc.Container(
                        [
                            dbc.Row([tankHFO,tankMGO,tankFwater,tankSewageBilge]),
                            dbc.Row([])
                        ],
                        fluid=True)
                    ],
                    label="Engine room",
                ),
                dbc.Tab(label="Wekly report")
            ]
        ),
    ],
    id="page-content")
app.layout = html.Div(
    [
        dcc.Store(
            id = 'store-data',
            data = {'vessels-position': dict(dfVessels) }
         ),
        sidebar, 
        content
     ]
 )

@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
 )
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback([Output('vessel-name-content','children'),
              Output('world-map-mapbox','figure')],
              [Input('navbar-vessel-name', 'value')],
              [State('store-data','data')])
def display_label(value,data):
    if value:
        df = pd.DataFrame(data['vessels-position'])
        #vesselPosition = df.loc[df['name'].str.contains(value.split(',')[1])]
        return str(f"MV {value.split(',')[1]}"), vesselspositionMapbox(df,value)
    else: 
        return 'FLEET', vesselspositionMapbox(data['vessels-position'])

if __name__ == "__main__":
    app.run_server(debug=False,port=8080,host="0.0.0.0")
