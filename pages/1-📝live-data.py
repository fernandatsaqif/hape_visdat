import time  #

import matplotlib.pyplot as plt
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
    page_title="Update - RectoGadget",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.set_option('deprecation.showPyplotGlobalUse', False)

dataset_url = "https://raw.githubusercontent.com/fernandatsaqif/hape_visdat/main/clean/smartphone.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

laptop = get_data()



st.title("Real-Time / Live Data Smartphone Dashboard")

st.markdown('''
            A Real-Time / Live Data Smartphone Dashboard is a mobile application interface designed to provide users with up-to-the-minute data visualizations and insights. This type of dashboard aggregates and displays live data streams from various sources, enabling users to monitor and analyze key metrics in real-time
    ''')

# st.sidebar.markdown('''
# > Sections Introduction
# 1. [Metric](#metric)
# 2. [Table](#table)
# ''', unsafe_allow_html=True)

# st.subheader("Metric")

# jumlah_brand = len(laptop['brand'].unique())
# processor_name = len(laptop['processor_name'].unique())
# processor_brand = len(laptop['processor_brand'].unique())
# ram_type = len(laptop['ram_type'].unique())
# total_product = len(laptop['brand'])

# col1, col2, col3, col4, col5 = st.columns(5)
# col1.metric("Total Product", f"{str(total_product)} Product", "20%")
# col2.metric("Brand Laptop", f"{str(jumlah_brand)} Brand", "-8%")
# col3.metric("Processor", f"{str(processor_name)} Type", "15%")
# col4.metric("Brand Procie", f"{str(processor_brand)} Brand", "5%")
# col5.metric("Ram Type", f"{str(jumlah_brand)} Type", "40%")

# st.subheader("Table")
# st.table(laptop)