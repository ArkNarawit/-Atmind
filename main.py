import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from statsmodels.tsa.arima.model import ARIMA
# โหลดข้อมูล
data = pd.read_csv('https://raw.githubusercontent.com/ArkNarawit/-Atmind/main/test_data.csv')



#จัดการข้อมูล
data['Date'] = pd.to_datetime(data['Date'])
data['Order Time'] = pd.to_datetime(data['Order Time'])
data['Serve Time'] = pd.to_datetime(data['Serve Time'])
data['Category'] = data['Category'].astype('category')
data['Kitchen Staff'] = data['Kitchen Staff'].astype('int64')
data['Drinks Staff'] = data['Drinks Staff'].astype('int64')
data['Hour'] = data['Hour'].astype('int64')
data['Minute'] = data['Minute'].astype('int64')

# Creating dummy variables for each menu item
menu_dummies = pd.get_dummies(data['Menu'])

# Add the date to the dummy dataframe
menu_dummies['Date'] = data['Date']

# Summing up the dummy variables for each day
daily_menu_summary = menu_dummies.groupby('Date').sum()

# Also, sum up the staff numbers and orders for each day
daily_staff_orders = data.groupby('Date').agg({'Kitchen Staff': 'max', 'Drinks Staff': 'max', 'Menu': 'count'})
daily_staff_orders.columns = ['max Kitchen Staff', 'max Drinks Staff', 'Total Orders']

# Combine the daily menu summary with the daily staff and orders summary
daily_summary = pd.concat([daily_menu_summary, daily_staff_orders], axis=1)


food_menu = data[data['Category'] == 'food']['Menu'].unique()
drinks_menu = data[data['Category'] == 'drink']['Menu'].unique()
# Creating new columns 'Food Menu' and 'Drinks Menu' in the daily_summary
daily_summary['Food Menu'] = daily_summary[food_menu].sum(axis=1)
daily_summary['Drinks Menu'] = daily_summary[drinks_menu].sum(axis=1)

# Creating a mapping of Date to Day Of Week
day_of_week_mapping = data[['Date', 'Day Of Week']].drop_duplicates().set_index('Date')['Day Of Week']

# Adding the Day Of Week to the daily_summary
daily_summary['Day Of Week'] = daily_summary.index.map(day_of_week_mapping)

# Displaying the updated daily_summary with the Day Of Week column
daily_summary[['Day Of Week', 'Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders']].head()
ds=daily_summary[['Day Of Week', 'Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders']]
# Calculate the ratio of orders to staff for each day
daily_summary['Kitchen Staff per Order'] = daily_summary['Food Menu'] / daily_summary['max Kitchen Staff']
daily_summary['Drinks Staff per Order'] = daily_summary['Drinks Menu'] / daily_summary['max Drinks Staff']

# Resetting the index of the daily_summary DataFrame to make 'Date' a column
daily_summary_reset = daily_summary.reset_index()

# Now 'Date' is a column, convert it to datetime format
daily_summary_reset['Date'] = pd.to_datetime(daily_summary_reset['Date'])

# Extract the month from the 'Date'
daily_summary_reset['Month'] = daily_summary_reset['Date'].dt.month

# Convert 'Date' to datetime format and extract the month
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.month
monthly_summary = daily_summary_reset.groupby('Month').agg({
    'Food Menu': 'sum',  # Total food sales for the month
    'Drinks Menu': 'sum',  # Total drinks sales for the month
    'max Kitchen Staff': 'sum',  # Average maximum kitchen staff
    'max Drinks Staff': 'sum',  # Average maximum drinks staff
    'Total Orders': 'sum',  # Total orders for the month
    'Kitchen Staff per Order': 'mean',  # Average kitchen staff per order
    'Drinks Staff per Order': 'mean'  # Average drinks staff per order
})




# Creating separate DataFrames for each month's data
monthly_dataframes_from_summary = {}

for month in daily_summary_reset['Month'].unique():
    # Filter the data for the month and store in the dictionary
    monthly_dataframes_from_summary[month] = daily_summary_reset[daily_summary_reset['Month'] == month]
