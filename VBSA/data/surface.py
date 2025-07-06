import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# import variable of another python script
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent / 'src'))
from main import parameters_1, repeated
sys.path.insert(0, str(script_dir.parent / 'data'))

df = pd.read_csv("results.csv")
header = list(df.columns)
strategy_1 = header[0]
strategy_2 = header[2]

# parameter axes
list1 = df[df.columns[0]].to_numpy().tolist()[:len(parameters_1)*repeated:repeated]
list2 = df[df.columns[2]].to_numpy().tolist()[::len(parameters_1)*repeated]

n, m = len(list1), len(list2)

# data of strategy_1
list3 = df[df.columns[1]].to_numpy().tolist()
# calculate the mean of 'repeated' consecutive elements
list3 = np.array(list3).reshape(-1, repeated).mean(axis=1).tolist()
matrix1 = np.array(list3).reshape((m, n))

# data of strategy_2
list3 = df[df.columns[3]].to_numpy().tolist()
# calculate the mean of 'repeated' consecutive elements
list3 = np.array(list3).reshape(-1, repeated).mean(axis=1).tolist()
matrix2 = np.array(list3).reshape((m, n))

# shared colorscale of the two plots
colorscale = 'Plasma'
zmin = 0 # min(matrix1.min(), matrix2.min())
zmax = max(matrix1.max(), matrix2.max())

fig = make_subplots(
    rows=1, cols=3,
    specs=[[{'type': 'surface'}, {'type': 'surface'}, {'type': 'surface'}]],
    subplot_titles=(header[0], header[2], "Overall (Mean)")
)

# ---------------------- surface plot strategy_1 ---------------------- 
fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix1,
    colorscale=colorscale,
    cmin=zmin, cmax=zmax,
    colorbar=dict(title="Z", len=0.75, x=0.30)),
    row=1, col=1
)

# ---------------------- surface plot strategy_2 ---------------------- 
fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix2,
    colorscale=colorscale,
    cmin=zmin, cmax=zmax,
    showscale=False),
    row=1, col=2
)

# ---------------------- surface plot overall ((strategy_1 + strategy_2) / 2) ---------------------- 
matrix3 = np.mean(np.array([matrix1, matrix2]), axis=0)
overall_zmin = 0 # matrix3.min()
overall_zmax = zmax # matrix3.max()

fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale,
    cmin=overall_zmin, cmax=overall_zmax,
    colorbar=dict(title="Z", len=0.75, x=0.66)),
    row=1, col=3
)

# Define axis ranges
x_min, x_max = min(list1), max(list1)
y_min, y_max = min(list2), max(list2)

fig.update_layout(
    scene=dict(
        aspectmode='cube',
        xaxis=dict(
            title=dict(text=strategy_1),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2), 
            range=[y_min, y_max]),
        zaxis=dict(range=[zmin, zmax])
    ),
    scene2=dict(
        aspectmode='cube',
        xaxis=dict(
            title=dict(text=strategy_1),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2), 
            range=[y_min, y_max]),
        zaxis=dict(range=[zmin, zmax])
    ),
    scene3=dict(
        aspectmode='cube',
        xaxis=dict(
            title=dict(text=strategy_1),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2), 
            range=[y_min, y_max]),
        zaxis=dict(range=[overall_zmin, overall_zmax])
    )
)

fig.show()
