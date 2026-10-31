import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
sns.set_theme(style='white')


st.set_page_config(
    page_title="E-Commerce Brazil Dashboard",
    page_icon= "🛍️",
    layout="wide"
)

top_delivered_category_by_states_df = pd.read_csv("top_delivered_category_by_states_df.csv")
monthly_delivery_df = pd.read_csv("monthly_delivery_df.csv")
repeat_category1_df = pd.read_csv("repeat_category_english_df.csv")
rfm_df = pd.read_csv("rfm.csv")

palette = ["#E6B3D9", "#E2E1E2", "#B0DBD1", "#92BAC1"]

st.title("E-Commerce Brazil Dashboard 🛍️")
st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs([
      "🏠 Overview",
      "🛍️ Regional Sales",
      "🚚 Delivery Performance",
      "💗 Repeat Purchase",
      "👥 RFM Segmentation"
])

with tab1:
      st.header("Bussiness Overview")
      st.caption( "An overview of sales performance, delivery, "
        "and customer purchasing behavior in Brazil.")

      with st.container(border=True):
            st.subheader("E-Commerce Brazil Public Dataset")
            st.write(
                  "Explore Brazilian e-commerce sales, "
                  "delivery performance, and customer behavior."
            )
      st.subheader("Key Metric")

      col1, col2, col3, col4 = st.columns(4)

      total_customers = rfm_df["customer_unique_id"].nunique()
      total_orders = rfm_df["frequency"].sum()
      repeat_customers = (rfm_df["frequency"] > 1).sum()
      total_segments = rfm_df["segment"].nunique()

      with col1:
        st.metric(
              label="Customers Analyzed",
              value=f"{total_customers:,}"
        )

      with col2:
        st.metric(
             label="Total Orders",
             value=f"{total_orders:,}"
        )

      with col3:
        st.metric(
            label="Repeat Customers",
            value=f"{total_customers:,}"
        )

      with col4:
        st.metric(
            label="Customer Segments",
            value=f"{total_segments:,}"
        )


with tab2:
      st.header("Regional Product Sales")
      st.caption("Explore product category sales across Brazilian states.")

      with st.container(border=True):
            st.subheader("Top 10 States by Units Sold")

            states_sales = (
                 top_delivered_category_by_states_df
                 .groupby("customer_state")["units_sold"]
                 .sum()
                 .sort_values(ascending=False)
                 .head(10)
                 .reset_index()
            )

            fig = px.bar(
                 states_sales,
                 x="customer_state",
                 y="units_sold",
                 labels={
                      "customer_state": "Brazilian State",
                      "units_sold" : "units_sold"
                 },
                 title="Top 10 States by Units Sold"
            )

            fig.update_traces(
                marker_color = [
                        palette[i % len(palette)]
                        for i in range(len(states_sales))
                ]
            )
            

            fig.update_layout(
                 plot_bgcolor="white",
                 paper_bgcolor="white",
                 font=dict(color="#BAFFF9"),
                 xaxis_title="Brazilian States",
                 yaxis_title="Units Sold"
            )

            st.plotly_chart(fig, use_container_width=True)

      with st.container(border=True):
            category_sales = (
            top_delivered_category_by_states_df
            .groupby("product_category_name")["units_sold"]
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
           )

            fig_category = px.bar(
                    category_sales,
                    x="units_sold",
                    y="product_category_name",
                    orientation="h",
                    labels={
                        "product_category_name": "Product Category",
                        "units_sold" : "units_sold"
                },
                    title="Top 10 Product Categories"
            )
           
            fig_category.update_traces(
                  marker_color = [
                       palette[i % len(palette)]
                       for i in range(len(category_sales))
                ]
            )
                       
           
            fig.update_layout(
                    plot_bgcolor="white",
                    paper_bgcolor="white",
                    font=dict(color="#BAFFF9"),
                    xaxis_title="Units Sold",
                    yaxis_title="Product Category",
                    yaxis=dict(autorange="reversed")
            )
           
            st.plotly_chart(fig_category, use_container_width=True)

