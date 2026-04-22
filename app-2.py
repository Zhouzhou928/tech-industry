import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ----------------------
# Global Configuration (Unified Style)
# ----------------------
st.set_page_config(page_title="Tech Firms Financial Analysis", layout="wide")
st.markdown("""
    <style>
    .stSelectbox, .stSlider {margin-bottom: 20px;}
    .metric-card {background: #f0f2f6; padding: 15px; border-radius: 8px; margin: 10px 0;}
    </style>
    """, unsafe_allow_html=True)

# ----------------------
# Step 1: Load Data + Global Filters (Shared Across All Sections)
# ----------------------
df = pd.read_csv("tech_finance_5firms.csv")
df = df.round(3)  # Format data for readability

# Sidebar: Core Filters (Global - one selection updates everything)
st.sidebar.header("📌 Filter Controls (Global)")
selected_companies = st.sidebar.multiselect(
    "Select Companies",
    options=df["tic"].unique(),
    default=["AAPL", "MSFT", "INDUSTRY"]
)
year_range = st.sidebar.slider(
    "Select Year Range",
    min_value=int(df["year"].min()),
    max_value=int(df["year"].max()),
    value=(2018, 2023)
)
selected_metric = st.sidebar.selectbox(
    "Primary Metric for Analysis",
    options=["profit_margin", "roe", "roa", "revt", "debt_asset"],
    format_func=lambda x: {
        "profit_margin": "Profit Margin",
        "roe": "Return on Equity (ROE)",
        "roa": "Return on Assets (ROA)",
        "revt": "Total Revenue",
        "debt_asset": "Debt-to-Asset Ratio"
    }[x]
)

# Global Filtered Data (used in all sections)
filtered_df = df[
    (df["tic"].isin(selected_companies)) &
    (df["year"] >= year_range[0]) &
    (df["year"] <= year_range[1])
]

# ----------------------
# Core Section 1: Data Overview + Key Metric Cards (Meaningful Table)
# ----------------------
st.title("📊 Tech Firms Financial Dashboard (2015-2023)")
st.subheader("1. Key Financial Summary (Real-time Filtered)")

# Calculate key metrics (from filtered data)
metrics_summary = filtered_df.groupby("tic")[selected_metric].agg(["mean", "max", "min"]).round(3)
metrics_summary.columns = ["Average", "Peak", "Trough"]

# Two-column layout: Metric Cards (intuitive) + Detailed Table (interactive)
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("### 📈 Top Performer (Average)")
    top_firm = metrics_summary["Average"].idxmax()
    top_value = metrics_summary["Average"].max()
    st.markdown(f"""
    <div class="metric-card">
        <h4>{top_firm}</h4>
        <p>{selected_metric.replace("_", " ").title()}: {top_value}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📉 Bottom Performer (Average)")
    bottom_firm = metrics_summary["Average"].idxmin()
    bottom_value = metrics_summary["Average"].min()
    st.markdown(f"""
    <div class="metric-card">
        <h4>{bottom_firm}</h4>
        <p>{selected_metric.replace("_", " ").title()}: {bottom_value}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"### Detailed {selected_metric.replace('_', ' ').title()} by Company")
    st.dataframe(metrics_summary, use_container_width=True)
    st.caption("👉 Table updates in real-time with your filter selections (companies/years/metric)")

# ----------------------
# Core Section 2: Dynamic Charts (Fully Filter-Driven)
# ----------------------
st.subheader("2. Interactive Trend Analysis (Filter-driven)")

# Chart 1: Core Metric Trend (filter-linked)
col3, col4 = st.columns(2)
with col3:
    fig_trend = px.line(
        filtered_df,
        x="year",
        y=selected_metric,
        color="tic",
        markers=True,
        title=f"{selected_metric.replace('_', ' ').title()} Trend ({year_range[0]}-{year_range[1]})"
    )
    fig_trend.update_layout(height=350)
    st.plotly_chart(fig_trend, use_container_width=True)

# Chart 2: Core Metric vs Profit Margin (filter-linked)
with col4:
    compare_metric = "profit_margin" if selected_metric != "profit_margin" else "roe"
    fig_scatter = px.scatter(
        filtered_df,
        x=selected_metric,
        y=compare_metric,
        color="tic",
        size="revt",
        animation_frame="year",
        title=f"{selected_metric.title()} vs {compare_metric.title()} (Size=Revenue)"
    )
    fig_scatter.update_layout(height=350)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Chart 3: Annual Comparison Bar Chart (filter-linked)
st.markdown("### Annual Metric Comparison")
fig_bar = px.bar(
    filtered_df,
    x="year",
    y=selected_metric,
    color="tic",
    barmode="group",
    title=f"Annual {selected_metric.replace('_', ' ').title()} by Company"
)
st.plotly_chart(fig_bar, use_container_width=True)

# ----------------------
# Core Section 3: Deep Dive Analysis (Filter-Driven)
# ----------------------
st.subheader("3. Deep Dive Analysis (Filter-driven)")

# Correlation Analysis (filtered data)
corr_metrics = ["profit_margin", "roe", "roa", "debt_asset"]
corr_df = filtered_df.pivot_table(index=["year", "tic"], values=corr_metrics).corr().round(2)

col5, col6 = st.columns(2)
with col5:
    st.markdown("### Correlation Matrix (Key Metrics)")
    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Metric Correlation (Filtered Data)"
    )
    fig_corr.update_layout(height=350)
    st.plotly_chart(fig_corr, use_container_width=True)

with col6:
    st.markdown("### Metric Distribution (Box Plot)")
    fig_box = px.box(
        filtered_df,
        x="tic",
        y=selected_metric,
        title=f"{selected_metric.title()} Distribution by Company"
    )
    fig_box.update_layout(height=350)
    st.plotly_chart(fig_box, use_container_width=True)

# ----------------------
# Non-Redundant Project Info (Footer - No Filler Sections)
# ----------------------
st.markdown("---")
st.markdown("""
### ℹ️ Project Information
- Data Source: WRDS Compustat (2015-2023) | Tools: Python/Streamlit/Plotly
- All visualizations and tables update in real-time with your filter selections
- Focus: Comparative financial performance analysis of leading tech firms
""")
