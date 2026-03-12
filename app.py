import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Autonomous Robot Navigation with Obstacle Avoidance")

# number of obstacles
num_obstacles = st.slider("Select number of obstacles", 1, 6, 3)

obstacles = []

st.write("Enter obstacle coordinates")

for i in range(num_obstacles):

    col1, col2 = st.columns(2)

    x = col1.number_input(f"Obstacle {i+1} X", 0, 10, key=f"x{i}")
    y = col2.number_input(f"Obstacle {i+1} Y", 0, 10, key=f"y{i}")

    obstacles.append(np.array([x, y]))

start = np.array([0.0, 0.0])
goal = np.array([10.0, 10.0])

plot_area = st.empty()

# -------- show graph BEFORE robot starts --------

fig, ax = plt.subplots()

ax.set_xlim(0,10)
ax.set_ylim(0,10)
ax.set_title("Robot Environment")

for obs in obstacles:
    ax.scatter(obs[0], obs[1], s=200)

ax.scatter(start[0], start[1], s=200)
ax.scatter(goal[0], goal[1], s=200)

plot_area.pyplot(fig)

# -------- start robot --------

if st.button("Start Robot"):

    position = start.copy()

    while np.linalg.norm(goal - position) > 0.4:

        direction = goal - position
        direction = direction / np.linalg.norm(direction)

        # obstacle avoidance
        for obs in obstacles:

            if np.linalg.norm(position - obs) < 1.5:

                avoid = position - obs
                avoid = avoid / np.linalg.norm(avoid)

                direction = direction + avoid

        direction = direction / np.linalg.norm(direction)

        position = position + direction * 0.4

        fig, ax = plt.subplots()

        ax.set_xlim(0,10)
        ax.set_ylim(0,10)

        for obs in obstacles:
            ax.scatter(obs[0], obs[1], s=200)

        ax.scatter(start[0], start[1], s=200)
        ax.scatter(goal[0], goal[1], s=200)

        ax.scatter(position[0], position[1], s=250)

        plot_area.pyplot(fig)

        time.sleep(0.4)

    st.success("Robot reached the goal!")
