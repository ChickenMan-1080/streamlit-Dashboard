import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title = "Tech Layoffs Dashboard",
                   page_icon = "📊",
                   layout = "wide",
)   

st.title("Tech Layoffs Dashboard") 


df = pd.read_csv("assets/tech_layoffs_2026_tracker.csv")

# --- SIDE BAR ---

st.sidebar.header("Filter here") #ตั้งหัวข้อ sidebar

Country = st.sidebar.multiselect(
    "Select the Country:", #Label
    options=df["country"].unique(), #.unique() คือสั่งของ pandas เพื่อกรองค่าซ้ำออก เหลือที่ไม่ซ้ำก (Unique values)
    default=df["country"].unique() #default คือการตั้งค่าเริ่มต้นให้เลือกทุกอย่างใน Column
) 

Layoff_size = st.sidebar.multiselect(
    "Select the Layoff Size:",
    options=df["layoff_size_category"].unique(),
    default=df["layoff_size_category"].unique()
)

df_selection = df.query(
    "country == @Country & layoff_size_category == @Layoff_size" # @ คือการอ้างอิงถึงซักอย่าง ในที่นี้คือการอ้างอิงถึงตัวแปร Country และ Layoff_size ที่เราได้สร้างขึ้นมาในส่วนของ sidebar
)

st.dataframe(df_selection) #แสดงตารางข้อมูลที่ผ่านการกรองแล้ว

# --- MAIN PAGE ---
st.title("Bar Chart : Layoffs Dashboard")

# Calculate
total_layoffs_2024 = int(df_selection['layoffs_2024'].sum())
total_layoffs_2025 = int(df_selection['layoffs_2025'].sum())

left_column , right_column = st.columns(2)
with left_column : 
    st.subheader("Layoffs in 2024 :")  #หัวข้อย่อย
    st.markdown(f'Total : {total_layoffs_2024}')
    
with right_column :
    st.subheader("Layoffs in 2025 :") 
    st.markdown(f'Total : {total_layoffs_2025}')
    
st.write("---") #ขีดเส้นแบ่ง
 
## ยังไม่ได้ clean data แยกปีออกมาเป็น 2024 , 2025 , 2026 😡