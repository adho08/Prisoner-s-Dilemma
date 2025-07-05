import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# data of strategy_1
list3 = df[df.columns[1]]
matrix1 = np.array(list3).reshape((n, m))

# data of strategy_2
list3 = df[df.columns[3]]
matrix2 = np.array(list3).reshape((n, m))

# shared colorscale of the two plots
colorscale = 'Plasma'
zmin = min(matrix1.min(), matrix2.min())
zmax = max(matrix1.max(), matrix2.max())

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}]],
    subplot_titles=("Strategy 1", "Strategy 2")
)

# ---------------------- surface plot strategy_1 ---------------------- 
fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix1,
    colorscale=colorscale,
    cmin=zmin, cmax=zmax,
    colorbar=dict(title="Z", len=0.75)),
    row=1, col=1
)

# ---------------------- surface plot strategy_2 ---------------------- 
fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix2,
    colorscale=colorscale,
    cmin=zmin, cmax=zmax,
    colorbar=dict(title="Z", len=0.75)
    ),
    row=1, col=2
)

fig.update_layout(
    scene=dict(
        aspectmode='cube',
        zaxis=dict(range=[zmin, zmax])
    ),
    scene2=dict(
        aspectmode='cube',
        zaxis=dict(range=[zmin, zmax])
    )
)

fig.show()
