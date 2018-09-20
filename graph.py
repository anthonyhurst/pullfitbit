import json
import pandas

def load_heart_data(filename="heart.json"):
    fh = open(filename, "r")
    content = fh.read()
    fh.close()
    obj = json.loads(content.strip())
    df = pandas.DataFrame.from_records(obj["activities-heart-intraday"]["dataset"])
    ax = df.plot()
    fig = ax.get_figure()
    fig.savefig("heart.pdf")

def load_sleep_data(filename="sleep.json"):
    fh = open(filename, "r")
    content = fh.read()
    fh.close()
    obj = json.loads(content.strip())
    dfs = []
    i = 0
    for session in obj["sleep"]:
        df_tmp = pandas.DataFrame.from_records(session["levels"]["data"])
        df_tmp["Session"] = i
        dfs.append(df_tmp)
        i+=1
    df = pandas.concat(dfs)
    colors = {
        "wake": "red",
        "rem": "lightblue",
        "deep": "darkblue",
        "light": "green",
    }
    df["color"] = df["level"].apply(lambda x: colors[x])
    df["dateTime"] = pandas.to_datetime(df['dateTime'])
    ax = df.plot(kind="bar", x="dateTime", y="seconds", color=df["color"], figsize=(50, 30))
    fig = ax.get_figure()
    fig.savefig("sleep.pdf")





load_heart_data()
load_sleep_data()