with tab3:
      st.header("Delivery Performance")
      st.caption("Monthly trends in average customer delivery time.")

      with st.container(border=True):
            st.subheader("Average Delivery Time by Month")

            delivery_data = monthly_delivery_df.copy()

            delivery_data["purchase_month"] = pd.to_datetime(
                 delivery_data["purchase_month"]
            )

            delivery_data = delivery_data.sort_values(
                 "purchase_month"
            )

            avg_delivery = delivery_data["delivery_time_days"].mean()

            fastest_delivery = delivery_data["delivery_time_days"].min()

            slowest_delivery = delivery_data["delivery_time_days"].max()

            col1, col2, col3 = st.columns(3)

            with col1:
                 st.metric(
                      label="Average Delivery Time",
                      value=f"{avg_delivery:.2f} days"
                 )

            with col2:
                 st.metric(
                      label="Fastest Monthly Average",
                      value=f"{fastest_delivery:.2f} days"
                 )

            with col3:
                 st.metric(
                      label="Slowest Monthly Average",
                      value=f"{slowest_delivery:.2f} days"
                 )

            fig_delivery = px.line(
                 delivery_data,
                 x="purchase_month",
                 y="delivery_time_days",
                 markers=True,
                 labels={
                      "purchase_month":"Purchase Month",
                      "delivery_time_days":"Average Delivery Time (Days)"
                 },
                 title="Monthly Average Delivery Time"
            )

            fig_delivery.update_traces(
                 line=dict(color="#92BAC1", width=3),
                 marker=dict(color="#E6B3D9",size=8)
            )

            fig_delivery.update_layout(
                 plot_bgcolor="white",
                 paper_bgcolor="white",
                 font=dict(color="#BAFFF9"),
                 xaxis_title="Purchase Mont",
                 yaxis_title="Average Delivery Time (Days)"
            )

            st.plotly_chart(fig_delivery, use_container_width=True)
            
with tab4:
      st.header("Customers Repeat Purchases")
      st.caption("Explore repeat customer behavior across product categories.")

      with st.container(border=True):
            st.subheader("Top 10 Categories by Repeat Customers")

            repeat_category = (
                 repeat_category1_df
                 .groupby("product_category_name_english")["repeat_customers"]
                 .sum()
                 .sort_values(ascending=False)
                 .head(10)
                 .reset_index()
            )

            fig_repeat = px.bar(
                 repeat_category,
                 x="repeat_customers",
                 y="product_category_name_english",
                 orientation="h",
                 labels={
                      "product_category_name_english" : "Product Category",
                      "repeat_customers" : "Repeat Customers"
                 }, 
                  title="Top 10 Categories by Repeat Customers"
            )

            fig_repeat.update_traces(
                  marker_color=[
                       palette[i % len(palette)]
                       for i in range(len(repeat_category))
                  ]
            )

            fig_repeat.update_layout(
                  plot_bgcolor="white",
                  paper_bgcolor="white",
                  font=dict(color="#BAFFF9"),
                  xaxis_title="Repeat Customer",
                  yaxis_title="Product Category",
                  yaxis=dict(autorange="reversed")
            )

            st.plotly_chart(fig_repeat,use_container_width=True)

            total_repeat_counts = repeat_category["repeat_customers"].sum()

            top_repeat_category = repeat_category.iloc[0][
                 "product_category_name_english"
            ]

            total_categories = repeat_category1_df[
                 "product_category_name_english"
            ].nunique()

            col1, col2, col3 = st.columns(3)

            with col1:
                 st.metric(
                      label="Repeat Customer Counts (Top 10)",
                      value=f"{total_repeat_counts}"
                 )

            with col2:
                 st.metric(
                      label="Top Repeat Purchase Category",
                      value=top_repeat_category
                 )

            with col3:
                 st.metric(
                      label="Categories Analyzed",
                      value=f"{total_categories:,}"
                 )

with tab5:
      st.header("RFM Customers Segmentation")
      st.caption("Understand customer behavior through Recency, Frequency, and Monetary analysis.")

      with st.container(border=True):
            st.subheader("Customer Segment Distribution")

            segment_counts = (
                 rfm_df["segment"]
                 .value_counts()
                 .reset_index()
            )

            segment_counts.column = ["segment","count"]

            fig_rfm = px.bar(
                 segment_counts,
                 x="segment",
                 y="count",
                 labels={
                      "segment":"Customer Segment",
                      "count":"Number of Customer"
                 },
                 title="Customer Distribution by RFM Segment"
            )

            fig_rfm.update_traces(
                  marker_color=[
                  palette[i % len(palette)]
                  for i in range(len(segment_counts))
                  ]
            )

            fig_rfm.update_layout(
                  plot_bgcolor="white",
                  paper_bgcolor="white",
                  font=dict(color="#BAFFF9"),
                  xaxis_title="Customer Segment",
                  yaxis_title="Number of Customer"
            )

            st.plotly_chart(fig_rfm,use_container_width=True)


with st.sidebar:
      st.image("/proyek_e-commerce_kursus/dashboard/ilustrasi_1.jpeg")

st.sidebar.title(
    "PROJECT SUBMISION FOR DICODDING IN DATA ANALYST "
)

st.sidebar.divider()

st.sidebar.subheader("EST 2026")

st.caption("(C) Thahira Riska Pasha For Dicoding Submission") 