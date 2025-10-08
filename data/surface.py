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
from main import strategy_1, strategy_2, rounds, repeated
sys.path.insert(0, str(script_dir.parent / 'data'))

df = pd.read_csv("results.csv")
header = list(df.columns)
parameters_1 = strategy_1.parameter_list

strategy_1 = str(strategy_1)
strategy_2 = str(strategy_2)

if strategy_1[-2:] == "_2":
    strategy_1_title = strategy_1.replace("_2", "")
else:
    strategy_1_title = strategy_1

if strategy_2[-2:] == "_2":
    strategy_2_title = strategy_2.replace("_2", "")
else:
    strategy_2_title = strategy_2

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
zmin = 0 
zmax = max(matrix1.max(), matrix2.max())

fig = make_subplots(
    rows=3, cols=2,
    specs=[
        [{'type': 'surface'}, {'type': 'surface'}],
        [{'type': 'surface'}, {'type': 'surface'}],
        [{'type': 'surface'}, None]
    ],
    subplot_titles=(
        strategy_1, 
        strategy_2, 
        f"Overall (Difference {strategy_1_title} - {strategy_2_title})",
        f"Overall (Difference {strategy_2_title} - {strategy_1_title})",
        "Overall (Added)",
    )
)

# different colorscales
colorscale_s = 'Plasma'
colorscale_a = 'Portland'
colorscale_d = 'Cividis'

# ---------------------- surface plot strategy_1 ---------------------- 
srf_1 = go.Surface(
        x=list1, y=list2, z=matrix1,
        colorscale=colorscale_s,
        showscale=False,
        cmin=zmin, cmax=zmax,
    )

fig.add_trace(srf_1, row=1, col=1)

# ---------------------- surface plot strategy_2 ---------------------- 
srf_2 = go.Surface(
        x=list1, y=list2, z=matrix2,
        colorscale=colorscale_s,
        cmin=zmin, cmax=zmax,
        colorbar=dict(title="Points", len=0.75, x=0.50)
    )

fig.add_trace(srf_2, row=1, col=2)

# ---------------------- surface plot overall (added) ---------------------- 
matrix3 = matrix1 + matrix2
overall_zmin = 0 
overall_zmax = 2 * rounds 

srf_3 = go.Surface(
        x=list1, y=list2, z=matrix3,
        colorscale=colorscale_a,
        cmin=overall_zmin, cmax=overall_zmax,
        colorbar=dict(title="Points", len=0.75, x=0.01)
    )

fig.add_trace(srf_3, row=3, col=1)

# ---------------------- surface plot overall (difference strategy_1) ---------------------- 
matrix3 = matrix1 - matrix2
diff_zmin = -zmax
diff_zmax = zmax

srf_4 = go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale_d,
    cmin=diff_zmin, cmax=diff_zmax,
    colorbar=dict(title="Points", len=0.75, x=0.99)
    )

# combine difference surface with plane at z=0
fig.add_trace(srf_4, row=2, col=2)

# Then, add the z=0 plane (same x and y, z = 0)
fig.add_trace(go.Surface(
    x=list1, y=list2,
    z=np.zeros_like(matrix3),  # plane at z=0
    showscale=False,
    opacity=0.4,  # semi-transparent
    colorscale=[[0, 'gray'], [1, 'gray']],
    name='z=0 Plane'),
    row=2, col=2
)

# ---------------------- surface plot overall (difference strategy2) ---------------------- 
matrix3 = matrix2 - matrix1

# combine difference surface with plane at z=0
srf_5 = go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale_d,
    showscale=False,
    cmin=diff_zmin, cmax=diff_zmax,
    )

fig.add_trace(srf_5, row=2, col=1)

# Then, add the z=0 plane (same x and y, z = 0)
fig.add_trace(go.Surface(
    x=list1, y=list2,
    z=np.zeros_like(matrix3),  # plane at z=0
    showscale=False,
    opacity=0.4,  # semi-transparent
    colorscale=[[0, 'gray'], [1, 'gray']],
    name='z=0 Plane'),
    row=2, col=1
)


# ---------------------- format of all the surfaces ---------------------- 

# Define axis ranges
x_min, x_max = min(list1), max(list1)
y_min, y_max = min(list2), max(list2)

fig.update_layout(
    scene=dict(
        aspectmode='cube',
        xaxis=dict(
            title=dict(text=strategy_1_title), range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2_title), 
            range=[y_min, y_max]),
        zaxis=dict(range=[zmin, zmax])
    ),
    scene2=dict(
        aspectmode='cube',
        xaxis=dict(
            title=dict(text=strategy_1_title),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2_title), 
            range=[y_min, y_max]),
        zaxis=dict(range=[zmin, zmax])
    ),
    scene3=dict(
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=2),
        xaxis=dict(
            title=dict(text=strategy_1_title),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2_title), 
            range=[y_min, y_max]),
        zaxis=dict(range=[diff_zmin, diff_zmax])
    ),
    scene4=dict(
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=2),
        xaxis=dict(
            title=dict(text=strategy_1_title),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2_title), 
            range=[y_min, y_max]),
        zaxis=dict(range=[diff_zmin, diff_zmax])
    ),
    scene5=dict(
        aspectmode='cube',
        xaxis=dict(
            title=dict(text=strategy_1_title),
            range=[x_min, x_max]),
        yaxis=dict(
            title=dict(text=strategy_2_title), 
            range=[y_min, y_max]),
        zaxis=dict(range=[overall_zmin, overall_zmax])
    ),
)

fig.show()
# pio.write_image(srf_1, f"plots/{strategy_1}_vs_{strategy_2}.png")
