import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Robot Navigation", layout="wide")

st.title("🤖 Autonomous Robot Navigation")

# Session storage
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []

goal = np.array([10,10])
start = np.array([0,0])

st.write("Click anywhere on the map to add obstacles.")

# Create interactive plot
fig = go.Figure()

# Obstacles
if len(st.session_state.obstacles) > 0:
    xs = [o[0] for o in st.session_state.obstacles]
    ys = [o[1] for o in st.session_state.obstacles]

    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        mode="markers",
        marker=dict(size=12,color="orange"),
        name="Obstacles"
    ))

# Goal
fig.add_trace(go.Scatter(
    x=[goal[0]],
    y=[goal[1]],
    mode="markers",
    marker=dict(size=18,color="green"),
    name="Goal"
))

fig.update_layout(
    xaxis=dict(range=[-1,12]),
    yaxis=dict(range=[-1,12]),
    height=500,
    clickmode="event+select"
)

# Capture click
clicked_points = plotly_events(fig)

if clicked_points:
    x = clicked_points[0]["x"]
    y = clicked_points[0]["y"]

    st.session_state.obstacles.append([x,y])
    st.rerun()

# Buttons
col1,col2 = st.columns(2)

with col1:
    start_robot = st.button("🚀 Start Robot")

with col2:
    if st.button("🗑 Clear Obstacles"):
        st.session_state.obstacles=[]
        st.rerun()

# Robot simulation
if start_robot:

    robot = start.copy()

    path_x=[robot[0]]
    path_y=[robot[1]]

    plot_area = st.empty()

    while np.linalg.norm(robot-goal) > 0.3:

        goal_force = goal - robot
        goal_force = goal_force / np.linalg.norm(goal_force)

        repulsive = np.array([0.0,0.0])

        for obs in st.session_state.obstacles:

            obs = np.array(obs)
            dist = np.linalg.norm(robot-obs)

            if dist < 2:
                direction = robot - obs
                direction = direction / np.linalg.norm(direction)
                repulsive += direction*(1/dist)

        move = goal_force + repulsive
        move = move / np.linalg.norm(move)

        robot += move*0.4

        path_x.append(robot[0])
        path_y.append(robot[1])

        fig2,ax = plt.subplots(figsize=(6,6))

        ax.plot(path_x,path_y,label="Path")

        ax.scatter(robot[0],robot[1],s=120,color="red",label="Robot")

        ax.scatter(goal[0],goal[1],marker='*',s=250,color="green",label="Goal")

        for obs in st.session_state.obstacles:
            circle = plt.Circle(obs,0.5,alpha=0.3,color="orange")
            ax.add_patch(circle)

        ax.set_xlim(-1,12)
        ax.set_ylim(-1,12)
        ax.grid()

        plot_area.pyplot(fig2)

        time.sleep(0.2)

    st.success("Goal Reached 🎯")
