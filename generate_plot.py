import plotly.graph_objects as go
import pandas as pd
import sys
import os 
from data_object import Data
from data_object import load


def generate_plot(args):

    utrecht = load()
    table = utrecht.display()
    dic = {}

    for i in table.index.unique(level='VarName'):
        dic[i] = table.loc[(i, )]

    # Generate a figure object to store the plots
    fig = go.Figure()
    fig.update_layout(
        title='Datalog',
        legend_title_text='Logged Tags',
        xaxis=dict(rangeslider=dict(visible=True))
    )
    fig.update_xaxes(title_text='Time')
    fig.update_yaxes(title_text='Value')

    # Iterate through the tags and add them to the graph
    # All lines are hidden to start and are shown by clicking in the legend
    for key in dic.keys():
        fig.add_trace(
            go.Scatter(
                x=dic[key].index, 
                y=dic[key]['VarValue'],
                name=key,
                visible='legendonly'
            )
        )

    # Convert figure to interactive html to run in browser
    name = args[1].split('.')[0]
    fig.write_html(f'{name}.html')

    # Automatically opens the graph once script has run
    os.system(f"start {name}.html")



if __name__ == '__main__':
    generate_plot(sys.argv)