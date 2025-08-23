import pandas as pd
import plotly.graph_objects as go

# Create data
x = list(range(0, 11))
y = [2.5/i if i != 0 else 1e6 for i in x]  # put large value at x=0

df = pd.DataFrame({"x": x, "y": y})

# Build figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=df["x"], 
        y=df["y"], 
        mode="lines+markers",
    )
)

# Set axes from 0 to 11 (large y will be clipped out)
fig.update_layout(
    xaxis=dict(range=[0, 10], title="Parameter of Adapt-Discrete", dtick=1),
    yaxis=dict(range=[0, 1], title="Opponent's maximum Investment", dtick=0.1
    )
)

fig.write_image("plots/Discussion/Adapt-Discrete/Adapt-Discrete_values_surpass_threshold.png")

