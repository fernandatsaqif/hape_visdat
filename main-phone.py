import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
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

st.set_option("deprecation.showPyplotGlobalUse", False)

st.markdown(f"<html style='scroll-behavior: smooth;'></html>", unsafe_allow_html=True)

dataset_url = "https://raw.githubusercontent.com/fernandatsaqif/hape_visdat/main/clean/smartphone.csv"

@st.cache_data
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)

phone = get_data()

st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
> Sections Introduction
1. [Top 5 Smartphone dengan Harga Tertinggi](#top-5-smartphone-dengan-harga-tertinggi)
2. [Prosesor yang Paling Banyak Digunakan](#prosesor-yang-paling-banyak-digunakan)
3. [Model Smartphone dari Tiap Brand Berdasarkan Harga dan Rating](#model-smartphone-dari-tiap-brand-berdasarkan-harga-dan-rating)
4. [Model Smartphone berdasarkan Prosesor](#distribution-of-processors-by-manufacturer-and-brand)
""",
    unsafe_allow_html=True,
)

st.write("""<h2 style="text-align: center; margin-top:0;">Smartphone Dashboard Sales</h2>""", unsafe_allow_html=True)
st.markdown("***")


# Data Summary
num_brands = phone["brand_name"].nunique()
num_models = phone["model"].nunique()
num_processors = phone["processor_brand"].nunique()

# Custom CSS styles
st.markdown("""
    <style>
    .summary-container {
        display: flex;
        justify-content: space-around;
        margin-bottom: 20px;
    }
    .summary-box {
        flex: 1;
        padding: 20px;
        margin: 10px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 18px;
        font-weight: bold;
    }
    .summary-box p.value {
        font-size: 32px;  /* Larger font size for the numbers */
        margin: 0;
    }
    .brand {
        background-color: #1f77b4;
    }
    .model {
        background-color: #ff7f0e;
    }
    .processor {
        background-color: #2ca02c;
    }
    </style>
    """, unsafe_allow_html=True)

# Display summary metrics with custom styles
st.markdown("""
    <div class="summary-container">
        <div class="summary-box brand">
            <p>Jumlah Brand</p>
            <p class="value">{}</p>
        </div>
        <div class="summary-box model">
            <p>Jumlah Model Smartphone</p>
            <p class="value">{}</p>
        </div>
        <div class="summary-box processor">
            <p>Jumlah Brand Prosesor</p>
            <p class="value">{}</p>
        </div>
    </div>
    """.format(num_brands, num_models, num_processors), unsafe_allow_html=True)

# Add map visualization for country of origin of smartphones
st.header("Peta Asal Smartphone Berdasarkan Negara")
country_counts = phone['country'].value_counts().reset_index()
country_counts.columns = ['country', 'count']
fig = px.choropleth(
    country_counts,
    locations="country",
    locationmode='country names',
    color="count",
    hover_name="country",
    color_continuous_scale=px.colors.sequential.Plasma,
    title='Jumlah Model Smartphone Berdasarkan Negara Asal'
)
fig.update_geos(
    showcoastlines=True,
    coastlinecolor="RebeccaPurple",
    showland=True,
    landcolor="LightGreen",
    showocean=True,
    oceancolor="LightBlue",
    showlakes=True,
    lakecolor="Blue",
    showrivers=True,
    rivercolor="Blue"
)
fig.update_layout(
    geo=dict(
        bgcolor='rgba(0,0,0,0)',
        showframe=False,
        projection_type='equirectangular',
        landcolor='white',
        showland=True,
        lakecolor='rgb(127,205,255)',
        showlakes=True,
        subunitcolor='black',
        countrycolor='black',
        countrywidth=0.5,
        subunitwidth=0.5
    ),
    margin=dict(l=0, r=0, t=30, b=0)
)
st.plotly_chart(fig, use_container_width=True)

category_df = phone.groupby(by="model", as_index=False)["price"].sum()
category_df = category_df.sort_values(by="price", ascending=False,)
category_df = category_df.head(5)

tabs = st.tabs(["Top 5 Smartphone", "Prosesor Terbanyak", "Smartphone Berdasarkan Harga & Rating", "Top 10 Smartphone dengan Prosesor Terbaik", "Distribusi RAM & Internal Storage"])

with tabs[0]:
    st.header("Top 5 Smartphone dengan Harga Tertinggi")
    fig = px.bar(category_df, x="model", y="price", 
                 text=['Rp {:,.0f}'.format(x) for x in category_df["price"]], template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with tabs[1]:
    st.header("Prosesor yang Paling Banyak Digunakan")
    fig = px.pie(phone, values="price", names="processor_brand", hole=0.5)
    fig.update_traces(text=phone["processor_brand"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

with tabs[2]:
    st.header("Model Smartphone dari Tiap Brand Berdasarkan Harga dan Rating")

    selected_brand = st.selectbox("Filter by Brand", phone["brand_name"].unique())

    min_price, max_price = st.slider("Filter by Price (Rp)", 
                                     int(phone["price"].min()), 
                                     int(phone["price"].max()), 
                                     (int(phone["price"].min()), int(phone["price"].max())), 
                                     step=100000)

    min_price_str = "Rp {:,.0f}".format(min_price)
    max_price_str = "Rp {:,.0f}".format(max_price)

    st.write(f"Minimum Price: {min_price_str} | Maximum Price: {max_price_str}")

    selected_rating = st.selectbox("Filter by Rating", [1, 2, 3, 4, 5])

    filtered_phone = phone[(phone["brand_name"] == selected_brand) & 
                           (phone["price"] >= min_price) & 
                           (phone["price"] <= max_price) & 
                           (phone["rating"] == selected_rating)]

    top_rated_phones = filtered_phone.sort_values(by="rating", ascending=False).head(10)

    fig = px.bar(top_rated_phones, x="model", y="price",
                 labels={"model": "Model", "price": "Price (Rp)"},
                 orientation="v", template="seaborn")
    fig.update_traces(text=['Rp {:,.0f}'.format(x) for x in top_rated_phones["price"]],
                      texttemplate='%{text}', textposition='inside')
    fig.update_layout(xaxis=dict(title='Model'), yaxis=dict(title='Price (Rp)'))
    st.plotly_chart(fig, use_container_width=True)

with tabs[3]:
    st.header("Top 10 Model Smartphone dengan Prosesor Terbaik")

    selected_brand_for_processor = st.selectbox("Filter by Brand (Processor)", (phone["brand_name"].unique()))

    top_10_phones = phone.groupby("brand_name").apply(lambda x: x.nlargest(10, 'processor_speed')).reset_index(drop=True)

    fig = px.bar(top_10_phones[top_10_phones["brand_name"] == selected_brand_for_processor], 
                 x="model", y="price", color="processor_brand",
                 text="price", hover_data=["model", "price", "processor_speed"],
                 labels={"price": "Price (Rp)", "model": "Model", "processor_brand": "Merek Prosesor", "processor_speed": "Processor Speed (GHz)"})
    fig.update_traces(text=['Rp {:,.0f}'.format(x) for x in top_10_phones["price"]],
                      texttemplate='%{text}', textposition='outside')
    fig.update_layout(xaxis=dict(title='Model'), yaxis=dict(title='Price (Rp)'), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

with tabs[4]:
    st.header("Distribusi RAM dan Internal Storage yang Paling Banyak Digunakan")

    selected_brand_for_ram_storage = st.selectbox("Filter by Brand (RAM & Internal)", (phone["brand_name"].unique()), key="ram_storage_brand_filter")

    col1, col2 = st.columns((2))

    with col1:
        st.subheader("Distribusi RAM yang Paling Banyak Digunakan")
        fig_ram = px.pie(phone[phone["brand_name"] == selected_brand_for_ram_storage], 
                     values="price", names="ram_capacity", hole=0.5)
        fig_ram.update_traces(text=phone["ram_capacity"], textposition="outside")
        st.plotly_chart(fig_ram, use_container_width=True)

    with col2:
        st.subheader("Distribusi Internal Storage yang Paling Banyak Digunakan")
        fig_storage = px.pie(phone[phone["brand_name"] == selected_brand_for_ram_storage], 
                            values="price", names="internal_memory", hole=0.5)
        fig_storage.update_traces(text=phone["internal_memory"], textposition="outside")
        st.plotly_chart(fig_storage, use_container_width=True)

        
