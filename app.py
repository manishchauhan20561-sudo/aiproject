import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Autonomous Robot Navigation AI Project")

# Start and Goal
start = np.array([0,0])
goal = np.array([10,10])

st.subheader("Robot Environment Setup")

# Choose number of obstacles
num_obstacles = st.slider("Select number of obstacles", 1, 6, 3)

obstacles = []

st.write("Enter obstacle coordinates:")

for i in range(num_obstacles):
    col1, col2 = st.columns(2)

    x = col1.number_input(f"Obstacle {i+1} X", 0, 10, key=f"x{i}")
    y = col2.number_input(f"Obstacle {i+1} Y", 0, 10, key=f"y{i}")

    obstacles.append(np.array([x,y]))

# Plot environment
fig, ax = plt.subplots()

# Start and Goal
ax.scatter(start[0], start[1], s=120, label="Start")
ax.scatter(goal[0], goal[1], marker="*", s=300, label="Goal")

# Obstacles
for obs in obstacles:
    ax.scatter(obs[0], obs[1], marker="x", s=150, label="Obstacle")

ax.set_xlim(-1,12)
ax.set_ylim(-1,12)
ax.grid()

ax.legend()

st.pyplot(fig)
