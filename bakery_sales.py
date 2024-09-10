
import streamlit as st
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#import matplotlib.pyplot as plt

## load data

# page config
st.set_page_config(page_title="Bakery sales", layout='centered', page_icon='📊')

# Title
st.title (" 📊  Bakery sales - Web App")
@st.cache_data

def load_data():
    df = pd.read_csv("bakerysales.csv")
    # data cleaning
    df.drop(columns = 'Unnamed: 0', inplace=True)
    df['date'] = pd.to_datetime(df.date)
    df['ticket_number'] = df.ticket_number.astype('object')
    df['unit_price'] = df.unit_price.str.replace(',', '.').str.replace(' €', '')
    df['unit_price'] = df.unit_price.astype('float')
    # calculate sales
    sales = df.Quantity * df.unit_price

    # add a new column to the dataframe
    df['sales'] = sales
    # return cleaned dataframe
    return df


df = load_data()
#st.title("bakery sales App")
st.sidebar.title("filters")

# display the dataset

st.subheader("Data  Preview")
st.dataframe(df.head())

# create a filter for articles and ticket numbers
articles = df['article'].unique()

# get top10 ticketNos
ticketNos10 = df['ticket_number'].value_counts().head(10).reset_index()['ticket_number']
#st.write(df['ticket_number'].unique())

# create a multislect for articles
selected_articles = st.sidebar.multiselect("Products", articles,[articles[0],articles[10]])
top_10_ticketsNos = st.sidebar.selectbox("Top 10 Tickets", ticketNos10[:10])

#selected_ticketNos = st.
filtered_articles = df[df["article"].isin(selected_articles)]
no_filtered_articles = filtered_articles['article'].nunique()
total_filtered_sales = np.round(filtered_articles['sales'].sum(),2)
total_filtered_qty = np.round(filtered_articles['Quantity'].sum(),2)
st.subheader("Filtered tables")
if not selected_articles:
    st.error("select an article")
else:
    st.dataframe(filtered_articles.sample(3))

# calculations
total_sales = np.round(df['sales'].sum())
total_qty = np.round(df['Quantity'].sum())
no_articles = len(articles)

# display in columns
col1,col2,col3 = st.columns(3)
col1.metric("Total Sales",f'{total_sales:,}')
col2.metric("Total Quantity",f'{total_qty:,}')
col3.metric("No of articles",no_articles)
# quantity
if no_articles:
    col2.metric("Quantity", f'{total_qty:,}')
else:
    col2.metric("Quantity", f'{total_filtered_qty:,}')
if not selected_articles:
    col3.metric("No of products", no_articles)
else:
    col3.metric("No. of Products", no_filtered_articles)

#charts
st.header("Plotting")
# data
article_grp = df.groupby('article')['sales'].sum()
article_grp = article_grp.sort_values(ascending=False)[:-3]
table = article_grp.reset_index()

filtered_table = table[table['article'].isin(selected_articles)]

