import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Autonomous Robot Navigation AI Project")

start = np.array([0.0,0.0])
goal = np.array([10.0,10.0])

if "obstacles" not in st.session_state:
    st.session_state.obstacles=[]

st.subheader("Add Obstacle")

col1,col2=st.columns(2)

x=col1.number_input("Obstacle X",0.0,10.0,0.0)
y=col2.number_input("Obstacle Y",0.0,10.0,0.0)

if st.button("Add Obstacle"):
    st.session_state.obstacles.append([x,y])

if st.button("Clear Obstacles"):
    st.session_state.obstacles=[]

fig=go.Figure()

fig.add_trace(go.Scatter(
    x=[start[0]],
    y=[start[1]],
    mode="markers",
    marker=dict(size=12,color="blue"),
    name="Start"
))

fig.add_trace(go.Scatter(
    x=[goal[0]],
    y=[goal[1]],
    mode="markers",
    marker=dict(size=15,symbol="star",color="green"),
    name="Goal"
))

if st.session_state.obstacles:

    ox=[o[0] for o in st.session_state.obstacles]
    oy=[o[1] for o in st.session_state.obstacles]

    fig.add_trace(go.Scatter(
        x=ox,
        y=oy,
        mode="markers",
        marker=dict(size=12,symbol="x",color="red"),
        name="Obstacles"
    ))

fig.update_layout(
    xaxis=dict(range=[-1,12]),
    yaxis=dict(range=[-1,12]),
    height=500
)

st.plotly_chart(fig)

if st.button("Start Robot"):

    robot=start.copy()

    path_x=[robot[0]]
    path_y=[robot[1]]

    for i in range(200):

        goal_force=goal-robot
        goal_force=goal_force/np.linalg.norm(goal_force)

        repulsive=np.array([0.0,0.0])

        for obs in st.session_state.obstacles:

            obs=np.array(obs)
            dist=np.linalg.norm(robot-obs)

            if dist<2:
                direction=robot-obs
                direction=direction/np.linalg.norm(direction)
                repulsive+=direction*(1/dist)

        move=goal_force+repulsive
        move=move/np.linalg.norm(move)

        robot=robot+move*0.4

        path_x.append(robot[0])
        path_y.append(robot[1])

        if np.linalg.norm(robot-goal)<0.3:
            break

    fig.add_trace(go.Scatter(
        x=path_x,
        y=path_y,
        mode="lines",
        line=dict(color="blue"),
        name="Robot Path"
    ))

    st.plotly_chart(fig)
