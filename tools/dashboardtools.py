import dash_daq as daq
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import json
import pandas as pd
import numpy as np
from shapely.geometry import shape, Point

from getFromDb import getDFfromDB
#Content tank visualization
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
#Use Plotly Graph
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
#Use Mapbox
def vesselspositionMapbox(df,vessel='deafult'):
    MAPBOX_ACCESS_TOKEN = "pk.eyJ1IjoiZGZ5ejg1IiwiYSI6ImNrMjV5YnlpZTBnNDIzbmt4a3A3OW9qbDYifQ.fmYKw9jhF5XKNnUh8nkyAA"
    MAPBOX_STYLE = "mapbox://styles/dfyz85/ck25zcdt704wp1cn4otpx4hwt"
    vesselNamess = df['name']
    latss = df['lat']
    lonss = df['lon']
    map_data_mapbox = [go.Scattermapbox(
                    lat=latss,
                    lon=lonss,
                    text=vesselNamess,
                    mode="markers+text",
                    opacity=1,
                    textposition='top center',
                    textfont={
                        "color":"white",
                        "size":8 
                    },
                    marker={
                        'size': 6,
                        'color':'#228B22',
                    },
                    hovertemplate =[(
                        "<b>Name:{} </b><br>" +
                        "IMO:{}<br>"+
                        "POSITION<br>"+
                        "Last update {} UTC<br>"+
                        "Longitude:{}<br>" +
                        "Latitude:{}<br>"+
                        "Status:{}  <br>"+
                        "Speed:{} <br>"+
                        "Course:{} <br>"+
                        "Trip from: {} <br>"+
                        "Trip to: {} <br>"+
                        "ETA(approximately): {}<br>"+
                        "CLASSIFICATION<br>"+
                        "Type:{}<br>"+
                        "Last:{}<br>"+
                        "Next:{}<br>"+
                        "<extra></extra>").format(vesselName,imo,time,lat,lon,status,speed,course,departure,arrival,eta,typeClass,registerLast,registerNext) for vesselName,imo,time,lat,lon,status,speed,course,departure,arrival,eta,typeClass,registerLast,registerNext in zip(vesselNamess,df['_id'],df['time'],latss,lonss,df['status'],df['speed'],df['course'],df['departure'],df['arrival'],df['eta'],df['registerType'],df['registerLast'],df['registerNext'])]
     )]
    map_layout_mapbox = {
        "mapbox": {
            "accesstoken": MAPBOX_ACCESS_TOKEN,
            "style": MAPBOX_STYLE,
            "center": {"lat": 50, "lon":10},
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
                    hovertemplate =[(
                        "<b>Name:{} </b><br>" +
                        "IMO:{}<br>"+
                        "POSITION<br>"+
                        "Last update {} UTC<br>"+
                        "Longitude:{}<br>" +
                        "Latitude:{}<br>"+
                        "Status:{}  <br>"+
                        "Speed:{} <br>"+
                        "Course:{} <br>"+
                        "Trip from: {} <br>"+
                        "Trip to: {} <br>"+
                        "ETA(approximately): {}<br>"+
                        "CLASSIFICATION<br>"+
                        "Type:{}<br>"+
                        "Last:{}<br>"+
                        "Next:{}<br>"+
                        "<extra></extra>").format(vesselName,imo,time,lat,lon,status,speed,course,departure,arrival,eta,typeClass,registerLast,registerNext) for vesselName,imo,time,lat,lon,status,speed,course,departure,arrival,eta,typeClass,registerLast,registerNext in zip(vesselNamess,df['_id'],df['time'],latss,lonss,df['status'],df['speed'],df['course'],df['departure'],df['arrival'],df['eta'],df['registerType'],df['registerLast'],df['registerNext'])]
                ))
        map_layout_mapbox['mapbox']['center'] = {'lat':int(float(dff['lat'].values[0])-5), 'lon':int(float(dff['lon'].values[0]))}
    figure={"data": map_data_mapbox, "layout": map_layout_mapbox}
    return figure
#Side-panel statistiks
def getVesselsStatistiks(df):
    with open('geodata/ECA-EU.geojson') as f:
        js1 = json.load(f)
    with open('geodata/ECA-US.geojson') as f:
        js2 = json.load(f)
    js = [js1,js2]
    vessels = df
    eca = 0
    divContent = []
    vesselsTotal = len(vessels.index)
    divContent.append(
         html.Div([
                    html.Span("Total vessels:"),
                    html.Span(vesselsTotal, className="badge badge-info nav-ridings-right"),
                    html.Hr(style={
                        'border-top':'1px solid white',
                        'margin-top': '0.5rem',
                        'margin-bottom': '0.5rem'
                    })
                ]))
    countStatus = df.groupby('status').name.nunique().to_dict()
    for i in countStatus:
        divContent.append(
            html.Div([
                    html.Span(f'{i} :'),
                    html.Span(countStatus[i], className="badge badge-info nav-ridings-right")
                ])
        )
    for x in range(len(vessels.index)):
        point = Point(float(vessels['lon'][x]), float(vessels['lat'][x]))
        for i in js:
            for feature in i['features']:
                polygon = shape(feature['geometry'])
                if polygon.contains(point):
                    eca = eca + 1
    
    divContent.append(
         html.Div([
                    html.Hr(style={
                        'border-top':'1px solid white',
                        'margin-top': '0.5rem',
                        'margin-bottom': '0.5rem'}),
                    html.Span("Vessels inside ECA zone:"),
                    html.Span(eca, className="badge badge-info nav-ridings-right")
                ]))

    return html.Div(divContent)                