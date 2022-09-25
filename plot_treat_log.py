import pandas as pd
import sys


def get_sec(time_str):
    """Get seconds from time."""
    print(time_str)
    h, m, s = time_str["time"].split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


if __name__ == "__main__":
    logfile = sys.argv[1]
    df = pd.read_csv(
        logfile,
        names=["date", "time", "loglevel", "type"]
    )
    df["seconds"] = df.apply(get_sec, axis=1)
    tricks = df ["type"] == "trick"
    treat = df ["type"] == "treat"
    tricks.plot.hist(column=["seconds"], by="type")