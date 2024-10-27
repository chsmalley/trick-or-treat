from flask import Flask, render_template, jsonify
from flask.logging import default_handler
import plotly.graph_objs as go
import pandas as pd
import datetime
import re
import json
# import picamera
import os
import time
import io
import subprocess

HALLOWEEN_FILE = '~/trick-or-treat/trick_or_treat.log'

app = Flask(__name__)


def parse_log_file():
    df = pd.read_csv(
        HALLOWEEN_FILE,
        names=["datetime", "loglevel", "type"]
    )
    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y:%m:%d:%H:%M:%S")
    df.set_index("datetime", drop=False, inplace=True)
    df["treats"] = df["type"] == "treat"
    df["tricks"] = df["type"] == "trick"
    # timestamps = []
    # log_events = []

    # with open(HALLOWEEN_FILE, 'r') as file:
    #     for line in file:
    #         match = re.search(r'(\d{4}:\d{2}:\d{2}:\d{2}:\d{2}:\d{2}) (\w{4}) (\w+)', line)
    #         if match:
    #             timestamp_str, level, event = match.groups()
    #             print(f"timestamp_str: {timestamp_str}")
    #             print(f"level: {level}")
    #             print(f"event: {event}")
    #             timestamps.append(datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S"))
    #             log_events.append(event)

    # return timestamps, log_events
    return df

@app.route('/data')
def data():
    data_df = parse_log_file()
    df_tmp = data_df[["tricks", "treats"]].groupby(
            pd.Grouper(freq="15Min")).sum()
    result = {
        'dates': df_tmp.index.astype(str).tolist(),
        'tricks': df_tmp['tricks'].tolist(),
        'treats': df_tmp['treats'].tolist()
    }
    # timestamps, log_events = parse_log_file()
    # level_counts = {level: log_events.count(level) for level in set(log_levels)}
    # print(data_df.to_json())
    # return jsonify(level_counts)
    # return data_df.to_json()
    return json.dumps(result)

@app.route('/plot')
def plot():
    # df = pd.read_json(parse_log_file())
    df = parse_log_file()
    # _, log_levels = parse_log_file()
    # level_counts = {level: log_levels.count(level) for level in set(log_levels)}

    # fig = go.Figure(data=[
    #     go.Bar(x=list(level_counts.keys()), y=list(level_counts.values()), marker_color=['green', 'red', 'orange'])
    # ])
    
    # fig.update_layout(title='Log Level Counts',
    #                   xaxis_title='Log Level',
    #                   yaxis_title='Counts')

    # return fig.to_html(full_html=False)
    df_tmp = df[["tricks", "treats"]].groupby(
            pd.Grouper(freq="15Min")).sum()
    
    # Creating a Plotly figure for the data
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_tmp.index,
        y=df_tmp['tricks'],
        name='Tricks'
    ))
    fig.add_trace(go.Bar(
        x=df_tmp.index,
        y=df_tmp['treats'],
        name='Treats'
    ))

    fig.update_layout(
        title='Halloween Results',
        xaxis_title='Datetime',
        yaxis_title='Count',
        xaxis=dict(
            tickformat='%Y-%m-%d %H:%M:%S',  # Format of the x-axis datetime labels
            tickmode='auto',
            nticks=20  # Number of ticks on the x-axis
        )
    )

    # Convert the Plotly figure to HTML and pass to template
    plot_div = fig.to_html(full_html=False)
    return render_template('index.html', plot_div=plot_div)

# Route to display time series plot
@app.route('/')
def index():
    df = pd.read_csv(
        HALLOWEEN_FILE,
        names=["datetime", "loglevel", "type"]
    )
    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y:%m:%d:%H:%M:%S")
    df.set_index("datetime", drop=False, inplace=True)
    df["treats"] = df["type"] == "treat"
    df["tricks"] = df["type"] == "trick"
    df_tmp = df[["tricks", "treats"]].groupby(
            pd.Grouper(freq="15Min")).sum()
    
    # Creating a Plotly figure for the data
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_tmp.index,
        y=df_tmp['tricks'],
        name='Tricks'
    ))
    fig.add_trace(go.Bar(
        x=df_tmp.index,
        y=df_tmp['treats'],
        name='Treats'
    ))

    fig.update_layout(
        title='Halloween Results',
        xaxis_title='Datetime',
        yaxis_title='Count',
        xaxis=dict(
            tickformat='%Y-%m-%d %H:%M:%S',  # Format of the x-axis datetime labels
            tickmode='auto',
            nticks=20  # Number of ticks on the x-axis
        )
    )

    # Convert the Plotly figure to HTML and pass to template
    plot_div = fig.to_html(full_html=False)
    return render_template('index.html', plot_div=plot_div)



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

