import streamlit as st
import pandas as pd
import plotly.express as px

st.title(':::::E-commerce Sales Analysis Dashboard:::::')

def load_data(file_path):
    data=pd.read_csv(file_path)
    return data

data_path="./supermarket_sales.csv"

data = load_data(data_path)

st.sidebar.header("Filters")

select_branch=st.sidebar.multiselect("Select Branch",options=data["Branch"].unique())
select_product=st.sidebar.multiselect("Select Product",options=data["Product line"].unique())
select_customer=st.sidebar.multiselect("Select Customer Type",options=data["Customer type"].unique())

st.dataframe(data)

filtered_data= data[
    (data["Branch"].isin(select_branch))&
    (data["Product line"].isin(select_product))&
    (data["Customer type"].isin(select_customer))
]

st.dataframe(filtered_data)
