import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import seaborn as sns

# Page configuration
st.set_page_config(
    page_title="Smart City Citizen Dashboard",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #424242;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #f0f0f0;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1E88E5;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #616161;
    }
    .stPlotlyChart {
        background-color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .stSelectbox label, .stMultiselect label, .stSlider label {
        font-weight: 600;
        color: #424242;
    }
    .css-1d391kg {  /* Sidebar background */
        background-color: #f9fafb;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🚀 Smart City Citizen Activity Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    "Explore citizen behavior, transportation patterns, carbon footprint, and lifestyle trends "
    "in our connected urban environment."
)

# Function to load or generate data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("dataset/smart_city_citizen_activity.csv")
    except FileNotFoundError:
        # Generate mock data if file not found
        st.info("Using generated mock data. Replace with your actual dataset for production use.")
        return generate_mock_data(300)

def generate_mock_data(n_samples):
    np.random.seed(42)  # For reproducible results
    
    # Define possible values
    transport_modes = ['Bus', 'Car', 'Bicycle', 'Walk', 'EV', 'Train', 'Motorcycle']
    genders = ['Male', 'Female', 'Non-binary']
    districts = ['Downtown', 'Uptown', 'Westside', 'Eastside', 'Suburbs', 'Industrial']
    
    # Generate data
    data = {
        'Age': np.random.randint(18, 80, n_samples),
        'Gender': np.random.choice(genders, n_samples),
        'District': np.random.choice(districts, n_samples),
        'Mode_of_Transport': np.random.choice(transport_modes, n_samples),
        'Carbon_Footprint_kgCO2': np.random.normal(10, 5, n_samples).clip(0, 30),
        'Steps_Walked': np.random.randint(1000, 15000, n_samples),
        'Sleep_Hours': np.random.normal(7, 1.5, n_samples).clip(4, 10),
        'Social_Media_Hours': np.random.exponential(2, n_samples).clip(0, 10),
        'Public_Transport_Usage': np.random.choice(['Daily', 'Weekly', 'Monthly', 'Rarely', 'Never'], n_samples),
        'Recycling_Rate': np.random.normal(65, 20, n_samples).clip(0, 100),
        'Digital_Service_Usage': np.random.randint(1, 10, n_samples)
    }
    
    return pd.DataFrame(data)

# Load data
df = load_data()

# Sidebar filters
with st.sidebar:
    st.markdown('<div class="sub-header">🔍 Filters</div>', unsafe_allow_html=True)
    
    # Date range filter (using current date for demo)
    today = datetime.now().date()
    date_range = st.date_input(
        "Date Range",
        value=(today, today),
        help="Filter data by date range"
    )
    
    # Age range slider
    age_range = st.slider(
        "Age Range", 
        int(df["Age"].min()), int(df["Age"].max()), 
        (20, 60),
        help="Filter citizens by age"
    )
    
    # Gender multiselect
    gender_filter = st.multiselect(
        "Gender",
        options=df["Gender"].unique(),
        default=list(df["Gender"].unique()),
        help="Select one or more gender categories"
    )
    
    # District filter
    if "District" in df.columns:
        district_filter = st.multiselect(
            "District",
            options=df["District"].unique(),
            default=list(df["District"].unique()),
            help="Filter by city district"
        )
    else:
        district_filter = list(df["District"].unique()) if "District" in df.columns else None
    
    # Transport mode filter
    transport_filter = st.multiselect(
        "Transport Mode",
        options=df["Mode_of_Transport"].unique(),
        default=list(df["Mode_of_Transport"].unique()),
        help="Filter by transportation method"
    )
    
    # Apply filters
    filtered_df = df[
        (df["Age"] >= age_range[0]) & 
        (df["Age"] <= age_range[1]) & 
        (df["Gender"].isin(gender_filter)) & 
        (df["Mode_of_Transport"].isin(transport_filter))
    ]
    
    if district_filter and "District" in df.columns:
        filtered_df = filtered_df[filtered_df["District"].isin(district_filter)]
    
    # Show number of records after filtering
    st.info(f"Showing {len(filtered_df)} of {len(df)} records")
    
    # Reset filters button
    if st.button("Reset Filters", use_container_width=True):
        st.rerun()

# Display key metrics at the top
st.markdown('<div class="sub-header">📊 Key Metrics</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{:.1f}</div>
        <div class="metric-label">Average Carbon Footprint (kg CO₂)</div>
    </div>
    """.format(filtered_df["Carbon_Footprint_kgCO2"].mean()), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{:.0f}</div>
        <div class="metric-label">Average Daily Steps</div>
    </div>
    """.format(filtered_df["Steps_Walked"].mean()), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{:.1f}</div>
        <div class="metric-label">Average Sleep Hours</div>
    </div>
    """.format(filtered_df["Sleep_Hours"].mean()), unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">{:.1f}</div>
        <div class="metric-label">Daily Social Media Hours</div>
    </div>
    """.format(filtered_df["Social_Media_Hours"].mean()), unsafe_allow_html=True)

# Main tabs for visualizations
tab1, tab2, tab3 = st.tabs(["📋 Demographics", "🚗 Transport & Environment", "🌐 Lifestyle Trends"])

# ---------- TAB 1: Demographics ----------
with tab1:
    st.markdown('<div class="sub-header">Citizen Demographics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age distribution (Plotly)
        fig = px.histogram(
            filtered_df, 
            x="Age",
            nbins=20,
            color_discrete_sequence=['#1E88E5'],
            title="Age Distribution of Citizens",
            labels={"Age": "Age", "count": "Number of Citizens"},
            opacity=0.8
        )
        fig.update_layout(
            xaxis_title="Age",
            yaxis_title="Number of Citizens",
            plot_bgcolor='rgba(0,0,0,0)',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gender distribution (Plotly)
        gender_counts = filtered_df["Gender"].value_counts().reset_index()
        gender_counts.columns = ['Gender', 'Count']
        
        fig = px.pie(
            gender_counts, 
            values='Count', 
            names='Gender',
            title="Gender Distribution",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # District distribution if available
    if "District" in filtered_df.columns:
        district_counts = filtered_df["District"].value_counts().reset_index()
        district_counts.columns = ['District', 'Count']
        
        fig = px.bar(
            district_counts,
            x="District",
            y="Count",
            color="District",
            title="Citizen Distribution by District",
            labels={"District": "District", "Count": "Number of Citizens"},
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig.update_layout(
            xaxis_title="District",
            yaxis_title="Number of Citizens",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

# ---------- TAB 2: Transport & Environment ----------
with tab2:
    st.markdown('<div class="sub-header">Transportation & Environmental Impact</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Transport mode distribution
        transport_counts = filtered_df["Mode_of_Transport"].value_counts().reset_index()
        transport_counts.columns = ['Mode', 'Count']
        
        fig = px.bar(
            transport_counts,
            x="Mode",
            y="Count",
            color="Mode",
            title="Transportation Modes Used",
            labels={"Mode": "Mode of Transport", "Count": "Number of Citizens"},
            color_discrete_sequence=px.colors.qualitative.Safe
        )
        fig.update_layout(
            xaxis_title="Mode of Transport",
            yaxis_title="Number of Citizens",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average carbon footprint by transport mode
        transport_carbon = filtered_df.groupby("Mode_of_Transport")["Carbon_Footprint_kgCO2"].mean().reset_index()
        transport_carbon = transport_carbon.sort_values("Carbon_Footprint_kgCO2")
        
        fig = px.bar(
            transport_carbon,
            x="Carbon_Footprint_kgCO2",
            y="Mode_of_Transport",
            orientation='h',
            title="Average Carbon Footprint by Transport Mode",
            labels={
                "Carbon_Footprint_kgCO2": "Average CO₂ (kg)",
                "Mode_of_Transport": "Mode of Transport"
            },
            color="Carbon_Footprint_kgCO2",
            color_continuous_scale='Reds'
        )
        fig.update_layout(
            yaxis_title="Mode of Transport",
            xaxis_title="Average CO₂ (kg)",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # EV usage by age group
    st.markdown('<div class="sub-header">EV Adoption Patterns</div>', unsafe_allow_html=True)
    
    # Create age groups
    age_bins = [18, 25, 35, 45, 55, 65, 75, 100]
    age_labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
    df_age_group = df.copy()
    df_age_group["Age_Group"] = pd.cut(df_age_group["Age"], bins=age_bins, labels=age_labels, right=False)
    
    # EV users by age group
    ev_age_df = df_age_group[df_age_group["Mode_of_Transport"] == "EV"]
    ev_age_distribution = ev_age_df["Age_Group"].value_counts().sort_index().reset_index()
    ev_age_distribution.columns = ['Age_Group', 'Count']
    
    fig = px.bar(
        ev_age_distribution,
        x="Age_Group",
        y="Count",
        title="EV Usage by Age Group",
        labels={"Age_Group": "Age Group", "Count": "Number of EV Users"},
        color="Count",
        color_continuous_scale='Greens'
    )
    fig.update_layout(
        xaxis_title="Age Group",
        yaxis_title="Number of EV Users",
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Carbon footprint map if district data is available
    if "District" in filtered_df.columns:
        st.markdown('<div class="sub-header">Carbon Footprint by District</div>', unsafe_allow_html=True)
        district_carbon = filtered_df.groupby("District")["Carbon_Footprint_kgCO2"].mean().reset_index()
        
        fig = px.choropleth_mapbox(
            district_carbon,
            geojson=None,  # This would use a real geojson in a production app
            locations="District",
            color="Carbon_Footprint_kgCO2",
            color_continuous_scale="Reds",
            mapbox_style="carto-positron",
            zoom=10,
            center={"lat": 37.7749, "lon": -122.4194},  # Sample coordinates
            opacity=0.7,
            labels={"Carbon_Footprint_kgCO2": "Avg CO₂ (kg)"}
        )
        fig.update_layout(
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            height=400
        )
        
        # Placeholder message instead of the actual map (since we don't have real geographic data)
        st.warning("This would display a choropleth map of carbon footprint by district with real geographic data.")

# ---------- TAB 3: Lifestyle Trends ----------
with tab3:
    st.markdown('<div class="sub-header">Lifestyle & Well-being Trends</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Sleep hours distribution
        fig = px.histogram(
            filtered_df,
            x="Sleep_Hours",
            nbins=12,
            color_discrete_sequence=['#9c27b0'],
            title="Distribution of Sleep Hours",
            labels={"Sleep_Hours": "Sleep Hours", "count": "Number of Citizens"},
            opacity=0.7
        )
        fig.update_layout(
            xaxis_title="Sleep Hours",
            yaxis_title="Number of Citizens",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Average steps walked by gender
        gender_steps = filtered_df.groupby("Gender")["Steps_Walked"].mean().reset_index()
        
        fig = px.bar(
            gender_steps,
            x="Gender",
            y="Steps_Walked",
            color="Gender",
            title="Average Steps Walked by Gender",
            labels={"Gender": "Gender", "Steps_Walked": "Average Steps"},
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig.update_layout(
            xaxis_title="Gender",
            yaxis_title="Average Steps",
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Social media vs sleep hours
    st.markdown('<div class="sub-header">Digital Habits & Well-being</div>', unsafe_allow_html=True)
    
    fig = px.scatter(
        filtered_df,
        x="Social_Media_Hours",
        y="Sleep_Hours",
        color="Gender",
        size="Age",
        opacity=0.7,
        title="Social Media Usage vs Sleep Hours",
        labels={
            "Social_Media_Hours": "Social Media Hours",
            "Sleep_Hours": "Sleep Hours",
            "Gender": "Gender",
            "Age": "Age"
        },
        color_discrete_sequence=px.colors.qualitative.G10
    )
    
    fig.update_layout(
        xaxis_title="Social Media Hours",
        yaxis_title="Sleep Hours",
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    # Add trendline
    fig.update_traces(marker=dict(line=dict(width=0.5, color='DarkSlateGrey')))
    fig.add_traces(
        px.scatter(
            filtered_df, x="Social_Media_Hours", y="Sleep_Hours", trendline="ols"
        ).data[1]
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # If we have recycling rate data
    if "Recycling_Rate" in filtered_df.columns:
        col1, col2 = st.columns(2)
        
        with col1:
            # Recycling rate by age group
            df_age_group = filtered_df.copy()
            if "Age_Group" not in df_age_group.columns:
                df_age_group["Age_Group"] = pd.cut(
                    df_age_group["Age"], 
                    bins=[18, 25, 35, 45, 55, 65, 75, 100], 
                    labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"], 
                    right=False
                )
            
            recycling_by_age = df_age_group.groupby("Age_Group")["Recycling_Rate"].mean().reset_index()
            
            fig = px.line(
                recycling_by_age,
                x="Age_Group",
                y="Recycling_Rate",
                markers=True,
                title="Recycling Rate by Age Group",
                labels={"Age_Group": "Age Group", "Recycling_Rate": "Average Recycling Rate (%)"},
                color_discrete_sequence=['#4caf50']
            )
            fig.update_layout(
                xaxis_title="Age Group",
                yaxis_title="Recycling Rate (%)",
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Digital service usage by district if available
            if "District" in filtered_df.columns and "Digital_Service_Usage" in filtered_df.columns:
                digital_by_district = filtered_df.groupby("District")["Digital_Service_Usage"].mean().reset_index()
                
                fig = px.bar(
                    digital_by_district,
                    x="District",
                    y="Digital_Service_Usage",
                    color="District",
                    title="Digital Service Adoption by District",
                    labels={
                        "District": "District", 
                        "Digital_Service_Usage": "Digital Service Usage Score (1-10)"
                    },
                    color_discrete_sequence=px.colors.qualitative.Bold
                )
                fig.update_layout(
                    xaxis_title="District",
                    yaxis_title="Digital Service Usage",
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #f0f0f0;">
    <p style="color: #9e9e9e; font-size: 0.8rem;">
        Smart City Citizen Dashboard • Data Visualization Project • © 2025
    </p>
</div>
""", unsafe_allow_html=True)