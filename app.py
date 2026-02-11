import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="NFHS Dashboard", layout="wide")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("All India National Family Health Survey.csv")
    return df

df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.title("Filters")

states = st.sidebar.multiselect(
    "Select State(s)",
    options=sorted(df["India/States/UTs"].unique()),
    default=["India"]
)

survey_round = st.sidebar.multiselect(
    "Select Survey Round",
    options=sorted(df["Survey"].unique()),
    default=df["Survey"].unique()
)

area_type = st.sidebar.multiselect(
    "Select Area Type",
    options=sorted(df["Area"].unique()),
    default=["Total"]
)

# Filter dataframe
filtered_df = df[
    (df["India/States/UTs"].isin(states)) &
    (df["Survey"].isin(survey_round)) &
    (df["Area"].isin(area_type))
]

# -------------------------
# Indicator Selection
# -------------------------
indicator_columns = df.columns[3:]  # skip first 3 descriptive columns

selected_indicator = st.selectbox(
    "Select Health Indicator",
    indicator_columns
)

# -------------------------
# Dashboard Layout
# -------------------------
st.title("National Family Health Survey (NFHS) Dashboard")

col1, col2 = st.columns(2)

# -------------------------
# KPI Display
# -------------------------
with col1:
    st.subheader("Key Value")

    latest_data = filtered_df.dropna(subset=[selected_indicator])

    if not latest_data.empty:
        value = latest_data[selected_indicator].mean()
        st.metric(label=selected_indicator, value=round(value, 2))
    else:
        st.warning("No data available for selected filters")

# -------------------------
# Trend Chart
# -------------------------
with col2:
    st.subheader("Trend by Survey Round")

    trend_data = filtered_df.dropna(subset=[selected_indicator])

    if not trend_data.empty:
        fig_trend = px.line(
            trend_data,
            x="Survey",
            y=selected_indicator,
            color="India/States/UTs",
            markers=True
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.warning("No data available")

# -------------------------
# State Comparison
# -------------------------
st.subheader("State Comparison")

comparison_df = df[
    (df["Survey"].isin(survey_round)) &
    (df["Area"].isin(area_type))
].dropna(subset=[selected_indicator])

if not comparison_df.empty:
    fig_bar = px.bar(
        comparison_df,
        x="India/States/UTs",
        y=selected_indicator,
        color="Survey",
        barmode="group"
    )
    fig_bar.update_layout(xaxis_tickangle=45)
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("No comparison data available")

# -------------------------
# Raw Data Table
# -------------------------
st.subheader("Filtered Data Table")
st.dataframe(filtered_df)
