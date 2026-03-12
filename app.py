import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_page_config(page_title="Autonomous Robot Navigation", layout="wide")

st.title("🤖 Autonomous Robot Navigation with Obstacles")

# Sidebar controls
st.sidebar.header("Settings")

# Number of obstacles
num_obs = st.sidebar.slider("Number of Obstacles", 1, 6, 3)

# Goal coordinates
goal_x = st.sidebar.number_input("Goal X", value=10.0)
goal_y = st.sidebar.number_input("Goal Y", value=10.0)

goal = np.array([goal_x, goal_y])

# Obstacle coordinates
st.sidebar.subheader("Obstacle Coordinates")

obstacles = []

for i in range(num_obs):

    x = st.sidebar.number_input(f"Obstacle {i+1} X", value=float(i+3), key=f"x{i}")
    y = st.sidebar.number_input(f"Obstacle {i+1} Y", value=float(i+4), key=f"y{i}")

    obstacles.append(np.array([x,y]))

# Obstacle size
OBSTACLE_RADIUS = 0.6

# -----------------------------
# REFERENCE MAP
# -----------------------------

st.subheader("Reference Map (Environment)")

fig_ref, ax_ref = plt.subplots(figsize=(6,6))

# Plot obstacles
for obs in obstacles:

    circle = plt.Circle(obs, OBSTACLE_RADIUS, color="orange", alpha=0.3)
    ax_ref.add_patch(circle)

    ax_ref.scatter(obs[0], obs[1], marker='x', s=100, color="black")

# Plot goal
ax_ref.scatter(goal[0], goal[1], marker='*', s=300, color="green", label="Goal")

# Plot start
ax_ref.scatter(0,0,color="red",s=120,label="Start")

ax_ref.set_xlim(-1,12)
ax_ref.set_ylim(-1,12)

ax_ref.grid(True)
ax_ref.set_title("Reference Map")

ax_ref.legend()

st.pyplot(fig_ref)

# -----------------------------
# START ROBOT BUTTON
# -----------------------------

if st.button("🚀 Start Robot"):

    start = np.array([0.0,0.0])

    robot = start.copy()

    path_x = [robot[0]]
    path_y = [robot[1]]

    plot_area = st.empty()

    step = 0

    while np.linalg.norm(robot-goal) > 0.3:

        step += 1

        # Attractive force
        goal_force = goal - robot
        goal_force = goal_force / np.linalg.norm(goal_force)

        # Repulsive force
        repulsive = np.array([0.0,0.0])

        for obs in obstacles:

            dist = np.linalg.norm(robot-obs)

            if dist < 2.5:

                direction = robot - obs
                direction = direction / np.linalg.norm(direction)

                repulsive += direction * (1/dist)

        # Movement direction
        move = goal_force + repulsive
        move = move / np.linalg.norm(move)

        # Move robot slowly
        robot = robot + move * 0.3

        path_x.append(robot[0])
        path_y.append(robot[1])

        # Plot simulation
        fig, ax = plt.subplots(figsize=(6,6))

        ax.plot(path_x, path_y, linewidth=2, label="Robot Path")

        ax.scatter(robot[0], robot[1], s=120, color="red", label="Robot")

        ax.scatter(goal[0], goal[1], marker='*', s=300, color="green", label="Goal")

        # Draw obstacles
        for obs in obstacles:

            circle = plt.Circle(obs, OBSTACLE_RADIUS, color="orange", alpha=0.3)
            ax.add_patch(circle)

            ax.scatter(obs[0], obs[1], marker='x', s=100, color="black")

        ax.set_xlim(-1,12)
        ax.set_ylim(-1,12)

        distance = np.linalg.norm(robot-goal)

        ax.set_title(f"Step {step} | Distance to Goal: {distance:.2f}")

        ax.grid(True)

        ax.legend()

        plot_area.pyplot(fig)

        time.sleep(0.4)

    st.success("🎯 Goal Reached!")
