import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv("results.csv")

# parameter axes
list1 = df[df.columns[0]].to_numpy().tolist()
list2 = df[df.columns[2]].to_numpy().tolist()

# make elements unique
list1 = list(set(list1))
list2 = list(set(list2))

n, m = len(list1), len(list2)

list3 = df[df.columns[1]]
matrix3 = np.array(list3).reshape((n, m))


fig = go.Figure(go.Surface(
    # contours = {
    #     "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color":"white"},
    #     "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05}
    # },
    x = list1,
    y = list2,
    z = matrix3
    ))
fig.update_layout(
        scene = dict(
            xaxis = dict(nticks=4, range=[0,10],),
            yaxis = dict(nticks=4, range=[0,10],),
            zaxis = dict(nticks=4, range=[0,100],),),
        width=700, height = 700,
        margin=dict(r=20, l=10, b=10, t=10)
        )

fig.show()
