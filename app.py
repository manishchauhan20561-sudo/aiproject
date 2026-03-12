import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

st.title("Autonomous Robot Navigation")

# Number of obstacles
num_obstacles = st.slider("Select number of obstacles", 1, 6, 3)

obstacles = []

st.write("Enter obstacle coordinates")

# Input obstacle coordinates
for i in range(num_obstacles):

    col1, col2 = st.columns(2)

    x = col1.number_input(f"Obstacle {i+1} X", 0, 10, key=f"x{i}")
    y = col2.number_input(f"Obstacle {i+1} Y", 0, 10, key=f"y{i}")

    obstacles.append(np.array([x, y]))

# Start robot button
start_robot = st.button("Start Robot")

plot = st.empty()

if start_robot:

    start = np.array([0.0, 0.0])
    goal = np.array([10.0, 10.0])
    position = start.copy()

    while np.linalg.norm(goal - position) > 0.3:

        direction = goal - position
        direction = direction / np.linalg.norm(direction)

        position = position + direction * 0.5

        # Plot
        fig, ax = plt.subplots()

        ax.set_xlim(0,10)
        ax.set_ylim(0,10)

        # obstacles
        for obs in obstacles:
            ax.scatter(obs[0], obs[1], marker='s', s=200)

        # start & goal
        ax.scatter(start[0], start[1], s=200)
        ax.scatter(goal[0], goal[1], s=200)

        # robot
        ax.scatter(position[0], position[1], s=200)

        plot.pyplot(fig)

        time.sleep(0.4)

    st.success("Robot reached goal!")
