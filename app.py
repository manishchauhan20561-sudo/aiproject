import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Autonomous Robot Navigation AI Project")

start = np.array([0.0, 0.0])
goal = np.array([10.0, 10.0])

if "obstacles" not in st.session_state:
    st.session_state.obstacles = []

st.write("Click on the graph to add obstacles")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=[start[0]],
    y=[start[1]],
    mode="markers",
    marker=dict(size=12),
    name="Start"
))

fig.add_trace(go.Scatter(
    x=[goal[0]],
    y=[goal[1]],
    mode="markers",
    marker=dict(size=15, symbol="star"),
    name="Goal"
))

if st.session_state.obstacles:
    ox = [o[0] for o in st.session_state.obstacles]
    oy = [o[1] for o in st.session_state.obstacles]

    fig.add_trace(go.Scatter(
        x=ox,
        y=oy,
        mode="markers",
        marker=dict(size=12, symbol="x"),
        name="Obstacles"
    ))

fig.update_layout(
    xaxis=dict(range=[-1, 12]),
    yaxis=dict(range=[-1, 12]),
    height=500
)

clicked = st.plotly_chart(fig, use_container_width=True, on_select="rerun")

if clicked and "points" in clicked:
    for p in clicked["points"]:
        st.session_state.obstacles.append([p["x"], p["y"]])

if st.button("Clear Obstacles"):
    st.session_state.obstacles = []

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
        name="Robot Path"
    ))

    st.plotly_chart(fig)
