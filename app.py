import streamlit as st
import requests
import folium
from streamlit_folium import st_folium
import polyline

BACKEND_URL = "https://place-be-7.onrender.com"

START = [17.3850, 78.4867]

st.title("🧭 Live Navigation System (AI + Real Routes)")


# Sample destinations
places = {
    "Charminar": [17.3616, 78.4747],
    "Golconda Fort": [17.3833, 78.4011],
    "Hussain Sagar": [17.4239, 78.4738]
}

place = st.selectbox("Choose Destination", list(places.keys()))
dest = places[place]


if st.button("🚀 Start Navigation"):

    res = requests.get(
        f"{BACKEND_URL}/navigate",
        params={
            "dest_lat": dest[0],
            "dest_lng": dest[1]
        }
    )

    data = res.json()

    if "error" in data:
        st.error(data["error"])
    else:

        st.success(f"Distance: {data['distance_km']} km")
        st.info(f"Duration: {data['duration_min']} min")

        # =========================
        # TURN-BY-TURN DIRECTIONS
        # =========================
        st.subheader("🧭 Turn-by-Turn Navigation")

        for i, step in enumerate(data["instructions"], 1):
            st.write(f"{i}. {step['instruction']}")

        # =========================
        # MAP
        # =========================
        m = folium.Map(location=START, zoom_start=12)

        folium.Marker(START, popup="Start", icon=folium.Icon(color="red")).add_to(m)
        folium.Marker(dest, popup=place, icon=folium.Icon(color="green")).add_to(m)

        # Decode real route
        route_points = polyline.decode(data["geometry"])

        folium.PolyLine(route_points, color="blue", weight=5).add_to(m)

        st.subheader("🗺️ Live Route Map")
        st_folium(m, width=1000, height=500)
