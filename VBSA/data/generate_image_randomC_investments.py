import pandas as pd
import plotly.graph_objects as go

# Build figure
fig = go.Figure()

def add_trace_to_fig(fig, list_y, name):
    global list_parameters 
    fig.add_trace(
        go.Scatter(
            x=list(list_parameters),
            y=list_y, 
            name=name
        )
    )

parameter_B = 5
parameter_start = 0
parameter_end = 10
list_parameters = range(parameter_start, parameter_end+1)
add_trace_to_fig(fig, [0.5 + 0.05 * j for j in list_parameters], "Upper Investment")
add_trace_to_fig(fig, [0.5] * len(list_parameters), "Anchor")
add_trace_to_fig(fig, [0.5 + -0.05 * j for j in list_parameters], "Lower Investment")

fig.update_layout(
    xaxis=dict(range=[0, 10], title="Parameter of Random-Continuous", dtick=1),
    yaxis=dict(range=[0, 1], title="Investment", dtick=0.1)
)

fig.write_image("plots/Discussion/Random-Continuous/investments.png")
