import plotly.graph_objects as go

# Build figure
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=list(range(0, 11)),
        y=[5, 4, 4, 3, 3, 3, 3, 2, 2, 2, 2], 
        mode="lines"
    )
)

fig.update_layout(
    xaxis=dict(range=[0, 10], title="Random-Continuous", dtick=1),
    yaxis=dict(range=[0, 10], title="Adapt-Discrete", dtick=1, scaleanchor="x", scaleratio=1),
    margin=dict(l=140, r=140, t=20, b=20),
    width=600,
    height=600
)

fig.write_image(f"plots/Discussion/Random-Discrete_vs_Adapt-Discrete/surface_2D.png")
