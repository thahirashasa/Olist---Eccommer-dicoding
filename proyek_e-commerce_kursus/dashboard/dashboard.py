import pandas as pd
import seaborn as sns
import streamlit as st
import plotly.express as px
import numpy as np
from pathlib import Path
sns.set_theme(style='white')

BASE_DIR = Path(__file__).resolve().parent

st.set_page_config(
    page_title="E-Commerce Brazil Dashboard",
    page_icon= "🛍️",
    layout="wide"
) 

top_delivered_category_by_states_df = pd.read_csv("https://raw.githubusercontent.com/thahirashasa/Olist---Eccommer-dicoding/refs/heads/main/proyek_e-commerce_kursus/dashboard/top_delivered_category_by_states_df.csv")
monthly_delivery_df = pd.read_csv("https://raw.githubusercontent.com/thahirashasa/Olist---Eccommer-dicoding/refs/heads/main/proyek_e-commerce_kursus/dashboard/monthly_delivery_df.csv")
repeat_category1_df = pd.read_csv("https://raw.githubusercontent.com/thahirashasa/Olist---Eccommer-dicoding/refs/heads/main/proyek_e-commerce_kursus/dashboard/repeat_category_english_df.csv")
rfm_df = pd.read_csv("https://raw.githubusercontent.com/thahirashasa/Olist---Eccommer-dicoding/refs/heads/main/proyek_e-commerce_kursus/dashboard/rfm.csv")

main_df = pd.read_csv(
    BASE_DIR / "main_data.csv",
    parse_dates=[
        "order_purchase_timestamp",
        "order_delivered_customer_date"
    ]
)

palette = ["#E6B3D9", "#E2E1E2", "#B0DBD1", "#92BAC1"]

st.title("E-Commerce Brazil Dashboard 🛍️")
st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
      "🏠 Overview",
      "🛍️ Regional Sales",
      "🚚 Delivery Performance",
      "💗 Repeat Purchase",
      "👥 RFM Segmentation",
      "🔎 Data Explorer"
])

with st.sidebar:
      st.image("https://raw.githubusercontent.com/thahirashasa/Olist---Eccommer-dicoding/main/proyek_e-commerce_kursus/dashboard/ilustrasi_1.jpeg")
      
      st.title("E-Commerce Brazil Dashboard")
      st.divider()

      st.subheader("Global Filters")

      state_options = sorted(main_df["customer_state"].dropna().unique())
      
      category_options = sorted(
            main_df["product_category_name"].dropna().unique()
      )

      category_translation = (
            repeat_category1_df[
                  ["product_category_name", "product_category_name_english"]
            ]
            .drop_duplicates(subset="product_category_name")
            .set_index("product_category_name")["product_category_name_english"]
            .to_dict()
      )

      if "selected_states" not in st.session_state:
        st.session_state.selected_states = state_options.copy()

      if "selected_categories" not in st.session_state:
            st.session_state.selected_categories = category_options.copy()

      def reset_filters():
            st.session_state.selected_states = state_options.copy()
            st.session_state.selected_categories = category_options.copy()

      st.multiselect(
            "Select Brazilian States",
            options=state_options,
            key="selected_states"
      )

      st.multiselect(
            "Select Product Categories",
            options=category_options,
            format_func=lambda category: category_translation.get(
                 category, category
            ),
            key="selected_categories"
      )

      st.button(
            "↻ Reset Filters",
            on_click=reset_filters,
            width="stretch"
      )


      filtered_df = main_df[
            main_df["customer_state"].isin(st.session_state.selected_states)
            & main_df["product_category_name"].isin(st.session_state.selected_categories)
      ].copy()

st.sidebar.title(
    "PROJECT SUBMISION FOR DICODDING IN DATA ANALYST "
)

st.sidebar.divider()

st.sidebar.subheader("EST 2026")

st.sidebar.divider()

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

      total_customers = filtered_df["customer_unique_id"].nunique()

      total_orders = filtered_df["order_id"].nunique()

      repeat_customers =(
            filtered_df.groupby("customer_unique_id")["order_id"]
            .nunique()
            .gt(1)
            .sum() 
      )
      
      overview_rfm_source = (
            filtered_df[
                  (filtered_df["order_status"] == "delivered")
                  & (filtered_df["customer_unique_id"].notna())
            ]
            .drop_duplicates(subset="order_id")
            .copy()
      )

      total_segments = overview_rfm_source[
            "customer_unique_id"
      ].nunique()     

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
            value=f"{repeat_customers:,}"
        )

      with col4:
        st.metric(
            label="Customer Segments",
            value=f"{total_segments:,}"
        )


