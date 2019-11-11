import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import State, Input, Output
import plotly.graph_objs as go

from getFromDb import getDFfromDB

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

MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiZGZ5ejg1IiwiYSI6ImNrMjV5YnlpZTBnNDIzbmt4a3A3OW9qbDYifQ.fmYKw9jhF5XKNnUh8nkyAA"
MAPBOX_STYLE = "mapbox://styles/dfyz85/ck2uhftc60a6n1cn9knp63m13"

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Link", href="#")),
        dbc.DropdownMenu(
            nav=True,
            in_navbar=True,
            label="Menu",
            children=[
                dbc.DropdownMenuItem("Entry 1"),
                dbc.DropdownMenuItem("Entry 2"),
                dbc.DropdownMenuItem(divider=True),
                dbc.DropdownMenuItem("Entry 3"),
            ],
        ),
    ],
    brand="Demo",
    brand_href="#",
    sticky="top",
)

graph = dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )

df = getDFfromDB()
map_data2 = [go.Scattergeo(
                    lat=df['lat'],
                    lon=df['lon'],
                    text=df['name'],
                    mode='markers',
                    opacity=0.7,
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
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 4,
                        
                    },
                ) for i in range(len(df.index))]

map_layout_mapbox = {
    "mapbox": {
        "accesstoken": MAPBOX_ACCESS_TOKEN,
        "style": MAPBOX_STYLE,
        "center": {"lat": 45},
    },
    "showlegend": False,
    "autosize": True,
    "paper_bgcolor": "#1e1e1e",
    "plot_bgcolor": "#1e1e1e",
    "margin": {"t": 0, "r": 0, "b": 0, "l": 0},
}

map_graph = html.Div(
    id="world-map-wrapper",
    children=[
        dcc.Graph(
            id="world-map",
            figure={"data": map_data2, "layout": map_layout},
            config={"displayModeBar": False, "scrollZoom": False},
        ),
    ],
)
map_graph_mapbox = html.Div(
    id="world-map-wrapper-mapbox",
    children=[
        dcc.Graph(
            id="world-map-mapbox",
            figure={"data": map_data2_mapbox, "layout": map_layout_mapbox},
            config={"displayModeBar": False, "scrollZoom": False},
        ),
    ],
)

form2 = dbc.Container([
    map_graph_mapbox,
    map_graph
],
className="mt-4"
)

app.layout = html.Div([navbar, form2])

if __name__ == '__main__':
    app.run_server(debug=True,port=80)