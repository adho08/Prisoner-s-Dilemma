import plotly.graph_objects as go

# Example colorscale
colorscale = "Viridis"

fig = go.Figure(data=go.Heatmap(
    z=[[0,1],[0,1]],  # simple 2x2 dummy data
    colorscale=colorscale,
    showscale=True    # show colorbar
))

# Save as PNG
fig.write_image("colorscale.png")
