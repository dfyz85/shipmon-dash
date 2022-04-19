import pandas as pd
import dash
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output, State
from getFromDb import getVesselsFromDB, getDFfromDB
from tools.dashboardtools import tanks, vesselspositionScat, vesselspositionMapbox, getVesselsStatistiks

#external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(
    __name__,
    external_scripts = [
        'https://api.mapbox.com/mapbox-gl-js/v2.6.1/mapbox-gl.js',
        'https://api.mapbox.com/mapbox-gl-js/plugins/mapbox-gl-draw/v1.2.2/mapbox-gl-draw.js'
    ],
    #external_stylesheets=external_stylesheets,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1, maximum-scale=1, user-scalable=0"},
        {'name': 'description','content': 'Fleet monitor Service for monitoring vessels. Crete by BRIESE CREW'},
    ],
    )
app.index_string = ''' <!DOCTYPE html>
            <html>
                <head>
                    {%metas%}
                    <title> Ship Monitor</title>
                    {%favicon%}
                    {%css%}
                </head>
                <body>
                    {%app_entry%}
                    <footer>
                        {%config%}
                        {%scripts%}
                        {%renderer%}
                    </footer>
                </body>
            </html> '''
server = app.server #For Digital ocean
mapOffLine = 'http://localhost/assets/'
#SIDEBAR
#'local' 
#veseelsCharterLink = dcc.Dropdown(style={'color':'black'})
#veseelsGroupLink = dcc.Dropdown(style={'color':'black'})
#CONTENT
# vesselNameContent = dbc.Col(
#     dbc.Label(
#         'FLEET',
#          id='vessel-name-content'
#     ),
#     className='col-sm-12 label-background-grey',
#     id='vessel-name-content-div'
#  )
tankHFO = tanks(180,'HFO','tons','black',110)
tankMGO = tanks(100,'MGO','tons','#ef647c',50)
tankFwater = tanks(150,'Fresh Water','tons','blue',70)
tankSewageBilge = tanks(80,'Sewage','tons','brown',5)
#tempME 
#Vessels MAP-BOX

def serve_layout():
    dfVessels  = getDFfromDB()#'local'
    vesselsName = getVesselsFromDB()
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
    vesselsNameLink = dbc.Row(
        dbc.Col(
            [
                dcc.Dropdown( 
                    id="navbar-vessel-name",
                    options=[
                        {'label': f"{vesselsName[x]['label']}", 'value': f"{vesselsName[x]['value']},{vesselsName[x]['label']}"} for x in range(len(vesselsName))
                    ],
                    value='',
                    placeholder="Select vessel.",
                    #className='m-0',
                    #style={'color':'black'}
                )
            ],
            className="dash-black px-3 pl-sm-0"
        ),
        className="m-0 py-1",
        style={'height': '7vh','min-height':'45px'}
     )
    vesselsStatistiks = html.Div(
        getVesselsStatistiks(dfVessels),
        className='pt-2',
        id="blurb",
     )
    vesselsMenu = dbc.Button(
        "Vessel menu", 
        id="vessel-menu", 
        color="primary", 
        block=True, 
        className='my-2',
        n_clicks=0,
        style={'visibility':'hidden'})
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
                            style={'height': '93vh'}
                            ),  
                        ],
                    #style={'margin-left': '0px','margin-top':'-10px'}
                    #style = {'display': 'inline-block', 'height': '100%'}
                    ),
                className = "p-0"
             ),
            className='m-0'     
         ),
        fluid=True,
        className = "p-0",
        )
    sidebar = html.Div(
        [
            sidebar_header,
            # we wrap the horizontal rule and short blurb in a div that can be
            # hidden on a small screen
            # use the Collapse component to animate hiding / revealing links
            dbc.Collapse(
                dbc.Nav(
                    [
                        # html.P('Group filter'),
                        # veseelsGroupLink,
                        # html.P('Charter filter'),
                        # veseelsCharterLink,
                        vesselsStatistiks,
                        vesselsMenu
                    ],
                    vertical=True,
                    pills=True,
                ),
                id="collapse",
            ),
        ],
        id="sidebar",
     )
    content = html.Div(
        [
            vesselsNameLink,
            vesselsPositionMap
            # dbc.Tabs(
            #     [
            #         dbc.Tab(
            #             [
            #                 dbc.Container(
            #                 [
            #                     dbc.Row(vesselsPositionMap),
            #                 ],
            #                 fluid=True)
            #             ],
            #             label="Map"),
            #         dbc.Tab(
            #             [
            #                 dbc.Container(
            #                 [
            #                     dbc.Row([tankHFO,tankMGO,tankFwater,tankSewageBilge]),
            #                     dbc.Row([])
            #                 ],
            #                 fluid=True)
            #             ],
            #             label="Engine room",
            #         ),
            #         dbc.Tab(label="Wekly report")
            #     ]
            # ),
        ],
        id="page-content",
        #style={'padding-right': '1px'}
     )
    return html.Div(
        [
            dcc.Location(id='url', refresh=False),
            dcc.Store(
                id = 'store-data',
                data = {'vessels-position': dict(dfVessels)}
            ),     
            sidebar, 
            content
        ],
        id="content"
     )
app.layout = serve_layout

@app.callback(
    Output("collapse", "is_open"),
    [Input("toggle", "n_clicks")],
    [State("collapse", "is_open")],
 )
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(Output('world-map-mapbox','figure'),
              [Input('navbar-vessel-name', 'value')],
              [State('store-data','data')])
def display_label(value,data):
    df = pd.DataFrame(data['vessels-position'])
    if value:
        #vesselPosition = df.loc[df['name'].str.contains(value.split(',')[1])]
        return vesselspositionMapbox(df,value)
    else:
        return vesselspositionMapbox(df)
        #return 'FLEET', vesselspositionMapbox(data['vessels-position'])

@app.callback(Output('world-map-wrapper-mapbox', 'children'),
              [Input('vessel-menu', 'n_clicks')],
              [State('store-data','data')])
def display_page(n,data):
    if n%2:
        return html.H3("You on VESSEL MENU")
    elif n:
        df = pd.DataFrame(data['vessels-position'])
        return dcc.Graph(
                    className="main-wrapper",
                    id="world-map-mapbox",
                    figure=vesselspositionMapbox(df),
                    config={"displayModeBar": False, "scrollZoom": False},
                ),
    else:
        raise PreventUpdate
    
if __name__ == "__main__":
    app.run_server(debug=True,port=8080,host="0.0.0.0")
