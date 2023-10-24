import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_day_cnt(df):
    monthly_cnt = df.resample(rule='D', on='dteday_x').agg({
        "instant": "nunique",
        "cnt_x": "sum"
    })
    monthly_cnt = monthly_cnt.reset_index()
    monthly_cnt.rename(columns={
        "instant": "instant_count",
        "cnt_x": "cnt_count"
    }, inplace=True)

    return monthly_cnt

def create_day_casual(df):
    monthly_casual = df.resample(rule='D', on='dteday_x').agg({
        "instant": "nunique",
        "casual_x": "sum"
    })
    monthly_casual = monthly_casual.reset_index()
    monthly_casual.rename(columns={
        "instant": "instant_count",
        "casual_x": "casual_count"
    }, inplace=True)

    return monthly_casual

def create_day_registered(df):
    monthly_registered = df.resample(rule='D', on='dteday_x').agg({
        "instant": "nunique",
        "registered_x": "sum"
    })
    monthly_registered = monthly_registered.reset_index()
    monthly_registered.rename(columns={
        "instant": "instant_count",
        "registered_x": "registered_count"
    }, inplace=True)

    return monthly_registered

def create_byweathersit(df):
    byweathersit = df.groupby(by="weathersit_x").instant.nunique().reset_index()
    byweathersit.rename(columns={
        "instant": "instant_count"
    }, inplace=True)
    return byweathersit

def create_byholiday(df):
    byholiday = df.groupby(by="holiday_x").instant.nunique().reset_index()
    byholiday.rename(columns={
        "instant": "instant_count"
    }, inplace=True)
    return byholiday

def create_byworkingday(df):
    byworkingday = df.groupby(by="workingday_x").instant.nunique().reset_index()
    byworkingday.rename(columns={
        "instant": "instant_count"
    }, inplace=True)
    return byworkingday

def create_byweekday(df):
    byweekday = df.groupby(by="weekday_x").cnt_x.sum().reset_index()
    byweekday.rename(columns={
        "instant": "cnt_x"
    }, inplace=True)
    return byweekday

def create_r_cnt_df(df):
    r_cnt = day_hour.groupby(by="instant", as_index=False).agg({
    "dteday_x": "max",
    "cnt_x": "sum",
})
    return r_cnt

day_hour = pd.read_csv("day_hour.csv")

datetime_columns = ["dteday_x", "dteday_y"]
day_hour.sort_values(by="dteday_x", inplace=True)
day_hour.reset_index(inplace=True)

for column in datetime_columns:
    day_hour[column] = pd.to_datetime(day_hour[column])

min_date = day_hour["dteday_x"].min()
max_date = day_hour["dteday_x"].max()

with st.sidebar:
    st.image("bike-sharing-logo.jpg")

    start_date, end_date = st.date_input(
        label='Time Range', min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
main_data = day_hour[(day_hour["dteday_x"] >= str(start_date)) &
                     (day_hour["dteday_x"] <= str(end_date))]

monthly_casual = create_day_casual(main_data)
monthly_registered = create_day_registered(main_data)
monthly_cnt = create_day_cnt(main_data)
byweathersit = create_byweathersit(main_data)
byholiday = create_byholiday(main_data)
byworkingday = create_byworkingday(main_data)
byweekday = create_byweekday(main_data)
r_cnt = create_r_cnt_df(main_data)

st.header('Bike-Sharing Data Analisis')

st.subheader('Total Bike Sharing Statistic')

col1, col2 = st.columns(2)

with col1:
    total_instant = monthly_cnt.instant_count.sum()
    st.metric("Total Instant", value=total_instant)

with col2:
    total_cnt = monthly_cnt.cnt_count.sum()
    st.metric("Total Bike Sharing", value=total_cnt)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_cnt["dteday_x"],
    monthly_cnt["cnt_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)

st.subheader('Casual bike-sharing user statistics')

col1, col2 = st.columns(2)

with col1:
    total_instant = monthly_casual.instant_count.sum()
    st.metric("Total Instant", value=total_instant)

with col2:
    total_casual = monthly_casual.casual_count.sum()
    st.metric("Total Casual", value=total_casual)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_casual["dteday_x"],
    monthly_casual["casual_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.subheader('Registered bike-sharing user statistics')

col1, col2 = st.columns(2)

with col1:
    total_instant = monthly_registered.instant_count.sum()
    st.metric("Total Instant", value=total_instant)

with col2:
    total_registered = monthly_registered.registered_count.sum()
    st.metric("Total Registered", value=total_registered)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    monthly_registered["dteday_x"],
    monthly_registered["registered_count"],
    marker='o',
    linewidth=2,
    color="#90CAF9")
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)

st.pyplot(fig)


st.subheader("Total of Sharing Bike (Instant) According to Weathersit")

byweathersit = day_hour.groupby(by="weathersit_x").instant.nunique().reset_index()
byweathersit.rename(columns={
    "instant": "instant_count"
}, inplace=True)

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
sns.barplot(
y="instant_count",
x="weathersit_x",
data=byweathersit.sort_values(by="instant_count", ascending=True),
palette=colors,
ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)


st.subheader("Performa Bike Sharing According to Holiday, Workingday and Weekday")

col1, col2, col3 = st.columns(3)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#72BCD4", "#D3D3D3"]
    sns.barplot(
        y="instant_count",
        x="holiday_x",
        data=byholiday.sort_values(by="instant_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Performa Bike Sharing (Instant) According to Holiday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        y="instant_count",
        x="workingday_x",
        data=byworkingday.sort_values(by="instant_count", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Performa Bike Sharing (Instant) According to Workingday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)
    st.pyplot(fig)

with col3:
    fig, ax = plt.subplots(figsize=(20, 10))
    colors = ["#72BCD4", "#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#72BCD4"]
    sns.barplot(
        y="cnt_x",
        x="weekday_x",
        data=byweekday.sort_values(by="cnt_x", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Performa Bike Sharing According to Weekday", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=35)
    st.pyplot(fig)


st.subheader("Sharing Bikes Total According to Recently")
   
r_cnt = day_hour.groupby(by="instant", as_index=False).agg({
    "dteday_x": "max",
    "cnt_x": "sum"
})
fig, ax = plt.subplots(figsize=(15, 10))
colors = ["#72BCD4"]
sns.barplot(
    y = "cnt_x",
    x = "instant",
    data = r_cnt.sort_values(by="dteday_x", ascending=False).head(10),
    palette = colors,
    ax=ax
)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=25)
ax.tick_params(axis='y', labelsize=25)
st.pyplot(fig)

st.caption('Copyright © My Final Project at Dicoding 2023')