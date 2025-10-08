import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio
import sys
import os
from pathlib import Path

# import variable of main.py
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent / 'src'))
from main import strategy_1, strategy_2, rounds, repeated
from game import PrisonersDilemma as PD
sys.path.insert(0, str(script_dir.parent / 'data'))

cwd = os.getcwd()
plots_dir = os.path.join(cwd, "plots")
final_dir = os.path.join(plots_dir, f"{strategy_1}_vs_{strategy_2}")
if not os.path.exists(final_dir):
    os.mkdir(final_dir)

df = pd.read_csv(f"./results/{strategy_1}_vs_{strategy_2}_results.csv")
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
list3 = df[df.columns[1]].to_numpy().astype(float).tolist()
# calculate the mean of 'repeated' consecutive elements
list3 = np.array(list3, dtype=float).reshape(-1, repeated).mean(axis=1).tolist()
matrix1 = np.array(list3).reshape((m, n))

# data of strategy_2
list3 = df[df.columns[3]].to_numpy().astype(float).tolist()
# calculate the mean of 'repeated' consecutive elements
list3 = np.array(list3, dtype=float).reshape(-1, repeated).mean(axis=1).tolist()
matrix2 = np.array(list3).reshape((m, n))

# different colorscales
colorscale_s = 'Plasma'
colorscale_a = 'Portland'
colorscale_d = 'Cividis'
# least points possible (except in difference plots)
zmin = 0
# most points possible
zmax = rounds * (1 + PD.c)

# ---------------------- function for updating the fig layout ---------------------- 
def update_fig_layout(fig, title:str, range, x=1, y=1, z=1.0):

    label_axis_size = 40

    fig.update_layout(
        title=dict(
            text=title,
            x=0.5,
            xanchor="center"
            ),
        scene=dict(
            xaxis=dict(
                title=dict(
                    text=strategy_1_title,
                    font=dict(size=label_axis_size),
                    ),
                ),
            yaxis=dict(
                title=dict(
                    text=strategy_2_title,
                    font=dict(size=label_axis_size),
                    ),
                ),
            zaxis=dict(
                title=dict(
                    text="Points",
                    font=dict(size=label_axis_size),
                    ),
                dtick=10,
                range=range
                ),
            aspectmode='manual',
            aspectratio=dict(x=x, y=y, z=z)
            ),
        margin=dict(l=0, r=0, b=0, t=0),  # reduce padding cuts
        scene_camera=dict(
            eye=dict(x=2.0, y=2.0, z=2.0)  # move camera further back
            ),
        font=dict(size=20),
    )

# ---------------------- surface plot strategy_1 ---------------------- 
fig1 = go.Figure(
        data=go.Surface(
            x=list1, y=list2, z=matrix1,
            colorscale=colorscale_s,
            showscale=False,
            cmin=zmin, cmax=zmax,),
)

update_fig_layout(fig1, strategy_1, [zmin, zmax])

# ---------------------- surface plot strategy_2 ---------------------- 
fig2 = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix2,
    colorscale=colorscale_s,
    showscale=False,
    cmin=zmin, cmax=zmax,
    )
)

update_fig_layout(fig2, strategy_2, [zmin, zmax])

# ---------------------- surface plot overall (added) ---------------------- 
matrix3 = matrix1 + matrix2
added_zmin = 0
added_zmax = 2 * rounds 

fig4 = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale_a,
    showscale=False,
    cmin=added_zmin, cmax=added_zmax,
    )
)

update_fig_layout(fig4, f"{strategy_1_title} + {strategy_2_title}", [added_zmin, added_zmax], z=4/3)

# ---------------------- surface plot overall (difference strategy1) ---------------------- 
matrix3 = matrix1 - matrix2
diff_zmin = -zmax
diff_zmax = zmax

# combine difference surface with plane at z=0
fig5 = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale_d,
    showscale=False,
    cmin=diff_zmin, cmax=diff_zmax,
    )
)

# Then, add the z=0 plane (same x and y, z = 0)
fig5.add_trace(go.Surface(
    x=list1, y=list2,
    z=np.zeros_like(matrix3),  # plane at z=0
    showscale=False,
    opacity=0.4,  # semi-transparent
    colorscale=[[0, 'gray'], [1, 'gray']],
    name='z=0 Plane'),
)

update_fig_layout(fig5, f"{strategy_1_title} - {strategy_2_title}", [diff_zmin, diff_zmax], z=2)

# ---------------------- surface plot overall (difference strategy2) ---------------------- 
matrix3 = matrix2 - matrix1

# combine difference surface with plane at z=0
fig6 = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale_d,
    showscale=False,
    cmin=diff_zmin, cmax=diff_zmax,
    )
)

# Then, add the z=0 plane (same x and y, z = 0)
fig6.add_trace(go.Surface(
    x=list1, y=list2,
    z=np.zeros_like(matrix3),  # plane at z=0
    showscale=False,
    opacity=0.4,  # semi-transparent
    colorscale=[[0, 'gray'], [1, 'gray']],
    name='z=0 Plane'),
)

update_fig_layout(fig6, f"{strategy_2_title} - {strategy_1_title}", [diff_zmin, diff_zmax], z=2)

# ---------------------- write plots into png's ---------------------- 
pio.write_images(
    fig=[fig1, fig2, fig4],
    file=[f"{final_dir}/{strategy_1}.png", f"{final_dir}/{strategy_2}.png", f"{final_dir}/added.png"],
    width=700,
    height=1000
)
pio.write_images(
    fig=[fig5, fig6],
    file=[f"{final_dir}/{strategy_1}_diff.png", f"{final_dir}/{strategy_2}_diff.png"],
    width=700,
    height=1000
)

