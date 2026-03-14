import streamlit as st
import pandas as pd
import plotly.express as px #visualization (dynamic)
#import matplotlib.pyplot as plt #visualization (static)
#import seaborn as sns #visualization (scientific)

st.title(':::E-comm Analysis Dashboard:::')

def load_data(file_path):
    data=pd.read_csv(file_path)
    return data

data_path="./supermarket_sales.csv"

data=load_data(data_path)

st.sidebar.header("filters")

select_branch=st.sidebar.multiselect("Select Branch",options=data["Branch"].unique(),default=data["Branch"].unique())
select_product=st.sidebar.multiselect("Select Product",options=data["Product line"].unique(),default=data["Product line"].unique())
select_customer=st.sidebar.multiselect("Select Customer Type",options=data["Customer type"].unique(),default=data["Customer type"].unique())

st.dataframe(data)

filtered_data=data[
    (data["Branch"].isin(select_branch))&
    (data["Product line"].isin(select_product))&
    (data["Customer type"].isin(select_customer))
]

st.dataframe(filtered_data)

#key metrics #KPI

#filtered_data['T']

total_sales=filtered_data['Total'].sum().round(2)
total_quantity=filtered_data['Quantity'].sum().round(2)
gross_income=filtered_data['gross income'].sum().round(2)
avg_rating=filtered_data['Rating'].mean().round(2)

#key metrics

st.subheader("Key Performance Indicator")
col1,col2,col3,col4=st.columns(4)

with col1:
    st.metric(label="Total Sales",value=f"{total_sales}")

with col2:
    st.metric(label="Total Quantity",value=f"{total_quantity}")

with col3:
    st.metric(label="Gross Income",value=f"{gross_income}")

with col4:
    st.metric(label="Average Rating",value=f"{avg_rating}")

#visualization

#branch wise sales

branch_sales = filtered_data.groupby("Branch")["Total"].sum().reset_index()

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

#st.subheader("Sales by Customer Type")
fig_customer=px.pie(
    sales_by_customer_type,
    names="Customer type",
    values="Total",
    title="Sales by Customer Type",
    color="Customer type"
)

st.plotly_chart(fig_customer)

#City wise Sales

city_wise_orders = filtered_data.groupby("City")["Invoice ID"].count().reset_index()

#st.subheader("Sales by Customer Type")
fig_city=px.pie(
    city_wise_orders,
    names="City",
    values="Invoice ID",
    title="City wise Orders",
    color="City"
)

st.plotly_chart(fig_city)

sales_by_payment_method = filtered_data.groupby("Payment")["Total"].sum().reset_index()

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