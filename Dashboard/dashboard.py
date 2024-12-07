import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# LIST FOR ORDERING MONTHS
new_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# PREPARING amount_per_year (RENTAL AMOUN PER YEAR, GROUP BY MONTH)
def create_amount_per_year(df, year):
    amount_per_year = df[df["yr"] == year].groupby(by="mnth").agg({
        "cnt": "sum"
    })
    amount_per_year = amount_per_year.reindex(new_order, level=1)
    return amount_per_year

# PREPARING amount_by_hour (RENTAL AMOUNT GROUP BY HOUR)
def create_amount_by_hour(df):
    amount_by_hour = df.groupby(by=["hr"]).agg({
        "cnt": "sum"
    }).reset_index().sort_values(by=["cnt"], ascending=False)
    amount_by_hour['hr'] = amount_by_hour['hr'].astype(str) + ":00"
    return amount_by_hour

# PREPARING bytime_df (AMOUNT OF RENTAL BY TIME GROUP)
def create_bytime_df(df):
    df["time_group"] = df.hr.apply(lambda x: "Evening" if x <= 4 else ("Afternoon" if x > 10 else "Morning"))
    bytime_df = df.groupby(by="time_group").agg({
        "cnt": "sum"
    }).reset_index().sort_values(by="cnt", ascending=False)
    return bytime_df

# PREPARING bytemp_df (AMOUNT OF RENTAL BY TEMPERATURE GROUP)
def create_bytemp_df(df):
    df["temp_group"] = df.temp.apply(lambda x: "Cold" if x < 10 else ("Chilly" if x < 18 else ("Warm" if x < 24 else "Hot")))
    bytemp_df = df.groupby(by="temp_group").agg({
        "cnt": "sum"
    }).reset_index().sort_values(by="cnt", ascending=False)
    return bytemp_df

# READ THE DATA (CSV)
data_df = pd.read_csv("Dashboard/data.csv")

# CALL ALL THE FUNCTIONS
amount_by_hour = create_amount_by_hour(data_df)
bytime_df = create_bytime_df(data_df)
bytemp_df = create_bytemp_df(data_df)

with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ff5757; font-size: 36px; margin-bottom: 30px;'>Welcome, Admin</h1>", unsafe_allow_html=True)
    st.image("Dashboard/logo.png")

st.header('Bike Sharing Dashboard :sparkles:')

# 1st GRAPH: AMOUNT OF RENTAL BY YEAR (2011 AND 2012)
st.subheader('Daily Rental per Month')

col1, col2 = st.columns((6, 10))

with col1:
    rdo_year = st.radio(
        label="Year filter",
        options=(2011, 2012),
        horizontal=False
    )

amount_per_year = create_amount_per_year(data_df, rdo_year)

with col2:
    col3, mid_col, col4 = st.columns((10,1,10))
    with col3:
        highest = amount_per_year.sort_values(by="cnt", ascending=False).head(1)
        st.metric("Highest amount", value=str(highest["cnt"].iloc[-1])+" ("+str(highest.index[-1])[0:3]+")")
    
    with col4:
        lowest = amount_per_year.sort_values(by="cnt", ascending=True).head(1)
        st.metric("Lowest amount", value=str(lowest["cnt"].iloc[-1])+" ("+str(lowest.index[-1])[0:3]+")")

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    amount_per_year.index,
    amount_per_year["cnt"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=20, rotation=45)
# ITERATION FOR DISPLAYING THE VALUE ON EACH POINT
for x, y in zip(amount_per_year.index, amount_per_year["cnt"]):
    ax.text(x, y+1000, str(y), ha="center", va="bottom", fontsize=15)

st.pyplot(fig)

# 2nd GRAPH: AMOUNT OF RENTAL BY HOUR
st.subheader("Times of Highest and Lowest Rental Amounts")

col5, inter_col, col6 = st.columns((4,5,3))

with col5:
    highest_hour = amount_by_hour.sort_values(by="cnt", ascending=False).head(1)
    st.metric("Highest amount", value=str(highest_hour["cnt"].iloc[-1])+" ("+highest_hour["hr"].iloc[0]+")")

with col6:
    lowest_hour = amount_by_hour.sort_values(by="cnt", ascending=True).head(1)
    st.metric("Lowest amount", value=str(lowest_hour["cnt"].iloc[-1])+" ("+lowest_hour["hr"].iloc[0]+")")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x="cnt", y="hr", data=amount_by_hour.head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel("Hour", fontsize=30)
ax[0].set_xlabel("Amount of Rental", fontsize=30)
ax[0].set_title("Times of Highest Rental Amounts", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

# ITERATION FOR DISPLAYING THE VALUE INSIDE THE BAR
for p in ax[0].patches:
    width = p.get_width()
    ax[0].text(p.get_width() - 40000, p.get_y() + p.get_height() / 2, str(int(width)), ha="center", va="center", fontsize=30, color="black")

# CREATE A GRAPH FOR DISPLAYING THE AMOUNT OF THE TOP 5 LOWEST RENTAL
sns.barplot(x="cnt", y="hr", data=amount_by_hour.sort_values(by="cnt", ascending=True).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel("Hour", fontsize=30)
ax[1].set_xlabel("Amount of Rental", fontsize=30)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Times of Lowest Rental Amounts", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

# ITERATION FOR DISPLAYING THE VALUE INSIDE THE BAR
for p in ax[1].patches:
    width = p.get_width()
    ax[1].text(p.get_width() - 2000, p.get_y() + p.get_height() / 2, str(int(width)), ha="center", va="center", fontsize=30, color="black")

st.pyplot(fig)

# 3rd GRAPH: AMOUNT OF RENTAL BY TIME GROUP
st.subheader("Amount of Rental By SI Base Units Group")

col7, empty_col, col8 = st.columns((12, 5, 8))

with col7:
    highest_time = bytime_df.sort_values(by="cnt", ascending=False).head(1)
    st.metric("Highest amount of time group", value=str(highest_time["cnt"].iloc[-1])+" ("+highest_time["time_group"].iloc[0]+")")

with col8:
    highest_temp = bytemp_df.sort_values(by="cnt", ascending=False).head(1)
    st.metric("Highest amount of temp group", value=str(highest_temp["cnt"].iloc[-1])+" ("+highest_temp["temp_group"].iloc[0]+")")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    graph3 = sns.barplot(
        y="cnt", 
        x="time_group",
        data=bytime_df.sort_values(by="cnt", ascending=False),
        palette=colors,
        ax=ax
    )

    for g3 in graph3.patches:
        graph3.annotate(
            format(g3.get_height(), '.0f'),
            (g3.get_x() + g3.get_width() / 2., g3.get_height() / 1.4),
            ha='center', va='center',
            fontsize=30, color='black',
            xytext=(0, 10),
            textcoords='offset points'
        )


    ax.set_title("Number of Rental by Time Group", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

# 4th GRAPH: AMOUNT OF RENTAL BY TEMPERATURE GROUP
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))

    graph4 = sns.barplot(
        y="cnt", 
        x="temp_group",
        data=bytemp_df.sort_values(by="cnt", ascending=False),
        palette=colors,
        ax=ax
    )

    for g4 in graph4.patches:
        graph4.annotate(
            format(g4.get_height(), '.0f'),
            (g4.get_x() + g4.get_width() / 2., g4.get_height() / 1.4),
            ha='center', va='center',
            fontsize=30, color='black',
            xytext=(0, 10),
            textcoords='offset points'
        )

    ax.set_title("Number of Rental by Temperature Group", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)