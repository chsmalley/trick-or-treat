import pandas as pd
import sys


def get_sec(time_str):
    """Get seconds from time."""
    h, m, s = time_str["time"].split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)

def get_hour(time_str):
    """Get seconds from time."""
    h, m, s = time_str["time"].split(':')
    return h


if __name__ == "__main__":
    logfile = sys.argv[1]
    df = pd.read_csv(
        logfile,
        names=["datetime", "loglevel", "type"]
    )
    df["datetime"] = pd.to_datetime(df["datetime"], format="%Y:%m:%d:%H:%M:%S")
    df.set_index("datetime", drop=False, inplace=True)
    df["treats"] = df["type"] == "treat"
    df["tricks"] = df["type"] == "trick"
    ax = df[["tricks", "treats"]].groupby(
        pd.Grouper(freq="15Min")).sum().plot(kind="bar", rot=30, title="Tricks and Treats")
    fig = ax.get_figure()
    fig.savefig("treats.png")