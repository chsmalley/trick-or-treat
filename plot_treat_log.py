import pandas as pd
import sys


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