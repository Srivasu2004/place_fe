import streamlit as st
import requests
import folium
from streamlit_folium import st_folium

BACKEND_URL = "S_url"

HYDERABAD = [17.3850, 78.4867]

st.title("🗺️ AI Travel + Real Route Map")


# Sample place
places = {
    "Charminar": [17.3616, 78.4747],
    "Golconda Fort": [17.3833, 78.4011],
    "Hussain Sagar": [17.4239, 78.4738]
}

place = st.selectbox("Select Place", list(places.keys()))
dest = places[place]


if st.button("🚗 Show Real Route"):

    res = requests.get(
        f"{BACKEND_URL}/route",
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

        # ======================
        # MAP
        # ======================
        m = folium.Map(location=HYDERABAD, zoom_start=10)

        # Start marker
        folium.Marker(HYDERABAD, popup="Hyderabad", icon=folium.Icon(color="red")).add_to(m)

        # Destination marker
        folium.Marker(dest, popup=place, icon=folium.Icon(color="green")).add_to(m)

        # ======================
        # REAL ROUTE LINE
        # ======================
        coords = data["route_geometry"]

        # decode polyline
        import polyline
        route_points = polyline.decode(coords)

        folium.PolyLine(
            route_points,
            color="blue",
            weight=5,
            opacity=0.8
        ).add_to(m)

        st_folium(m, width=1000, height=500)
