import pandas as pd
import plotly.graph_objects as go

# Build figure
fig = go.Figure()

def add_trace_to_fig(fig, list_y):
    global list_parameters 
    fig.add_trace(
        go.Scatter(
            x=list(list_parameters),
            y=list_y, 
        )
    )

directory = "AdaptC_AlwaysS_simulation"
parameter_B = 5
parameter_start = 0
parameter_end = 10
list_parameters = range(parameter_start, parameter_end+1)
add_trace_to_fig(fig, [0.5 * j for j in list_parameters])
add_trace_to_fig(fig, [-0.5 * j for j in list_parameters])
add_trace_to_fig(fig, [len(list_parameters) * 0.5])

fig.update_layout(
    xaxis=dict(range=[1, 20], title="Round", dtick=1),
    yaxis=dict(range=[0, 1], title="Adapt-Continuous's Invesment", dtick=0.1
    )
)

fig.write_image("plots/Discussion/RandomC/investments.png")

