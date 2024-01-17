import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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



# ตั้งค่าหัวข้อหลักของ Dashboard
st.title('Restaurant Performance Dashboard')

# แสดงตารางข้อมูล
st.subheader('Data Overview')
st.write(data)

# แสดงการกระจายของรายการอาหาร/เครื่องดื่มที่สั่ง
st.subheader('food Menu Distribution')

selected_category = 'food'
selected_category1 = 'drink'

filtered_data = data[data['Category'] == selected_category]
filtered_data1 = data[data['Category'] == selected_category1]

menu_count = filtered_data['Menu'].value_counts()
menu_count1 = filtered_data1['Menu'].value_counts()
st.bar_chart(menu_count)
st.subheader('drink Menu Distribution')
st.bar_chart(menu_count1)


# Convert 'Date' to datetime format and extract the month
data['Date'] = pd.to_datetime(data['Date'])
data['Month'] = data['Date'].dt.month


st.subheader('monthly_summary')
st.write(monthly_summary)
# Assuming monthly_dataframes_from_summary is defined correctly
for month_names, df in monthly_dataframes_from_summary.items():
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(15, 7), tight_layout=True)

    # Set the title for each set of plots with the respective month
    fig.suptitle(f'Sales and Staff Data for Month {month_names}', fontsize=16)

    # Food and Drinks Menu Sales
    df.plot(kind='bar', x='Day Of Week', y=['Food Menu', 'Drinks Menu'], ax=axes[0], color=['blue', 'green'])
    axes[0].set_title('Food and Drinks Menu Sales')
    axes[0].set_ylabel('Sales')

    # Staff per Order
    df.plot(kind='bar', x='Day Of Week', y=['Kitchen Staff per Order', 'Drinks Staff per Order'], ax=axes[1], color=['red', 'purple'])
    axes[1].set_title('Staff per Order')
    axes[1].set_ylabel('Staff/Order Ratio')

    # Show plot for each month in Streamlit
    st.pyplot(fig)


# สมมติว่า 'sales_data' เป็น DataFrame ที่มีคอลัมน์ 'Food Menu'

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

st.write(merged_df)