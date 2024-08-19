from flask import Flask, render_template, Response
import plotly.graph_objs as go
import pandas as pd
import picamera
import os
import time
import subprocess

HALLOWEEN_FILE = '~/trick_or_treat.log'
app = Flask(__name__)


def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Take a photo when pressing camera button
@app.route('/picture')
def take_picture():
    pi_camera.take_picture()
    return "None"

def generate():
    with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
        # Allow camera to warm up
        camera.start_preview()
        time.sleep(2)
        stream = io.BytesIO()
        for _ in camera.record_sequence(stream, format='mjpeg'):
            stream.seek(0)
            frame = stream.read()
            stream.seek(0)
            stream.truncate()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


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


@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

