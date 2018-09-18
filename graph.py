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



load_heart_data()
