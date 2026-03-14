import pandas as pd
import streamlit as st
import plotly.express as px

st.title(":::E-commerce Sales Dashboard:::")

def load_data(file_path):
    data=pd.read_csv(file_path)
    return data

data_path="./supermarket_sales.csv"

data = load_data(data_path)

st.sidebar.header("Filters")

select_branch=st.sidebar.multiselect("Select Branch",options=data["Branch"].unique(),default=data["Branch"].unique())
select_product=st.sidebar.multiselect("Select Product",options=data["Product line"].unique(),default=data["Product line"].unique())
select_customer=st.sidebar.multiselect("Select Customer Type",options=data["Customer type"].unique(),default=data["Customer type"].unique())

#st.dataframe(data)

filtered_data = data[
    (data["Branch"].isin(select_branch))&
    (data["Product line"].isin(select_product))&
    (data["Customer type"].isin(select_customer))
]

st.dataframe(filtered_data)

#Key Metrics #KPIs

st.subheader("Key Performance Indicator")
col1,col2,col3,col4=st.columns(4)

total_sales=filtered_data['Total'].sum().round()
total_quantity=filtered_data['Quantity'].sum().round()
gross_income=filtered_data['gross income'].sum().round()
avg_rating=filtered_data['Rating'].mean().round()

with col1:
    st.metric(label="Total Sales",value=f"{total_sales}")

with col2:
    st.metric(label="Quantity Sold",value=f"{total_quantity}")

with col3:
    st.metric(label="Gross Income",value=f"{gross_income}")

with col4:
    st.metric(label="Average Rating",value=f"{avg_rating}")

#visualization

col11,col14=st.columns(2)
col12,col13=st.columns(2)
#branch wise sales


branch_sales = filtered_data.groupby("Branch")["Total"].sum().reset_index()
with col11:
#st.subheader("Total Sales by Branch")
    fig_branch=px.bar(
        branch_sales,
        x="Branch",
        y="Total",
        text="Total",
        title="Total Sales by Branch",
        color="Branch"
    )

    st.plotly_chart(fig_branch)

#Sales by Customer type vs Sales


sales_by_customer_type = filtered_data.groupby("Customer type")["Total"].sum().reset_index()
with col12:
#st.subheader("Sales by Customer Type")
    fig_customer=px.pie(
        sales_by_customer_type,
        names="Customer type",
        values="Total",
        title="Sales by Customer Type",
        color="Customer type"
    )

    st.plotly_chart(fig_customer)

#City wise Orders


city_wise_orders = filtered_data.groupby("City")["Invoice ID"].count().reset_index()
with col13:
#st.subheader("City wise Orders")
    fig_city=px.pie(
        city_wise_orders,
        names="City",
        values="Invoice ID",
        title="City wise Orders",
        color="City"
    )

    st.plotly_chart(fig_city)


sales_by_payment_method = filtered_data.groupby("Payment")["Total"].sum().reset_index()
with col14:
    fig_payment = px.treemap(
        sales_by_payment_method,
        path=["Payment"], #hierarchical path
        values="Total",
        title="Sales by Payment Method"
    )

    fig_payment.update_layout(
        width=650,
        height=500,
        margin=dict(t=50,l=25,r=25,b=25)
    ) 

    st.plotly_chart(fig_payment)
