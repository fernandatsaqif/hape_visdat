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
    page_title="RectoGadget",
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



# Set Dashboard Title
st.write("""<h2 style="text-align: center; margin-top:0;">Update data Smartphone Sales</h2>""", unsafe_allow_html=True)
st.markdown("***")

st.markdown('''
            A Real-Time / Live Data Smartphone Dashboard is a mobile application interface designed to provide users with up-to-the-minute data visualizations and insights. This type of dashboard aggregates and displays live data streams from various sources, enabling users to monitor and analyze key metrics in real-time
    ''')

st.sidebar.markdown('''
> Sections Introduction
1. [Metric](#metric)
2. [Table](#table)
''', unsafe_allow_html=True)

st.subheader("Metric")

jumlah_brand = len(laptop['brand_name'].unique())
model = len(laptop['model'].unique())
processor_brand = len(laptop['processor_brand'].unique())
ram_capacity = len(laptop['ram_capacity'].unique())
total_product = len(laptop['brand_name'])


col1, col2, col3 = st.columns(3)
col1.metric("Total Product", f"{str(total_product)} Product", "20%")
col2.metric("Brand Smartphone", f"{str(jumlah_brand)} Brand", "-8%")
col3.metric("Brand Processor", f"{str(processor_brand)} Brand", "5%")

st.subheader("Table Data")
st.table(laptop)