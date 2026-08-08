import streamlit as st
import pandas as pd
from db import Database
from graph import Graph
from algorithms import SearchAlgorithms

# Page configuration
st.set_page_config(
    page_title="AI Travel Planner - Bangladesh",
    page_icon="🇧🇩",
    layout="wide"
)

# Initialize database and graph
@st.cache_resource
def init_data():
    db = Database()
    graph = Graph()
    
    all_cities = db.get_cities()
    all_routes = db.get_routes()
    graph.build_graph(all_cities, all_routes)
    search_algo = SearchAlgorithms(graph)
    
    return db, graph, search_algo, all_cities, all_routes

# Load data
db, graph, search_algo, cities, routes = init_data()

# Create city list for dropdowns
city_names = [city['name'] for city in cities]

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #e3f2fd 0%, #f0f8ff 50%, #e8f4fd 100%);
    }
    .main-header {
        background: linear-gradient(135deg, #0984e3 0%, #74b9ff 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    }
    .route-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>🇧🇩 AI Travel Planner - Bangladesh</h1><p>Plan your journey across beautiful Bangladesh</p></div>', unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗺️ Plan Your Journey")
    
    # Route selection
    source = st.selectbox("📍 From City", city_names, key="source")
    destination = st.selectbox("📍 To City", city_names, key="dest")
    
    # Filters
    col_budget, col_time = st.columns(2)
    with col_budget:
        budget = st.number_input("💰 Budget (৳)", min_value=0.0, step=100.0, value=None, placeholder="No limit")
    with col_time:
        max_time = st.number_input("⏱️ Max Time (minutes)", min_value=0, step=30, value=None, placeholder="No limit")
    
    # Search algorithms
    st.subheader("Choose Search Algorithm:")
    search_type = st.radio(
        "Select algorithm",
        ["💰 Cheapest (Uniform Cost)", "⚡ Fastest (Greedy Best-First)", "⭐ Best (A*)", "🛑 Least Stops (BFS)"],
        horizontal=True
    )
    
    # Map search type to algorithm
    type_map = {
        "💰 Cheapest (Uniform Cost)": "cheapest",
        "⚡ Fastest (Greedy Best-First)": "fastest",
        "⭐ Best (A*)": "best",
        "🛑 Least Stops (BFS)": "least_stops"
    }
    
    # Search button
    if st.button("🚀 Find Route", type="primary", use_container_width=True):
        if source == destination:
            st.error("❌ Source and destination cannot be the same!")
        else:
            with st.spinner("Searching for the best route..."):
                algorithm = type_map[search_type]
                
                # Call the search algorithm
                if algorithm == "cheapest":
                    path, total_cost, total_time, avg_rating = search_algo.uniform_cost_search(
                        source, destination, budget, max_time
                    )
                elif algorithm == "fastest":
                    path, total_cost, total_time, avg_rating = search_algo.greedy_best_first_search(
                        source, destination, budget, max_time
                    )
                elif algorithm == "best":
                    path, total_cost, total_time, avg_rating = search_algo.a_star_search(
                        source, destination, budget, max_time
                )
                else:  # least_stops
                    path, total_cost, total_time, avg_rating = search_algo.bfs(
                        source, destination, budget, max_time
                    )
                
                if path:
                    st.success("✅ Route found!")
                    
                    # Display route details
                    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
                    with col_r1:
                        st.metric("📍 Path", " → ".join(path))
                    with col_r2:
                        st.metric("💰 Total Cost", f"৳{total_cost:.2f}")
                    with col_r3:
                        st.metric("⏱️ Total Time", f"{total_time} min")
                    with col_r4:
                        st.metric("⭐ Avg Rating", f"{avg_rating:.1f} ⭐")
                    
                    # Show route on map (if you have coordinates)
                    # st.map(...)
                else:
                    st.error("❌ No route found matching your criteria. Try adjusting budget or time constraints.")

with col2:
    st.subheader("📍 Available Cities")
    city_df = pd.DataFrame(cities)
    st.dataframe(city_df[['name']], hide_index=True, use_container_width=True)

# Show all routes
st.markdown("---")
st.subheader("🗺️ All Available Routes")

# Create a DataFrame for routes
routes_df = pd.DataFrame(routes)
routes_df['cost'] = routes_df['cost'].astype(float)
routes_df['rating'] = routes_df['rating'].astype(float)

# Add currency symbol
routes_df['cost_formatted'] = routes_df['cost'].apply(lambda x: f"৳{x:.2f}")
routes_df['rating_formatted'] = routes_df['rating'].apply(lambda x: f"{x:.1f} ⭐")

# Display table
st.dataframe(
    routes_df[['source', 'destination', 'cost_formatted', 'time', 'distance', 'rating_formatted']],
    column_config={
        "source": "From",
        "destination": "To",
        "cost_formatted": "Cost",
        "time": "Time (min)",
        "distance": "Distance (km)",
        "rating_formatted": "Rating"
    },
    hide_index=True,
    use_container_width=True
)

# Footer
st.markdown("---")
st.markdown("🇧🇩 AI Travel Planner - Made for Bangladesh | 20 Cities | 100 Routes")
