import plotly.graph_objects as go
import pandas as pd
import sys
import os 



def generate_plot(args):

    # Data is saved to second argument if given
    if len(args) == 3:
        df = pd.read_csv(args[2], delimiter=';', low_memory=False, decimal=',')
    # Data is overwritten if only 1 arg given
    else:
        df = pd.read_csv(args[1], delimiter=';', low_memory=False, decimal=',')

    # Convert times to datetime
    df['TimeString'] = pd.to_datetime(df['TimeString'], format='%d.%m.%Y %H:%M:%S')

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