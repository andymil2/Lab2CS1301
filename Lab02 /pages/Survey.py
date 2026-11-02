# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Sports Fan Survey 🏀")
st.write("Please fill out the form below about your sports habits.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    favorite_sport = st.text_input("What is your favorite sport?")
    hours_watched = st.text_input("How many hours per week do you watch sports?")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.
        if favorite_sport.strip() == "" or hours_watched.strip() == "":
            st.warning("Please fill out both boxes.")
        elif not hours_watched.isdigit():
            st.warning("Please enter a whole number for hours watched.")
        else:
            new_data = pd.DataFrame({"Favorite Sport": [favorite_sport], "Hours Watched": [int(hours_watched)]})
            if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
                with open("data.csv", "a") as file:
                    file.write("\n")
                new_data.to_csv("data.csv", mode="a", header=False, index=False)
            else:
                new_data.to_csv("data.csv", index=False)
            st.success("Your data has been submitted!")
            st.write(f"You entered: **Favorite sport:** {favorite_sport}, **Hours watched:** {hours_watched}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Sports Survey Data")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists("data.csv") and os.path.getsize("data.csv") > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv("data.csv")
    # Display the DataFrame as a table.
    current_data_df.index = current_data_df.index + 1
    st.dataframe(current_data_df)
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
