import plotly.graph_objects as go
import pandas as pd
import numpy as np
import plotly.io as pio
import sys
import os
from pathlib import Path

# import variable of another python script
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir.parent / 'src'))
from main import strategy_1, strategy_2, rounds, repeated
from game import PrisonersDilemma as PD
sys.path.insert(0, str(script_dir.parent / 'data'))

cwd = os.getcwd()
plots_dir = cwd + r"/plots"
final_dir = os.path.join(plots_dir, rf"{strategy_1}_vs_{strategy_2}")
if not os.path.exists(final_dir):
    os.mkdir(final_dir)

df = pd.read_csv(rf"results/{strategy_1}_vs_{strategy_2}_results.csv")
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
# least points possible
zmin = 0
# most points possible
zmax = rounds * (1 + PD.c)

# ---------------------- function for updating the fig layout ---------------------- 
def update_fig_layout(fig, title:str, range, x=1, y=1, z=1):
    fig.update_layout(
        # title=dict(
        #     text=title,
        #     x=0.5,
        #     xanchor="center"
        # ),
        scene=dict(
            xaxis=dict(
                title=dict(
                    text=strategy_1
                ),
            ),
            yaxis=dict(
                title=dict(
                    text=strategy_2
                )
            ),
            zaxis=dict(
                title=dict(
                    text="Points"
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
        )
    )

# ---------------------- surface plot strategy_1 ---------------------- 
fig1 = go.Figure(
    data=go.Surface(
    x=list1, y=list2, z=matrix1,
    colorscale=colorscale_s,
    showscale=False,
    cmin=zmin, cmax=zmax,),
)

# Then, add the z=0 plane (same x and y, z = 0)
# fig1.add_trace(go.Surface(
#     x=list1, y=list2,
#     z=np.zeros_like(matrix1),  # plane at z=0
#     showscale=False,
#     opacity=0.4,  # semi-transparent
#     colorscale=[[0, 'gray'], [1, 'gray']],
#     name='z=0 Plane'),
# )

update_fig_layout(fig1, strategy_1, [zmin, zmax])

# ---------------------- surface plot strategy_2 ---------------------- 
fig2 = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix2,
    colorscale=colorscale_s,
    showscale=False,
    cmin=zmin, cmax=zmax,
    )
)

# Then, add the z=0 plane (same x and y, z = 0)
# fig2.add_trace(go.Surface(
#     x=list1, y=list2,
#     z=np.zeros_like(matrix2),  # plane at z=0
#     showscale=False,
#     opacity=0.4,  # semi-transparent
#     colorscale=[[0, 'gray'], [1, 'gray']],
#     name='z=0 Plane'),
# )

update_fig_layout(fig2, strategy_2, [zmin, zmax])

# ---------------------- surface plot overall (mean) ---------------------- 
# matrix3 = np.mean(np.array([matrix1, matrix2]), axis=0)
# added_zmin = zmin # matrix3.min()
# added_zmax = zmax # matrix3.max()
#
# fig3 = go.Figure(data=go.Surface(
#     x=list1, y=list2, z=matrix3,
#     colorscale=colorscale_s,
#     showscale=False,
#     cmin=added_zmin, cmax=added_zmax,
#     )
# )
#
# update_fig_layout(fig3, f"{strategy_1} + {strategy_2}")

# ---------------------- surface plot overall (added) ---------------------- 
matrix3 = matrix1 + matrix2
added_zmin = 2 * zmin 
added_zmax = 2 * zmax

fig4 = go.Figure(data=go.Surface(
    x=list1, y=list2, z=matrix3,
    colorscale=colorscale_a,
    showscale=False,
    cmin=added_zmin, cmax=added_zmax,
    )
)

# Then, add the z=0 plane (same x and y, z = 0)
# fig4.add_trace(go.Surface(
#     x=list1, y=list2,
#     z=np.zeros_like(matrix3),  # plane at z=0
#     showscale=False,
#     opacity=0.4,  # semi-transparent
#     colorscale=[[0, 'gray'], [1, 'gray']],
#     name='z=0 Plane'),
# )

update_fig_layout(fig4, f"{strategy_1} + {strategy_2}", [added_zmin, added_zmax], z=2)

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

update_fig_layout(fig5, f"{strategy_1} - {strategy_2}", [diff_zmin, diff_zmax], z=2)

# ---------------------- surface plot overall (difference strategy2) ---------------------- 
matrix3 = matrix2 - matrix1
# diff_zmin = -1 * (zmax - zmin)
# diff_zmax = zmax - zmin

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

update_fig_layout(fig6, f"{strategy_2} - {strategy_1}", [diff_zmin, diff_zmax], z=2)

# ---------------------- generate an object of each colorscale ---------------------- 
def make_colorscale_fig(colorscale, range):

    # Make dummy data for the colorbar
    z = np.linspace(range[0], range[1]).reshape(-1, 1)  # column vector

    cscale = go.Figure(
        data=go.Heatmap(
            z=z,
            colorscale=colorscale,  # change to any Plotly colorscale
            colorbar=dict(
                thickness=50,   # width of the colorbar
            )
        )
    )
    cscale.update_xaxes(visible=False)
    cscale.update_yaxes(visible=False)
    cscale.update_layout(
        margin=dict(l=0, r=80, t=0, b=0),  # leave room for the colorbar
        width=200,
        height=400
    )

    return cscale

# cscale_s = make_colorscale_fig(colorscale_s, [zmin, zmax])
# cscale_a = make_colorscale_fig(colorscale_a, [added_zmin, added_zmax])
# cscale_d = make_colorscale_fig(colorscale_d, [diff_zmin, diff_zmax])
#
# cscales = [cscale_s, cscale_a, cscale_d]

# ---------------------- write plots into png's ---------------------- 
# pio.write_images(
#     fig=[fig1, fig2, fig4, fig5, fig6],
#     file=[f"{final_dir}/{strategy_1}.png", f"{final_dir}/{strategy_2}.png", f"{final_dir}/added.png", f"{final_dir}/{strategy_1}_diff.png", f"{final_dir}/{strategy_2}_diff.png"],
#     width=500,
#     height=500
# )

# for i, cscale in enumerate(cscales):
#     cscale.write_image(f"{final_dir}/../{i}.png")