Jun=monthly_dataframes_from_summary[6][['Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders','Day Of Week','Kitchen Staff per Order','Drinks Staff per Order']]
Jul=monthly_dataframes_from_summary[7][['Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders','Day Of Week','Kitchen Staff per Order','Drinks Staff per Order']]
Aug=monthly_dataframes_from_summary[8][['Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders','Day Of Week','Kitchen Staff per Order','Drinks Staff per Order']]
Sep=monthly_dataframes_from_summary[9][['Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders','Day Of Week','Kitchen Staff per Order','Drinks Staff per Order']]
Oct=monthly_dataframes_from_summary[10][['Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders','Day Of Week','Kitchen Staff per Order','Drinks Staff per Order']]
Nov=monthly_dataframes_from_summary[11][['Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders','Day Of Week','Kitchen Staff per Order','Drinks Staff per Order']]
Dec=monthly_dataframes_from_summary[12][['Food Menu', 'Drinks Menu', 'max Kitchen Staff', 'max Drinks Staff', 'Total Orders','Day Of Week','Kitchen Staff per Order','Drinks Staff per Order']]
# Loop through each month's DataFrame and generate the plots











st.title('Restaurant Performance Dashboard')


st.subheader('Data Overview')
st.write(data)





item_counts = data['Menu'].value_counts()
item_revenue = data.groupby('Menu').agg({'Price': 'sum'})

item_analysis = pd.DataFrame({'Count': item_counts, 'Revenue': item_revenue['Price']})
item_analysis = item_analysis.sort_values(by='Revenue', ascending=False)

top_items_by_count = item_analysis.sort_values(by='Count', ascending=False).head(10)
top_items_by_revenue = item_analysis.head(10)

# Streamlit Visualization
st.title('Menu Item Analysis')
fig, ax = plt.subplots(1, 2, figsize=(18, 6))
sns.barplot(x=top_items_by_count['Count'], y=top_items_by_count.index, palette="viridis", ax=ax[0])
ax[0].set_title('Top 10 Most Ordered Items')
ax[0].set_xlabel('Number of Orders')

sns.barplot(x=top_items_by_revenue['Revenue'], y=top_items_by_revenue.index, palette="mako", ax=ax[1])
ax[1].set_title('Top 10 Highest Revenue Generating Items')
ax[1].set_xlabel('Total Revenue')
st.pyplot(fig)

# Displaying DataFrames
col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 10 Most Ordered Items")
    st.dataframe(top_items_by_count)
with col2:
    st.subheader("Top 10 Highest Revenue Generating Items")
    st.dataframe(top_items_by_revenue)
st.subheader('การวิเคราะห์เกี่ยวกับรายการอาหารและเครื่องดื่มที่ได้รับความนิยมและสร้างรายได้มากที่สุด')
st.write('- รายการที่สั่งมากที่สุด: กราฟด้านซ้ายแสดงรายการอันดับ 10 อันดับแรกตามจำนวนครั้งที่สั่ง "Supreme Burger" และ"Veggie Burger" เป็นรายการที่ถูกสั่งบ่อยที่สุด ตามมาด้วยเครื่องดื่มทั่วไปเช่น "Soda" และ "Coke".')
st.write('- รายการที่สร้างรายได้สูงสุด: กราฟด้านขวาแสดงรายการ 10 อันดับแรกตามรายได้รวม "Cheese Burger" และ "Classic Burger" นำในการสร้างรายได้ ตามมาอย่างใกล้ชิดโดย "Veggie Burger" และ "Supreme Burger".')





import plotly.express as px
st.title('Sales Data Analysis')

# Convert 'Date' to datetime
data['Date'] = pd.to_datetime(data['Date'])

# Aggregate sales data
daily_sales = data.groupby(data['Date']).agg({'Price': 'sum'}).reset_index()
weekly_sales = data.groupby(data['Date'].dt.isocalendar().week).agg({'Price': 'sum'}).reset_index()
monthly_sales = data.groupby(data['Date'].dt.month).agg({'Price': 'sum'}).reset_index()

# Plotting with Plotly
# Daily Sales
fig_daily = px.line(daily_sales, x='Date', y='Price', title='Daily Sales')
fig_daily.update_layout(yaxis_title='Total Sales', xaxis_title='Date')

