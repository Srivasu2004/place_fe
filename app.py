import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

# ======================
# BACKEND URL
# ======================
BACKEND_URL = "url_place"   # change to Render URL when deployed

# ======================
# HYDERABAD CENTER
# ======================
HYDERABAD_LAT = 17.3850
HYDERABAD_LNG = 78.4867


# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Hyderabad Tourist AI",
    layout="wide"
)

st.title("🌍 Hyderabad Tourist Route Finder")


# ======================
# FETCH PLACES FROM BACKEND
# ======================
@st.cache_data
def load_places():
    try:
        res = requests.get(f"{BACKEND_URL}/places", timeout=10)
        return res.json()
    except:
        return []


PLACES = load_places()


if not PLACES:
    st.error("Backend not connected or /places API failed")
    st.stop()


# ======================
# UI - SELECT PLACE
# ======================
place_names = [p["name"] for p in PLACES]

selected_name = st.selectbox("Choose a Tourist Place", place_names)

selected_place = next(p for p in PLACES if p["name"] == selected_name)


# ======================
# SHOW DETAILS
# ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Place Details")
    st.write("Name:", selected_place["name"])
    st.write("Address:", selected_place["address"])

with col2:
    st.subheader("📊 Quick Info")
    st.metric("Latitude", selected_place["lat"])
    st.metric("Longitude", selected_place["lng"])


# ======================
# MAP - MARKER VIEW
# ======================
st.subheader("🗺️ Map View")

map_obj = folium.Map(
    location=[HYDERABAD_LAT, HYDERABAD_LNG],
    zoom_start=10
)

# Hyderabad marker
folium.Marker(
    [HYDERABAD_LAT, HYDERABAD_LNG],
    popup="Hyderabad",
    icon=folium.Icon(color="red")
).add_to(map_obj)

# Selected place marker
folium.Marker(
    [selected_place["lat"], selected_place["lng"]],
    popup=selected_place["name"],
    icon=folium.Icon(color="green")
).add_to(map_obj)

st_folium(map_obj, width=1000, height=500)


# ======================
# ROUTE BUTTON
# ======================
if st.button("🚗 Get Route from Hyderabad"):

    try:
        response = requests.get(
            f"{BACKEND_URL}/route",
            params={
                "dest_lat": selected_place["lat"],
                "dest_lng": selected_place["lng"]
            },
            timeout=15
        )

        data = response.json()

        if response.status_code != 200:
            st.error(data.get("detail", "Error fetching route"))
        else:
            st.success(f"📍 Place: {data['place_name']}")
            st.info(f"📏 Distance: {data['distance']}")
            st.info(f"⏱ Duration: {data['duration']}")
            st.write(f"🏠 Location: {data['location']}")

            # ======================
            # ROUTE MAP
            # ======================
            route_map = folium.Map(
                location=[HYDERABAD_LAT, HYDERABAD_LNG],
                zoom_start=10
            )

            folium.Marker(
                [HYDERABAD_LAT, HYDERABAD_LNG],
                popup="Hyderabad",
                icon=folium.Icon(color="red")
            ).add_to(route_map)

            folium.Marker(
                [selected_place["lat"], selected_place["lng"]],
                popup=selected_place["name"],
                icon=folium.Icon(color="green")
            ).add_to(route_map)

            folium.PolyLine(
                [
                    [HYDERABAD_LAT, HYDERABAD_LNG],
                    [selected_place["lat"], selected_place["lng"]]
                ],
                weight=5,
                color="blue"
            ).add_to(route_map)

            st.subheader("🛣️ Route Map")
            st_folium(route_map, width=1000, height=600)

    except requests.exceptions.RequestException as e:
        st.error(f"Backend Error: {e}")
