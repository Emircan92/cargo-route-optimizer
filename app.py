import streamlit as st
import json
import networkx as nx
import folium
from streamlit.components.v1 import html

BASE_COST_PER_KM = 1.0
HUB_DISCOUNT = 0.8  # 20% cheaper

# Load the data
with open("data.json", "r") as f:
    data = json.load(f)

# Step 1: Create a graph
G = nx.Graph()

# Step 2: Add cities (nodes)
for country in data["countries"]:
    for city in country["cities"]:
        G.add_node(city["name"], is_hub=city["is_hub"], coords=city["coords"])

# Step 3: Add routes (egdes with distance)
for route in data["routes"]:
    from_city = route["from"]
    to_city = route["to"]
    distance = route["distance"]
    
    cost = distance * BASE_COST_PER_KM
    
    # Bias: apply 20% discount if either side is a hub
    if G.nodes[from_city]["is_hub"] or G.nodes[to_city]["is_hub"]:
        cost *= HUB_DISCOUNT
    
    G.add_edge(from_city, to_city, weight=cost, distance=distance)

city_names = sorted(G.nodes)

# Streamlit UI
st.title("🌍 Cargo Route Optimizer")
source = st.selectbox("Select source city", city_names)
target = st.selectbox("Select destination city", city_names)

if st.button("Find Best Route"):
    if source == target:
        st.warning("Please select different cities.")
    else:
        try:
            path = nx.dijkstra_path(G, source, target, weight="weight")
            total_cost = nx.dijkstra_path_length(G, source, target, weight="weight")

            # Total distance
            total_distance = 0
            for i in range(len(path) - 1):
                edge = G.get_edge_data(path[i], path[i + 1])
                total_distance += edge["distance"]

            st.success(f"✅ Route found: {' → '.join(path)}")
            st.markdown(f"- **Total cost**: {total_cost:.2f} units")
            st.markdown(f"- **Total distance**: {total_distance:.0f} km")

            # Generate folium map
            all_coords = {city: G.nodes[city]['coords'] for city in G.nodes}
            avg_lat = sum(c[0] for c in all_coords.values()) / len(all_coords)
            avg_lon = sum(c[1] for c in all_coords.values()) / len(all_coords)

            m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)

            # Draw all edges
            for u, v in G.edges:
                folium.PolyLine(
                    [G.nodes[u]['coords'], G.nodes[v]['coords']],
                    color='gray', weight=2, opacity=0.4
                ).add_to(m)

            # Draw all cities
            for city in G.nodes:
                folium.CircleMarker(
                    location=G.nodes[city]['coords'],
                    radius=6,
                    color='green' if G.nodes[city]['is_hub'] else 'blue',
                    fill=True,
                    popup=f"{city} (HUB)" if G.nodes[city]['is_hub'] else city
                ).add_to(m)

            # Draw optimized path
            route_coords = [G.nodes[city]["coords"] for city in path]
            folium.PolyLine(route_coords, color="red", weight=5, popup="Optimized Route").add_to(m)

            # Show map
            m.save("map.html")
            with open("map.html", "r", encoding="utf-8") as f:
                map_html = f.read()
            html(map_html, height=600)

        except nx.NetworkXNoPath:
            st.error("No path found between the selected cities.")

st.markdown(
    """
    <hr style="margin-top: 2em; margin-bottom: 0.5em;">
    <div style="text-align: center; font-size: 0.85em; color: #888;">
        Made with ❤️ using <a href="https://streamlit.io" target="_blank" style="color: #6A0DAD;">Streamlit</a> |
        <a href="https://github.com/Emircan92/cargo-route-optimizer" target="_blank" style="color: #6A0DAD;">View on GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)