# Weekly Sales
fig_weekly = px.line(weekly_sales, x='week', y='Price', title='Weekly Sales')
fig_weekly.update_layout(yaxis_title='Total Sales', xaxis_title='Week')

# Monthly Sales
fig_monthly = px.line(monthly_sales, x='Date', y='Price', title='Monthly Sales')
fig_monthly.update_layout(yaxis_title='Total Sales', xaxis_title='Month')

# Display the Plotly plots in Streamlit
st.subheader('ยอดขายรายวัน')
st.write('กราฟนี้แสดงยอดขายรวมในแต่ละวัน ช่วยให้ระบุวันที่มียอดขายผิดปกติสูงหรือต่ำ ซึ่งอาจบ่งบอกถึงเหตุการณ์พิเศษหรือรูปแบบที่เกิดขึ้น')
st.plotly_chart(fig_daily)
st.subheader('ยอดขายรายสัปดาห์')
st.write('กราฟนี้แสดงยอดขายรวมตามสัปดาห์ ช่วยให้เข้าใจวงจรยอดขายรายสัปดาห์และระบุสัปดาห์ที่มีผลการดำเนินงานโดดเด่นหรือต่ำกว่าปกติ')
st.plotly_chart(fig_weekly)
st.subheader('ยอดขายรายเดือน')
st.write('กราฟยอดขายรายเดือนให้มุมมองที่กว้างขึ้นเกี่ยวกับประสิทธิภาพของยอดขาย ช่วยให้ระบุแนวโน้มตามฤดูกาลหรือการเปลี่ยนแปลงยาวนานในแนวโน้มของยอดขาย')
st.plotly_chart(fig_monthly)

hourly_sales = data.groupby(data['Order Time'].dt.hour).agg({'Price': 'sum'}).reset_index()

# Streamlit application for displaying the analysis
st.title('Peak Hours Analysis')

# Display the bar plot
st.subheader('Sales by Hour of the Day')
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Order Time', y='Price', data=hourly_sales, palette="rocket", ax=ax)
ax.set_title('Sales by Hour of the Day')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Total Sales')
ax.set_xticks(range(0, 24))
ax.grid(axis='y')
st.pyplot(fig)

col1, col2 = st.columns(2)
with col1:
    st.subheader('Hourly Sales Data')
    st.write(hourly_sales)
with col2:
    st.subheader("การวิเคราะห์ยอดขายตามชั่วโมงของวันเผยให้เห็นข้อมูลดังนี้")
    st.write('- ชั่วโมงที่มียอดขายสูงสุดคือระหว่าง 12.00 น. ถึง 14.00 น. และพบว่ามีจุดสูงสุดอีกครั้งระหว่าง 18.00 น. ถึง 19.00 น. เวลาเหล่านี้น่าจะสอดคล้องกับช่วงเวลาที่คนมากินอาหารกลางวันและเย็นตามลำดับ')
    st.write('- ยอดขายมักจะลดลงในช่วงบ่าย (15.00 น. ถึง 16.00 น.) และช่วงเย็นหลังจาก 20.00 น')
    st.write('- มียอดขายเพิ่มขึ้นเล็กน้อยหลังจาก 22.00 น. ซึ่งอาจบ่งบอกถึงกลุ่มลูกค้าที่มาใช้บริการในช่วงดึก.')






# Convert 'Date' to datetime format and extract the month
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.month


#st.subheader('Monthly_summary')
#st.write(monthly_summary)








# โค้ด Streamlit
st.title("ARIMA Model Forecasting")

# รับจำนวนวันที่ต้องการพยากรณ์จากผู้ใช้
forecast_days = st.number_input("Enter the number of days for forecasting", min_value=1, value=7)


result1 = daily_summary_reset.groupby('Date')[['Food Menu'
                              ]].sum().reset_index()
