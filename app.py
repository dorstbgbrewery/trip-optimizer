import streamlit as st
import googlemaps
import re

# Initialize Google Maps Client
# Get your key at: https://console.cloud.google.com/
gmaps = googlemaps.Client(key='YOUR_API_KEY')

st.title("📍 Optimal Trip Planner")
st.subheader("Turn Map Links into an Efficient Route")

# 1. User Input
raw_links = st.text_area("Paste Google Maps Links (one per line):", height=200)

if st.button("Optimize My Route"):
    if raw_links:
        # 2. Simple Extraction Logic
        # (This cleans the input and identifies the locations)
        stops = [line.strip() for line in raw_links.split('\n') if line.strip()]
        
        if len(stops) < 2:
            st.error("Please provide at least 2 locations.")
        else:
            with st.spinner('Calculating the shortest path...'):
                # 3. Call Google Directions with Optimization
                # We use the first link as the Start and End point
                result = gmaps.directions(
                    origin=stops[0],
                    destination=stops[0],
                    waypoints=stops[1:],
                    optimize_waypoints=True,
                    mode="driving"
                )

                # 4. Extract the optimized order
                order = result[0]['waypoint_order']
                # Re-index our list based on Google's logic
                optimized_list = [stops[0]]
                for idx in order:
                    optimized_list.append(stops[idx + 1])
                optimized_list.append(stops[0])

                # 5. Display Result
                st.success("Route Optimized!")
                for i, stop in enumerate(optimized_list):
                    st.write(f"**Stop {i}:** {stop}")
                
                # 6. Create a "Master Link"
                # This opens all stops in order in the Google Maps app
                base_url = "https://www.google.com/maps/dir/"
                final_url = base_url + "/".join(optimized_list).replace(" ", "+")
                st.link_button("🚀 Open Route in Google Maps", final_url)
    else:
        st.warning("Please paste some links first!")

