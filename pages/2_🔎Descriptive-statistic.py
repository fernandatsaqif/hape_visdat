import time  #
import matplotlib.pyplot as plt
import numpy as np  # import np
import pandas as pd  # import pd
import plotly.express as px  # import chart
import plotly.graph_objects as go
import streamlit as st
import altair as alt
import math
from PIL import Image
import seaborn as sns
from pandas import DataFrame

st.set_page_config(
    page_title="RectoGadget",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)

dataset_url = "https://raw.githubusercontent.com/novinbukannopin/uas-visdat/main/assets/clean/phone-price.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

phone = get_data()

st.header("Descriptive Statistic")  # Descriptive Data Visualization
st.write("")

def format_number(number):
    return f"{int(number)}"

def kpi(subheader, label, option_columns, method):
    st.subheader(subheader)
    if option_columns == "all":
        hue_opt = st.selectbox(label=label, options=phone.columns)
    else:
        hue_opt = st.selectbox(label=label, options=option_columns)

    column = hue_opt.lower()
    title = hue_opt.replace("_", " ").upper()
    st.markdown(f"<h4 style='text-align: center; color: #6554AF;'>{title}</h3>", unsafe_allow_html=True)
    count = phone[column].nunique()
    if count != None:
        st.markdown(f"<h1 style='text-align: center; color: #9575DE;'>{count} item</h1>", unsafe_allow_html=True)
        if method == "counts":
            st.table(phone[column].value_counts())
        elif method == "mean":
            mean_values = phone[column].groupby(phone['brand_name']).mean().apply(format_number)
            st.table(mean_values)
        elif method == "range":
            min_value = phone[column].groupby(phone['brand_name']).min().apply(format_number)
            max_value = phone[column].groupby(phone['brand_name']).max().apply(format_number)
            range = (max_value.astype(float) - min_value.astype(float)).apply(format_number)
            st.table(
                {"range": range, "min": min_value, "max": max_value}
            )

kpi_count, kpi_mean, kpi_range = st.columns(3)
with kpi_count:
    kpi(
        subheader=":department_store: This is a Count",  # Count, Count Data, Count Visualization, Count Data Visualization
        label="count",
        option_columns="all",
        method="counts")

with kpi_mean:
    kpi(
        subheader=":snowman: This is Average",  # Average, Average Data, AVG Data, Average Visualization, visualization of the mean
        label="mean",
        option_columns=(['price', 'rating']),
        method="mean")

with kpi_range:
    kpi(
        subheader=":snowman: This is Range",  # Range, Range Data, Range Visualization, Visualization of the data range
        label="range",
        option_columns=(['price', 'rating']),
        method="range")

st.markdown("<hr/>", unsafe_allow_html=True)
