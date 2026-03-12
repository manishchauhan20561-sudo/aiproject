import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Autonomous Robot Navigation AI Project")

start = np.array([0,0])
goal = np.array([10,10])

obstacles = [
    np.array([3,4]),
    np.array([5,5]),
    np.array([7,8]),
    np.array([6,2])
]

fig, ax = plt.subplots()

ax.scatter(start[0],start[1],label="Start")
ax.scatter(goal[0],goal[1],marker="*",s=200,label="Goal")

for obs in obstacles:
    ax.scatter(obs[0],obs[1],marker="x")

ax.set_xlim(-1,12)
ax.set_ylim(-1,12)
ax.grid()

ax.legend()

st.pyplot(fig)
