import pandas as pd
import plotly.graph_objects as go

# Build figure
fig = go.Figure()

def add_trace_to_fig(fig, csv_file, i):
    df = pd.read_csv(csv_file)
    fig.add_trace(
        go.Scatter(
            x=df[df.columns[0]], 
            y=df[df.columns[2]], 
            name=f"Parameter {i}"
        )
    )

directory = "AdaptC_AlwaysS_simulation"
parameter_B = 5
parameter_start = 5
parameter_end = 10
list_parameters = range(parameter_start, parameter_end+1)
for i in list_parameters:
    add_trace_to_fig(fig, f"{directory}/AdaptC_vs_AlwaysS_simulation_{i}_{parameter_B}.csv", i)

fig.update_layout(
    xaxis=dict(range=[1, 20], title="Round", dtick=1),
    yaxis=dict(range=[0, 1], title="Adapt-Continuous's Pay-off", dtick=0.1
    )
)

fig.write_image(f"plots/Discussion/Adapt-Continuous/Approx_pay-offs_{parameter_B}_line_chart_{parameter_start}-{parameter_end}.png")

