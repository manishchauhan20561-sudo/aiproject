import streamlit as st
import numpy as np

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

if start_robot:

    st.success("Robot Started")

    start = np.array([0, 0])
    goal = np.array([10, 10])

    st.write("Start Position:", start)
    st.write("Goal Position:", goal)

    st.write("Obstacles:", obstacles)

    # Example robot movement logic
    position = start.copy()

    while np.linalg.norm(goal - position) > 0.5:

        direction = goal - position
        direction = direction / np.linalg.norm(direction)

        position = position + direction

        st.write("Robot Position:", position)

    st.success("Robot Reached Goal!")
