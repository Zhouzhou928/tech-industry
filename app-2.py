import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page setup
st.set_page_config(page_title="Tech Firms Analysis", layout="wide")

# Multi-page sidebar navigation
page = st.sidebar.selectbox("Navigation Menu", ["Home", "Visualizations", "Analysis", "About"])

# Load your existing dataset
df = pd.read_csv("tech_finance_5firms.csv")

# ----------------------
# PAGE 1: HOME
# ----------------------
if page == "Home":
    st.title("📊 Technology Companies Financial Dashboard")
    st.subheader("5 Leading Tech Firms & Industry Benchmark (2015–2023)")
    
    st.markdown("""
    ### Included Companies
    - Apple (AAPL)  
    - Microsoft (MSFT)  
    - Industry Average  
    - And more technology firms  

    ### Key Financial Metrics
    - Profit Margin  
    - Return on Equity (ROE)  
    - Return on Assets (ROA)  
    - Total Revenue  
    - Debt-to-Asset Ratio  
    """)

    st.subheader("Sample Dataset")
    st.dataframe(df.head(20), use_container_width=True)

# ----------------------
# PAGE 2: VISUALIZATIONS (ALL CHARTS)
# ----------------------
elif page == "Visualizations":
    st.title("📈 Financial Charts & Visualizations")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Profit Margin Trend by Year")
        fig1 = px.line(df, x="year", y="profit_margin", color="tic", markers=True)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.subheader("Return on Equity (ROE) Trend")
        fig2 = px.line(df, x="year", y="roe", color="tic", markers=True)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Return on Assets (ROA) Trend")
        fig3 = px.line(df, x="year", y="roa", color="tic", markers=True)
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.subheader("Debt-to-Asset Ratio Trend")
        fig4 = px.line(df, x="year", y="debt_asset", color="tic", markers=True)
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Total Revenue Comparison (Animated)")
    fig5 = px.bar(df, x="tic", y="revt", color="tic", animation_frame="year")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("ROE vs Profit Margin (Risk-Return Scatter)")
    fig6 = px.scatter(df, x="roe", y="profit_margin", color="tic", size="revt", animation_frame="year")
    st.plotly_chart(fig6, use_container_width=True)

# ----------------------
# PAGE 3: ANALYSIS (INTERACTIVE TOOL)
# ----------------------
elif page == "Analysis":
    st.title("🔍 Custom Financial Analysis")

    selected_firms = st.multiselect("Select Companies to Compare", df["tic"].unique(), default=df["tic"].unique())
    year_range = st.slider("Select Year Range", 2015, 2023, (2015, 2023))
    selected_metric = st.selectbox("Choose Financial Metric", 
                                  ["profit_margin", "roe", "roa", "revt", "debt_asset"])

    # Filter data
    filtered_df = df[
        (df["tic"].isin(selected_firms)) &
        (df["year"] >= year_range[0]) &
        (df["year"] <= year_range[1])
    ]

    st.subheader("Filtered Data Table")
    st.dataframe(filtered_df.round(2), use_container_width=True)

    st.subheader("Trend Chart for Selected Metric")
    fig = px.line(filtered_df, x="year", y=selected_metric, color="tic", markers=True)
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# PAGE 4: ABOUT
# ----------------------
elif page == "About":
    st.title("ℹ️ About This Project")
    st.markdown("""
    ### Course Assignment  
    Track 4 – Financial Analytics & Data Visualization  

    ### Data Source  
    WRDS Compustat Database  

    ### Tools Used  
    - Python  
    - Streamlit (Interactive Dashboard)  
    - Plotly (Visualizations)  

    ### Purpose  
    Analyze and compare financial performance of major technology companies.  
    """)

st.success("✅ Dashboard loaded successfully!")