import streamlit as st
from utils import *

# 1. Initialize UI, Page Config, Header, and Sidebar FIRST
# This function will set up st.session_state.menu
main()

# 2. Load data
df = load_data()

# 3. Get the selected menu item from the session state
menu = st.session_state.menu

# 4. Route to the correct page
if menu == "DASHBOARD":
    st.subheader("📊 DASHBOARD OVERVIEW")
    create_dashboard_tab(df)

elif menu == "KPI":
    st.subheader("📈 KEY PERFORMANCE INDICATORS")
    # Add KPI function here

elif menu == "TIME":
    st.subheader("🕒 TIME ANALYSIS")
    # Add Time function here

elif menu == "LOCATION":
    st.subheader("📍 LOCATION ANALYSIS")
    # Add Location function here

elif menu == "CONTRIBUTING FACTORS":
    st.subheader("🚗 CONTRIBUTING FACTORS")
    create_contributing_factors_tab(df)

elif menu == "INJURIES":
    st.subheader("🚑 INJURIES")
    create_injuries_tab()

elif menu == "PREDICTIONS":
    st.subheader("🔮 PREDICTIONS")
    create_predictions_tab()