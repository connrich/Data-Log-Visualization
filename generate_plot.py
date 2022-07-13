import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys

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

    table = pd.pivot_table(data=df, index=['VarName', 'TimeString'])

    # Find all unique device tags and store the data in a dictionary
    # Dictionary key = tag string
    # Dictionary value = dataframe with time and device value
    dic = {}
    for i in table.index.unique(level='VarName'):
        dic[i] = table.loc[(i, )]

    tag = 'PT565_Value'

    fig = px.line(x=dic[tag].index.tolist(), y=dic[tag]['VarValue'],
                    labels={
                        'x': 'Time',
                        'y': 'Value'
                    },
                    title=tag
    )

    # Fig = go.Figure()
    # Fig.add_trace(
    #     go.Scatter(x=dic[tag].index.tolist(), y=list(dic[tag]['VarValue']))
    # )

    # # Add range slider
    # Fig.update_layout(
    #     xaxis=dict(
    #         rangeselector=dict(
    #             buttons=list([
    #                 dict(count=1,
    #                     label="1m",
    #                     step="month",
    #                     stepmode="backward"),
    #                 dict(count=6,
    #                     label="6m",
    #                     step="month",
    #                     stepmode="backward"),
    #                 dict(count=1,
    #                     label="YTD",
    #                     step="year",
    #                     stepmode="todate"),
    #                 dict(count=1,
    #                     label="1y",
    #                     step="year",
    #                     stepmode="backward"),
    #                 dict(step="all")
    #             ])
    #         ),
    #         rangeslider=dict(
    #             visible=True
    #         ),
    #         type="date"
    #     )
    # )

    # Convert figure to interactive html to run in browser
    fig.write_html('plotly_test.html')



if __name__ == '__main__':
    generate_plot(sys.argv)