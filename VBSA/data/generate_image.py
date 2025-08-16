import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import plotly.io as pio

# import variable of another python script
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent / 'src'))
from main import strategy_1, strategy_2, repeated
sys.path.insert(0, str(script_dir.parent / 'data'))

df = pd.read_csv("results.csv")
header = list(df.columns)
# strategy_1 = header[0].split('.')[0]
# strategy_2 = header[2].split('.')[0]
parameters_1 = strategy_1.parameter_list

strategy_1 = str(strategy_1)
strategy_2 = str(strategy_2)

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

# ---------------------- surface plot strategy_1 ---------------------- 
fig = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix1,
    colorscale=colorscale,
    cmin=zmin, cmax=zmax,
    # colorbar=dict(title="Points", len=0.75, x=0.45)
    )
)

fig.update_layout(
    title=dict(
        text=strategy_1,
        x=0.5,
        xanchor="center"
    ),
    scene=dict(
        xaxis_title=strategy_1,
        yaxis_title=strategy_2,
        zaxis_title="Points"
    ),
    margin=dict(l=0, r=0, b=0, t=40)  # reduce padding cuts
)

fig.write_image(f"plots/{strategy_1}_vs_{strategy_2}_1.png")

# ---------------------- surface plot strategy_2 ---------------------- 
fig = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix2,
    colorscale=colorscale,
    showscale=False,
    cmin=zmin, cmax=zmax,
    # colorbar=dict(title="Points", len=0.75, x=0.55)
    )
)

fig.update_layout(
    title=dict(
        text=strategy_2,
        x=0.5,
        xanchor="center"
    ),
    scene=dict(
        xaxis_title=strategy_1,
        yaxis_title=strategy_2,
        zaxis_title="Points"
    ),
    margin=dict(l=0, r=0, b=0, t=40)  # reduce padding cuts
)

fig.write_image(f"plots/{strategy_1}_vs_{strategy_2}_2.png")

# ---------------------- surface plot overall (mean) ---------------------- 
matrix3 = np.mean(np.array([matrix1, matrix2]), axis=0)
overall_zmin = 0 # matrix3.min()
overall_zmax = zmax # matrix3.max()

fig = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale,
    showscale=False,
    cmin=overall_zmin, cmax=overall_zmax)
)

fig.update_layout(
    title=dict(
        text=f"{strategy_1} + {strategy_2}",
        x=0.5,
        xanchor="center"
    ),
    scene=dict(
        xaxis_title=strategy_1,
        yaxis_title=strategy_2,
        zaxis_title="Points"
    ),
    margin=dict(l=0, r=0, b=0, t=40)  # reduce padding cuts
)

fig.write_image(f"plots/{strategy_1}_vs_{strategy_2}_mean.png")

# ---------------------- surface plot overall (difference strategy1) ---------------------- 
matrix3 = matrix1-matrix2
diff_zmin = matrix3.min()
diff_zmax = zmax # matrix4.max()

# combine difference surface with plane at z=0
fig = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale,
    showscale=False,
    cmin=diff_zmin, cmax=diff_zmax)
)

# Then, add the z=0 plane (same x and y, z = 0)
fig.add_trace(go.Surface(
    x=list1, y=list2,
    z=np.zeros_like(matrix3),  # plane at z=0
    showscale=False,
    opacity=0.4,  # semi-transparent
    colorscale=[[0, 'gray'], [1, 'gray']],
    name='z=0 Plane'),
)

fig.update_layout(
    title=dict(
        text=f"{strategy_1} - {strategy_2}",
        x=0.5,
        xanchor="center"
    ),
    scene=dict(
        xaxis_title=strategy_1,
        yaxis_title=strategy_2,
        zaxis_title="Points"
    ),
    margin=dict(l=0, r=0, b=0, t=40)  # reduce padding cuts
)

fig.write_image(f"plots/{strategy_1}_vs_{strategy_2}_diff1.png")

# ---------------------- surface plot overall (difference strategy2) ---------------------- 
matrix3 = matrix2-matrix1
diff_zmin = matrix3.min()
diff_zmax = zmax # matrix4.max()

# combine difference surface with plane at z=0
fig = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale,
    showscale=False,
    cmin=diff_zmin, cmax=diff_zmax)
)

# Then, add the z=0 plane (same x and y, z = 0)
fig.add_trace(go.Surface(
    x=list1, y=list2,
    z=np.zeros_like(matrix3),  # plane at z=0
    showscale=False,
    opacity=0.4,  # semi-transparent
    colorscale=[[0, 'gray'], [1, 'gray']],
    name='z=0 Plane'),
)

fig.update_layout(
    title=dict(
        text=f"{strategy_2} - {strategy_1}",
        x=0.5,
        xanchor="center"
    ),
    scene=dict(
        xaxis_title=strategy_1,
        yaxis_title=strategy_2,
        zaxis_title="Points"
    ),
    margin=dict(l=0, r=0, b=0, t=40)  # reduce padding cuts
)

fig.write_image(f"plots/{strategy_1}_vs_{strategy_2}_diff2.png")

print("finished")
