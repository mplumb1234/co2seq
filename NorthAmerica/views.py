from django.shortcuts import render
import plotly.graph_objects as go
from plotly.offline import plot
from NorthAmerica.util import load_dfs, get_traces_from_dfs

'''https://medium.com/analytics-vidhya/plotly-for-geomaps-bb75d1de189f
https://plotly.com/python/map-configuration/
https://plotly.com/python/bubble-maps/#bubble-map-with-goscattergeo'''


# Create your views here.
def NorthAmericaView(request):
    # add two dataframes
    dfs = load_dfs("Data")
    traces = get_traces_from_dfs(dfs)

    fig = go.Figure()

    for trace in traces:
        fig.add_trace(trace)

    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_mapboxes(center=go.layout.mapbox.Center(lat=40, lon=-99), zoom=3)

    fig.update_layout(
        legend=dict(
            x=1,
            y=1,
            traceorder="reversed",
            title_font_family="Times New Roman",
            font=dict(
                family="Courier",
                size=20,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=2
        )
    )

    map_plot = plot({'data': fig}, output_type='div')

    return render(request, 'northAmericanMap.html', context={'map_plot': map_plot})