import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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

# ตั้งค่าหัวข้อหลักของ Dashboard
st.title('Restaurant Performance Dashboard')

# แสดงตารางข้อมูล
st.subheader('Data Overview')
st.write(data)

# แสดงการกระจายของรายการอาหาร/เครื่องดื่มที่สั่ง
st.subheader('Menu Distribution')
menu_count = data['Menu'].value_counts()
st.bar_chart(menu_count)

# แสดงยอดขายตามวัน
st.subheader('Sales by Day of Week')
sales_by_day = data.groupby('Day Of Week')['Price'].sum()
st.line_chart(sales_by_day)

# แสดงข้อมูลการทำงานของพนักงาน
st.subheader('Staff Performance')

# ตรวจสอบว่าข้อมูลมีคอลัมน์ 'Kitchen Staff' และ 'Drinks Staff' อยู่หรือไม่
if 'Kitchen Staff' in data.columns and 'Drinks Staff' in data.columns:
    # กลุ่มข้อมูลตามพนักงานในครัวและพนักงานเครื่องดื่ม และนับจำนวน
    staff_performance = data.groupby(['Kitchen Staff', 'Drinks Staff']).size().reset_index(name='Count')

    # สร้างแผนภูมิจากข้อมูลนี้
    st.bar_chart(staff_performance, x='Kitchen Staff', y='Count', use_container_width=True)
else:
    st.write("No 'Kitchen Staff' or 'Drinks Staff' data available.")


