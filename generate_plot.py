import plotly.graph_objects as go
import pandas as pd
import sys
import os 

from csv_processor import clean_data

def generate_plot(args):
    # Cleans commas 
    clean_data(args)

    # Clean data is saved to second arguement if given
    if len(args) == 3:
        df = pd.read_csv(args[2])
    # Clean data is overwritten if only 1 arg given
    else:
        df = pd.read_csv(args[1])

    # Pivot the dataframe so it is easier to select data by tag name
    table = pd.pivot_table(data=df, index=['VarName', 'TimeString'])

    # Find all unique device tags and store the data in a dictionary
    # Dictionary key = tag string
    # Dictionary value = dataframe with time and device value
    dic = {}
    for i in table.index.unique(level='VarName'):
        dic[i] = table.loc[(i, )]

    # Generate a figure object to store the plots
    fig = go.Figure()
    fig.update_layout(
        title='Datalog',
        legend_title_text='Logged Tags',
        xaxis=dict(rangeslider=dict(visible=True), type='category')
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
    fig.write_html('plotly_test.html')

    # Automatically opens the graph once script has run
    os.system("start plotly_test.html")



if __name__ == '__main__':
    generate_plot(sys.argv)