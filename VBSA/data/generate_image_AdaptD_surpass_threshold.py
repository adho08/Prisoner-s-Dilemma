import pandas as pd
import plotly.graph_objects as go

# Create data
x = list(range(0, 11))
y = [1-2.5/i if i != 0 else -1e6 for i in x]  # put large value at x=0

df = pd.DataFrame({"x": x, "y": y})

# Build figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["x"], 
        y=df["y"], 
        mode="lines+markers",
        name="Threshold Values"
    )
)

# def randomC_investm(parameter):
#     return 0.5 - parameter/20

# def fig_add_trace(parameter_B):
#     fig.add_trace(
#         go.Scatter(
#             x=df["x"], 
#             y=[randomC_investm(parameter_B)]*len(df["x"]), 
#             mode="lines",
#             name=f"RC {parameter_B} Lower"
#         )
#     )
#
# fig_add_trace(0)
# fig_add_trace(1)
# fig_add_trace(2)
# fig_add_trace(3)
# fig_add_trace(6)
# fig_add_trace(7)

# Set axes from 0 to 11 (large y will be clipped out)
fig.update_layout(
    xaxis=dict(range=[0, 10], title="Parameter of Adapt-Discrete", dtick=1),
    yaxis=dict(range=[0, 1], title="Investment", dtick=0.1),
     showlegend=True,
)

fig.write_image("plots/Discussion/Adapt-Discrete/Adapt-Discrete_values_surpass_threshold_abs.png")

