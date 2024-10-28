import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import FastMarkerCluster
from pathlib import Path
from streamlit_folium import st_folium

# HELPER FUNCTION

def countplot_format(df, x, ax, title, xlabel, ylabel, hue, y=None, order=None, custom_label=None, rotate_label=False, padding_label=-0.1, palette='flare', legend=False):

    if order:
        sns.countplot(x=x, y=y, data=df, ax=ax, hue=hue, order=order, palette=palette, legend=legend)
    else:
        sns.countplot(x=x, y=y, data=df, ax=ax, hue=hue, palette=palette, legend=False)

    ax.set_title(title, pad=24)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.xaxis.set_label_coords(0.5, padding_label)

    if custom_label:
        ax.set_xticklabels(custom_label)

    if rotate_label:
        ax.tick_params(axis='x', labelrotation=45)

    if legend:
        ax.legend(loc='upper left')

    ncount = len(df)

    for p in ax.patches:
        x = p.get_bbox().get_points()[:, 0]
        y = p.get_bbox().get_points()[1, 1]
        ax.annotate('{}\n{:.1f}%'.format(int(y), 100. * y / ncount), (x.mean(), y), ha='center', va='bottom')

# READ DATA

orders = pd.read_csv(Path(__file__).parent / './orders.csv')
orders_payments_merge = pd.read_csv(Path(__file__).parent / './orders_payments_merge.csv')
geo_cities_group = pd.read_csv(Path(__file__).parent / './geo_cities_group.csv')
locations = pd.read_csv(Path(__file__).parent / './locations.csv')

# VISUALIZATION

st.set_page_config(layout="wide")

st.markdown('# 🛒 Brazilian E-Commerce Dashboard')

st.write('---')

st.markdown('## Yearly Transaction Trends')

col1, col2 = st.columns(2)

with col1:
  st.markdown('### By Years')

  # Bar plot - plot jumlah transaksi per tahun

  fig = plt.figure(figsize=(15, 7.5))
  ax = fig.add_subplot()

  countplot_format(orders,
                  ax=ax,
                  x='order_purchase_year',
                  title='Total Pesanan Tahun 2016-2018',
                  xlabel='Tahun',
                  ylabel='Jumlah',
                  hue='order_purchase_year')

  st.pyplot(fig)

with col2:
  st.markdown('### By Months')

  fig = plt.figure(figsize=(15, 7))
  ax = fig.add_subplot()

  countplot_format(orders_payments_merge,
                  x='order_purchase_year_month',
                  ax=ax,
                  title='Tren Jumlah Transaksi dari 2016 hingga 2018',
                  xlabel='Bulan dan Tahun',
                  ylabel='Jumlah Transaksi',
                  rotate_label=True,
                  padding_label=-0.15,
                  order=sorted(orders_payments_merge['order_purchase_year_month'].unique()),
                  hue='order_purchase_year',
                  legend=True)

  st.pyplot(fig)

st.write('---')

st.markdown('## Weekly and Daily Orders Trends')

col1, col2 = st.columns(2)

with col1:
  st.markdown('### Weekly')

  fig = plt.figure(figsize=(20, 10))
  ax = fig.add_subplot()

  weekday_label = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jum\'at', 'Sabtu', 'Minggu']

  countplot_format(orders,
                  x='order_purchase_dayofweek',
                  ax=ax,
                  title='Total Pesanan dalam Satu Minggu',
                  xlabel='Hari dalam satu minggu',
                  ylabel='Jumlah',
                  custom_label=weekday_label,
                  hue='order_purchase_dayofweek')

  st.pyplot(fig)

with col2:
  st.markdown('### Daily')

  fig = plt.figure(figsize=(20, 10))
  ax = fig.add_subplot()

  countplot_format(orders,
                  x='order_purchase_time_day',
                  ax=ax,
                  title='Total Pesanan dalam Satu Hari',
                  xlabel='Waktu dalam satu hari',
                  ylabel='Jumlah',
                  hue='order_purchase_time_day')

  st.pyplot(fig)

st.write('---')

st.markdown('## Top 20 Cities with Highest Orders')

fig = plt.figure(figsize=(20, 5))
ax = fig.add_subplot()

sns.barplot(x='geolocation_city', y='order_id', data=geo_cities_group, ax=ax, hue='geolocation_city', palette='flare', legend=False)

ax.set_title('10 Kota di Brazil dengan Jumlah Pesanan Terbanyak')
ax.set_xlabel('Kota')
ax.set_ylabel('Jumlah')
ax.xaxis.set_label_coords(0.5, -0.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.tick_params(axis='x', labelrotation=45)

for p in ax.patches:
    x = p.get_bbox().get_points()[:, 0]
    y = p.get_bbox().get_points()[1, 1]
    ax.annotate('{}\n{:.1f}%'.format(int(y), 100. * y / len(orders)), (x.mean(), y), ha='center', va='bottom')

st.pyplot(fig)

st.write('---')

st.markdown('## Customer Distribution by Cities')

map = folium.Map(location=[-15, -50], zoom_start=4.0)

FastMarkerCluster(data=locations).add_to(map)

st_data = st_folium(map, width=1500, height=600)