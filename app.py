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

# Enter obstacle coordinates dynamically
st.sidebar.subheader("Obstacle Coordinates")
obstacles = []
for i in range(num_obs):
    x = st.sidebar.number_input(f"Obstacle {i+1} X", value=float(i+3), key=f"x{i}")
    y = st.sidebar.number_input(f"Obstacle {i+1} Y", value=float(i+4), key=f"y{i}")
    obstacles.append(np.array([x, y]))

# Obstacle radius
OBSTACLE_RADIUS = 0.6

# Show Reference Graph
st.subheader("Reference Map (Obstacles & Goal)")
fig_ref, ax_ref = plt.subplots(figsize=(6,6))

# Plot obstacles
for idx, obs in enumerate(obstacles):
    circle = plt.Circle(obs, OBSTACLE_RADIUS, color="orange", alpha=0.3)
    ax_ref.add_patch(circle)
    ax_ref.scatter(obs[0], obs[1], marker='x', s=100, color="black")
    ax_ref.text(obs[0]+0.2, obs[1]+0.2, f"O{idx+1}", fontsize=10)

# Plot goal
ax_ref.scatter(goal[0], goal[1], marker='*', s=300, color="green", label="Goal")

ax_ref.set_xlim(-1,12)
ax_ref.set_ylim(-1,12)
ax_ref.grid(True)
ax_ref.set_title("Reference Map")
ax_ref.legend()
st.pyplot(fig_ref)

# Start robot button
if st.button("🚀 Start Robot"):

    start = np.array([0.0, 0.0])
    robot = start.copy()
    path_x = [robot[0]]
    path_y = [robot[1]]

    plot_area = st.empty()
    step = 0

    while np.linalg.norm(robot - goal) > 0.3:
        step += 1

        # Attractive force to goal
        goal_force = goal - robot
        goal_force = goal_force / np.linalg.norm(goal_force)

        # Repulsive force from obstacles
        repulsive = np.array([0.0, 0.0])
        for obs in obstacles:
            dist = np.linalg.norm(robot - obs)
            if dist < 2.5:
                direction = robot - obs
                direction = direction / np.linalg.norm(direction)
                repulsive += direction * (2.0 / dist**2)  # stronger repulsion

        # Total movement
        move = goal_force + repulsive
        move = move / np.linalg.norm(move)
        robot += move * 0.2  # smaller steps for smoothness

        path_x.append(robot[0])
        path_y.append(robot[1])

        # Plotting
        fig, ax = plt.subplots(figsize=(6,6))
        ax.plot(path_x, path_y, label="Robot Path", color="blue", linewidth=2)
        ax.scatter(robot[0], robot[1], s=80, color="red", edgecolors='black', label="Robot", zorder=5)
        ax.scatter(goal[0], goal[1], marker='*', s=300, color="green", label="Goal")

        for idx, obs in enumerate(obstacles):
            circle = plt.Circle(obs, OBSTACLE_RADIUS, color="orange", alpha=0.3)
            ax.add_patch(circle)
            ax.scatter(obs[0], obs[1], marker='x', s=100, color="black")
            ax.text(obs[0]+0.2, obs[1]+0.2, f"O{idx+1}", fontsize=10)

        ax.set_xlim(-1, 12)
        ax.set_ylim(-1, 12)
        ax.set_title(f"Step {step} | Distance to Goal: {np.linalg.norm(robot-goal):.2f}")
        ax.grid(True)
        ax.legend()

        plot_area.pyplot(fig)
        time.sleep(0.1)

    st.success("🎯 Goal Reached!")