sales_data = result1
sales_data.set_index('Date', inplace=True)
best_aic = float("inf")
best_order = (0, 0, 1) 
for p in range(5):  # ตัวอย่างการทดลองค่า p จาก 0 ถึง 7
    for d in range(5):  # ตัวอย่างการทดลองค่า d จาก 0 ถึง 6
        for q in range(5):  # ตัวอย่างการทดลองค่า q จาก 0 ถึง 7
            if d < p and d < q:  # ตรวจสอบเงื่อนไข d < p และ d < q
                try:
                    model = ARIMA(sales_data['Food Menu'].values, order=(p, d, q))  # ใช้ .values เพื่อดึงค่าจริงๆ จาก series
                    arima_model = model.fit()

                    if arima_model.aic < best_aic:  # ค้นหาค่า AIC ที่น้อยที่สุด
                        best_aic = arima_model.aic
                        best_order = (p, d, q)
                except:
                    continue

model = ARIMA(sales_data, order=best_order)  # ตั้งค่าพารามิเตอร์ของโมเดล ARIMA
arima_model = model.fit()
# ทำการพยากรณ์
forecast = arima_model.forecast(steps=forecast_days)

# แสดงผล

st.write("Forecast Food menu for the next", forecast_days, "days:")
st.write("Best ARIMA Model order:", best_order)
st.line_chart(forecast)
result2 = daily_summary_reset.groupby('Date')[['Drinks Menu'
                              ]].sum().reset_index()
sales_data1 = result2
sales_data1.set_index('Date', inplace=True)
best_aic = float("inf")
best_order = (0, 0, 1) 
for p in range(5):  # ตัวอย่างการทดลองค่า p จาก 0 ถึง 7
    for d in range(5):  # ตัวอย่างการทดลองค่า d จาก 0 ถึง 6
        for q in range(5):  # ตัวอย่างการทดลองค่า q จาก 0 ถึง 7
            if d < p and d < q:  # ตรวจสอบเงื่อนไข d < p และ d < q
                try:
                    model = ARIMA(sales_data1['Drinks Menu'].values, order=(p, d, q))  # ใช้ .values เพื่อดึงค่าจริงๆ จาก series
                    arima_model = model.fit()

                    if arima_model.aic < best_aic:  # ค้นหาค่า AIC ที่น้อยที่สุด
                        best_aic = arima_model.aic
                        best_order = (p, d, q)
                except:
                    continue
model = ARIMA(sales_data, order=best_order)  # ตั้งค่าพารามิเตอร์ของโมเดล ARIMA
arima_model = model.fit()
forecast1 = arima_model.forecast(steps=forecast_days)


st.write("Forecast Drinks Menu for the next", forecast_days, "days:")
st.write("Best ARIMA Model order:", best_order)
st.line_chart(forecast1)

average_kitchen_staff_ratio = daily_summary['Kitchen Staff per Order'].mean()
average_drinks_staff_ratio = daily_summary['Drinks Staff per Order'].mean()

forecast_df = pd.DataFrame(list(forecast.items()), columns=['Date', 'food menu'])
forecast1_df = pd.DataFrame(list(forecast1.items()), columns=['Date', 'drinks Menu'])
merged_df = pd.merge(forecast_df, forecast1_df, left_on='Date', right_on='Date')
merged_df['food menu'] = (merged_df['food menu'] + 1).astype(int)
merged_df['kitchen_staff']=merged_df["food menu"]/average_kitchen_staff_ratio
merged_df['kitchen_staff'] = (merged_df['kitchen_staff'] + 1).astype(int)
merged_df['drinks Menu'] = (merged_df['drinks Menu'] + 1).astype(int)
merged_df['drinks_Staff']=merged_df["drinks Menu"]/average_drinks_staff_ratio
merged_df['drinks_Staff'] = (merged_df['drinks_Staff'] + 1).astype(int)

st.subheader("Staff management ")
st.write(merged_df)

st.subheader("การจัดการพนักงานในแต่ประเภท")
st.write("- จากตารางด้านบนได้ทำการทำนายจำนวนเมนูอาหารและเครื่องดื่มมาโดยใช้โมเดล ARIMA ที่สามาถกำหนดจำนวนวันที่จะทำนายได้แล้วเอามาหาจำนวนพนักงานที่เหมาะสมในวันนั้นๆ")