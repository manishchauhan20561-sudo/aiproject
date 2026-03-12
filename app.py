import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events

st.title("Autonomous Robot Navigation AI Project")

start = np.array([0.0, 0.0])
goal = np.array([10.0, 10.0])

# Store obstacles
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []

st.write("Click on the graph to place obstacles")

# Create figure
fig = go.Figure()

# Start
fig.add_trace(go.Scatter(
    x=[start[0]],
    y=[start[1]],
    mode="markers",
    marker=dict(size=12, color="blue"),
    name="Start"
))

# Goal
fig.add_trace(go.Scatter(
    x=[goal[0]],
    y=[goal[1]],
    mode="markers",
    marker=dict(size=16, symbol="star", color="green"),
    name="Goal"
))

# Obstacles
if st.session_state.obstacles:
    ox = [o[0] for o in st.session_state.obstacles]
    oy = [o[1] for o in st.session_state.obstacles]

    fig.add_trace(go.Scatter(
        x=ox,
        y=oy,
        mode="markers",
        marker=dict(size=12, symbol="x", color="red"),
        name="Obstacles"
    ))

fig.update_layout(
    xaxis=dict(range=[-1, 12]),
    yaxis=dict(range=[-1, 12]),
    height=500
)

# Detect clicks
selected_points = plotly_events(fig, click_event=True)

# Add obstacle where clicked
if selected_points:
    x = selected_points[0]["x"]
    y = selected_points[0]["y"]

    st.session_state.obstacles.append([x, y])
    st.rerun()

# Clear obstacles
if st.button("Clear Obstacles"):
    st.session_state.obstacles = []
    st.rerun()

# Start robot simulation
if st.button("Start Robot"):

    robot = start.copy()
    path_x = [robot[0]]
    path_y = [robot[1]]

    for i in range(200):

        goal_force = goal - robot
        goal_force = goal_force / np.linalg.norm(goal_force)

        repulsive = np.array([0.0, 0.0])

        for obs in st.session_state.obstacles:

            obs = np.array(obs)
            dist = np.linalg.norm(robot - obs)

            if dist < 2:
                direction = robot - obs
                direction = direction / np.linalg.norm(direction)
                repulsive += direction * (1 / dist)

        move = goal_force + repulsive
        move = move / np.linalg.norm(move)

        robot = robot + move * 0.4

        path_x.append(robot[0])
        path_y.append(robot[1])

        if np.linalg.norm(robot - goal) < 0.3:
            break

    fig.add_trace(go.Scatter(
        x=path_x,
        y=path_y,
        mode="lines",
        line=dict(color="blue"),
        name="Robot Path"
    ))

    st.plotly_chart(fig)

else:
    st.plotly_chart(fig)
