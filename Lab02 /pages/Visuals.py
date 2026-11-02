# This creates the page for displaying data visualizations.

import streamlit as st
import json
import matplotlib.pyplot as plt
import pandas as pd

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")


# PART 1: GRAPHS FROM data.json
with open("data.json", "r") as file:
    data = json.load(file)

chart_title = data["chart_title"]
data_points = data["data_points"]

team_names = []
win_totals = []

for point in data_points:
    team_names.append(point["label"])
    win_totals.append(point["value"])

#GRAPH 1
    
st.header("NBA Team Wins")
fig, ax = plt.subplots(figsize=(10,6))

ax.bar(team_names, win_totals, width=0.5)
ax.set_title(chart_title)
ax.set_xlabel("NBA Team")
ax.set_ylabel("Number of Wins")

plt.xticks(rotation=45, ha="right")
plt.tight_layout()

st.pyplot(fig)

#GRAPH 2

st.header("Explore a Team")

if "selected_team" not in st.session_state:
    st.session_state.selected_team = team_names[0]

selected_team = st.selectbox("Choose an NBA team:", team_names, key="selected_team")

for point in data_points:
    if point["label"] == selected_team:
        selected_wins = point["value"]
        selected_losses = point["losses"]

st.subheader(selected_team + ": Wins vs. Losses")

fig2, ax2 = plt.subplots()

ax2.pie([selected_wins, selected_losses], labels=["Wins", "Losses"], autopct="%1.1f%%", startangle=90)
ax2.set_title(selected_team + " Season Record")

st.pyplot(fig2)

# PART 2: GRAPHS FROM data.csv

# STATIC VISUALIZATION

st.header("Sports Survey Results")
sports_data = pd.read_csv("data.csv")

if len(sports_data) > 0:
    sport_counts = sports_data["Favorite Sport"].value_counts()
    fig3, ax3 = plt.subplots()
    ax3.pie(sport_counts.values, labels=sport_counts.index, autopct = "%1.1f%%")
    ax3.set_title("Favorite Sports")
    st.pyplot(fig3)
else:
    st.warning("There is no survey data yet.")

# DYNAMIC VISUALIZATION

st.subheader("Favorite Sports by Hours Watched")
if "min_hours" not in st.session_state:
    st.session_state.min_hours = 0
max_hours = int(sports_data["Hours Watched"].max())
min_hours = st.slider("Minimum hours watched per week:", min_value = 0, max_value = max(1, max_hours), key = "min_hours")
filtered_data = sports_data[sports_data["Hours Watched"] >= min_hours]
filtered_counts = filtered_data["Favorite Sport"].value_counts()
if len(filtered_data) > 0:
    fig4, ax4 = plt.subplots()
    ax4.bar(filtered_counts.index, filtered_counts.values)
    ax4.set_title("Favorite Sports for Selected Hours")
    ax4.set_xlabel("Favorite Sport")
    ax4.set_ylabel("Number of Responses")
    ax4.yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig4)
else:
    st.warning("No responses match your selection.")


