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
strategy_1 = header[0].split('.')[0]
strategy_2 = header[2].split('.')[0]

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
    rows=2, cols=2,
    specs=[[{'type': 'surface'}, {'type': 'surface'}], [{'type': 'surface'}, {'type': 'surface'}]],
    subplot_titles=(header[0], header[2], "Overall (Mean)", "Overall (Difference)")
)

# ---------------------- surface plot strategy_1 ---------------------- 
fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix1,
    colorscale=colorscale,
    cmin=zmin, cmax=zmax,
    colorbar=dict(title="Points", len=0.75, x=0.30)),
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

# ---------------------- surface plot overall (mean) ---------------------- 
matrix3 = np.mean(np.array([matrix1, matrix2]), axis=0)
overall_zmin = 0 # matrix3.min()
overall_zmax = zmax # matrix3.max()

fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale,
    cmin=overall_zmin, cmax=overall_zmax,
    colorbar=dict(title="Points", len=0.75, x=0.66)),
    row=2, col=1
)

# ---------------------- surface plot overall (difference) ---------------------- 
matrix4 = matrix2-matrix1
diff_zmin = matrix4.min()
diff_zmax = zmax # matrix4.max()

# combine difference sruface with plane at z=0
fig.add_trace(go.Surface(
    x=list1, y=list2, z=matrix4,
    colorscale=colorscale,
    cmin=diff_zmin, cmax=diff_zmax,
    colorbar=dict(title="Points", len=0.75, x=0.66)),
    row=2, col=2
)

# Then, add the z=0 plane (same x and y, z = 0)
fig.add_trace(go.Surface(
    x=list1, y=list2,
    z=np.zeros_like(matrix4),  # plane at z=0
    showscale=False,
    opacity=0.4,  # semi-transparent
    colorscale=[[0, 'gray'], [1, 'gray']],
    name='z=0 Plane'),
    row=2, col=2
)

# Define axis ranges
x_min, x_max = min(list1), max(list1)
y_min, y_max = min(list2), max(list2)

fig.update_layout(
    scene=dict(
        aspectmode='cube',
        xaxis=dict(
            title=dict(text=strategy_1), range=[x_min, x_max]),
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
    ),
    scene4=dict(
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=2),
        xaxis=dict(
            title=dict(text=strategy_1),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2), 
            range=[y_min, y_max]),
        zaxis=dict(range=[diff_zmin, diff_zmax])
    )
)

fig.show()
