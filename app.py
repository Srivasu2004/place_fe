import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

# ======================
# BACKEND URL
# ======================
BACKEND_URL = "ORS_API_KEY"   # change this when deploying

# ======================
# HYDERABAD CENTER
# ======================
HYDERABAD_LAT = 17.3850
HYDERABAD_LNG = 78.4867


# ======================
# PAGE CONFIG
# ======================
st.set_page_config(
    page_title="Hyderabad Tourist Explorer",
    layout="wide"
)

st.title("🌍 Hyderabad Tourist Explorer (AI Route System)")


# ======================
# LOAD PLACES FROM BACKEND
# ======================
@st.cache_data
def get_places():
    try:
        res = requests.get(f"{BACKEND_URL}/places", timeout=10)
        return res.json()
    except:
        return []


places = get_places()

if not places:
    st.error("❌ Backend not running or /places API failed")
    st.stop()


# ======================
# SELECT PLACE
# ======================
place_names = [p["name"] for p in places]

selected_name = st.selectbox("Select a Tourist Place", place_names)

selected_place = next(p for p in places if p["name"] == selected_name)


# ======================
# DETAILS SECTION
# ======================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📍 Place Info")
    st.write("Name:", selected_place["name"])
    st.write("Address:", selected_place["address"])

with col2:
    st.subheader("📊 Coordinates")
    st.metric("Latitude", selected_place["lat"])
    st.metric("Longitude", selected_place["lng"])


# ======================
# MAP VIEW
# ======================
st.subheader("🗺️ Map View")

map_view = folium.Map(
    location=[HYDERABAD_LAT, HYDERABAD_LNG],
    zoom_start=10
)

# Hyderabad marker
folium.Marker(
    [HYDERABAD_LAT, HYDERABAD_LNG],
    popup="Hyderabad",
    icon=folium.Icon(color="red")
).add_to(map_view)

# Selected place marker
folium.Marker(
    [selected_place["lat"], selected_place["lng"]],
    popup=selected_place["name"],
    icon=folium.Icon(color="green")
).add_to(map_view)

st_folium(map_view, width=1000, height=500)


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
            st.error(data.get("detail", "Something went wrong"))
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

            # start marker
            folium.Marker(
                [HYDERABAD_LAT, HYDERABAD_LNG],
                popup="Start: Hyderabad",
                icon=folium.Icon(color="red")
            ).add_to(route_map)

            # destination marker
            folium.Marker(
                [selected_place["lat"], selected_place["lng"]],
                popup=selected_place["name"],
                icon=folium.Icon(color="green")
            ).add_to(route_map)

            # straight route line (API does NOT return real polyline in your backend)
            folium.PolyLine(
                [
                    [HYDERABAD_LAT, HYDERABAD_LNG],
                    [selected_place["lat"], selected_place["lng"]]
                ],
                color="blue",
                weight=5
            ).add_to(route_map)

            st.subheader("🛣️ Route Map")
            st_folium(route_map, width=1000, height=600)

    except requests.exceptions.RequestException as e:
        st.error(f"Backend Error: {e}")
