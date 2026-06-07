import streamlit as st
import requests
import pandas as pd
import folium

from streamlit_folium import st_folium

BACKEND_URL = "url_place"

HYDERABAD_LAT = 17.3850
HYDERABAD_LNG = 78.4867

PLACES = [
    {
        "name": "Birla Mandir",
        "lat": 17.4062,
        "lng": 78.4691,
        "rating": 4.7,
        "address": "Hill Fort Road, Hyderabad"
    },
    {
        "name": "Golconda Fort",
        "lat": 17.3833,
        "lng": 78.4011,
        "rating": 4.6,
        "address": "Khair Complex, Hyderabad"
    },
    {
        "name": "Ramoji Film City",
        "lat": 17.2543,
        "lng": 78.6808,
        "rating": 4.6,
        "address": "Abdullapurmet, Hyderabad"
    },
    {
        "name": "Charminar",
        "lat": 17.3616,
        "lng": 78.4747,
        "rating": 4.5,
        "address": "Old City, Hyderabad"
    },
    {
        "name": "Hussain Sagar",
        "lat": 17.4239,
        "lng": 78.4738,
        "rating": 4.4,
        "address": "Tank Bund, Hyderabad"
    }
]

st.set_page_config(
    page_title="Wonderful Places Hyderabad",
    layout="wide"
)

st.title("🌍 Wonderful Tourist Places Near Hyderabad")

top_n = st.number_input(
    "Enter Number of Top Places",
    min_value=1,
    max_value=len(PLACES),
    value=3
)

filtered_places = PLACES[:top_n]

st.subheader("🏆 Top Tourist Places")

for i, place in enumerate(filtered_places, start=1):
    st.markdown(f"### {i}. {place['name']}")
    st.write(f"⭐ Rating : {place['rating']}")
    st.write(f"📍 Address : {place['address']}")
    st.divider()

st.subheader("📋 Places Table")

df = pd.DataFrame(filtered_places)

st.dataframe(
    df[["name", "rating", "address"]],
    width="stretch"
)

place_name = st.selectbox(
    "Select Tourist Place",
    [p["name"] for p in filtered_places]
)

selected_place = next(
    p for p in filtered_places
    if p["name"] == place_name
)

st.subheader("📍 Selected Place")

col1, col2 = st.columns(2)

with col1:
    st.write("Place:", selected_place["name"])
    st.write("Rating:", selected_place["rating"])

with col2:
    st.write("Address:", selected_place["address"])

m = folium.Map(
    location=[HYDERABAD_LAT, HYDERABAD_LNG],
    zoom_start=10
)

folium.Marker(
    [HYDERABAD_LAT, HYDERABAD_LNG],
    popup="Hyderabad"
).add_to(m)

folium.Marker(
    [selected_place["lat"], selected_place["lng"]],
    popup=selected_place["name"]
).add_to(m)

st.subheader("🗺️ Location Map")

st_folium(
    m,
    width=1000,
    height=500
)

if st.button("🚗 Show Route"):

    try:

        response = requests.get(
            f"{BACKEND_URL}/route",
            params={
                "dest_lat": selected_place["lat"],
                "dest_lng": selected_place["lng"]
            }
        )

        data = response.json()

        if "error" in data:
            st.error(data["error"])

        else:

            st.success(
                f"📍 Place : {data['place_name']}"
            )

            st.success(
                f"📏 Distance : {data['distance']}"
            )

            st.info(
                f"⏱ Travel Time : {data['duration']}"
            )

            st.write(
                f"🏠 Location : {data['location']}"
            )

            route_map = folium.Map(
                location=[HYDERABAD_LAT, HYDERABAD_LNG],
                zoom_start=10
            )

            folium.Marker(
                [HYDERABAD_LAT, HYDERABAD_LNG],
                popup="Hyderabad"
            ).add_to(route_map)

            folium.Marker(
                [selected_place["lat"],
                 selected_place["lng"]],
                popup=selected_place["name"]
            ).add_to(route_map)

            folium.PolyLine(
                [
                    [HYDERABAD_LAT, HYDERABAD_LNG],
                    [
                        selected_place["lat"],
                        selected_place["lng"]
                    ]
                ],
                weight=6
            ).add_to(route_map)

            st.subheader("🛣️ Route Map")

            st_folium(
                route_map,
                width=1000,
                height=600
            )

    except Exception as e:
        st.error(f"Error: {str(e)}")