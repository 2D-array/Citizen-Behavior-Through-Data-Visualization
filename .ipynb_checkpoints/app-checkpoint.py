import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="Smart City Citizen Dashboard", layout="wide")

# Title
st.title("🚀 Smart City Citizen Activity Dashboard")
st.markdown("Explore citizen behavior, transportation patterns, carbon footprint, and lifestyle trends.")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("dataset/smart_city_citizen_activity.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
age_range = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (20, 60))
gender_filter = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=list(df["Gender"].unique()))

filtered_df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1]) & (df["Gender"].isin(gender_filter))]

# Layout for visualizations
tab1, tab2, tab3 = st.tabs(["📊 Demographics", "🚗 Transport & Environment", "🌐 Lifestyle Trends"])

# ---------- TAB 1: Demographics ----------
with tab1:
    st.subheader("Age Distribution")
    fig, ax = plt.subplots()
    ax.hist(filtered_df["Age"], color="red", edgecolor="black", alpha=0.7)
    ax.set_xlabel("Age")
    ax.set_ylabel("Frequency")
    ax.set_title("Age Distribution of Citizens")
    ax.grid(axis="y", alpha=0.5)
    st.pyplot(fig)

    st.subheader("Gender Distribution")
    gender_counts = filtered_df["Gender"].value_counts()
    fig2, ax2 = plt.subplots()
    ax2.pie(gender_counts, labels=gender_counts.index, autopct="%1.1f%%", startangle=140,
            colors=["lightblue", "lightcoral", "gray"])
    ax2.set_title("Gender Distribution")
    st.pyplot(fig2)

# ---------- TAB 2: Transport & Environment ----------
with tab2:
    st.subheader("Transport Mode Distribution")
    transport_counts = filtered_df["Mode_of_Transport"].value_counts()
    fig3, ax3 = plt.subplots()
    ax3.bar(transport_counts.index, transport_counts.values, color="lightblue", edgecolor="black")
    ax3.set_xlabel("Mode of Transport")
    ax3.set_ylabel("Frequency")
    ax3.set_title("Transportation Modes Used")
    ax3.tick_params(axis='x', rotation=45)
    ax3.grid(axis="y", linestyle="--")
    st.pyplot(fig3)

    st.subheader("Average Carbon Footprint by Transport Mode")
    transport_carbon = filtered_df.groupby("Mode_of_Transport")["Carbon_Footprint_kgCO2"].mean().sort_values()
    fig4, ax4 = plt.subplots()
    ax4.bar(transport_carbon.index, transport_carbon.values, color="tomato", edgecolor="black")
    ax4.set_xlabel("Mode of Transport")
    ax4.set_ylabel("Average CO2 (kg)")
    ax4.set_title("Carbon Footprint per Transport Mode")
    ax4.tick_params(axis='x', rotation=45)
    ax4.grid(axis="y", linestyle="--", alpha=0.6)
    st.pyplot(fig4)

    st.subheader("EV Usage by Age Group")
    age_bins = [18, 25, 35, 45, 55, 65, 75, 100]
    age_labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
    df["Age_Group"] = pd.cut(df["Age"], bins=age_bins, labels=age_labels, right=False)
    ev_age_distribution = df[df["Mode_of_Transport"] == "EV"]["Age_Group"].value_counts().sort_index()

    fig5, ax5 = plt.subplots()
    ax5.bar(ev_age_distribution.index, ev_age_distribution.values, color="lightgreen", edgecolor="black")
    ax5.set_xlabel("Age Group")
    ax5.set_ylabel("Number of EV Users")
    ax5.set_title("EV Usage by Age Group")
    ax5.grid(axis="y", linestyle="--", alpha=0.7)
    st.pyplot(fig5)

# ---------- TAB 3: Lifestyle Trends ----------
with tab3:
    st.subheader("Sleep Hours Distribution")
    fig6, ax6 = plt.subplots()
    ax6.hist(filtered_df["Sleep_Hours"], bins=10, color="purple", edgecolor="black", alpha=0.7)
    ax6.set_xlabel("Sleep Hours")
    ax6.set_ylabel("Frequency")
    ax6.set_title("Distribution of Sleep Hours")
    ax6.grid(axis="y", linestyle="--", alpha=0.5)
    st.pyplot(fig6)

    st.subheader("Average Steps Walked by Gender")
    gender_steps = filtered_df.groupby("Gender")["Steps_Walked"].mean()
    fig7, ax7 = plt.subplots()
    ax7.bar(gender_steps.index, gender_steps.values, color=["skyblue", "lightcoral"], edgecolor="black")
    ax7.set_xlabel("Gender")
    ax7.set_ylabel("Steps Walked")
    ax7.set_title("Average Steps by Gender")
    ax7.grid(axis="y", linestyle="--", alpha=0.5)
    st.pyplot(fig7)

    st.subheader("Social Media Hours vs Sleep Hours")
    fig8, ax8 = plt.subplots()
    ax8.scatter(filtered_df["Social_Media_Hours"], filtered_df["Sleep_Hours"], alpha=0.6, color="orange", edgecolor="black")
    ax8.set_xlabel("Social Media Hours")
    ax8.set_ylabel("Sleep Hours")
    ax8.set_title("Social Media vs Sleep")
    ax8.grid(True, linestyle="--", alpha=0.5)
    st.pyplot(fig8)
