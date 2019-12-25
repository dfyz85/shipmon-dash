import dash_daq as daq
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas

from getFromDb import getDFfromDB

def tanks(tankMax=100, tankLabel='Tank',tankUnits='tons',tankColor='blue',tankValue=0):
    bar = daq.Tank(
        className = 'ml-2 pb-2',
        showCurrentValue=True,
        min=0,
        max=tankMax,
        units=tankUnits,
        value=tankValue,
        label=tankLabel,
        labelPosition='top',
        color=tankColor
     )

    return dbc.Card(
                [
                    #dbc.CardHeader("Fuel"),
                    dbc.CardBody(bar, className='p-0'),
                    dbc.CardFooter("This is the footer"),
                ],
                className='m-1 mt-2'
            )

def vesselspositionScat(df):
    map_data = [go.Scattergeo(
                    lat=df['lat'],
                    lon=df['lon'],
                    text=df['name'],
                    mode='markers+text',
                    textposition='top center',
                    textfont={
                        "color":"Black",
                        "size":8    
                    },
                    opacity=1,
                    marker={
                        'size': 8,
                        'line': {'width': 1, 'color': 'white'}
                    },
                )]
    map_layout = {
        "title": 'Vessels positinon',
        "showlegend": False,
        "autosize": True,
        "margin": {"t": 0, "r": 0, "b": 0, "l": 0},
        #"width" : 1000,
        #"height" : 500,
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
            "lonaxis": { 'range': [-20, 40] },
            "lataxis": { 'range': [32, 67] }
        }
     }
    figure={"data": map_data, "layout": map_layout}
    return figure
def vesselspositionMapbox(df,vessel='deafult'):
    MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiZGZ5ejg1IiwiYSI6ImNrMjV5YnlpZTBnNDIzbmt4a3A3OW9qbDYifQ.fmYKw9jhF5XKNnUh8nkyAA"
    MAPBOX_STYLE = "mapbox://styles/dfyz85/ck25zcdt704wp1cn4otpx4hwt"
    map_data_mapbox = [go.Scattermapbox(
                    lat=df['lat'],
                    lon=df['lon'],
                    text=df['name'],
                    hoverinfo="text+lon+lat",
                    mode="markers+text",
                    opacity=1,
                    textposition='top center',
                    textfont={
                        "color":"white",
                        "size":8 
                    },
                    marker={
                        'size': 6,
                        'color':'#228B22'                  
                    },
                ) ]
    
    map_layout_mapbox = {
        "mapbox": {
            "accesstoken": MAPBOX_ACCESS_TOKEN,
            "style": MAPBOX_STYLE,
            "center": {"lat": 50, "lon":0},
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
    if not vessel=='deafult':
        dff = df.loc[df['name'].str.contains(vessel.split(',')[1])]
        map_data_mapbox.append(go.Scattermapbox(
                    lat=dff['lat'],
                    lon=dff['lon'],
                    text=dff['name'],
                    hoverinfo="text+lon+lat",
                    mode="markers+text",
                    opacity=1,
                    textposition='top center',
                    textfont={
                        "color":"white",
                        "size":12,
                    },
                    marker={
                        'size': 10,
                        'color':'red'                   
                    },
                ))
        map_layout_mapbox['mapbox']['center'] = {'lat':int(float(dff['lat'].values[0])), 'lon':int(float(dff['lon'].values[0]))}
    figure={"data": map_data_mapbox, "layout": map_layout_mapbox}
    return figure
    