with tab2:
      st.header("Regional Product Sales")
      st.caption("Explore product category sales across Brazilian states.")

      regional_data = filtered_df[
            filtered_df["order_status"] == "delivered"
      ].copy()

      if regional_data.empty:
            st.warning("No data available for the selected filters.")

      else:
            with st.container(border=True):
                  st.subheader("Top 10 States by Units Sold")

                  states_sales = (
                      regional_data
                      .groupby("customer_state")
                      .size()
                      .sort_values(ascending=False)
                      .head(10)
                      .reset_index(name="units_sold")
                  )

                  fig = px.bar(
                      states_sales,
                      x="customer_state",
                      y="units_sold",
                      title="Top 10 States by Units Sold",
                      labels={
                            "customer_state": "Brazilian State",
                            "units_sold": "Units Sold"
                      }
                  )

                  fig.update_traces(
                      marker_color=[
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

            st.plotly_chart(fig, width="stretch")

            with st.container(border=True):
                  category_sales = (
                  regional_data
                  .groupby("product_category_name")
                  .size()
                  .sort_values(ascending=False)
                  .head(10)
                  .reset_index(name="units_sold")
                  )

                  category_translation = (
                        repeat_category1_df[
                              [
                                    "product_category_name",
                                    "product_category_name_english"
                              ]
                        ]
                  .drop_duplicates(subset="product_category_name")
                  )

                  category_sales = category_sales.merge(
                        category_translation,
                        on="product_category_name",
                        how="left"
                  )

                  category_sales["product_category_name_english"] = (
                        category_sales["product_category_name_english"]
                        .fillna(category_sales["product_category_name"])
                  )

                  fig_category = px.bar(
                      category_sales,
                      x="units_sold",
                      y="product_category_name_english",
                      orientation="h",
                      title="Top 10 Product Categories",
                      labels={
                            "product_category_name_english": "Product Category",
                            "units_sold": "Units Sold"
                      }
                  )

                  fig_category.update_traces(
                      marker_color=[
                            palette[i % len(palette)]
                            for i in range(len(category_sales))
                      ]
                  )

                  fig_category.update_layout(
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      yaxis=dict(autorange="reversed"),
                      xaxis_title="Units Sold",
                      yaxis_title="Product Category"
            )

            st.plotly_chart(fig_category, width="stretch")

with tab3:
      st.header("Delivery Performance")
      st.caption("Monthly trends in average customer delivery time.")

      with st.container(border=True):
            st.subheader("Average Delivery Time by Month")

           
            delivery_data = filtered_df[
                  (filtered_df["order_status"] == "delivered")
                  & (filtered_df["order_delivered_customer_date"].notna())
                  & (filtered_df["order_purchase_timestamp"].notna())
            ].copy()


            delivery_data = delivery_data.drop_duplicates(
                  subset="order_id"
            )

            if delivery_data.empty:
                  st.warning(
                  "No delivered orders available for the selected filters."
                  )
            else:

                  delivery_data["delivery_time_days"] = (
                      delivery_data["order_delivered_customer_date"]
                      - delivery_data["order_purchase_timestamp"]
                  ).dt.total_seconds() / 86400

                  delivery_data["purchase_month"] = (
                      delivery_data["order_purchase_timestamp"]
                      .dt.to_period("M")
                      .dt.to_timestamp()
                  )

                  monthly_delivery = (
                      delivery_data.groupby("purchase_month")["delivery_time_days"]
                      .mean()
                      .reset_index()
                      .sort_values("purchase_month")
                  )

                  avg_delivery = delivery_data["delivery_time_days"].mean()
                  fastest_delivery = monthly_delivery["delivery_time_days"].min()
                  slowest_delivery = monthly_delivery["delivery_time_days"].max()

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
                      monthly_delivery,
                      x="purchase_month",
                      y="delivery_time_days",
                      markers=True,
                      labels={
                            "purchase_month": "Purchase Month",
                            "delivery_time_days": "Average Delivery Time (Days)"
                  },
                  title="Monthly Average Delivery Time"
                  )

                  fig_delivery.update_traces(
                      line=dict(color="#92BAC1", width=3),
                      marker=dict(color="#E6B3D9", size=8)
                  )

                  fig_delivery.update_layout(
                      plot_bgcolor="white",
                      paper_bgcolor="white",
                      font=dict(color="#BAFFF9"),
                      xaxis_title="Purchase Month",
                      yaxis_title="Average Delivery Time (Days)"
                  )

                  st.plotly_chart(fig_delivery, width="stretch")
            
with tab4:
      st.header("Customers Repeat Purchases")
      st.caption("Explore repeat customer behavior across product categories.")

      with st.container(border=True):
            st.subheader("Top 10 Categories by Repeat Customers")

            customer_category_orders = (
                filtered_df
                .dropna(subset=["customer_unique_id", "product_category_name"])
                .groupby(
                    ["product_category_name", "customer_unique_id"]
                )["order_id"]
                .nunique()
                .reset_index(name="order_count")
        )
            
            repeat_category = (
                  customer_category_orders[
                  customer_category_orders["order_count"] > 1
                  ]
                  .groupby("product_category_name")["customer_unique_id"]
                  .nunique()
                  .sort_values(ascending=False)
                  .head(10)
                  .reset_index(name="repeat_customers")
            )

            if repeat_category.empty:
                  st.warning(
                  "No repeat purchases found for the selected filters."
                  )
            else:

                  category_translation = (
                        repeat_category1_df[
                              [
                                    "product_category_name",
                                    "product_category_name_english"
                              ]
                        ]
                        .drop_duplicates(subset="product_category_name")
                  )

                  repeat_category = repeat_category.merge(
                        category_translation,
                        on="product_category_name",
                        how="left"
                  )

                  repeat_category["product_category_name_english"] = (
                        repeat_category["product_category_name_english"]
                        .fillna(repeat_category["product_category_name"])
                  )

                  fig_repeat = px.bar(
                        repeat_category,
                        x="repeat_customers",
                        y="product_category_name_english",
                        orientation="h",
                        labels={
                              "product_category_name_english": "Product Category",
                              "repeat_customers": "Repeat Customers"
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
                      xaxis_title="Repeat Customers",
                      yaxis_title="Product Category",
                      yaxis=dict(autorange="reversed")
                  )

                  st.plotly_chart(fig_repeat, width="stretch")

                  total_repeat_counts = repeat_category["repeat_customers"].sum()

                  top_repeat_category = repeat_category.iloc[0][
                      "product_category_name_english"
                  ]

                  total_categories = filtered_df[
                      "product_category_name"
                  ].nunique()

                  col1, col2, col3, col4 = st.columns(4)

                  with col1:
                        st.metric(
                              label="Repeat Customer-Category Counts (Top 10)",
                              value=f"{total_repeat_counts:,}"
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

                  with col4:
                        st.metric(
                              label="Product Categories",
                              value=f"{total_categories:,}"
                  )

with tab5:
      st.header("RFM Customers Segmentation")
      st.caption("Understand customer behavior through Recency, Frequency, and Monetary analysis.")

      with st.container(border=True):
            st.subheader("Customer Segment Distribution")

            rfm_source = (
            filtered_df[
                filtered_df["order_status"] == "delivered"
            ]
            .drop_duplicates(subset="order_id")
            .copy()
        )

            if rfm_source.empty:
                  st.warning(
                  "No delivered orders available for the selected filters."
                  )

            else:
                  reference_date = (
                  rfm_source["order_purchase_timestamp"].max()
                  + pd.Timedelta(days=1)
                  )

                  rfm_dashboard = (
                  rfm_source
                  .groupby("customer_unique_id")
                  .agg(
                        recency=(
                              "order_purchase_timestamp",
                              lambda x: (reference_date - x.max()).days
                        ),
                        frequency=("order_id", "nunique"),
                        monetary=("payment_value", "sum")
                  )
                  .reset_index()
                  )

                  if len(rfm_dashboard) < 5:
                        st.warning(
                              "At least 5 customers are required for RFM scoring."
                  )

                  else:
                  
                        rfm_dashboard["R_score"] = pd.qcut(
                              rfm_dashboard["recency"].rank(method="first"),
                              5,
                              labels=[5, 4, 3, 2, 1]
                        ).astype(int)

                        rfm_dashboard["F_score"] = pd.cut(
                              rfm_dashboard["frequency"],
                              bins=[0, 1, 2, 3, 4, float("inf")],
                              labels=[1, 2, 3, 4, 5]
                        ).astype(int)

                        rfm_dashboard["M_score"] = pd.qcut(
                              rfm_dashboard["monetary"].rank(method="first"),
                              5,
                              labels=[1, 2, 3, 4, 5]
                        ).astype(int)

                        rfm_dashboard["RFM_score"] = (
                              rfm_dashboard["R_score"].astype(str)
                              + rfm_dashboard["F_score"].astype(str)
                              + rfm_dashboard["M_score"].astype(str)
                        )

                        conditions = [
                              (
                                    (rfm_dashboard["R_score"] >= 4)
                                    & (rfm_dashboard["F_score"] >= 4)
                                    & (rfm_dashboard["M_score"] >= 4)
                              ),
                              (
                                    (rfm_dashboard["R_score"] >= 3)
                                    & (rfm_dashboard["F_score"] >= 2)
                              ),
                              (rfm_dashboard["M_score"] >= 4),
                              (
                                    (rfm_dashboard["R_score"] >= 4)
                                    & (rfm_dashboard["F_score"] == 1)
                              ),
                              (
                                    (rfm_dashboard["R_score"] <= 2)
                                    & (rfm_dashboard["F_score"] <= 2)
                              )
                        ]

                        segments = [
                              "Champions",
                              "Loyal Customers",
                              "Big Spenders",
                              "New Customers",
                              "At Risk"
                        ]

                        rfm_dashboard["segment"] = np.select(
                              conditions,
                              segments,
                              default="Potential Customers"
                        )

                        if (
                              rfm_dashboard.empty
                              or "segment" not in rfm_dashboard.columns
                              or rfm_dashboard["segment"].isna().all()
                        ):
                              st.info(
                                    "No customer segments could be generated "
                                    "for the selected filters."
                              )

                        else:
                              segment_counts = (
                                    rfm_dashboard["segment"]
                                    .value_counts()
                                    .reindex(
                                    segments + ["Potential Customers"],
                                    fill_value=0
                                    )
                                    .reset_index()
                              )

                              segment_counts.columns = ["segment", "count"]

                              segment_counts = segment_counts[
                                    segment_counts["count"] > 0
                              ]

                              if segment_counts.empty:
                                    st.info(
                                    "No customer segments available "
                                    "for the selected filters."
                                    )

                              else:
                                    fig_rfm = px.bar(
                                    segment_counts,
                                    x="segment",
                                    y="count",
                                    labels={
                                          "segment": "Customer Segment",
                                          "count": "Number of Customers"
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
                                        yaxis_title="Number of Customers"
                                    )

                                    st.plotly_chart(fig_rfm, width="stretch")

with tab6:
      st.header("Interactive Data Explorer")
      st.caption(
            "Explore product sales across Brazilian states "
            "and product categories."
      )

      explorer_data = filtered_df.copy()

      if explorer_data.empty:
        st.warning("No data available for the selected filters.")

      else:
        st.success(f"{len(explorer_data):,} records found.")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Total Units Sold",
                value=f"{len(explorer_data):,}"
            )

        with col2:
            st.metric(
                label="States Selected",
                value=f"{explorer_data['customer_state'].nunique():,}"
            )

        with col3:
            st.metric(
                label="Categories Selected",
                value=f"{explorer_data['product_category_name'].nunique():,}"
            )

        st.divider()

        st.subheader("Product Sales Exploration")

        category_explorer = (
            explorer_data
            .groupby("product_category_name")
            .size()
            .sort_values(ascending=False)
            .reset_index(name="units_sold")
        )

        category_translation = (
            repeat_category1_df[
                [
                    "product_category_name",
                    "product_category_name_english"
                ]
            ]
            .drop_duplicates(subset="product_category_name")
        )

        category_explorer = category_explorer.merge(
            category_translation,
            on="product_category_name",
            how="left"
        )

        category_explorer["product_category_name_english"] = (
            category_explorer["product_category_name_english"]
            .fillna(category_explorer["product_category_name"])
        )

        fig_explorer = px.bar(
            category_explorer,
            x="units_sold",
            y="product_category_name_english",
            orientation="h",
            title="Units Sold by Product Category",
            labels={
                "units_sold": "Units Sold",
                "product_category_name_english": "Product Category"
            },
            color="units_sold",
            color_continuous_scale=[
                "#E2E1E2",
                "#B0DBD1",
                "#92BAC1",
                "#E6B3D9"
            ]
        )

        fig_explorer.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            yaxis=dict(autorange="reversed"),
            xaxis_title="Units Sold",
            yaxis_title="Product Category"
        )

        st.plotly_chart(fig_explorer, width="stretch")

        st.divider()

        with st.expander("View Filtered Dataset"):
            explorer_display = explorer_data.merge(
                repeat_category1_df[
                    [
                        "product_category_name",
                        "product_category_name_english"
                    ]
                ].drop_duplicates(
                    subset="product_category_name"
                ),
                on="product_category_name",
                how="left"
            )

            explorer_display["product_category_name"] = (
                explorer_display["product_category_name_english"]
                .fillna(explorer_display["product_category_name"])
            )

            explorer_display = explorer_display.drop(
                columns=["product_category_name_english"]
            )

            st.dataframe(
                explorer_display.sort_values(
                    by="order_purchase_timestamp",
                    ascending=False
                ),
                width="stretch",
                hide_index=True
            )

st.caption("(C) Thahira Riska Pasha For Dicoding Submission") 
