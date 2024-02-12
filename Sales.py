import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

df = pd.read_csv('Amazon Sales data.csv')

# Order Date and Ship Date to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['Ship Date'] = pd.to_datetime(df['Ship Date'])

df['Order_Year'] = df['Order Date'].dt.year
df['Order_Month'] = df['Order Date'].dt.month
df['Ship_Year'] = df['Ship Date'].dt.year
df['Ship_Month'] = df['Ship Date'].dt.month

# Sales trend month-wise for order date
monthly_sales_order = df.groupby('Order_Month')['Total Revenue'].sum()

# Sales trend year-wise for order date
yearly_sales_order = df.groupby('Order_Year')['Total Revenue'].sum()

# Sales trend yearly-month-wise for order date
yearly_monthly_sales_order = df.groupby(['Order_Year', 'Order_Month'])['Total Revenue'].sum().reset_index()

# Sales trend month-wise for ship date
monthly_sales_ship = df.groupby('Ship_Month')['Total Revenue'].sum()

# Sales trend year-wise for ship date
yearly_sales_ship = df.groupby('Ship_Year')['Total Revenue'].sum()

# Sales trend yearly-month-wise for ship date
yearly_monthly_sales_ship = df.groupby(['Ship_Year', 'Ship_Month'])['Total Revenue'].sum().reset_index()

# Factors
total_sales = df['Total Revenue'].sum()
average_sales_per_customer = df['Total Revenue'].sum() / df['Order ID'].nunique()
sales_by_product_category = df.groupby('Item Type')['Total Revenue'].sum()

# Streamlit
st.set_page_config(page_title="Sales Trends Dashboard", page_icon=":bar_chart:")
st.title(':bar_chart: Amazon Sale Trends')

# Sidebar
st.sidebar.title('Filters')
sales_channel = st.sidebar.selectbox('Select Sales Channel', df['Sales Channel'].unique())
item = st.sidebar.selectbox('Select Item', df['Item Type'].unique())

# Filter the data based on user input
filtered_df = df[(df['Sales Channel'] == sales_channel) & (df['Item Type'] == item)]

df['Profit Margin'] = (df['Total Profit'] / df['Total Revenue']) * 100

# Visualization
fig_unit_price_vs_revenue = px.scatter(df, x='Unit Price', y='Total Revenue', title='Unit Price vs. Total Revenue')

# Total sales based on the filtered data
total_sales_filtered = filtered_df['Total Revenue'].sum()

# Average sales per customer based on the filtered data
average_sales_per_customer_filtered = filtered_df['Total Revenue'].sum() / filtered_df['Order ID'].nunique()

# Handling NaN values 
average_sales_per_customer_filtered = np.nan_to_num(average_sales_per_customer_filtered, nan=0)

# Rating based on average sales per customer
rating = min(5, max(1, int(average_sales_per_customer_filtered / 1000)))
rating_stars = '⭐' * rating

# Display total sales
st.subheader('Total Sales')
st.write(f"The total sales for {sales_channel} in {item} is: {total_sales_filtered}")

# Display average sales per customer 
st.subheader('Average Sales per Customer')
st.write(f"The average sales per customer for {sales_channel} in {item} is: {average_sales_per_customer_filtered}")

# Display the rating
st.subheader('Rating')
st.write(f"The rating for {sales_channel} in {item} is: {rating_stars}")

st.subheader(':chart_with_upwards_trend: Unit Price and Unit Cost Analysis')
st.write('Explore the relationship between unit price, unit cost, total revenue, and profit.')

# Adding filters 
sales_channel = st.selectbox('Select Sales Channel', df['Sales Channel'].unique(), key='sales_channel_unique_key')
item_type = st.selectbox('Select Item Type', df['Item Type'].unique())

# Filtering the data based on user input
filtered_df = df[(df['Sales Channel'] == sales_channel) & (df['Item Type'] == item_type)]

# Displaying the filtered data
st.write('Filtered Data:')
st.write(filtered_df)

st.plotly_chart(fig_unit_price_vs_revenue)

# Display sales trend month-wise for order date 
st.subheader('Sales Trend Month-wise for Order Date')
fig_monthly_order = px.line(x=monthly_sales_order.index, y=monthly_sales_order.values, labels={'x':'Month', 'y':'Total Revenue'}, title='Monthly Sales Trend for Order Date')
st.plotly_chart(fig_monthly_order)

# Display sales trend year-wise for order date 
st.subheader('Sales Trend Year-wise for Order Date')
fig_yearly_order = px.line(x=yearly_sales_order.index, y=yearly_sales_order.values, labels={'x':'Year', 'y':'Total Revenue'}, title='Yearly Sales Trend for Order Date')
st.plotly_chart(fig_yearly_order)

# Display sales trend yearly-month-wise for order date 
st.subheader('Sales Trend Yearly-Month-wise for Order Date')
fig_yearly_monthly_order = px.line(yearly_monthly_sales_order, x='Order_Month', y='Total Revenue', color='Order_Year', labels={'x':'Month', 'y':'Total Revenue'}, title='Yearly-Monthly Sales Trend for Order Date')
st.plotly_chart(fig_yearly_monthly_order)

# Display sales trend month-wise for ship date 
st.subheader('Sales Trend Month-wise for Ship Date')
fig_monthly_ship = px.line(x=monthly_sales_ship.index, y=monthly_sales_ship.values, labels={'x':'Month', 'y':'Total Revenue'}, title='Monthly Sales Trend for Ship Date')
st.plotly_chart(fig_monthly_ship)

# Display sales trend year-wise for ship date 
st.subheader('Sales Trend Year-wise for Ship Date')
fig_yearly_ship = px.line(x=yearly_sales_ship.index, y=yearly_sales_ship.values, labels={'x':'Year', 'y':'Total Revenue'}, title='Yearly Sales Trend for Ship Date')
st.plotly_chart(fig_yearly_ship)

# Display sales trend yearly-month-wise for ship date 
st.subheader('Sales Trend Yearly-Month-wise for Ship Date')
fig_yearly_monthly_ship = px.line(yearly_monthly_sales_ship, x='Ship_Month', y='Total Revenue', color='Ship_Year', labels={'x':'Month', 'y':'Total Revenue'}, title='Yearly-Monthly Sales Trend for Ship Date')
st.plotly_chart(fig_yearly_monthly_ship)
