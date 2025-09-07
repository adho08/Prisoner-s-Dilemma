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
        name="Surpass Threshold Up",
        line=dict(color="green")
    )
)

y = [1-2.5/i if i != 0 else -1e6 for i in x]  # put large value at x=0
df = pd.DataFrame({"x": x, "y": y})

fig.add_trace(
    go.Scatter(
        x=df["x"], 
        y=df["y"], 
        mode="lines+markers",
        name="Surpass Threshold Down",
        line=dict(color="blue")
    )
)

def randomC_investm_up(parameter):
    return 0.5 + parameter/20

def randomC_investm_down(parameter):
    return 0.5 - parameter/20

def fig_add_trace_up(parameter_B, colour, name):
    fig.add_trace(
        go.Scatter(
            x=df["x"], 
            y=[randomC_investm_up(parameter_B)]*len(df["x"]), 
            mode="lines",
            name=name,
            line=dict(color=colour)
        )
    )

def fig_add_trace_down(parameter_B, colour, name):
    fig.add_trace(
        go.Scatter(
            x=df["x"], 
            y=[randomC_investm_down(parameter_B)]*len(df["x"]), 
            mode="lines",
            name=name,
            line=dict(color=colour)
        )
    )

colours = ["red", "green", "pink", "yellow", "black", "brown"]

fig_add_trace_up(5, "red",  "RC 5 Upper")
fig_add_trace_down(5, "orange", "RC 5 Lower")

# Set axes from 0 to 11 (large y will be clipped out)
fig.update_layout(
    xaxis=dict(range=[0, 10], title="Parameter of Adapt-Discrete", dtick=1),
    yaxis=dict(range=[0, 1], title="Investment", dtick=0.1
    )
)

fig.write_image("plots/Discussion/Random-Continuous_vs_Adapt-Discrete/Adapt-Discrete_values_surpass_threshold_up.png")

