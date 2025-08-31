import pandas as pd
import plotly.graph_objects as go

# Build figure
fig = go.Figure()

list_payoffs = []
directory = "AdaptC_AlwaysS_simulation"
parameter_B = 5
parameter_start = 0
parameter_end = 10
for i in range(parameter_start, parameter_end+1):
    df = pd.read_csv(f"{directory}/AdaptC_vs_AlwaysS_simulation_{i}_{parameter_B}.csv")
    list_payoffs.append(sum(df[df.columns[2]]))

fig.add_trace(
    go.Scatter(
        x=[i for i in range(parameter_start, parameter_end+1)],
        y=list_payoffs, 
    )
)

fig.update_layout(
    xaxis=dict(range=[parameter_start, parameter_end], title="Adapt-Continuous' Parameter", dtick=1),
    yaxis=dict(range=[0, 30], title="Adapt-Continuous's Pay-off", dtick=5
    )
)

fig.write_image(f"plots/Discussion/Adapt-Continuous/Payoffs_{parameter_B}_line_chart_{parameter_start}-{parameter_end}.png")

