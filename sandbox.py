import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import State, Input, Output
import plotly.graph_objs as go

from getFromDb import getDFfromDB, getVesselsFromDB

class CustomDash(dash.Dash):
    def interpolate_index(self,**kwargs):
        kwargs['app_entry'] = """
                              <div id="react-entry-point">
                                  <div class="loader"></div>
                                  <div class="logo"> Briese</div>
                              </div>
                              """
        return '''<!DOCTYPE html>
                      <html>
                        <head>
                            {metas}
                            <title>{title}</title>
                            {favicon}
                            {css}
                            <link href="https://fonts.googleapis.com/css?family=Teko:700&display=swap" rel="stylesheet"> 
                        </head>
                        <body>
                            {app_entry}
                            <footer>
                                {config}
                                {scripts}
                                {renderer}
                            </footer>
                        </body>
                    </html>
        '''.format(app_entry=kwargs.get('app_entry'),
                                      config=kwargs.get('config'),
                                      scripts=kwargs.get('scripts'),
                                      renderer=kwargs.get('renderer'),
                                      metas=kwargs.get('metas'),
                                      css=kwargs.get('css'),
                                      favicon=kwargs.get('favicon'),
                                      title=kwargs.get('title')
                                      )

external_stylesheets = [dbc.themes.BOOTSTRAP]
dash.Dash.interpolate_index
app = CustomDash(__name__, external_stylesheets=external_stylesheets)
server = app.server

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiZGZ5ejg1IiwiYSI6ImNrMjV5YnlpZTBnNDIzbmt4a3A3OW9qbDYifQ.fmYKw9jhF5XKNnUh8nkyAA"
MAPBOX_STYLE = "mapbox://styles/dfyz85/ck25zcdt704wp1cn4otpx4hwt?optimize=true"
vesselsName = getVesselsFromDB()

vesselsNameLink = dcc.Dropdown(
    id="navbar-vessel-name",
    options=[
        {'label': f"{vesselsName[x]['label']}", 'value': f"{vesselsName[x]['value']}"} for x in range(len(vesselsName))
    ],
    placeholder="Select vessel."
)
navbarCheckBox = dcc.Checklist(
    options=[
        {'label': 'New York City', 'value': 'NYC'},
    ],
    id="navbar-checkbox",
    value=['NYC'],
    labelStyle={'display': 'inline-block'}
)  

navbar = dbc.NavbarSimple(
    children=[
        navbarCheckBox,
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        vesselsNameLink
    ],
    brand="ShipsMonitor",
    brand_href="#",
    sticky="top",
)

df = getDFfromDB()
map_data2 = [go.Scattergeo(
                    lat=df['lat'],
                    lon=df['lon'],
                    text=df['name'],
                    mode='markers',
                    opacity=1,
                    marker={
                        'size': 4,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                ) for i in range(len(df.index))]

map_layout = {
    "title": 'Feb. 2011 American Airline flight paths',
    "showlegend": False,
    "geo":{
        "scope": 'world',
        "projection": {
            "type":'equirectangular'
        },
        "showocean":True,
        "showsubunits":True,
        "showcoastlines":False,
        "showcountries":True,
        "boardercolor":"black",
        #"showrivers":True,
        "rivercolor": "blue",
        #"showlakes":True,
        "lakecolor": "blue",
        "showland": True,
        "landcolor": 'rgb(243,243,243)',
        "countrycolor": 'rgb(204,204,204)',
        #"lonaxis": { 'range': [-30, 60] },
        #"lataxis": { 'range': [30, 70] }
    }
}
map_data2_mapbox = [go.Scattermapbox(
                    lat=df['lat'],
                    lon=df['lon'],
                    text=df['name'],
                    hoverinfo="text+lon+lat",
                    mode="markers+text",
                    opacity=1,
                    textposition='top center',
                    textfont={
                        "color":"white"
                    },
                    marker={
                        'size': 6,
                        'color':'#228B22'                        
                    },
                ) for i in range(len(df.index))]

map_layout_mapbox = {
    "mapbox": {
        "accesstoken": MAPBOX_ACCESS_TOKEN,
        "style": MAPBOX_STYLE,
        "center": {"lat": 40, "lon":0},
        "zoom":3,
        "minzoom":3,
        "maxzoom":7
    },
    "showlegend": False,
    "autosize": True,
    #"paper_bgcolor": "#1e1e1e",
    #"plot_bgcolor": "#1e1e1e",
    "margin": {"t": 0, "r": 0, "b": 0, "l": 0},
}

map_graph = html.Div(
    id="world-map-wrapper",
    children=[
        dcc.Loading(
            dcc.Graph(
                id="world-map",
                figure={"data": map_data2, "layout": map_layout},
                config={"displayModeBar": False, "scrollZoom": False},
            )
         ),
    ],
)
map_graph_mapbox = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.Div(
                id="world-map-wrapper-mapbox",
                children=[
                    dcc.Graph(
                        className="main-wrapper",
                        id="world-map-mapbox",
                        figure={"data": map_data2_mapbox, "layout": map_layout_mapbox},
                        config={"displayModeBar": False, "scrollZoom": False},
                        ),  
                    ],
                ),
                className = "p-0"
            )
        ),
    fluid=True)

form2 = dbc.Container([
    map_graph_mapbox,
    map_graph
],
className="mt-4"
)
contentLayout = html.Div([navbar, map_graph_mapbox])
app.layout = contentLayout
# @app.callback(Output(component_id='world-map-wrapper-mapbox', component_property='children'),
#               [Input('navbar-checkbox', 'value')])
# def display_page(mapCheckbox):
#     if 'NYC' in mapCheckbox :
#         return [dcc.Graph(
#                         className="main-wrapper",
#                         id="world-map-mapbox",
#                         figure={"data": map_data2_mapbox, "layout": map_layout_mapbox},
#                         config={"displayModeBar": False, "scrollZoom": False},
#                         )]
#     else:
#         return []



if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=False,port=8080)
